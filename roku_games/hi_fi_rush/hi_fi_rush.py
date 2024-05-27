from talon import Module, Context, actions
from .hi_fi_rush_ui import show_commands, hide_commands

mod = Module()
ctx = Context()

mod.apps.hi_fi_rush = r"""
os: windows
and app.exe: Hi-Fi-RUSH.exe
"""

ctx.matches = r"""
os: windows
app: hi_fi_rush
"""

ctx_game = Context()
ctx_game.matches = r"""
os: windows
app: hi_fi_rush
mode: user.game
"""

key = actions.key
spam = False

def toggle_spam():
    global spam
    spam = not spam

def peppermint_mode():
    global parrot_config
    key("alt:down"),
    parrot_config = peppermint_config
    show_commands(parrot_config, background_color="45f24888")

def rpg_mode():
    global parrot_config
    parrot_config = nav_config
    show_commands(parrot_config, background_color="FCD12A88")

default_config = {
    "eh":         ('forward', actions.user.game_move_dir_hold_w),
    "guh":        ("back", actions.user.game_move_dir_hold_s),
    "ah":         ("left", actions.user.game_move_dir_hold_a),
    "oh":         ("right", actions.user.game_move_dir_hold_d),
    "ee":         ("stop", actions.user.game_stopper),
    "pop":        ("L click", actions.user.game_mouse_click_left),
    "cluck":      ("R click", actions.user.game_mouse_click_right),
    "nn":         ("E", lambda: actions.key("e")),
    "palate":     ("Q", lambda: key("q")),
    "t":          ("shift", lambda: key("shift")),
    "hiss":       ("R", lambda: key("r") if not spam else key("space")),
    "shush:th_100": ("space", lambda: key("space")),
    "er":         ("exit mode", actions.user.game_mode_disable),
    "tut":        ("alt", lambda: key("alt")),
    "tut er":     ("look mode", rpg_mode),
    "tut ah":     ("turn left", actions.user.game_turn_left_90),
    "tut oh":     ("turn right", actions.user.game_turn_right_90),
    "tut guh":    ("turn around", actions.user.game_turn_180),
    "tut ee":     ("switch char", lambda: key("f")),
    "tut hiss":   ("toggle spam", toggle_spam),
    "tut pop":    ("L click hold", actions.user.game_mouse_hold_left),
    "tut cluck":  ("R click hold", actions.user.game_mouse_hold_right),
    "tut shush":  ("space hold", lambda: key("space:down")),
    "tut nn":     ("E hold", lambda: key("e:down")),
    "tut palate": ("Q hold", lambda: key("q:down")),
    "tut tut":    ("reset y", actions.user.game_reset_center_y),
    "tut tut tut":("alt hold", peppermint_mode),
}

parrot_config = default_config

def rpg_mouse_mode_disable():
    global parrot_config
    actions.user.rpg_mouse_stop()
    parrot_config = default_config

def rpg_mouse_click_stop():
    actions.user.rpg_mouse_stop()
    actions.user.mouse_click()

def rpg_mouse_click_exit():
    global parrot_config
    actions.user.rpg_mouse_stop()
    actions.user.mouse_click()
    parrot_config = default_config
    show_commands(parrot_config)

nav_config = {
    "cluck":  ("exit", rpg_mouse_mode_disable),
    "nn":     ("click", rpg_mouse_click_stop),
    "pop":    ("click exit", rpg_mouse_click_exit),
    "ah":     ("left", actions.user.rpg_mouse_move_left),
    "oh":     ("right", actions.user.rpg_mouse_move_right),
    "hiss":   ("down", actions.user.rpg_mouse_move_down),
    "shush":  ("up", actions.user.rpg_mouse_move_up),
    "palate": ("repeat", actions.user.rpg_mouse_repeat_dir_by_increment),
    "tut":    ("reverse", actions.user.rpg_mouse_repeat_reverse_dir_by_increment),
    "ee":     ("stop", actions.user.rpg_mouse_stop),
    "t":      ("slow", actions.user.rpg_mouse_move_slow),
    "guh":    ("fast", actions.user.rpg_mouse_move_fast),
    "er":     ("exit mode", rpg_mouse_mode_disable),
}

def shoot_and_exit():
    key("alt")
    rpg_mouse_mode_disable()

peppermint_config = {
    "cluck":  ("exit", shoot_and_exit),
    "nn":     ("click", shoot_and_exit),
    "pop":    ("click exit", shoot_and_exit),
    "ah":     ("left", actions.user.rpg_mouse_move_left),
    "oh":     ("right", actions.user.rpg_mouse_move_right),
    "hiss":   ("down", actions.user.rpg_mouse_move_down),
    "shush":  ("up", actions.user.rpg_mouse_move_up),
    "palate": ("repeat", actions.user.rpg_mouse_repeat_dir_by_increment),
    "tut":    ("reverse", actions.user.rpg_mouse_repeat_reverse_dir_by_increment),
    "ee":     ("stop", actions.user.rpg_mouse_stop),
    "t":      ("slow", actions.user.rpg_mouse_move_slow),
    "guh":    ("fast", actions.user.rpg_mouse_move_fast),
    "er":     ("exit mode", shoot_and_exit),
}

@ctx.action_class("user")
class Actions:
    def game_mode_enable():
        show_commands(parrot_config)
        actions.next()

@ctx_game.action_class("user")
class Actions:
    def game_mode_disable():
        hide_commands()
        actions.next()

    def parrot_config():
        return parrot_config