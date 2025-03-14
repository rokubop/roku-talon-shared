from talon import Module, Context, actions, cron
from talon.types import Rect, Point2d
from .actions import (
    location,
    toggle_parrot_v6,
    mouse_move_smooth_to_gaze,
    mouse_jump_and_move_continuous,
    mouse_move_smooth_from_gaze,
    mouse_move_stop,
    mouse_move_continuous,
    mouse_shove_and_move,
    shove_modifier,
    scan_modifier,
    toggle_full_tracking,
    stopper,
    jump_to_gaze_and_head_track,
    click,
    roaming_a,
    roaming_x,
    roaming_b,
    roaming_y,
    roaming_left_walk_or_camera,
    roaming_right_walk_or_camera,
    roaming_up_walk_or_camera,
    roaming_down_walk_or_camera,
    roaming_switch_x_mode,
    roaming_switch_y_mode,
    roaming_switch_left,
    roaming_switch_right,
    roaming_switch_up,
    roaming_switch_down,
    shoot_and_stop,
    zoom_toggle_and_stop
)
from .ui import ui

mod = Module()
ctx = Context()

mod, ctx, ctx_game = Module(), Context(), Context()
# mod.apps.mass_effect_1 = "os: windows\nand app.exe: /code.exe/i"
mod.apps.mass_effect_1 = "os: windows\nand app.exe: /masseffect1.exe/i"
ctx.matches = "os: windows\napp: mass_effect_1"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

