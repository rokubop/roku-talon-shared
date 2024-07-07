from talon import Module, Context, actions
from .talos_2_ui import show_ui, hide_ui, refresh_ui

mod = Module()
ctx = Context()

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.talos_2 = "os: windows\nand app.exe: Talos2-Win64-Shipping.exe"
ctx.matches = "os: windows\napp: talos_2"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

def enter_look_mode():
    global parrot_config
    parrot_config = look_config
    refresh_ui(parrot_config)

def exit_look_mode():
    global parrot_config
    parrot_config = default_config
    refresh_ui(parrot_config)

default_config = {
    "eh":         ("forward", actions.user.game_move_dir_hold_w),
    "guh":        ("back", actions.user.game_move_dir_hold_s),
    "ah":         ("left", actions.user.game_move_dir_hold_a_curved),
    "oh":         ("right", actions.user.game_move_dir_hold_d_curved),
    "ee":         ("stop", actions.user.game_stopper),
    "hiss":       ("turn left", actions.user.game_turn_left_continuous_10),
    "hiss_stop":  ("", actions.user.game_turn_continuous_stop),
    "shush":      ("turn right", actions.user.game_turn_right_continuous_10),
    "shush_stop": ("", actions.user.game_turn_continuous_stop),
    "-":          ("-"),
    "nn":         ("E", lambda: actions.user.game_key("e")),
    "palate":     ("space", lambda: actions.user.game_key("space")),
    "pop":        ("L click", actions.user.game_mouse_click_left),
    "cluck":      ("R click", actions.user.game_mouse_click_right),
    "t":          ("shift", lambda: actions.user.game_key("shift")),
    "-":          ("-"),
    "tut":        ("reset y", actions.user.game_reset_center_y),
    "tut tut":    ("look mode", enter_look_mode),
    "tut hiss":   ("look down", lambda: (
        actions.user.game_look_down_15(),
        enter_look_mode()
    )),
    "tut shush":  ("look up", lambda: (
        actions.user.game_look_up_15(),
        enter_look_mode()
    )),
    "tut ah":     ("left 90", actions.user.game_turn_left_90),
    "tut oh":     ("right 90", actions.user.game_turn_right_90),
    "tut guh":    ("180", actions.user.game_turn_180),
    "er":         ("exit mode", actions.user.game_mode_disable),
}

look_config = {
    **default_config,
    "ah":         ("look left", actions.user.game_turn_left_continuous_5),
    "oh":         ("look right", actions.user.game_turn_right_continuous_5),
    "hiss":       ("look down", actions.user.game_look_down_continuous_10),
    "hiss_stop":  ("", actions.user.game_turn_continuous_stop),
    "shush":      ("look up", actions.user.game_look_up_continuous_10),
    "shush_stop": ("", actions.user.game_turn_continuous_stop),
    "er":         ("exit look", exit_look_mode)
}

parrot_config = default_config

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        show_ui(parrot_config)

    def on_game_mode_disabled():
        hide_ui()

    def parrot_config():
        return parrot_config