from talon import Module, Context, actions, ctrl, cron
from .animal_well_ui import show_ui, hide_ui, highlight, highlight_briefly, unhighlight


mod = Module()
ctx = Context()

mod.apps.animal_well = r"""
os: windows
and app.exe: Animal Well.exe
"""

ctx.matches = r"""
os: windows
app: animal_well
"""

ctx_game = Context()
ctx_game.matches = r"""
os: windows
app: animal_well
mode: user.game
"""

def up():
    actions.user.game_move_dir_hold_up()
    highlight("W")
    unhighlight("S")
    unhighlight("A")
    unhighlight("D")

def down():
    actions.user.game_move_dir_hold_down()
    highlight("S")
    unhighlight("W")
    unhighlight("A")
    unhighlight("D")

def left():
    actions.user.game_move_dir_hold_left()
    highlight("A")
    unhighlight("W")
    unhighlight("S")
    unhighlight("D")

def right():
    actions.user.game_move_dir_hold_right()
    highlight("D")
    unhighlight("W")
    unhighlight("S")
    unhighlight("A")

def stop():
    actions.user.game_stopper()
    unhighlight("W")
    unhighlight("S")
    unhighlight("A")
    unhighlight("D")

def space_key():
    actions.key("space")
    highlight_briefly("SP")

parrot_config = {
    "eh":         ('W', up),
    "ah":         ("A", left),
    "guh":        ("S", down),
    "oh":         ("D", right),
    "ee":         ("stop", stop),
    "cluck":      ("item", lambda: actions.key("c")),
    "t":          ("map", lambda: actions.key("v")),
    "nn":         ("space", space_key),
    "palate":     ("X", lambda: actions.key("x")),
    "shush": ("X", lambda: actions.key("x:down")),
    "shush_stop:db_100": ("", lambda: actions.key("x:up")),
    "er":         ("exit mode", actions.user.game_mode_disable),
    "tut": ("Z", lambda: actions.key("z")),
}

@ctx.action_class("user")
class Actions:
    def game_mode_enable():
        show_ui(parrot_config)
        actions.next()

@ctx_game.action_class("user")
class Actions:
    def game_mode_disable():
        hide_ui()
        actions.next()

    def parrot_config():
        return parrot_config