from talon import Module, Context, actions
from .hades_ui import show_ui, hide_ui

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.hades = "os: windows\nand app.exe: Hades.exe"
ctx.matches = "os: windows\napp: hades"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

parrot_config = {
    "eh":         ('forward', actions.user.game_move_dir_hold_w),
    "guh":        ("back", actions.user.game_move_dir_hold_s),
    "ah":         ("left", actions.user.game_move_dir_hold_a),
    "oh":         ("right", actions.user.game_move_dir_hold_d),
    "ee":         ("stop", actions.user.game_stopper),
    "t":          ("f-up", actions.user.game_move_dir_hold_up_horizontal),
    "mm":         ("f-down", actions.user.game_move_dir_hold_down_horizontal),
    "shush:th_100":("l click", actions.user.game_mouse_click_left),
    "shush_stop": ("", lambda: None),
    "hiss:th_100":("r click", actions.user.game_mouse_click_right),
    "hiss_stop":  ("", lambda: None),
    "pop":        ("e", lambda: actions.user.game_key("e")),
    "cluck":      ("q", lambda: actions.user.game_key("q")),
    "palate":     ("dash", lambda: actions.user.game_key("space")),
    "er":         ("f", lambda: actions.user.game_key("f")),
    "tut ah":     ("g", lambda: actions.user.game_key("g")),
    "tut oh":     ("c", lambda: actions.user.game_key("c")),
    "tut ee":     ("b", lambda: actions.user.game_key("b")),
    "tut tut":    ("exit mode", actions.user.game_mode_disable),
}

@ctx_game.action_class("user")
class Actions:
    def parrot_config():
        return parrot_config

    def on_game_mode_enabled():
        show_ui(parrot_config)

    def on_game_mode_disabled():
        hide_ui()
