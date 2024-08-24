from talon import Module, Context, actions
from .rdr2_ui import show_ui, hide_ui

mod, ctx, ctx_game = Module(), Context(), Context()
# for testing in vscode instead of rdr2
# mod.apps.rdr2 = "os: windows\nand app.exe: /code.exe/i"
mod.apps.rdr2 = "os: windows\nand app.exe: /rdr2.exe/i"
ctx.matches = "os: windows\napp: rdr2"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

def set_noises(mode):
    noises = dynamic_noises[mode]
    for noise, (action_name, action) in noises.items():
        actions.user.dynamic_actions_set(noise, action_name, action)

def wheel_stop(click = False):
    if click:
        actions.user.game_mouse_click()
    actions.user.game_xbox_button_release("lb")
    actions.user.drag_mode_hide()
    set_noises("default")

def stop():
    actions.user.game_stopper()
    actions.user.game_xbox_stopper()

dynamic_noises = {
    "default": {
        "hiss": ("stop", stop),
        "pop": ("A", lambda: actions.user.game_xbox_button_press('a')),
    },
    "mover": {
        "hiss": ("stop", stop),
        "pop": ("A", lambda: actions.user.game_xbox_button_press('a')),
    },
    "wheel": {
        "hiss": ("close", lambda: wheel_stop(click = False)),
        "pop": ("pick and close", lambda: wheel_stop(click = True)),
    },
    "shooter": {
        "hiss": ("stop", stop),
        "pop": ("RT", lambda: actions.user.game_xbox_button_press('rt')),
    },
    "brawler": {
        "hiss": ("toggle B", lambda: actions.user.game_xbox_button_toggle('b')),
        "pop": ("A", lambda: actions.user.game_xbox_button_press('a')),
    },
    "repeater": {
        "hiss": ("stop", stop),
        "pop": ("repeat", actions.core.repeat_phrase),
    }
}

@mod.action_class
class Actions:
    def rdr2_wheel():
        """wheel"""
        actions.user.game_xbox_button_hold("lb")
        actions.user.drag_mode_show()
        set_noises("wheel")

    def rdr2_noise_mode(mode: str):
        """Change noise mode"""
        set_noises(mode)

def stop_all():
    actions.user.game_stopper()
    actions.user.game_xbox_stopper()

def register_dynamic_noises():
    actions.user.dynamic_actions_enable()
    actions.user.dynamic_actions_set_pop(
        action_name = "A",
        action = lambda: actions.user.game_xbox_button_press('a')
    )
    actions.user.dynamic_actions_set_hiss(
        action_name="stop",
        action = stop_all,
        alias = "wish"
    )

def on_mount():
    register_dynamic_noises()

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        print("Game mode enabled")
        actions.user.game_csv_game_words_setup(ctx_game, __file__)
        actions.user.game_xbox_gamepad_enable()
        show_ui(on_mount)

    def on_game_mode_disabled():
        actions.user.game_xbox_gamepad_disable()
        actions.user.dynamic_actions_disable()
        hide_ui()
        print("Game mode disabled")