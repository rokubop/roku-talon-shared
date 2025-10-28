from talon import Module, actions, cron, ui, ctrl, settings
import re
import inspect
mod = Module()

event_subscribers = []

mod.setting("parrot_config_combo_window", type=int, default=300, desc="The time window to wait for a combo to complete")

def get_base_noise(noise):
    """The part before colon or @ e.g.'pop' in 'pop:db_170' or 'pop@top'"""
    base_combo = noise.split(':')[0].split('@')[0]
    base_noises = base_combo.split(' ')
    return base_combo.strip(), base_noises

def get_base_with_location_noise(noise):
    """The part before colon or @ e.g.'pop' in 'pop:db_170' or 'pop@top'"""
    base_noise = noise.split(':')[0]
    return base_noise.strip()

def executeActionOrLocationAction(action):
    if isinstance(action, dict):
        rect = ui.main_screen().rect
        (x, y) = ctrl.mouse_pos()
        cur_location = "bottom"
        if y < rect.height / 2:
            cur_location = "top"
        action[cur_location]()
    else:
        action()

def get_modified_action(noise, action):
    if ":th" in noise:
        match = re.search(r':th_(\d+)', noise)
        throttle_amount = int(match.group(1)) if match else 100
        base_noise = noise.replace(f":th_{throttle_amount}", "")
        return (action[0], lambda: parrot_throttle(throttle_amount, base_noise, action[1]))
    if ":db" in noise:
        match = re.search(r':db_(\d+)', noise)
        debounce_amount = int(match.group(1)) if match else 100
        base_noise = noise.replace(f":db_{debounce_amount}", "")
        return (action[0], lambda: parrot_debounce(debounce_amount, base_noise, action[1]))
    return action

def has_variables(noise_pattern: str) -> bool:
    return '$' in noise_pattern

