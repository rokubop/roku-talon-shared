from talon import Module, Context, actions
from .sheepy_ui import show_ui, hide_ui

mod, ctx, ctx_game = Module(), Context(), Context()

mod.apps.sheepy = "os: windows\nand app.exe: /SheepyAShortAdventure.exe/i"
ctx.matches = "os: windows\napp: sheepy"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

def shift_key():
    # f7 is mapped to actual X button in playability app
    # alternatively, just do actions.key("shift"), but you
    # won't get the extra speed boost
    actions.key("f7")
    actions.user.ui_elements_highlight_briefly("shift")

parrot_config = {
    "eh":         ('W', actions.user.game_arrows_hold_up),
    "ah":         ("A", actions.user.game_arrows_hold_left),
    "guh":        ("S", actions.user.game_arrows_hold_down),
    "oh":         ("D", actions.user.game_arrows_hold_right),
    "ee":         ("stop", actions.user.game_stopper),
    "pop":        ("E", lambda: actions.user.game_key("e")),
    "tut":        ("hold E", lambda: actions.user.game_key_hold("e")),
    "mm":         ("space", lambda: actions.user.game_key("space")),
    "shush:th_50":("ctrl", lambda: actions.user.game_key("ctrl")),
    "hiss:th_50": ("shift", shift_key),
    "er":         ("exit mode", actions.user.game_mode_disable),
    "cluck":      ("stop timer", lambda: actions.key("keypad_1")),
}

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        show_ui(parrot_config)

    def on_game_mode_disabled():
        hide_ui()

    def parrot_config():
        return parrot_config