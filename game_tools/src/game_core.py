from talon import Module, Context, actions, cron, ctrl, clip, settings
from .game_events import (
    event_on_game_mode,
    event_on_key,
    event_on_mouse,
)

mod = Module()
ctx = Context()

_move_dir = None
_move_dir_last_horizontal = "d"
_horizontal_keys = { "right", "left", "a", "d" }
_step_dir = None
_step_job = None
_last_calibrate_value_x = 0
_last_calibrate_value_y = 0
_curve_dir = None
_curve_type = "inward"
_curve_speed = None
_held_keys = set()
_held_mouse_buttons = set()
_key_up_pending_jobs = {}
_camera_speed = None
_camera_snap_angle = None
_game_key_repeat_wait = 16.0

DIR_MODE_CAM_CONTINUOUS = "continuous"
DIR_MODE_CAM_SNAP = "snap"
DIR_MODE_MOVE = "move"
SNAP_DIR_X = "x"
SNAP_DIR_Y = "y"

_preferred_dir_mode = DIR_MODE_CAM_CONTINUOUS
_dir_mode = None
_last_snap_dir = SNAP_DIR_X

queue = []

arrow_to_wasd = {
    "left": "a",
    "right": "d",
    "up": "w",
    "down": "s",
}

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
    curve_dir_stop()
    if isinstance(keys, tuple):
        for k in keys:
            actions.key(f"{k}:up")
            event_on_key.fire_release(k)
            if k in _held_keys:
                _held_keys.remove(k)
    else:
        actions.key(f"{keys}:up")
        event_on_key.fire_release(keys)
        if keys in _held_keys:
                _held_keys.remove(keys)

def hold_dir(keys):
    if isinstance(keys, tuple):
        for k in keys:
            actions.key(f"{k}:down")
            event_on_key.fire_hold(k)
            _held_keys.add(k)
    else:
        actions.key(f"{keys}:down")
        event_on_key.fire_hold(keys)
        _held_keys.add(keys)

def move_dir(keys: str | tuple[str, str]):
    """Hold a direction key"""
    global _move_dir, _move_dir_last_horizontal

    if _move_dir:
        release_dir(_move_dir)

    _move_dir = keys

    if keys in _horizontal_keys:
        _move_dir_last_horizontal = keys

    hold_dir(_move_dir)

def curve_dir(key: str):
    global _curve_dir
    curve_dir_stop()
    if key in ["a", "left"]:
        actions.user.mouse_move_continuous(-1, 0, _curve_speed)
    elif key in ["d", "right"]:
        actions.user.mouse_move_continuous(1, 0, _curve_speed)
    _curve_dir = key

def curve_dir_stop():
    global _curve_dir
    if _curve_dir:
        actions.user.mouse_move_continuous_stop()
        _curve_dir = None

def move_dir_curve(key: str, initial_curve_amount: int = None):
    """Hold a direction key with a curve"""
    global _curve_speed
    if _curve_speed is None:
        _curve_speed = initial_curve_amount or settings.get("user.game_mouse_move_continuous_default_speed")
    move_dir(key)
    curve_dir(key)

def move_dir_toggle(keys: str | tuple[str, str]):
    """Toggle a direction key"""
    global _move_dir

    if _move_dir:
        release_dir(_move_dir)
        if _move_dir == keys:
            _move_dir = None
            return

    _move_dir = keys
    hold_dir(_move_dir)

def game_arrows_hold_up_horizontal():
    if _move_dir_last_horizontal == "right":
        move_dir(('right', 'up'))
    elif _move_dir_last_horizontal == "left":
        move_dir(('left', 'up'))
    elif _move_dir_last_horizontal == "d":
        move_dir(('d', 'w'))
    elif _move_dir_last_horizontal == "a":
        move_dir(('a', 'w'))

def game_arrows_hold_down_horizontal():
    if _move_dir_last_horizontal == "right":
        move_dir(('right', 'down'))
    elif _move_dir_last_horizontal == "left":
        move_dir(('left', 'down'))
    elif _move_dir_last_horizontal == "d":
        move_dir(('d', 's'))
    elif _move_dir_last_horizontal == "a":
        move_dir(('a', 's'))

def game_dir_hold_last_horizontal():
    if _move_dir_last_horizontal == "right":
        actions.user.game_arrows_hold_right()
    elif _move_dir_last_horizontal == "left":
        actions.user.game_arrows_hold_left()
    elif _move_dir_last_horizontal == "d":
        actions.user.game_wasd_hold_d()
    elif _move_dir_last_horizontal == "a":
        actions.user.game_wasd_hold_a()

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
        event_on_key.fire_release(_step_dir)
        if _step_dir in _held_keys:
            _held_keys.remove(_step_dir)
        cron.cancel(_step_job)
        _step_job = None
        _step_dir = None

