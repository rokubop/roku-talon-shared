from talon import Module, actions, cron, ui, ctrl
import re
mod = Module()


def get_base_noise(noise):
    """The part before colon or @ e.g.'pop' in 'pop:db_170' or 'pop@top'"""
    base_noise = noise.split(':')[0].split('@')[0]
    return base_noise.strip()

def get_base_with_location_noise(noise):
    """The part before colon or @ e.g.'pop' in 'pop:db_170' or 'pop@top'"""
    base_noise = noise.split(':')[0]
    return base_noise.strip()

def is_prefix_of_other(cmd):
    return any(other_cmd.startswith(f"{cmd} ") and other_cmd != cmd for other_cmd in commands)

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
    if "th" in noise:
        match = re.search(r':th_(\d+)', noise)
        throttle_amount = int(match.group(1)) if match else 100
        return (action[0], lambda: parrot_throttle(throttle_amount, noise, action[1]))
    return action

def categorize_commands(commands):
    """Determine immediate vs delayed commands"""
    immediate_commands = {}
    delayed_commands = {}
    base_noise_set = set()
    base_noise_map = {}

    for noise in commands.keys():
        base_noise = get_base_noise(noise)

        base_noise_set.add(base_noise)
        base_noise_map[noise] = base_noise

    for noise, action in commands.items():
        (_base_noise, _modifiers, location) = parse_modifiers(noise)
        modified_action = get_modified_action(noise, action)
        base = base_noise_map[noise]
        if any(other_noise.startswith(f"{base} ") and other_noise != base for other_noise in base_noise_set):
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

    return immediate_commands, delayed_commands

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
        self.parrot_config_ref = None
        self.immediate_commands = {}
        self.delayed_commands = {}
        self.combo_chain = ""
        self.combo_job = None
        self.pending_combo = None

    def setup(self, parrot_config):
        if self.combo_job:
            cron.cancel(self.combo_job)
            self.combo_job = None
        self.combo_chain = ""
        self.pending_combo = None
        self.parrot_config_ref = parrot_config
        commands = parrot_config.get("commands", {}) if "commands" in parrot_config else parrot_config
        self.immediate_commands, self.delayed_commands = categorize_commands(commands)

    def _delayed_combo_execute(self):
        if self.combo_job:
            cron.cancel(self.combo_job)
            self.combo_job = None
        action = self.delayed_commands[self.pending_combo][1]
        executeActionOrLocationAction(action)
        self.combo_chain = ""
        self.pending_combo = None

    def execute(self, noise: str):
        if self.combo_job:
            cron.cancel(self.combo_job)
            self.combo_job = None

        self.combo_chain = self.combo_chain + f" {noise}" if self.combo_chain else noise

        if self.combo_chain in self.delayed_commands:
            self.pending_combo = self.combo_chain
            self.combo_job = cron.after("300ms", self._delayed_combo_execute)
        elif self.combo_chain in self.immediate_commands:
            action = self.immediate_commands[self.combo_chain][1]
            executeActionOrLocationAction(action)
            self.combo_chain = ""
            self.pending_combo = None
        elif noise in self.immediate_commands:
            if self.pending_combo:
                self._delayed_combo_execute()
                actions.sleep("20ms")
            action = self.immediate_commands[noise][1]
            executeActionOrLocationAction(action)

# todo: try using the user's direct reference instead
parrot_config_saved = ParrotConfig()

parrot_throttle_busy = {}

def parrot_throttle_disable(id):
    global parrot_throttle_busy
    parrot_throttle_busy[id] = False

def parrot_throttle(time_ms: int, id: str, command: callable):
    """Throttle the command once every time_ms"""
    global parrot_throttle_busy
    if parrot_throttle_busy.get(id):
        return
    parrot_throttle_busy[id] = True
    command()
    cron.after(f"{time_ms}ms", lambda: parrot_throttle_disable(id))

def use_parrot_config(sound: str):
    config = actions.user.parrot_config()
    if parrot_config_saved.parrot_config_ref != config:
        parrot_config_saved.setup(config)

    parrot_config_saved.execute(sound)
