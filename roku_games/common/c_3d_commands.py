from talon import Module, Context, actions, noise, cron
from .c_3d_commands_ui import show_ui, hide_ui, update_current_noises_ui

mod, ctx = Module(), Context()
mod.tag("game_3d_commands", desc="Tag for enabling common 3D commands")
ctx.matches = r"""
# app: hi_fi_rush
app: bg_3
tag: user.game_3d_commands
mode: user.game
"""

commands = [
    "left",
    "right",
    "back",
    "go",
    "go <dir>",
    "jump",
    "stop",
    "crouch",
    "run",
    "round",
    "up",
    "down",
    "exit",
]

spam_job = None

def spam(is_active):
    global spam_job
    if not spam_job and is_active:
        spam_job = cron.interval("100ms", lambda: actions.user.game_mouse_click_left())
    else:
        cron.cancel(spam_job)
        spam_job = None

def shoot_exit():
    actions.user.game_set_noise_mode(state["last_noise_mode"])

# def exit_pepper():
#     actions.user.game_key_up("alt")
#     actions.user.game_set_noise_mode(state["last_noise_mode"])

tracking_state = False

def toggle_eye_tracking():
    global tracking_state
    if tracking_state:
        actions.user.tracking_control_head_toggle(False)
        actions.user.tracking_control_gaze_toggle(False)
    else:
        if not actions.tracking.control_enabled():
            actions.tracking.control_toggle(True)
        actions.user.tracking_control_head_toggle(True)
        actions.user.tracking_control_gaze_toggle(True)
    tracking_state = not tracking_state

noise_modes = {
    "fighter": {
        "color": "FF0000",
        "pop": ("L click", actions.user.game_mouse_click_left),
        "hiss": ("stop", lambda is_active: is_active and actions.user.game_stop_all())
    },
    "spammer": {
        "color": "00FF00",
        "pop": ("L click", actions.user.game_mouse_click_left),
        "hiss": ("stop", spam)
    },
    "talker": {
        "color": "5555FF",
        "pop": ("E", lambda: actions.user.game_key("e")),
        "hiss": ("repeat", lambda is_active: is_active and actions.user.repeat()),
    },
    "mover": {
        "color": "00FF00",
        "pop": ("jump", lambda: actions.user.game_key("space")),
        "hiss": ("stop", lambda is_active: is_active and actions.user.game_stop_all())
    },
    "dasher": {
        "color": "000066",
        "pop": ("dash", lambda: actions.user.game_key("shift")),
        "hiss": ("stop", lambda is_active: is_active and actions.user.game_stop_all())
    },
    "menu": {
        "color": "990066",
        "pop": ("E", lambda: actions.user.game_key("e")),
        "hiss": ("repeat", lambda is_active: is_active and actions.user.repeat()),
    },
    "jumper": {
        "color": "FF00FF",
        "pop": ("jump", lambda: actions.user.game_key("space")),
        "hiss": ("stop", lambda is_active: is_active and actions.user.game_stop_all())
    },
    "repeater": {
        "color": "00FFFF",
        "pop": ("repeat", actions.user.repeat),
        "hiss": ("stop", lambda is_active: is_active and actions.user.game_stop_all())
    },
    "heavy": {
        "color": "FF0000",
        "pop": ("L click", actions.user.game_mouse_click_left),
        "hiss": ("R click", lambda is_active: is_active and actions.user.game_mouse_click_right())
    },
    "jump_fight": {
        "color": "FF00FF",
        "pop": ("L click", actions.user.game_mouse_click_left),
        "hiss": ("jump", lambda is_active: is_active and actions.user.game_key("space"))
    },
    "hooker": {
        "color": "FF00FF",
        "pop": ("L click", lambda: actions.user.game_key("q")),
        "hiss": ("stop", lambda is_active: is_active and actions.user.game_stop_all())
    },
    "pepper": {
        "color": "FF00FF",
        "on_enter": lambda: actions.user.game_key_down("alt"),
        "on_exit": lambda: actions.user.game_key_up("alt"),
        "pop": ("shoot and exit", lambda: shoot_exit()),
        "hiss": ("stop", lambda is_active: is_active and actions.user.game_stop_all())
    },
    "clicker": {
        "color": "FF00FF",
        "pop":  ("click", lambda: actions.user.game_mouse_click_left()),
        "hiss": ("stop", lambda is_active: is_active and actions.user.game_stop_all())
    },
    "tracker": {
        "color": "FF007D",
        "pop":  ("click", lambda: actions.user.game_mouse_click_left()),
        "hiss": ("toggle eye tracker", lambda is_active: is_active and toggle_eye_tracking())
    },
}