def step_dir(key: str, duration_ms: int):
    """Step in a direction for a duration"""
    global _step_dir, _step_job
    step_stop()
    _step_dir = key
    actions.key(f"{_step_dir}:down")
    event_on_key.fire_hold(_step_dir)
    _step_job = cron.after(f"{duration_ms}ms", step_stop)

def mouse_release_all():
    """Release all mouse buttons"""
    global _held_mouse_buttons
    for button in _held_mouse_buttons:
        actions.mouse_release(button)
        event_on_mouse.fire_release(button)
    _held_mouse_buttons.clear()

def mouse_hold(button: int, duration_ms: int = None):
    """Hold a mouse button"""
    global _held_mouse_buttons
    if duration_ms:
        ctrl.mouse_click(button, hold=duration_ms*1000)
    else:
        ctrl.mouse_click(button, down=True)
    _held_mouse_buttons.add(button)
    event_on_mouse.fire_hold(button)

def mouse_toggle(button: int):
    """Toggle a mouse button"""
    global _held_mouse_buttons
    if button in _held_mouse_buttons:
        mouse_release(button)
    else:
        mouse_hold(button)

def mouse_release(button: int):
    """Release a mouse button"""
    global _held_mouse_buttons
    if button in _held_mouse_buttons:
        actions.mouse_release(button)
        event_on_mouse.fire_release(button)
        _held_mouse_buttons.remove(button)

def mouse_click(button: int, duration_ms: int = None):
    """Click a mouse button"""
    ctrl.mouse_click(button, hold=(duration_ms or settings.get("user.game_mouse_click_hold"))*1000)
    event_on_mouse.fire_click(button)

def stopper():
    """Perform general purpose stopper based on priority"""
    global _move_dir, _step_job, _curve_dir, _held_mouse_buttons
    if actions.user.mouse_move_info()["continuous_active"] and not _curve_dir:
        actions.user.mouse_move_continuous_stop()
        if _held_mouse_buttons:
            mouse_release_all()
        return

    curve_dir_stop()
    if _move_dir:
        move_dir_stop()
    if _step_job:
        step_stop()
    if _held_mouse_buttons:
        mouse_release_all()
    if _held_keys:
        for key in list(_held_keys):
            game_key_release(key)

def mouse_reset_center_y():
    """Reset the mouse to the center of the screen."""

    game_mouse_move_degrees(0, 180, 100)
    actions.user.mouse_move_smooth_queue(lambda: game_mouse_move_degrees(0, -90, 100))

def on_calibrate_x_360_tick(value):
    actions.skip()
#     global _last_calibrate_value_x
#     actions.user.game_ui_calibrate_update(_last_calibrate_value_x + value.dx)
#     if value.type == "stop":
#         _last_calibrate_value_x += value.dx

def on_calibrate_y_90_tick(value):
    actions.skip()
#     global _last_calibrate_value_y
#     actions.user.game_ui_calibrate_update(_last_calibrate_value_y - value.dy)
#     if value.type == "stop":
#         _last_calibrate_value_y -= value.dy

def game_mouse_calibrate_x_360(dx360: int):
    actions.skip()
#     """Calibrate a 360 spin"""
#     global _last_calibrate_value_x
#     _last_calibrate_value_x = 0
#     actions.user.mouse_move_smooth_delta(dx360, 0, 1000, on_calibrate_x_360_tick, mouse_api_type="windows")

def game_mouse_calibrate_x_360_adjust_last(dx: int):
    actions.skip()
#     """Add or subtract to the last x calibration."""
#     actions.user.mouse_move_smooth_delta(dx, 0, 500, on_calibrate_x_360_tick, mouse_api_type="windows")

def game_mouse_calibrate_y_90_adjust_last(dy: int):
    actions.skip()
#     """Add or subtract to the last x calibration."""
#     actions.user.mouse_move_smooth_delta(0, dy, 500, on_calibrate_y_90_tick, mouse_api_type="windows")

def game_calibrate_90_y(dy_90: int):
    actions.skip()
