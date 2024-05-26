from talon import Module, Context, actions

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

user = actions.user
key = actions.key
spam = False

@ctx.action_class("user")
class Actions:
    def on_parrot_v5_mode_enable(ev: dict):
        # actions.user.parrot_config_show_commands()
        actions.next(ev)

    def on_parrot_v5_mode_disable(ev: dict):
        # actions.user.parrot_config_hide_commands()
        actions.user.event_mouse_move_stop_hard()
        actions.user.game_v2_stop_all()
        actions.user.game_v2_canvas_hide()
        actions.next(ev)

##################################################
# GAME MODE
##################################################

mod.mode("hi_fi_rush_parrot", "Parrot mode for hi_fi_rush game")
ctx_parrot = Context()
ctx_parrot.matches = r"""
app: hi_fi_rush
mode: user.parrot_v5
and mode: user.hi_fi_rush_parrot
"""
ctx_parrot.settings = {
    "user.game_v2_calibrate_x_360" : 3090,
    "user.game_v2_calibrate_y_ground_to_center" : 542
}


def toggle_spam():
    global spam
    spam = not spam
    # show_default_game_commands()

def peppermint_mode():
    key("alt:down"),
    user.parrot_v5_mode_enable("user.hi_fi_rush_peppermint")

def rpg_mode():
    user.parrot_v5_mode_enable("user.rpg_mouse")

# def throttled_jump():
#     user.parrot_throttle(100, "jump", lambda: key("space"))

parrot_commands = {
    "eh":         ('forward', user.game_v2_move_dir_w),
    "guh":        ("back", user.game_v2_move_dir_s),
    "ah":         ("left", user.game_v2_move_dir_a),
    "oh":         ("right", user.game_v2_move_dir_d),
    "ee":         ("stop", user.game_v2_stop_layer_by_layer),
    "pop":        ("L click", lambda: user.event_mouse_click(0)),
    "cluck":      ("R click", lambda: user.event_mouse_click(1)),
    "nn":         ("E", lambda: key("e")),
    "palate":     ("Q", lambda: key("q")),
    "t":          ("shift", lambda: key("shift")),
    "hiss":       ("R", lambda: key("r") if not spam else key("space")),
    "shush:th_100": ("space", lambda: key("space")),
    "er":         ("exit mode", user.parrot_v5_mode_disable),
    "tut":        ("alt", lambda: key("alt")),
    "tut er":     ("look mode", rpg_mode),
    "tut ah":     ("turn left", lambda: user.game_v2_turn_left(90, 200)),
    "tut oh":     ("turn right", lambda: user.game_v2_turn_right(90, 200)),
    "tut guh":    ("turn around", user.game_v2_snap_180),
    "tut ee":     ("switch char", lambda: key("f")),
    "tut hiss":   ("toggle spam", toggle_spam),
    "tut pop":    ("L click hold", lambda: user.event_mouse_drag(0)),
    "tut cluck":  ("R click hold", lambda: user.event_mouse_drag(1)),
    "tut shush":  ("space hold", lambda: key("space:down")),
    "tut nn":     ("E hold", lambda: key("e:down")),
    "tut palate": ("Q hold", lambda: key("q:down")),
    "tut tut":    ("reset y", user.game_v2_reset_center_y),
    "tut tut tut":("alt hold", peppermint_mode),
}

game_config = {
    "mode": "game",
    "color": "222666",
    "commands" : parrot_commands
}

@ctx_parrot.action_class("user")
class Actions:
    def parrot_config():
        return game_config

##################################################
# MENU MODE
##################################################

def no_op():
    pass

ctx_menu = Context()
ctx_menu.matches = r"""
app: hi_fi_rush
mode: user.parrot_v5
and mode: user.parrot_v5_default
"""

