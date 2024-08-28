from talon import Module, Context, actions
from .rdr2_ui import show_ui, hide_ui

mod, ctx, ctx_game = Module(), Context(), Context()
# for testing in vscode instead of rdr2
# mod.apps.rdr2 = "os: windows\nand app.exe: /code.exe/i"
mod.apps.rdr2 = "os: windows\nand app.exe: /rdr2.exe/i"
ctx.matches = "os: windows\napp: rdr2"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

def stop():
    actions.user.game_stopper()

def wheel_stop(click = False):
    if click:
        actions.user.game_mouse_click()
    actions.user.game_xbox_button_release("lb")
    actions.user.drag_mode_hide()
    actions.user.dynamic_noises_set_mode("default")

def wheel():
    actions.user.game_xbox_button_hold("lb")
    actions.user.drag_mode_show()

@mod.action_class
class Actions:
    def rdr2_set_noise_mode(mode: str):
        """Set noise mode"""
        if mode == "wheel":
            wheel()
        actions.user.dynamic_noises_set_mode(mode)

noise_modes = {
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

@ctx_game.action_class("user")
class Actions:
    def dynamic_noise_modes():
        return noise_modes

    def on_game_mode_enabled():
        actions.user.game_csv_game_words_setup(ctx_game, __file__)
        actions.user.game_xbox_gamepad_enable()
        actions.user.dynamic_noises_enable()
        show_ui()

    def on_game_mode_disabled():
        actions.user.game_xbox_gamepad_disable()
        actions.user.dynamic_noises_disable()
        hide_ui()