#     """Calibrate looking down to the ground and looking up to center."""
#     global _last_calibrate_value_y
#     _last_calibrate_value_y = 0
#     actions.user.mouse_move_smooth_delta(0, dy_90 * 2, 100, mouse_api_type="windows")
#     actions.user.mouse_move_smooth_queue(lambda: actions.user.mouse_move_smooth_delta(0, -dy_90, 100, on_calibrate_y_90_tick, mouse_api_type="windows"))

def game_key_release(key):
    global _key_up_pending_jobs
    actions.key(f"{key}:up")
    event_on_key.fire_release(key)
    if _key_up_pending_jobs.get(key):
        cron.cancel(_key_up_pending_jobs[key])
        _key_up_pending_jobs[key] = None
    if key in _held_keys:
        _held_keys.remove(key)

def game_key_down(key: str):
    """Hold a key down"""
    actions.key(f"{key}:down")
    event_on_key.fire_hold(key)
    _held_keys.add(key)

def game_key(key: str):
    """Press a game key"""
    actions.key(key)
    event_on_key.fire_press(key)
    if _key_up_pending_jobs.get(key):
        cron.cancel(_key_up_pending_jobs[key])
        _key_up_pending_jobs[key] = None
    if key in _held_keys:
        _held_keys.remove(key)

def game_key_hold(key: str, hold: int = None, retrigger: bool = True):
    """Hold a game key"""
    global _key_up_pending_jobs
    if not hold:
        game_key_down(key)
        return

    if retrigger and key in _held_keys:
        game_key_release(key)
        actions.sleep(_game_key_repeat_wait)

    game_key_down(key)
    _key_up_pending_jobs[key] = cron.after(f"{hold}ms", lambda: game_key_release(key))

def game_key_toggle(key: str):
    """Toggle a game key"""
    if key in _held_keys:
        game_key_release(key)
    else:
        game_key_down(key)

def game_key_sequence(keys: str, delay_ms: int = 0):
    for key in keys.split(" "):
        game_key(key)
        if delay_ms:
            actions.sleep(delay_ms / 1000)

def get_held_keys():
    """Get the held keys"""
    return _held_keys

def get_held_mouse_buttons():
    """Get the held mouse buttons"""
    return _held_mouse_buttons

def game_mouse_move_degrees(dx_degrees: int, dy_degrees: int, duration_ms = None, callback_stop = None):
    dx_360 = settings.get("user.game_mouse_calibrate_x_360")
    dy_90 = settings.get("user.game_mouse_calibrate_y_90")
    dx_total = dx_360 / 360 * dx_degrees
    dy_total = dy_90 / 90 * dy_degrees
    actions.user.mouse_move_smooth_delta(dx_total, dy_total, duration_ms, callback_stop=callback_stop)

def mouse_move_deg(deg_x: int, deg_y: int, mouse_button: int = None):
    if mouse_button is not None:
        mouse_hold(mouse_button)

        def on_stop():
            mouse_release(mouse_button)

        game_mouse_move_degrees(deg_x, deg_y, callback_stop=on_stop)
    else:
        game_mouse_move_degrees(deg_x, deg_y)

def mouse_move_continuous(x: int, y: int, speed: int, mouse_button: int = None):
    if mouse_button is not None:
        mouse_hold(mouse_button)
    actions.user.mouse_move_continuous(x, y, speed)

def mouse_move_continuous_stop(debounce_ms: int = 150):
    if get_held_mouse_buttons():
        mouse_release_all()
    actions.user.mouse_move_continuous_stop(debounce_ms)

def camera_continuous_dynamic(dir: str):
    global _dir_mode, _camera_speed
    _dir_mode = DIR_MODE_CAM_CONTINUOUS

    if not _camera_speed:
        _camera_speed = settings.get("user.game_mouse_move_continuous_default_speed")

    if dir == "left":
        mouse_move_continuous(-1, 0, _camera_speed)
    elif dir == "right":
        mouse_move_continuous(1, 0, _camera_speed)
    elif dir == "up":
        mouse_move_continuous(0, -1, _camera_speed)
    elif dir == "down":
        mouse_move_continuous(0, 1, _camera_speed)

def camera_continuous_dynamic_set_speed(speed: int):
    global _camera_speed
    _camera_speed = speed

