from talon import Module, Context, actions
from .stray_ui import show_ui, hide_ui

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.stray = "os: windows\nand app.exe: /Stray-Win64-Shipping.exe/i"
ctx.matches = "os: windows\napp: stray"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

parrot_config = {
    "eh":         ('forward', actions.user.game_move_dir_hold_w),
    "guh":        ("back", actions.user.game_move_dir_hold_s),
    "ah":         ("left", actions.user.game_move_dir_hold_a),
    "oh":         ("right", actions.user.game_move_dir_hold_d),
    "ee":         ("stop", actions.user.game_stopper),
    "shush":      ("look up", actions.user.game_look_up_continuous_5),
    "shush_stop": ("", actions.user.game_look_continuous_stop),
    "hiss":       ("look down", actions.user.game_look_down_continuous_5),
    "hiss_stop":  ("", actions.user.game_look_continuous_stop),
    "-":          ("-"),
    "cluck":      ("L click", actions.user.game_mouse_click_left),
    "cluck cluck":("R click", actions.user.game_mouse_click_right),
    "pop":        ("space", lambda: actions.user.game_key("space")),
    "palate":     ("q", lambda: actions.user.game_key("q")),
    "mm":         ("e", lambda: actions.user.game_key("e")),
    "t":          ("shift", lambda: actions.user.game_key("shift")),
    "er":         ("tab", lambda: actions.user.game_key("tab")),
    "tut":        ("alt", lambda: actions.user.game_key("alt")),
    "--":         ("--"),
    "tut er":     ("exit mode", actions.user.game_mode_disable),
    "tut ah":     ("turn left", actions.user.game_turn_left_90),
    "tut oh":     ("turn right", actions.user.game_turn_right_90),
    "tut guh":    ("turn around", actions.user.game_turn_180),
    "tut palate": ("hold space", lambda: actions.user.game_key_hold("space")),
}

@ctx_game.action_class("user")
class Actions:
    def parrot_config():
        return parrot_config

    def on_game_mode_enabled():
        show_ui(parrot_config)

    def on_game_mode_disabled():
        hide_ui()
