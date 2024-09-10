from talon import Module, Context, actions
from .rdr2_ui import show_ui, hide_ui

mod, ctx, ctx_game = Module(), Context(), Context()
# for testing in vscode instead of rdr2
# mod.apps.rdr2 = "os: windows\nand app.exe: /code.exe/i"
mod.apps.ryujinx = "os: windows\nand app.exe: /ryujinx.exe/i"
ctx.matches = "os: windows\napp: ryujinx"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

def wheel_stop(click = False):
    if click:
        actions.user.game_mouse_click()
    actions.user.game_xbox_button_release("lb")
    actions.user.drag_mode_hide()
    actions.user.dynamic_noises_use_mode("default")

def wheel():
    actions.user.game_xbox_button_hold("lb")
    actions.user.drag_mode_show()

default = {
    "pop": ("A", lambda: actions.user.game_xbox_button_press('a')),
    "hiss": ("stop", actions.user.game_stopper),
}

dynamic_noises = {
    "default": default,
    "mover": default,
    "wheel": {
        "on_enable": wheel,
        "hiss": ("close", lambda: wheel_stop(click = False)),
        "pop": ("pick and close", lambda: wheel_stop(click = True)),
    },
    "shooter": {
        **default,
        "pop": ("RT", lambda: actions.user.game_xbox_button_press('rt')),
    },
    "brawler": {
        "pop": ("B", lambda: actions.user.game_xbox_button_press('b')),
        "hiss": ("toggle x", lambda: actions.user.game_xbox_button_toggle('x')),
    },
    "repeater": {
        **default,
        "pop": ("repeat", actions.core.repeat_phrase),
    }
}

@ctx_game.action_class("user")
class Actions:
    def dynamic_noises():
        return dynamic_noises

    def on_game_mode_enabled():
        actions.user.game_csv_game_words_setup(ctx_game, __file__)
        actions.user.game_xbox_gamepad_enable()
        actions.user.dynamic_noises_enable()
        show_ui()

    def on_game_mode_disabled():
        actions.user.game_xbox_gamepad_disable()
        actions.user.dynamic_noises_disable()
        hide_ui()