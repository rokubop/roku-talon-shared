from talon import Module, actions, cron, ctrl, clip
from typing import Any

mod = Module()
# mod.mode("game_menu", "game menu mode")
mod.mode("game", "game play mode")
# mod.mode("game_nav", "game nav mode")
mod.mode("game_calibrating_x", "calibrating x")
mod.mode("game_calibrating_y", "calibrating y")

mod.setting(
    "game_calibrate_x_360",
    desc="x amount that is equivalent to 360 degrees",
    type=int,
    default=2000
)
mod.setting(
    "game_calibrate_y_90",
    desc="y amount that is equivalent to 90 degrees",
    type=int,
    default=500
)
_move_dir = None
_move_dir_last_horizontal = "d"
_horizontal_keys = { "right", "left", "a", "d" }
_step_dir = None
_step_job = None
_last_calibrate_value_x = 0
_last_calibrate_value_y = 0

queue = []

def no_op():
    pass

def queue_action(action, number):
    """Queue an action with optional modifier number"""
    global queue
    # go 2, left, go 3, right
    # if queue:
    #     queue.append((action, number))
    # else:
    #     action, number = queue.pop(0)
    #     queue_action(action, number)

def release_dir(keys):
    if isinstance(keys, tuple):
        for k in keys:
            actions.key(f"{k}:up")
            actions.user.game_event_trigger_on_key(k, "release")
            if k in held_keys:
                held_keys.remove(k)
    else:
        actions.key(f"{keys}:up")
        actions.user.game_event_trigger_on_key(keys, "release")
        if keys in held_keys:
                held_keys.remove(keys)

def hold_dir(keys):
    if isinstance(keys, tuple):
        for k in keys:
            actions.key(f"{k}:down")
            actions.user.game_event_trigger_on_key(k, "hold")
            held_keys.add(k)
    else:
        actions.key(f"{keys}:down")
        actions.user.game_event_trigger_on_key(keys, "hold")
        held_keys.add(keys)

def move_dir(keys: str | tuple[str, str]):
    """Hold a direction key"""
    global _move_dir, _move_dir_last_horizontal

    if _move_dir:
        release_dir(_move_dir)

    _move_dir = keys

    if keys in _horizontal_keys:
        _move_dir_last_horizontal = keys

    hold_dir(_move_dir)

def move_dir_toggle(keys: str | tuple[str, str]):
    """Toggle a direction key"""
    global _move_dir
    if _move_dir:
        release_dir(keys)
        if _move_dir == keys:
            _move_dir = None
            return

    _move_dir = keys
    hold_dir(_move_dir)

def game_move_dir_hold_up_horizontal():
    if _move_dir_last_horizontal == "right":
        move_dir(('right', 'up'))
    elif _move_dir_last_horizontal == "left":
        move_dir(('left', 'up'))
    elif _move_dir_last_horizontal == "d":
        move_dir(('d', 'w'))
    elif _move_dir_last_horizontal == "a":
        move_dir(('a', 'w'))

def game_move_dir_hold_down_horizontal():
    if _move_dir_last_horizontal == "right":
        move_dir(('right', 'down'))
    elif _move_dir_last_horizontal == "left":
        move_dir(('left', 'down'))
    elif _move_dir_last_horizontal == "d":
        move_dir(('d', 's'))
    elif _move_dir_last_horizontal == "a":
        move_dir(('a', 's'))

def game_move_dir_hold_last_horizontal():
    if _move_dir_last_horizontal == "right":
        actions.user.game_move_dir_hold_right()
    elif _move_dir_last_horizontal == "left":
        actions.user.game_move_dir_hold_left()
    elif _move_dir_last_horizontal == "d":
        actions.user.game_move_dir_hold_d()
    elif _move_dir_last_horizontal == "a":
        actions.user.game_move_dir_hold_a()

def game_state_switch_horizontal():
    global _move_dir_last_horizontal
    if _move_dir_last_horizontal == "right":
        _move_dir_last_horizontal = "left"
    elif _move_dir_last_horizontal == "left":
        _move_dir_last_horizontal = "right"
    elif _move_dir_last_horizontal == "d":
        _move_dir_last_horizontal = "a"
    elif _move_dir_last_horizontal == "a":
        _move_dir_last_horizontal = "d"