menu_commands = {
    "nn": ("click", no_op),
    "pop": ("click + exit", no_op),
    "hiss": ("scroll down", no_op),
    "shush": ("scroll up", no_op),
    "ah": ("hold left", no_op),
    "oh": ("right click", no_op),
    "eh": ("teleport", no_op),
    "er": ("look mode", no_op),
    "cluck": ("exit", no_op),
    "guh": ("ctrl", no_op),
    "t": ("shift", no_op),
    "tut": ("alt", no_op),
    "palate": ("repeat", no_op),
    "ee": ("stop", no_op),
}

menu_config = {
    "mode": "menu",
    "color": "ff0000",
    "commands" : menu_commands
}

@ctx_menu.action_class("user")
class Actions:
    def parrot_config():
        return menu_config

##################################################
# NAVIGATION MODE
##################################################

ctx_nav = Context()
ctx_nav.matches = r"""
app: hi_fi_rush
mode: user.parrot_v5
and mode: user.rpg_mouse
"""

def rpg_mouse_mode_disable():
    user.rpg_mouse_stop()
    user.clear_screen_regions()
    user.parrot_v5_mode_enable("user.hi_fi_rush_parrot")

def rpg_mouse_click_stop():
    user.rpg_mouse_stop()
    user.mouse_click()

def rpg_mouse_click_exit():
    user.rpg_mouse_stop()
    user.mouse_click()
    user.clear_screen_regions()
    user.parrot_v5_mode_enable("user.hi_fi_rush_parrot")

nav_commands = {
    "cluck":  ("exit", rpg_mouse_mode_disable),
    "nn":     ("click", rpg_mouse_click_stop),
    "pop":    ("click exit", rpg_mouse_click_exit),
    "ah":     ("left", user.rpg_mouse_move_left),
    "oh":     ("right", user.rpg_mouse_move_right),
    "hiss":   ("down", user.rpg_mouse_move_down),
    "shush":  ("up", user.rpg_mouse_move_up),
    "palate": ("repeat", user.rpg_mouse_repeat_dir_by_increment),
    "tut":    ("reverse", user.rpg_mouse_repeat_reverse_dir_by_increment),
    "ee":     ("stop", user.rpg_mouse_stop),
    "t":      ("slow", user.rpg_mouse_move_slow),
    "guh":    ("fast", user.rpg_mouse_move_fast),
    "er":     ("exit mode", rpg_mouse_mode_disable),
}

nav_config = {
    "mode": "nav",
    "color": "FCD12A",
    "commands" : nav_commands
}

@ctx_nav.action_class("user")
class Actions:
    def parrot_config():
        return nav_config

##################################################
# PEPPERMINT MODE
##################################################

mod.mode("hi_fi_rush_peppermint", "Peppermint mode for hi_fi_rush game")
ctx_peppermint = Context()
ctx_peppermint.matches = r"""
app: hi_fi_rush
mode: user.parrot_v5
and mode: user.hi_fi_rush_peppermint
"""

def shoot_and_exit():
    key("alt")
    rpg_mouse_mode_disable()

peppermint_commands = {
    "cluck":  ("exit", shoot_and_exit),
    "nn":     ("click", shoot_and_exit),
    "pop":    ("click exit", shoot_and_exit),
    "ah":     ("left", user.rpg_mouse_move_left),
    "oh":     ("right", user.rpg_mouse_move_right),
    "hiss":   ("down", user.rpg_mouse_move_down),
    "shush":  ("up", user.rpg_mouse_move_up),
    "palate": ("repeat", user.rpg_mouse_repeat_dir_by_increment),
    "tut":    ("reverse", user.rpg_mouse_repeat_reverse_dir_by_increment),
    "ee":     ("stop", user.rpg_mouse_stop),
    "t":      ("slow", user.rpg_mouse_move_slow),
    "guh":    ("fast", user.rpg_mouse_move_fast),
    "er":     ("exit mode", shoot_and_exit),
}

peppermint_config = {
    "mode": "peppermint",
    "color": "45f248",
    "commands" : peppermint_commands
}

@ctx_peppermint.action_class("user")
class Actions:
    def parrot_config():
        return peppermint_config