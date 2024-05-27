from talon import Module, actions, cron, ctrl, clip

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
_step_dir = None
_step_job = None
_last_calibrate_value_x = 0
_last_calibrate_value_y = 0

queue = []

def queue_action(action, number):
    """Queue an action with optional modifier number"""
    global queue
    # go 2, left, go 3, right
    # if queue:
    #     queue.append((action, number))
    # else:
    #     action, number = queue.pop(0)
    #     queue_action(action, number)

def move_dir(key: str):
    """Hold a direction key"""
    global _move_dir
    if _move_dir:
        actions.key(f"{_move_dir}:up")
    _move_dir = key
    actions.key(f"{_move_dir}:down")

def move_dir_toggle(key: str):
    """Toggle a direction key"""
    global _move_dir
    if _move_dir:
        actions.key(f"{_move_dir}:up")
        if _move_dir == key:
            _move_dir = None
            return
    _move_dir = key
    actions.key(f"{_move_dir}:down")

def move_dir_stop():
    """Stop holding a direction key"""
    global _move_dir
    if _move_dir:
        actions.key(f"{_move_dir}:up")
        _move_dir = None

def step_stop():
    """Stop stepping in a direction"""
    global _step_job, _step_dir
    if _step_job:
        actions.key(f"{_step_dir}:up")
        cron.cancel(_step_job)
        _step_job = None
        _step_dir = None

def step_dir(key: str, duration: str):
    """Step in a direction for a duration"""
    global _step_dir, _step_job
    step_stop()
    _step_dir = key
    actions.key(f"{_step_dir}:down")
    _step_job = cron.after(duration, step_stop)

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
        # actions.mode.disable("user.game_nav")
        # actions.mode.enable("user.game_menu")
        # actions.user.game_show_commands("Game Menu", [
        #     "play",
        #     "scan",
        #     "up",
        #     "down",
        #     "left",
        #     "right",
        #     "exit"
        # ])

    def game_mode_enable():
        """Enable play mode"""
        actions.mode.enable("user.game")
        actions.mode.disable("command")
        # actions.mode.disable("user.game_menu")
        # actions.mode.disable("user.game_nav")
        # actions.user.game_show_commands("Game Menu", [
        #     "menu",
        #     "scan",
        #     "exit",
        #     "go",
        #     "go [dir]",
        #     "back",
        #     "step [dir]",
        #     "jump",
        #     "stop",
        #     "stop all",
        #     "crouch",
        #     "run",
        #     "hop [num]",
        #     "round",
        #     "left",
        #     "right",
        #     "left [num]",
        #     "right [num]",
        #     "look up",
        #     "look down",
        #     "look up [num]",
        #     "look down [num]",
        #     "set | reset"
        # ], "666222")

    def game_nav_mode_enable():
        """Enable nav mode"""
        # actions.mode.disable("user.game_menu")
        actions.mode.disable("user.game")
        # actions.mode.enable("user.game_nav")

    def game_mode_disable():
        """Disable game mode"""
        # actions.mode.disable("user.game_menu")
        actions.mode.disable("user.game")
        actions.mode.enable("command")
        # actions.mode.disable("user.game_nav")
        stopper()
        # actions.user.game_hide_commands()

def mouse_reset_center_y():
    """Reset the mouse to the center of the screen."""
    print("resetting center")
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