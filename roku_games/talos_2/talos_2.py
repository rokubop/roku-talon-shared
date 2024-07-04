from talon import Module, Context, actions
from .talos_2_ui import show_ui, hide_ui

mod = Module()
ctx = Context()

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.talos_2 = "os: windows\nand app.exe: Talos2-Win64-Shipping.exe"
ctx.matches = "os: windows\napp: talos_2"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

default_config = {
    "eh":         ("forward", actions.user.game_move_dir_hold_w),
    "guh":        ("back", actions.user.game_move_dir_hold_s),
    "ah":         ("left", actions.user.game_move_dir_hold_a),
    "oh":         ("right", actions.user.game_move_dir_hold_d),
    "ee":         ("stop", actions.user.game_stopper),
    "nn":         ("L click", actions.user.game_mouse_click_left),
    "cluck":      ("R click", actions.user.game_mouse_click_right),
    "pop":        ("look down", actions.user.game_look_down_15),
    "palate":     ("look up", actions.user.game_look_up_15),
    "t":          ("shift", lambda: actions.user.game_key("shift")),
    "hiss":       ("turn left", actions.user.game_turn_left_continuous),
    "hiss_stop":  ("", actions.user.game_turn_continuous_stop),
    "shush":      ("turn right", actions.user.game_turn_right_continuous),
    "shush_stop": ("", actions.user.game_turn_continuous_stop),
    "tut":        ("reset y", actions.user.game_reset_center_y),
    "tut ah":     ("left 90", actions.user.game_turn_left_90),
    "tut oh":     ("right 90", actions.user.game_turn_right_90),
    "tut guh":    ("180", actions.user.game_turn_180),
    "er":         ("exit mode", actions.user.game_mode_disable),
}

# parrot(ee):                 user.game_v2_stop_layer_by_layer()
# parrot(ah):                 user.event_mouse_nav("left")
# parrot(oh):                 user.event_mouse_nav("right")
# parrot(hiss):               user.event_mouse_nav("down")
# parrot(hiss:stop):          skip()
# parrot(shush):              user.event_mouse_nav("up")
# parrot(shush:stop):         skip()
# parrot(er):                 user.game_v2_nav_mode_disable()

parrot_config = default_config

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        show_ui(parrot_config)

    def on_game_mode_disabled():
        hide_ui()

    def parrot_config():
        return parrot_config