def move_dir_toggle_last_horizontal():
    game_key_toggle(_move_dir_last_horizontal)

def move_dir_stop():
    """Stop holding a direction key"""
    global _move_dir
    if _move_dir:
        release_dir(_move_dir)
        _move_dir = None

def step_stop():
    """Stop stepping in a direction"""
    global _step_job, _step_dir
    if _step_job:
        actions.key(f"{_step_dir}:up")
        actions.user.game_event_trigger_on_key(_step_dir, "release")
        if _step_dir in held_keys:
            held_keys.remove(_step_dir)
        cron.cancel(_step_job)
        _step_job = None
        _step_dir = None

def step_dir(key: str, duration_ms: int):
    """Step in a direction for a duration"""
    global _step_dir, _step_job
    step_stop()
    _step_dir = key
    actions.key(f"{_step_dir}:down")
    actions.user.game_event_trigger_on_key(_step_dir, "hold")
    _step_job = cron.after(f"{duration_ms}ms", step_stop)

def stopper():
    """Perform stop based on a priority"""
    global _move_dir, _step_job
    if actions.user.mouse_move_info()["continuous_active"]:
        actions.user.mouse_move_continuous_stop()
        return

    actions.user.mouse_move_stop()
    if _move_dir:
        move_dir_stop()
    if _step_job:
        step_stop()

@mod.action_class
class Actions:
    def game_show_commands(title: str, text_lines: list, bg_color: str = "222666", align: str = "right"):
        """Show the game commands"""
        actions.user.ui_textarea_show({
            "title": title,
            "bg_color": bg_color,
            "align": align,
            "text_lines": text_lines
        })

    def game_hide_commands():
        """Hide the game commands"""
        actions.user.ui_textarea_hide()

    def game_menu_mode_enable():
        """Enable menu mode"""
        actions.mode.disable("user.game")

    def game_mode_enable():
        """Enable play mode"""
        actions.mode.enable("user.game")
        actions.mode.disable("command")
        actions.user.on_game_mode_enabled()

    def game_nav_mode_enable():
        """Enable nav mode"""
        actions.mode.disable("user.game")

    def game_mode_disable():
        """Disable game mode"""
        actions.user.on_game_mode_disabled()
        actions.mode.disable("user.game")
        actions.mode.enable("command")
        stopper()

def mouse_reset_center_y():
    """Reset the mouse to the center of the screen."""
    actions.user.mouse_move_delta_degrees(0, 180, 100)
    actions.user.mouse_move_queue(lambda: actions.user.mouse_move_delta_degrees(0, -90, 100))

def on_calibrate_x_360_tick(value):
    global _last_calibrate_value_x
    actions.user.ui_calibrate_update(_last_calibrate_value_x + value.dx)
    if value.type == "stop":
        _last_calibrate_value_x += value.dx

def on_calibrate_y_90_tick(value):
    global _last_calibrate_value_y
    actions.user.ui_calibrate_update(_last_calibrate_value_y - value.dy)
    if value.type == "stop":
        _last_calibrate_value_y -= value.dy

def mouse_calibrate_x_360(dx360: int):
    """Calibrate a 360 spin"""
    global _last_calibrate_value_x
    _last_calibrate_value_x = 0
    actions.user.rt_mouse_move_delta(dx360, 0, 1000, on_calibrate_x_360_tick, mouse_api_type="windows")

def game_calibrate_x_360_adjust_last(dx: int):
    """Add or subtract to the last x calibration."""
    actions.user.rt_mouse_move_delta(dx, 0, 500, on_calibrate_x_360_tick, mouse_api_type="windows")

def game_calibrate_y_90_adjust_last(dy: int):
    """Add or subtract to the last x calibration."""
    actions.user.rt_mouse_move_delta(0, dy, 500, on_calibrate_y_90_tick, mouse_api_type="windows")

def mouse_calibrate_90_y(dy_90: int):
    """Calibrate looking down to the ground and looking up to center."""
    global _last_calibrate_value_y
    _last_calibrate_value_y = 0
    actions.user.rt_mouse_move_delta(0, dy_90 * 2, 100, mouse_api_type="windows")
    actions.user.mouse_move_queue(lambda: actions.user.rt_mouse_move_delta(0, -dy_90, 100, on_calibrate_y_90_tick, mouse_api_type="windows"))

up_jobs = {}
held_keys = set()