def camera_snap_dynamic(dir: str):
    global _last_snap_dir, _dir_mode, _camera_snap_angle
    _dir_mode = DIR_MODE_CAM_SNAP

    if not _camera_snap_angle:
        _camera_snap_angle = settings.get("user.game_mouse_move_deg_default_angle")

    if dir == "left":
        mouse_move_deg(-_camera_snap_angle, 0)
        _last_snap_dir = SNAP_DIR_X
    elif dir == "right":
        mouse_move_deg(_camera_snap_angle, 0)
        _last_snap_dir = SNAP_DIR_X
    elif dir == "up":
        mouse_move_deg(0, -_camera_snap_angle)
        _last_snap_dir = SNAP_DIR_Y
    elif dir == "down":
        mouse_move_deg(0, _camera_snap_angle)
        _last_snap_dir = SNAP_DIR_Y
    elif dir == "back":
        mouse_move_deg(0, 180)

def camera_snap_dynamic_set_angle(angle: int):
    global _camera_snap_angle
    _camera_snap_angle = angle

def game_gear_set(gear_num: int):
    """Set the gear number"""
    if _dir_mode == DIR_MODE_CAM_CONTINUOUS:
        speed = settings.get("user.game_mouse_move_continuous_gears").split(" ").get(gear_num)
        camera_continuous_dynamic_set_speed(speed)
    elif _dir_mode == DIR_MODE_CAM_SNAP:
        angle = settings.get("user.game_mouse_move_deg_gears").split(" ").get(gear_num)
        camera_snap_dynamic_set_angle(angle)

def set_globals():
    global _game_key_repeat_wait
    _game_key_repeat_wait = settings.get("user.game_key_repeat_wait") / 1000

@mod.action_class
class Actions:
    def game_mode_enable():
        """Enable game mode - calls ctx def on_game_mode_enabled"""
        actions.mode.enable("user.game")
        if settings.get("user.game_mode_disables_command_mode"):
            actions.mode.disable("command")
        set_globals()
        print("game_mode_enable")
        event_on_game_mode.fire_enabled()
        actions.user.on_game_mode_enabled()

    def game_mode_disable():
        """Disable game mode"""
        actions.user.on_game_mode_disabled()
        event_on_game_mode.fire_disabled()
        stopper()
        actions.mode.disable("user.game")
        ctx.tags = []
        actions.mode.enable("command")
        print("game_mode_disable")

    # def game_mouse_calibrate_x_360_add(num: int):
    #     """Add to the current x calibration."""
    #     game_mouse_calibrate_x_360_adjust_last(num)

    # def game_mouse_calibrate_x_360_subtract(num: int):
    #     """Subtract to the current x calibration."""
    #     game_mouse_calibrate_x_360_adjust_last(-num)

    # def game_mouse_calibrate_y_90_add(num: int):
    #     """Add to the current x calibration."""
    #     game_mouse_calibrate_y_90_adjust_last(num)

    # def game_mouse_calibrate_y_90_subtract(num: int):
    #     """Subtract to the current x calibration."""
    #     game_mouse_calibrate_y_90_adjust_last(-num)

    # def game_mouse_calibrate_x_360_copy_to_clipboard():
    #     """Copy the last x calibration to the clipboard."""
    #     print("WIP")
    #     actions.skip()
    #     # clip.set_text(str(_last_calibrate_value_x))

    # def game_mouse_calibrate_y_90_copy_to_clipboard():
    #     """Copy the last y calibration to the clipboard."""
    #     print("WIP")
    #     actions.skip()
    #     # clip.set_text(str(_last_calibrate_value_y))

    # def game_mode_calibrate_x_enable():
    #     """Start calibrating x"""
    #     print("WIP")
    #     actions.skip()
    #     # actions.mode.disable("user.game_calibrating_y")
    #     # actions.mode.enable("user.game_calibrating_x")
    #     # actions.user.game_ui_show_calibrate_x()

    # def game_mode_calibrate_x_disable():
    #     """Start calibrating x"""
    #     print("WIP")
    #     actions.skip()
    #     # actions.mode.disable("user.game_calibrating_x")
    #     # actions.user.game_ui_hide_game_modal_large()

    # def game_mode_calibrate_y_enable():
    #     """Start calibrating y"""
    #     print("WIP")
    #     actions.skip()
    #     # actions.mode.disable("user.game_calibrating_x")
    #     # actions.mode.enable("user.game_calibrating_y")
    #     # actions.user.game_ui_show_calibrate_y()

    # def game_mode_calibrate_y_disable():
    #     """Start calibrating y"""
    #     print("WIP")
    #     actions.skip()
    #     # actions.mode.disable("user.game_calibrating_y")
    #     # actions.user.game_ui_hide_game_modal_large()

    def on_game_mode_enabled():
        """Triggered on game mode enabled"""
        no_op()

    def on_game_mode_disabled():
        """Triggered on game mode disabled"""
        no_op()
