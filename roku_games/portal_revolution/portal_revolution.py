from talon import Module, Context, actions
from .portal_revolution_ui import ui

mod = Module()
ctx = Context()

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.portal_revolution = "os: windows\nand app.exe: revolution.exe"
ctx.matches = "os: windows\napp: portal_revolution"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

def enter_look_mode():
    global parrot_config
    parrot_config = look_config
    actions.user.ui_elements_set_state("parrot_config", look_config)

def exit_look_mode():
    global parrot_config
    parrot_config = default_config
    actions.user.ui_elements_set_state("parrot_config", look_config)

def use_scroll_tick():
    global parrot_config
    parrot_config.pop('hiss', None)
    parrot_config.pop('shush', None)

    parrot_config = {
        **parrot_config,
        "hiss:th_100":("scroll tick down", lambda: actions.mouse_scroll(-1, by_lines=True)),
        "hiss_stop":  ("", lambda: None),
        "shush:th_100":("scroll tick up", lambda: actions.mouse_scroll(1, by_lines=True)),
        "shush_stop":  ("", lambda: None),
    }

look_down = False

def toggle_look_down():
    global look_down
    look_down = not look_down
    if look_down:
        actions.user.game_mouse_move_deg_down_45()
    else:
        actions.user.game_mouse_move_reset_center_y()

last_dir = None

def turn_dir():
    global last_dir
    actions.user.game_stopper()
    if last_dir == "left":
        actions.user.game_mouse_move_continuous_left_10()
    elif last_dir == "right":
        actions.user.game_mouse_move_continuous_right_10()

def left():
    global last_dir
    last_dir = "left"
    actions.user.game_wasd_hold_a()

def right():
    global last_dir
    last_dir = "right"
    actions.user.game_wasd_hold_d()

default_config = {
    "eh":         ("forward", actions.user.game_wasd_hold_w),
    "guh":        ("back", actions.user.game_wasd_hold_s),
    "ah":         ("left", left),
    "oh":         ("right", right),
    "ee":         ("stop", actions.user.game_stopper),
    "hiss":       ("turn dir", turn_dir),
    "hiss_stop":  ("", lambda: None),
    "shush:th_90": ("jump", lambda: actions.user.game_key("space")),
    "shush_stop": ("", lambda: None),
    "nn":         ("E", lambda: actions.user.game_key("e")),
    # "palate":     ("toggle look down", lambda: actions.user.game_key("space")),
    "cluck":      ("toggle look down", toggle_look_down),
    "pop":        ("L click", actions.user.game_mouse_click_left),
    "palate":      ("R click", actions.user.game_mouse_click_right),
    "t":          ("shift", lambda: actions.user.game_key("shift")),
    "-":          ("-"),
    "tut":    ("reset y", actions.user.game_mouse_move_reset_center_y),

    # "tut tut":    ("look mode", enter_look_mode),
    # "tut hiss":   ("look down", lambda: (
    #     actions.user.game_mouse_move_deg_down_15(),
    #     enter_look_mode()
    # )),
    # "tut shush":  ("look up", lambda: (
    #     actions.user.game_mouse_move_deg_up_15(),
    #     enter_look_mode()
    # )),
    "tut ah":     ("left 90", actions.user.game_mouse_move_deg_left_90),
    "tut oh":     ("right 90", actions.user.game_mouse_move_deg_right_90),
    "tut guh":    ("180", actions.user.game_mouse_move_deg_180),
    "tut pop":    ("hold L click", actions.user.game_mouse_hold_left),
    "tut cluck":  ("hold R click", actions.user.game_mouse_hold_right),
    # "tut ee":     ("scroll tick mode", use_scroll_tick),
    # "er":         ("exit mode", actions.user.game_mode_disable),
    "tut tut":    ("exit mode", actions.user.game_mode_disable),
}

look_config = {
    **default_config,
    "ah":         ("look left", actions.user.game_mouse_move_continuous_left_5),
    "oh":         ("look right", actions.user.game_mouse_move_continuous_right_5),
    "hiss":       ("look down", actions.user.game_mouse_move_continuous_down_10),
    "hiss_stop":  ("", actions.user.game_mouse_move_continuous_stop),
    "shush":      ("look up", actions.user.game_mouse_move_continuous_up_10),
    "shush_stop": ("", actions.user.game_mouse_move_continuous_stop),
    "er":         ("exit look", exit_look_mode),
}

parrot_config = default_config

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        actions.user.ui_elements_show(ui, initial_state={
            "parrot_config": parrot_config,
            "background_color": "22266688"
        })

    def on_game_mode_disabled():
        actions.user.ui_elements_hide_all()

    def parrot_config():
        return parrot_config