def game_key_up(key):
    global up_jobs
    actions.key(f"{key}:up")
    actions.user.game_event_trigger_on_key(key, "release")
    up_jobs[key] = None
    if key in held_keys:
        held_keys.remove(key)

def game_key_down(key: str):
    """Hold a key down"""
    actions.key(f"{key}:down")
    actions.user.game_event_trigger_on_key(key, "hold")
    held_keys.add(key)

def game_key(key: str):
    """Press a game key"""
    actions.key(key)
    actions.user.game_event_trigger_on_key(key, "press")
    if key in held_keys:
        held_keys.remove(key)

def game_key_hold(key: str, hold: int = None):
    """Hold a game key"""
    global up_jobs
    if not hold:
        game_key_down(key)
        return

    if up_jobs.get(key):
        cron.cancel(up_jobs[key])
    actions.key(f"{key}:up")
    actions.key(f"{key}:down")
    actions.user.game_event_trigger_on_key(key, "hold")
    up_jobs[key] = cron.after(f"{hold}ms", lambda: game_key_up(key))

def game_key_toggle(key: str):
    """Toggle a game key"""
    if key in held_keys:
        game_key_up(key)
    else:
        game_key_down(key)

@mod.action_class
class Actions:
    def game_calibrate_x_360_add(num: int):
        """Add to the current x calibration."""
        game_calibrate_x_360_adjust_last(num)

    def game_calibrate_x_360_subtract(num: int):
        """Subtract to the current x calibration."""
        game_calibrate_x_360_adjust_last(-num)

    def game_calibrate_y_90_add(num: int):
        """Add to the current x calibration."""
        game_calibrate_y_90_adjust_last(num)

    def game_calibrate_y_90_subtract(num: int):
        """Subtract to the current x calibration."""
        game_calibrate_y_90_adjust_last(-num)

    def game_calibrate_x_360_copy_to_clipboard():
        """Copy the last x calibration to the clipboard."""
        clip.set_text(str(_last_calibrate_value_x))

    def game_calibrate_y_90_copy_to_clipboard():
        """Copy the last y calibration to the clipboard."""
        clip.set_text(str(_last_calibrate_value_y))

    def game_mode_calibrate_x_enable():
        """Start calibrating x"""
        actions.mode.disable("user.game_calibrating_y")
        actions.mode.enable("user.game_calibrating_x")
        actions.user.ui_show_calibrate_x()

    def game_mode_calibrate_x_disable():
        """Start calibrating x"""
        actions.mode.disable("user.game_calibrating_x")
        actions.user.ui_hide_game_modal_large()

    def game_mode_calibrate_y_enable():
        """Start calibrating y"""
        actions.mode.disable("user.game_calibrating_x")
        actions.mode.enable("user.game_calibrating_y")
        actions.user.ui_show_calibrate_y()

    def game_mode_calibrate_y_disable():
        """Start calibrating y"""
        actions.mode.disable("user.game_calibrating_y")
        actions.user.ui_hide_game_modal_large()

    def on_game_mode_enabled():
        """Triggered on game mode enabled"""
        no_op()

    def on_game_mode_disabled():
        """Triggered on game mode disabled"""
        no_op()

    def game_event_register_on_key(callback: callable):
        """
        events:
        ```py
        "on_key", lambda key, state: # press/hold/release
        ```
        """
        global event_subscribers
        if "on_key" not in event_subscribers:
            event_subscribers["on_key"] = []
        event_subscribers["on_key"].append(callback)

    def game_event_unregister_on_key(callback: callable):
        """
        Unregister a callback for a specific game event.
        """
        global event_subscribers
        if "on_key" in event_subscribers:
            event_subscribers["on_key"].remove(callback)
            if not event_subscribers["on_key"]:
                del event_subscribers["on_key"]

    def game_event_trigger_on_key(key: str, state: str):
        """
        Trigger an event and call all registered callbacks.
        """
        global event_subscribers
        if "on_key" in event_subscribers:
            for callback in event_subscribers["on_key"]:
                callback(key, state)

event_subscribers = {}

    # def on_game_key_press(key: str):
    #     """On game key press"""
    #     pass

    # def on_game_key_hold(key: str):
    #     """On game key hold"""
    #     pass

    # def on_game_key_release(key: str):
    #     """On game key release"""
    #     pass