def extract_variables(noise_pattern: str) -> list[str]:
    variables = re.findall(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', noise_pattern)
    return variables

def pattern_to_regex(noise_pattern: str) -> str:
    escaped = re.escape(noise_pattern)
    # Replace escaped variable placeholders with regex groups
    # Use a lambda to avoid backslash interpretation issues
    pattern = re.sub(r'\\\$[a-zA-Z_][a-zA-Z0-9_]*', lambda m: r'(\w+)', escaped)
    return pattern

def validate_variable_action(noise_pattern: str, action: tuple) -> bool:
    if not isinstance(action, tuple) or len(action) < 2:
        return False

    variables = extract_variables(noise_pattern)
    lambda_func = action[1]

    if not callable(lambda_func):
        return False

    try:
        sig = inspect.signature(lambda_func)
        param_count = len(sig.parameters)
        variable_count = len(variables)
        return param_count == 0 or param_count == variable_count
    except (ValueError, TypeError):
        return True

def match_variable_pattern(noise: str, pattern: str) -> dict[str, str] | None:
    regex_pattern = pattern_to_regex(pattern)
    match = re.match(f'^{regex_pattern}$', noise)

    if not match:
        return None

    variables = extract_variables(pattern)
    values = match.groups()

    if len(variables) != len(values):
        return None

    result = dict(zip(variables, values))
    return result

def execute_variable_action(action: tuple, variables: dict[str, str]):
    lambda_func = action[1]

    try:
        sig = inspect.signature(lambda_func)
        param_count = len(sig.parameters)

        if param_count == 0:
            return lambda_func()
        else:
            var_values = list(variables.values())
            return lambda_func(*var_values)
    except (ValueError, TypeError):
        return lambda_func()

def process_command_categorization(noise, action, base_noise_map, combo_noise_set, immediate_commands, delayed_commands):
    (_base_noise, _modifiers, location) = parse_modifiers(noise)
    modified_action = get_modified_action(noise, action)
    base = base_noise_map[noise]

    if any(other_noise.startswith(f"{base} ") and other_noise != base for other_noise in combo_noise_set):
        if location:
            if not base in delayed_commands:
                delayed_commands[base] = (action[0], {})
            delayed_commands[base][1][location] = modified_action[1]
        else:
            delayed_commands[base] = modified_action
    else:
        if location:
            if not base in immediate_commands:
                immediate_commands[base] = (action[0], {})
            immediate_commands[base][1][location] = modified_action[1]
        else:
            immediate_commands[base] = modified_action

def process_variable_categorization(noise_pattern, action, variable_commands, combo_noise_set, immediate_variable_patterns, delayed_variable_patterns):
    (_base_noise, _modifiers, location) = parse_modifiers(noise_pattern)
    modified_action = get_modified_action(noise_pattern, action)
    base_pattern = get_base_noise(noise_pattern)[0]

    is_delayed = False

    # Check if any other variable patterns could conflict with this one
    # (i.e., this pattern is a prefix of another pattern)
    for other_pattern, _ in variable_commands:
        other_base = get_base_noise(other_pattern)[0]
        if other_pattern != noise_pattern and other_base.startswith(f"{base_pattern} "):
            is_delayed = True
            break

    # Check if any static combos could conflict with this pattern
    # (i.e., this pattern is a prefix of a static combo)
    if not is_delayed:
        for static_combo in combo_noise_set:
            if static_combo.startswith(f"{base_pattern} ") and static_combo != base_pattern:
                is_delayed = True
                break

    if is_delayed:
        if location:
            if not noise_pattern in delayed_variable_patterns:
                delayed_variable_patterns[noise_pattern] = (action[0], {})
            delayed_variable_patterns[noise_pattern][1][location] = modified_action[1]
        else:
            delayed_variable_patterns[noise_pattern] = modified_action
    else:
        if location:
            if not noise_pattern in immediate_variable_patterns:
                immediate_variable_patterns[noise_pattern] = (action[0], {})
            immediate_variable_patterns[noise_pattern][1][location] = modified_action[1]
        else:
            immediate_variable_patterns[noise_pattern] = modified_action

def categorize_commands(commands):
    immediate_commands = {}
    delayed_commands = {}
    immediate_variable_patterns = {}
    delayed_variable_patterns = {}
    base_pairs = set()
    combo_noise_set = set()
    base_noise_set = set()
    unique_combos = set()
    base_noise_map = {}
    active_commands = []
    variable_commands = []

    for noise, action in commands.items():
        if not noise or not isinstance(action, tuple) or len(action) < 2:
            continue

        try:
            if action[1] is None or not callable(action[1]):
                raise ValueError(
                    f"\nThe action for '{noise}' must be a callable (function or lambda).\n\n"
                    f"Valid examples:\n"
                    f'"pop": ("E", lambda: actions.user.game_key("e")),\n'
                    f'"pop": ("L click", actions.user.game_mouse_click_left),\n\n'
                    f"Invalid examples:\n"
                    f'"pop": ("E", actions.user.game_key("e")),\n'
                    f'"pop": ("L click", actions.user.game_mouse_click_left())\n'
                )
        except ValueError as e:
            print(e)
            continue

        if has_variables(noise):
            if not validate_variable_action(noise, action):
                print(f"Warning: Variable pattern '{noise}' has mismatched lambda signature")
                continue
            variable_commands.append((noise, action))
        else:
            base_combo, base_noises = get_base_noise(noise)

            if "_stop" in noise and len(base_noises) == 1:
                base_pairs.add(base_noises[0].replace("_stop", ""))

            if len(base_noises) > 1:
                unique_combos.add(base_combo)

            for base_noise in base_noises:
                base_noise_set.add(base_noise)

            combo_noise_set.add(base_combo)
            base_noise_map[noise] = base_combo
            active_commands.append((noise, action))

    # Also add base noises from variable patterns
    for noise_pattern, action in variable_commands:
        base_combo, base_noises = get_base_noise(noise_pattern)
        for base_noise in base_noises:
            # Only add if it's not a variable placeholder
            if not base_noise.startswith('$'):
                base_noise_set.add(base_noise)

    for noise, action in active_commands:
        process_command_categorization(noise, action, base_noise_map, combo_noise_set, immediate_commands, delayed_commands)

    for noise_pattern, action in variable_commands:
        process_variable_categorization(noise_pattern, action, variable_commands, combo_noise_set, immediate_variable_patterns, delayed_variable_patterns)

    return {
        "immediate_commands": immediate_commands,
        "delayed_commands": delayed_commands,
        "immediate_variable_patterns": immediate_variable_patterns,
        "delayed_variable_patterns": delayed_variable_patterns,
        "base_noise_set": base_noise_set,
        "base_pairs": base_pairs,
        "unique_combos": unique_combos
    }

def parse_modifiers(sound: str):
    base_noise, location, modifiers = sound, None, None

    if '@' in sound:
        base_noise, rest = sound.split('@', 1)
        if ':' in rest:
            location, modifiers = rest.split(':', 1)
        else:
            location = rest
    elif ':' in sound:
        base_noise, modifiers = sound.split(':', 1)

    return base_noise, modifiers, location

class ParrotConfig():
    def __init__(self):
        self.parrot_config_user_ref = None
        self.current_mode = None
        self.immediate_commands = {}
        self.delayed_commands = {}
        self.immediate_variable_patterns = {}
        self.delayed_variable_patterns = {}
        self.has_variables = False
        self.base_pairs = set()
        self.combo_chain = ""
        self.combo_job = None
        self.base_noises = None
        self.pending_combo = None
        self.combo_window = "300ms"
        self.unique_combos = set()

    def setup_mode(self, mode):
        if mode:
            if mode == self.current_mode:
                return
            else:
                parrot_config = self.parrot_config_user_ref[mode]
        else:
            parrot_config = self.parrot_config_user_ref
        if self.combo_job:
            cron.cancel(self.combo_job)
            self.combo_job = None
        self.current_mode = mode
        self.combo_chain = ""
        self.pending_combo = None
        commands = parrot_config.get("commands", {}) if "commands" in parrot_config else parrot_config

        categorized = categorize_commands(commands)
        self.immediate_commands = categorized["immediate_commands"]
        self.delayed_commands = categorized["delayed_commands"]
        self.immediate_variable_patterns = categorized["immediate_variable_patterns"]
        self.delayed_variable_patterns = categorized["delayed_variable_patterns"]
        self.has_variables = bool(self.immediate_variable_patterns or self.delayed_variable_patterns)
        self.base_noises = categorized["base_noise_set"]
        self.base_pairs = categorized["base_pairs"]
        self.unique_combos = categorized["unique_combos"]

        combo_window = settings.get("user.parrot_config_combo_window", 300)
        self.combo_window = f"{combo_window}ms"

    def setup(self, parrot_config):
        self.parrot_config_user_ref = parrot_config
        if "default" in parrot_config:
            self.setup_mode("default")
        else:
            self.setup_mode(None)

    def _delayed_combo_execute(self):
        if self.combo_job:
            cron.cancel(self.combo_job)
            self.combo_job = None
        action = self.delayed_commands[self.pending_combo][1]
        throttled = parrot_throttle_busy.get(self.pending_combo)
        executeActionOrLocationAction(action)
        if not throttled:
            command = self.delayed_commands[self.pending_combo][0]
            parrot_config_event_trigger(self.pending_combo, command)
        self.combo_chain = ""
        self.pending_combo = None

    def _delayed_potential_combo(self):
        if self.combo_job:
            cron.cancel(self.combo_job)
            self.combo_job = None

        # maybe needed for variable patterns
        # if self.combo_chain and self.combo_chain in self.immediate_commands:
        #     action = self.immediate_commands[self.combo_chain][1]
        #     throttled = parrot_throttle_busy.get(self.combo_chain)
        #     executeActionOrLocationAction(action)
        #     if not throttled:
        #         command = self.immediate_commands[self.combo_chain][0]
        #         parrot_config_event_trigger(self.combo_chain, command)

        self.combo_chain = ""
        self.pending_combo = None

    def _try_variable_patterns(self, noise_chain: str, pattern_dict: dict) -> bool:
        for pattern, action in pattern_dict.items():
            variables = match_variable_pattern(noise_chain, pattern)
            if variables is not None:
                if isinstance(action[1], dict):
                    executeActionOrLocationAction(action[1])
                else:
                    execute_variable_action(action, variables)

                command = action[0]
                parrot_config_event_trigger(pattern, command)
                return True
        return False

    def _prepare_delayed_command(self):
        self.pending_combo = self.combo_chain
        self.combo_job = cron.after(self.combo_window, self._delayed_combo_execute)

    def _execute_delayed_variable_command(self):
        self.pending_combo = self.combo_chain
        self.combo_job = cron.after(self.combo_window, self._delayed_combo_execute_variable)

    def _delayed_combo_execute_variable(self):
        if self.combo_job:
            cron.cancel(self.combo_job)
            self.combo_job = None
        # Try to match the pending combo against delayed variable patterns
        matched = self._try_variable_patterns(self.pending_combo, self.delayed_variable_patterns)
        self.combo_chain = ""
        self.pending_combo = None

    def _execute_immediate_command(self, noise: str):
        action = self.immediate_commands[self.combo_chain][1]
        throttled = parrot_throttle_busy.get(noise)
        executeActionOrLocationAction(action)
        if not throttled:
            command = self.immediate_commands[self.combo_chain][0]
            parrot_config_event_trigger(self.combo_chain, command)

        # if our combo ends in a continuous noise, we should force
        # a throttle so there is clear separation between the combo
        # and a followup noise.
        if self.combo_chain in self.unique_combos:
            last_noise = self.combo_chain.split(' ')[-1]
            if last_noise in self.base_pairs:
                parrot_throttle(90, last_noise, lambda: None)
                parrot_throttle(90, f"{last_noise}_stop", lambda: None)

        self.combo_chain = ""
        self.pending_combo = None

    def _execute_immediate_variable_pattern(self):
        self.combo_chain = ""
        self.pending_combo = None

    def _execute_single_immediate_command(self, noise: str):
        if self.pending_combo:
            self._delayed_combo_execute()
            actions.sleep("20ms")
        action = self.immediate_commands[noise][1]
        throttled = parrot_throttle_busy.get(noise)
        executeActionOrLocationAction(action)
        if not throttled:
            command = self.immediate_commands[noise][0]
            parrot_config_event_trigger(noise, command)
        self.combo_chain = ""
        self.pending_combo = None

    def _could_be_variable_pattern_start(self, combo_chain: str) -> bool:
        """Check if the current combo chain could be the start of a variable pattern"""
        if not self.has_variables:
            return False

        # Check immediate variable patterns
        for pattern in self.immediate_variable_patterns.keys():
            pattern_parts = pattern.split()
            combo_parts = combo_chain.split()

            # If we have fewer parts than the pattern and they match so far, it could be a start
            if len(combo_parts) < len(pattern_parts):
                matches_so_far = True
                for i, combo_part in enumerate(combo_parts):
                    pattern_part = pattern_parts[i]
                    if not pattern_part.startswith('$') and pattern_part != combo_part:
                        matches_so_far = False
                        break
                if matches_so_far:
                    return True

        # Check delayed variable patterns
        for pattern in self.delayed_variable_patterns.keys():
            pattern_parts = pattern.split()
            combo_parts = combo_chain.split()

            # If we have fewer parts than the pattern and they match so far, it could be a start
            if len(combo_parts) < len(pattern_parts):
                matches_so_far = True
                for i, combo_part in enumerate(combo_parts):
                    pattern_part = pattern_parts[i]
                    if not pattern_part.startswith('$') and pattern_part != combo_part:
                        matches_so_far = False
                        break
                if matches_so_far:
                    return True

        return False

    def _execute_potential_combo(self):
        self.combo_job = cron.after(self.combo_window, self._delayed_potential_combo)

    def execute(self, noise: str):
        global parrot_debounce_busy

        if noise not in self.base_noises:
            return

        if noise in self.base_pairs:
            if parrot_debounce_busy.get(f"{noise}_stop"):
                cron.cancel(parrot_debounce_busy[f"{noise}_stop"])
                parrot_debounce_busy[f"{noise}_stop"] = False
                return

        if self.combo_job:
            cron.cancel(self.combo_job)
            self.combo_job = None

        self.combo_chain = self.combo_chain + f" {noise}" if self.combo_chain else noise

        if self.combo_chain in self.delayed_commands:
            self._prepare_delayed_command()
        elif self.combo_chain in self.immediate_commands:
            if self._could_be_variable_pattern_start(self.combo_chain):
                self._execute_potential_combo()
            else:
                self._execute_immediate_command(noise)
        elif self.has_variables and self._try_variable_patterns(self.combo_chain, self.immediate_variable_patterns):
            self._execute_immediate_variable_pattern()
        elif self.has_variables and self._try_variable_patterns(self.combo_chain, self.delayed_variable_patterns):
            self._execute_delayed_variable_command()
        # Fallback to single noise commands
        elif noise in self.immediate_commands:
            self._execute_single_immediate_command(noise)
        else:
            self._execute_potential_combo()

# todo: try using the user's direct reference instead
parrot_config_saved = ParrotConfig()

parrot_throttle_busy = {}
parrot_debounce_busy = {}

def parrot_throttle_disable(id):
    global parrot_throttle_busy
    parrot_throttle_busy[id] = False

def parrot_throttle(time_ms: int, single_noise: str, command: callable):
    """Throttle the command once every time_ms"""
    global parrot_throttle_busy
    if parrot_throttle_busy.get(single_noise):
        return
    parrot_throttle_busy[single_noise] = True
    command()
    cron.after(f"{time_ms}ms", lambda: parrot_throttle_disable(single_noise))

def parrot_debounce_disable(id):
    global parrot_debounce_busy
    parrot_debounce_busy[id] = False

def parrot_debounce(time_ms: int, id: str, command: callable):
    """Debounce"""
    global parrot_debounce_busy
    if parrot_debounce_busy.get(id):
        cron.cancel(parrot_debounce_busy[id])
    parrot_debounce_busy[id] = cron.after(f"{time_ms}ms", lambda: (command(), parrot_debounce_disable(id)))

def parrot_config_noise(sound: str):
    config = actions.user.parrot_config()
    if parrot_config_saved.parrot_config_user_ref != config:
        print("init parrot config")
        parrot_config_saved.setup(config)

    parrot_config_saved.execute(sound)

def parrot_config_event_register(on_noise: callable):
    event_subscribers.append(on_noise)

def parrot_config_event_unregister(on_noise: callable):
    try:
        event_subscribers.remove(on_noise)
    except ValueError:
        # we may have lost the reference
        # see if the callback looks like one of the subscribers
        for subscriber in event_subscribers:
            if subscriber.__name__ == on_noise.__name__:
                event_subscribers.remove(subscriber)
                break

def parrot_config_event_trigger(noise: str, command: str):
    for on_noise_subscriber in event_subscribers:
        on_noise_subscriber(noise, command)

def parrot_config_get_mode() -> str:
    return parrot_config_saved.current_mode

def parrot_config_set_mode(mode: str):
    config = actions.user.parrot_config()
    if mode in config:
        # probably need to build a queue for this instead
        cron.after("30ms", lambda: parrot_config_saved.setup_mode(mode))
    else:
        raise ValueError(f"Mode '{mode}' not found in parrot_config")

def parrot_config_cycle_mode() -> str:
    config = actions.user.parrot_config()
    modes = list(config.keys())
    current_mode = parrot_config_get_mode()
    if current_mode in modes:
        current_index = modes.index(current_mode)
        next_index = (current_index + 1) % len(modes)
        next_mode = modes[next_index]
        parrot_config_set_mode(next_mode)
        return next_mode
    else:
        raise ValueError(f"Mode '{current_mode}' not found in parrot_config")