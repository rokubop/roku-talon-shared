from talon import Module, Context, actions
from .sheepy_ui import show_ui, hide_ui

mod, ctx, ctx_game = Module(), Context(), Context()

mod.apps.sheepy = "os: windows\nand app.exe: /SheepyAShortAdventure.exe/i"
ctx.matches = "os: windows\napp: sheepy"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

def xbox_x():
    # if we want extra speed boosts while running, we need
    # a binding to the real gamepad x button
    #
    # Option 1: don't worry about the extra speed boost.
    # It's not necessary to complete the game, just use "shift".
    # actions.user.game_key("shift")
    #
    # Option 2: use an external tool like Playability or vjoy to
    # bind an arbitrary key like f7 to the real X button, then map
    # this action to that key.
    # f7 is mapped to actual X button in playability app
    # actions.key("f7")
    #
    # Option 3: use xbox gamepad emulation
    actions.user.game_xbox_button("x")
    actions.user.ui_elements_highlight_briefly("shift")

parrot_config = {
    "eh":         ('W', actions.user.game_move_dir_hold_up),
    "ah":         ("A", actions.user.game_move_dir_hold_left),
    "guh":        ("S", actions.user.game_move_dir_hold_down),
    "oh":         ("D", actions.user.game_move_dir_hold_right),
    "ee":         ("stop", actions.user.game_stopper),
    "pop":        ("E", lambda: actions.user.game_key("e")),
    "tut":        ("hold E", lambda: actions.user.game_key_hold("e")),
    "mm":         ("space", lambda: actions.user.game_key("space")),
    "shush:th_50":("ctrl", lambda: actions.user.game_key("ctrl")),
    "hiss:th_50": ("shift", xbox_x),
    "er":         ("exit mode", actions.user.game_mode_disable),
    "cluck":      ("stop timer", lambda: actions.key("keypad_1")),
}

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        actions.user.game_xbox_gamepad_enable()
        show_ui(parrot_config)

    def on_game_mode_disabled():
        actions.user.game_xbox_gamepad_disable()
        hide_ui()

    def parrot_config():
        return parrot_config