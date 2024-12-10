from talon import Module, Context, actions
from .hi_fi_rush_ui import ui

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.hi_fi_rush = "os: windows\nand app.exe: /Hi-Fi-RUSH.exe/i"
ctx.matches = "os: windows\napp: hi_fi_rush"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

key = actions.key
spam = False

def toggle_spam():
    global spam
    spam = not spam

def peppermint_mode():
    global parrot_config
    key("alt:down"),
    parrot_config = peppermint_config
    actions.user.ui_elements_set_state({
        "parrot_config": peppermint_config,
        "background_color": "00800088",
    })

def rpg_mode():
    global parrot_config
    parrot_config = nav_config
    actions.user.ui_elements_set_state({
        "parrot_config": nav_config,
        "background_color": "FCD12A88",
    })

default_config = {
    "eh":         ('forward', actions.user.game_wasd_hold_w),
    "guh":        ("back", actions.user.game_wasd_hold_s),
    "ah":         ("left", actions.user.game_wasd_hold_a),
    "oh":         ("right", actions.user.game_wasd_hold_d),
    "ee":         ("stop", actions.user.game_stopper),
    "pop":        ("L click", actions.user.game_mouse_click_left),
    "cluck":      ("R click", actions.user.game_mouse_click_right),
    "nn":         ("E", lambda: actions.key("e")),
    "palate":     ("Q", lambda: key("q")),
    "t":          ("shift", lambda: key("shift")),
    "hiss":       ("R", lambda: key("r") if not spam else key("space")),
    "shush:th_100":("space", lambda: key("space")),
    "er":         ("exit mode", actions.user.game_mode_disable),
    "tut":        ("alt", lambda: key("alt")),
    "tut er":     ("look mode", rpg_mode),
    "tut ah":     ("turn left", actions.user.game_mouse_move_deg_left_90),
    "tut oh":     ("turn right", actions.user.game_mouse_move_deg_right_90),
    "tut guh":    ("turn around", actions.user.game_mouse_move_deg_180),
    "tut ee":     ("switch char", lambda: key("f")),
    "tut hiss":   ("toggle spam", toggle_spam),
    "tut pop":    ("L click hold", actions.user.game_mouse_hold_left),
    "tut cluck":  ("R click hold", actions.user.game_mouse_hold_right),
    "tut shush":  ("space hold", lambda: key("space:down")),
    "tut nn":     ("E hold", lambda: key("e:down")),
    "tut palate": ("Q hold", lambda: key("q:down")),
    "tut tut":    ("reset y", actions.user.game_mouse_move_reset_center_y),
    "tut tut tut":("alt hold", peppermint_mode),
}

parrot_config = default_config

def rpg_mouse_mode_disable():
    global parrot_config
    actions.user.mouse_move_continuous_stop()
    parrot_config = default_config
    actions.user.ui_elements_set_state({
        "parrot_config": default_config,
        "background_color": "22266688",
    })

def rpg_mouse_click_stop():
    actions.user.mouse_move_continuous_stop()
    actions.user.game_mouse_click()

def rpg_mouse_click_exit():
    global parrot_config
    actions.user.mouse_move_continuous_stop()
    actions.user.game_mouse_click()
    parrot_config = default_config
    actions.user.ui_elements_set_state({
        "parrot_config", default_config,
        "background_color", "22266688"
    })

nav_config = {
    "cluck":  ("exit", rpg_mouse_mode_disable),
    "nn":     ("click", rpg_mouse_click_stop),
    "pop":    ("click exit", rpg_mouse_click_exit),
    "ah":     ("left", actions.user.mouse_move_continuous_left),
    "oh":     ("right", actions.user.mouse_move_continuous_right),
    "hiss":   ("down", actions.user.mouse_move_continuous_down),
    "shush":  ("up", actions.user.mouse_move_continuous_up),
    "palate": ("repeat", actions.user.mouse_move_tick_last_direction),
    "tut":    ("reverse", actions.user.mouse_move_tick_reverse_last_direction),
    "ee":     ("stop", actions.user.mouse_move_continuous_stop),
    "t":      ("slow", actions.user.mouse_move_continuous_speed_decrease),
    "guh":    ("fast", actions.user.mouse_move_continuous_speed_increase),
    "er":     ("exit mode", rpg_mouse_mode_disable),
}

def shoot_and_exit():
    key("alt")
    rpg_mouse_mode_disable()

peppermint_config = {
    **nav_config,
    "cluck":  ("exit", shoot_and_exit),
    "nn":     ("click", shoot_and_exit),
    "pop":    ("click exit", shoot_and_exit),
    "er":     ("exit mode", shoot_and_exit),
}

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        actions.user.ui_elements_show(ui, initial_state={
            "parrot_config": parrot_config,
            "background_color": "22266688",
        })

    def on_game_mode_disabled():
        actions.user.ui_elements_hide_all()

    def parrot_config():
        return parrot_config