nav_modes = {
    "cam": {
        "default": "90",
        "angles": ["3", "10", "25", "45", "90"],
    },
    "look": {
        "default": "2",
        "speeds": ["1", "2", "3", "4", "0"],
    },
    "turn": {
        "default": "2",
        "durations": ["1", "2", "3", "4", "-1"],
    },
    "go": {
        "default": "-1",
        "durations": ["1", "2", "3", "4", "-1"],
    },
}

state = {
    "nav_mode": "cam",
    "noise_mode": "mover",
    "cam_angle": nav_modes["cam"]["default"],
    "look_speed": nav_modes["look"]["default"],
    "turn_duration": nav_modes["turn"]["default"],
    "go_duration": nav_modes["go"]["default"],
}

def noise_pop(_):
    noise_mode = state["noise_mode"]
    noise_modes[noise_mode]["pop"][1]()

def noise_hiss(is_active):
    noise_mode = state["noise_mode"]
    noise_modes[noise_mode]["hiss"][1](is_active)

move_modes = ["fighter", "mover", "heavy", "talker", "menu", "hooker"]
turn_modes = ["pepper"]
passive_modes = ["talker", "menu"]

@mod.action_class
class Actions:
    def game_on_go():
        """Move forward"""
        if state["noise_mode"] in passive_modes:
            actions.user.game_set_noise_mode("mover")

    def game_left_dynamic():
        """Move left"""
        if state["noise_mode"] in move_modes:
            actions.user.game_move_dir_hold_a()
        elif state["noise_mode"] in turn_modes:
            actions.user.game_turn_left_continuous_5()
        else:
            actions.user.game_turn_left_90()

    def game_right_dynamic():
        """Move right"""
        if state["noise_mode"] in move_modes:
            actions.user.game_move_dir_hold_d()
        elif state["noise_mode"] in turn_modes:
            actions.user.game_turn_right_continuous_5()
        else:
            actions.user.game_turn_right_90()

    def game_up_dynamic():
        """Move up"""
        if state["noise_mode"] in move_modes:
            actions.user.game_move_dir_hold_w()
        else:
            actions.user.game_look_up_continuous_5()

    def game_down_dynamic():
        """Move down"""
        if state["noise_mode"] in move_modes:
            actions.user.game_move_dir_hold_s()
        else:
            actions.user.game_look_down_continuous_5()

    def game_set_noise_mode(mode: str):
        """Set the noise mode"""
        global state
        if mode not in noise_modes:
            print(f"Invalid noise mode: {mode}")
            return
        noise_modes[state["noise_mode"]].get("on_exit", lambda: None)()
        state["last_noise_mode"] = state["noise_mode"]
        state["noise_mode"] = mode
        noise_modes[mode].get("on_enter", lambda: None)()
        noise_mode_text = get_noise_mode_text()
        update_current_noises_ui(mode, noise_mode_text)

def get_noise_mode_text():
    noise_mode = noise_modes[state["noise_mode"]]
    return {
        "color": noise_mode["color"],
        "pop": noise_mode["pop"][0],
        "hiss": noise_mode["hiss"][0],
    }

def get_noise_modes_text():
    return list(noise_modes.keys())

@ctx.action_class("user")
class Actions:
    def on_game_mode_enabled():
        noise.register("pop", noise_pop)
        noise.register("hiss", noise_hiss)
        noise_mode_text = get_noise_mode_text()
        noise_modes_text = get_noise_modes_text()
        show_ui(commands, state, noise_mode_text, noise_modes_text, nav_modes)

    def on_game_mode_disabled():
        noise.unregister("pop", noise_pop)
        noise.unregister("hiss", noise_hiss)
        hide_ui()

    def noise_pop():
        actions.skip()

    def noise_hiss():
        actions.skip()

    def on_pop():
        actions.skip()

    def on_hiss():
        actions.skip()
