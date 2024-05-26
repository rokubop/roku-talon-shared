from talon import Module, Context, actions
from talon import Module, actions
from .sheepy_ui import show_ui, hide_ui, highlight, highlight_briefly, unhighlight

mod = Module()
ctx = Context()

mod.apps.sheepy = r"""
os: windows
and app.exe: SheepyAShortAdventure.exe
"""

ctx.matches = r"""
os: windows
app: sheepy
"""

ctx_game = Context()
ctx_game.matches = r"""
os: windows
app: sheepy
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

def E():
    actions.key("e")
    highlight_briefly("E")

def hold_E():
    actions.key("e:down")
    highlight("E")

def space_key():
    actions.key("space")
    highlight_briefly("SP")

def ctrl_key():
    actions.key("ctrl")
    highlight_briefly("CT")

def shift_key():
    # f7 is mapped to actual X button in playability app
    # in order to get the speed boost
    actions.key("f7")
    highlight_briefly("SH")

parrot_config = {
    "eh":         ('W', up),
    "ah":         ("A", left),
    "guh":        ("S", down),
    "oh":         ("D", right),
    "ee":         ("stop", stop),
    "pop":        ("E", E),
    "tut":        ("hold E", hold_E),
    "mm":         ("space", space_key),
    "shush:th_50": ("ctrl", ctrl_key),
    "hiss:th_50": ("shift", shift_key),
    "er":         ("exit mode", actions.user.game_mode_disable),
    "cluck":      ("stop timer", lambda: actions.key("keypad_1")),
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