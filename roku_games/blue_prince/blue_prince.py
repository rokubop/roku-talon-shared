from talon import Module, Context, actions
from .blue_prince_ui import ui

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.blue_prince = "os: windows\nand app.exe: /blue prince.exe/i"
ctx.matches = "os: windows\napp: blue_prince"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

parrot_config = {
    "eh":         ('forward', actions.user.game_wasd_hold_w),
    "guh":        ("back", actions.user.game_wasd_hold_s),
    "ah":         ("left 90", actions.user.game_mouse_move_deg_left_90),
    "oh":         ("right 90", actions.user.game_mouse_move_deg_right_90),
    "ee":         ("stop", actions.user.game_stopper),
    # "shush":      ("look up", actions.user.game_mouse_move_continuous_up_5),
    # "shush_stop": ("", actions.user.game_mouse_move_continuous_stop),
    # "hiss":       ("look down", actions.user.game_mouse_move_continuous_down_5),
    # "hiss_stop":  ("", actions.user.game_mouse_move_continuous_stop),
    # "-":          ("-"),
    "shush":      ("click", actions.user.game_mouse_click_left),
    "mm":         ("e", lambda: actions.user.game_key("e")),
    "t":          ("shift", lambda: actions.user.game_key("shift")),
    "tut":        ("tab", lambda: actions.user.game_key("tab")),
    # "tut":        ("reset y", actions.user.game_mouse_reset_y),
    # "--":         ("--"),
    "tut tut":    ("exit mode", actions.user.game_mode_disable),
}

@ctx_game.action_class("user")
class Actions:
    def parrot_config():
        return parrot_config

    def on_game_mode_enabled():
        actions.user.ui_elements_show(ui, props={"parrot_config": parrot_config})

    def on_game_mode_disabled():
        actions.user.ui_elements_hide_all()