def move_in_dir_of_gaze_point_along_axis():
    actions.tracking.jump()
    x = actions.mouse_x()
    y = actions.mouse_y()

    screen_width = 1920
    screen_height = 1080

    # Calculate region boundaries

    middle_x_min = screen_width // 3
    middle_x_max = 2 * (screen_width // 3)

    top_y_max = screen_height // 3
    bottom_y_min = 2 * (screen_height // 3)

    # Determine region and trigger movement
    if middle_x_min <= x <= middle_x_max:  # Middle column
        if y < top_y_max:  # Top-middle region
            actions.user.game_mouse_move_continuous_up_10()
        elif y > bottom_y_min:  # Bottom-middle region
            actions.user.game_mouse_move_continuous_down_10()
        else:  # Middle row (default to X behavior)
            if x < (screen_width // 2):  # Left of screen center
                actions.user.game_mouse_move_continuous_left_10()
            else:  # Right of screen center
                actions.user.game_mouse_move_continuous_right_10()
    else:  # Left or right columns (default to X behavior)
        if x < (screen_width // 2):  # Left of screen center
            actions.user.game_mouse_move_continuous_left_10()
        else:  # Right of screen center
            actions.user.game_mouse_move_continuous_right_10()

def move_in_dir_of_gaze_point_directly():
    x = actions.mouse_x()
    y = actions.mouse_y()
    actions.tracking.jump()
    new_x = actions.mouse_x()
    new_y = actions.mouse_y()

    actions.user.mouse_move_smooth_from_to(x, y, new_x, new_y)

def weapon_swap():
    actions.tracking.jump()
    x = actions.mouse_x()
    y = actions.mouse_y()

    top_mid = Rect(640, 0, 640, 360)
    if top_mid.contains(Point2d(x, y)):
        actions.user.game_key("h") # put weapon away
        return

    if x < 960:
        actions.mouse_scroll(1, by_lines=True)
    else:
        actions.mouse_scroll(-1, by_lines=True)

def set_parrot_config(config_name):
    global parrot_config
    parrot_config = configs[config_name]
    actions.user.ui_elements_set_state("parrot_config_name", config_name)
    actions.user.ui_elements_set_state("parrot_config", parrot_config)
    actions.user.ui_elements_set_state("background_color", config_colors[config_name])

common_config = {
    "cluck cluck": ("exit", actions.user.game_mode_disable),
    "cluck ss":    ("controller mode", lambda: set_parrot_config("controller")),
    "cluck sh":    ("roaming mode", lambda: set_parrot_config("roaming")),
    "cluck t":     ("fighting mode", lambda: set_parrot_config("fighting")),
    "cluck pop":   ("ui mode", lambda: set_parrot_config("ui")),
    "cluck oh":    ("dpad right", lambda: actions.user.game_xbox_dpad_press_dir("right")),
    "cluck ah":    ("dpad left", lambda: actions.user.game_xbox_dpad_press_dir("left")),
    "cluck guh":   ("dpad down", lambda: actions.user.game_xbox_dpad_press_dir("down")),
    "cluck eh":    ("dpad up", lambda: actions.user.game_xbox_dpad_press_dir("up")),
}


controller_config = {
    "ah:th_90": ("dpad left", lambda: actions.user.game_xbox_dpad_press_dir("left")),
    "oh:th_90": ("dpad right", lambda: actions.user.game_xbox_dpad_press_dir("right")),
    "guh":      ("dpad down", lambda: actions.user.game_xbox_dpad_press_dir("down")),
    "eh":       ("dpad up", lambda: actions.user.game_xbox_dpad_press_dir("up")),
    "ee":       ("stop", stopper),
    "sh:th_90": ("A", lambda: actions.user.game_xbox_button_press("A")),
    "ss:th_90": ("B", lambda: actions.user.game_xbox_button_press("X")),
    "palate":   ("Y", lambda: actions.user.game_xbox_button_press("Y")),
    "er":       ("X", lambda: actions.user.game_xbox_button_press("B")),
    "tut":      ("L1", lambda: actions.user.game_xbox_button_press("LB")),
    "tut tut":  ("R1", lambda: actions.user.game_xbox_button_press("RB")),
    "t":        ("R2", lambda: actions.user.game_xbox_button_press("RT")),
    "pop":      ("L2", lambda: actions.user.game_xbox_button_press("LT")),
    "tut ah":   ("view", lambda: actions.user.game_xbox_button_press("view")),
    "tut oh":   ("menu", lambda: actions.user.game_xbox_button_press("guide")),
    "tut guh":  ("back", lambda: actions.user.game_xbox_button_press("back")),
    "cluck":    ("start", lambda: actions.user.game_xbox_button_press("menu")),
    "mm ah":    ("dpad left hold", lambda: actions.user.game_xbox_dpad_hold_only_dir("left")),
    "mm oh":    ("dpad right hold", lambda: actions.user.game_xbox_dpad_hold_only_dir("right")),
    "mm guh":   ("dpad down hold", lambda: actions.user.game_xbox_dpad_hold_only_dir("down")),
    "mm eh":    ("dpad up hold", lambda: actions.user.game_xbox_dpad_hold_only_dir("up")),
    "mm ss":    ("B hold", lambda: actions.user.game_xbox_button_hold("X")),
    "mm sh":    ("A hold", lambda: actions.user.game_xbox_button_hold("A")),
    "mm palate":("Y hold", lambda: actions.user.game_xbox_button_hold("Y")),
    "mm er":    ("X hold", lambda: actions.user.game_xbox_button_hold("B")),
    "mm pop":   ("R1 hold", lambda: actions.user.game_xbox_button_hold("RB")),
    "mm t":     ("R2 hold", lambda: actions.user.game_xbox_button_hold("RT")),
    "mm tut":   ("L1 hold", lambda: actions.user.game_xbox_button_hold("LB")),
    "mm cluck": ("L2 hold", lambda: actions.user.game_xbox_button_hold("LT")),
    **common_config
}

fighting_config = {
    **common_config
}

ui_config = {
    **common_config
}


default_config = {
    "ah":       ("left", lambda: actions.user.game_xbox_right_stick_hold_dir("left")),
    "oh":       ("right", lambda: actions.user.game_xbox_right_stick_hold_dir("right")),
    "eh":       ("up", lambda: actions.user.game_xbox_left_stick_hold_dir("up")),
    "guh":      ("down", lambda: actions.user.game_xbox_left_stick_hold_dir("down")),
    "ee":       ("stop", stopper),
    "sh:th_90": ("A or large boost", roaming_a),
    "ss:th_90": ("X or med boost", roaming_x),
    "palate":   ("Y or small boost", roaming_y),
    "er":       ("B or full stop", roaming_b),
    "pop":      ("L2", zoom_toggle_and_stop),
    "t":        ("R2", shoot_and_stop),
    "mm":       ("cursor to gaze", mouse_move_smooth_to_gaze),
    "mm ah":    ("walk left", lambda: actions.user.game_xbox_left_stick_hold_dir("left")),
    "mm oh":    ("walk right", lambda: actions.user.game_xbox_left_stick_hold_dir("right")),
    "mm guh":   ("180", actions.user.game_mouse_move_deg_180),
    "tut ah":   ("left 90", actions.user.game_mouse_move_deg_left_90),
    "tut oh":   ("right 90", actions.user.game_mouse_move_deg_right_90),
    "tut guh":  ("180", actions.user.game_mouse_move_deg_180),
    "tut tut":  ("holster", lambda: actions.user.game_xbox_button_press("view")),
    "cluck":    ("exit", actions.user.game_mode_disable),
}

aim_config = {
    **default_config,
    "eh":       ("up", lambda: actions.user.game_xbox_right_stick_hold_dir("up")),
    "guh":      ("down", lambda: actions.user.game_xbox_right_stick_hold_dir("down")),
    "pop":      ("L2", shoot_and_stop),
    "mm":       ("L2 toggle", lambda: actions.user.game_xbox_button_toggle("RT")),
    "tut":      ("cursor to gaze", mouse_move_smooth_to_gaze),
}

roaming_config = {
    **controller_config,
    "ah":       ("left", roaming_left_walk_or_camera),
    "oh":       ("right", roaming_right_walk_or_camera),
    "eh":       ("forward", roaming_up_walk_or_camera),
    "guh":      ("back", roaming_down_walk_or_camera),
    "ee":       ("stop", stopper),
    "sh:th_90": ("A or large boost", roaming_a),
    "ss:th_90": ("X or med boost", roaming_x),
    "palate":   ("Y or small boost", roaming_y),
    "er":       ("B or full stop", roaming_b),
    "pop":      ("L2", zoom_toggle_and_stop),
    "t":        ("R2", shoot_and_stop),
    "mm ah":    ("switch x cam/walk", roaming_switch_left),
    "mm oh":    ("switch x cam/walk", roaming_switch_right),
    "mm eh":    ("switch y cam/walk", roaming_switch_up),
    "mm guh":   ("switch y cam/walk", roaming_switch_down),
    "mm":       ("cursor to gaze", mouse_move_smooth_to_gaze),
    # "mm":           ("jump to gaze", jump_to_gaze_and_head_track),
    # "mm sh":        ("push to gaze", mouse_move_smooth_to_gaze),
    # "mm ss":        ("pull from gaze", mouse_move_smooth_from_gaze),
    # "mm eh":        ("jump + up", lambda: mouse_move_continuous("up")),
    # "mm guh":       ("jump + down", lambda: mouse_move_continuous("down")),
    # "tut mm":       ("toggle full tracking", toggle_full_tracking),
    # "tut":        ("reset y", actions.user.game_mouse_move_reset_center_y),
    "tut ah":     ("left 90", actions.user.game_mouse_move_deg_left_90),
    "tut oh":     ("right 90", actions.user.game_mouse_move_deg_right_90),
    "tut guh":    ("180", actions.user.game_mouse_move_deg_180),
    "tut tut":    ("holster", lambda: actions.user.game_xbox_button_press("view")),
    # "hiss:db_90": ("space", lambda: actions.user.game_key("space")),
    # "hiss_stop":  ("", lambda: None),
    # "shush":      ("cursor to gaze", enter_look_mode),
    # "shush_stop": ("", lambda: None),
    # # "palate":     ("space", lambda: actions.user.game_key("space")),
    # "pop":        ("L click", actions.user.game_mouse_click_left),
    # "palate":     ("R click", actions.user.game_mouse_click_right),
    # "t":          ("weapon swap", weapon_swap),
    # "tut pop":    ("hold L click", actions.user.game_mouse_hold_left),
    # "tut cluck":  ("hold R click", actions.user.game_mouse_hold_right),
    # "tut ee":     ("scroll tick mode", use_scroll_tick),
    # "er":         ("exit mode", actions.user.game_mode_disable),
    # **common_config
}

camera_config = {
    **roaming_config,
    # "sh": ("large burst", camera_speed_boost_long),
    # "ss": ("small burst", camera_speed_boost_short),
}

configs = {
    "controller": controller_config,
    "roaming": roaming_config,
    # "camera": camera_config,
    "fighting": fighting_config,
    "ui": ui_config
}

config_colors = {
    "controller": "22266688",
    "roaming": "22662288",
    "camera": "66222288",
    "fighting": "66662288",
    "ui": "22226688"
}

last_x_dir = None

def go_left_continuous():
    global last_x_dir
    last_x_dir = "left"
    actions.user.game_mouse_move_continuous_left_5()

def go_right_continuous():
    global last_x_dir
    last_x_dir = "right"
    actions.user.game_mouse_move_continuous_right_5()

def go_up_diagonal():
    if last_x_dir == "left":
        actions.user.game_mouse_move_continuous(-1, -1)
    else:
        actions.user.game_mouse_move_continuous(1, -1)

def go_down_diagonal():
    if last_x_dir == "left":
        actions.user.game_mouse_move_continuous(-1, 1)
    else:
        actions.user.game_mouse_move_continuous(1, 1)

parrot_config = default_config
pedal_center_up_job = None

def use_aim_mode():
    global parrot_config
    zoom_toggle_and_stop()
    parrot_config = aim_config
    actions.user.ui_elements_set_state("parrot_config", parrot_config)

def stop_aim_mode():
    global parrot_config, pedal_center_up_job
    pedal_center_up_job = None
    zoom_toggle_and_stop()
    parrot_config = default_config
    actions.user.ui_elements_set_state("parrot_config", parrot_config)

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        actions.user.game_xbox_gamepad_enable()
        actions.user.game_xbox_right_stick_set_gear(2)
        actions.user.ui_elements_show(ui, initial_state={
            "parrot_config_name": "default",
            "parrot_config": parrot_config,
            "background_color": "22266688"
        })

    def pedal_center_down():
        if pedal_center_up_job:
            cron.cancel(pedal_center_up_job)
            # do nothing - already running
        else:
            use_aim_mode()

    def pedal_center_up():
        global pedal_center_up_job
        pedal_center_up_job = cron.after("20ms", stop_aim_mode)

    def on_game_mode_disabled():
        actions.user.game_xbox_gamepad_disable()
        actions.user.ui_elements_hide_all()

    def parrot_config():
        return parrot_config