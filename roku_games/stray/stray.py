from talon import Module, Context, actions
from .stray_ui import ui

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.stray = "os: windows\nand app.exe: /Stray-Win64-Shipping.exe/i"
ctx.matches = "os: windows\napp: stray"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

parrot_config = {
    "eh":         ('forward', actions.user.game_wasd_hold_w),
    "guh":        ("back", actions.user.game_wasd_hold_s),
    "ah":         ("left", actions.user.game_wasd_hold_a),
    "oh":         ("right", actions.user.game_wasd_hold_d),
    "ee":         ("stop", actions.user.game_stopper),
    "shush":      ("look up", actions.user.game_mouse_move_continuous_up_5),
    "shush_stop": ("", actions.user.game_mouse_move_continuous_stop),
    "hiss":       ("look down", actions.user.game_mouse_move_continuous_down_5),
    "hiss_stop":  ("", actions.user.game_mouse_move_continuous_stop),
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
    "tut ah":     ("turn left", actions.user.game_mouse_move_deg_left_90),
    "tut oh":     ("turn right", actions.user.game_mouse_move_deg_right_90),
    "tut guh":    ("turn around", actions.user.game_mouse_move_deg_180),
    "tut palate": ("hold space", lambda: actions.user.game_key_hold("space")),
}

@ctx_game.action_class("user")
class Actions:
    def parrot_config():
        return parrot_config

    def on_game_mode_enabled():
        actions.user.ui_elements_show(ui, props={"parrot_config": parrot_config})

    def on_game_mode_disabled():
        actions.user.ui_elements_hide_all()
