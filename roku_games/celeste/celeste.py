from talon import Module, Context, actions, cron
from .celeste_ui import show_ui, hide_ui, refresh_ui, highlight, unhighlight

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.celeste = "os: windows\nand app.exe: Celeste.exe"
ctx.matches = "os: windows\napp: celeste"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

jump_primary_ms = 300
jump_secondary_ms = 120

def dash_forward_up():
    actions.user.game_move_dir_hold_last_horizontal()
    actions.user.game_key_hold("up", 100),
    actions.user.game_key("x")

def dash_forward_down():
    actions.user.game_move_dir_hold_last_horizontal()
    actions.user.game_key_hold("down", 100),
    actions.user.game_key("x")

def dash_forward():
    actions.user.game_move_dir_hold_last_horizontal()
    actions.user.game_key("x")

def dash_up():
    actions.user.game_move_dir_hold_up(),
    actions.user.game_key("x")

def dash_down():
    actions.user.game_move_dir_hold_down(),
    actions.user.game_key("x")

def dash_demo():
    actions.user.game_move_dir_hold_last_horizontal()
    actions.user.game_key("t")

def dash_backward():
    actions.user.game_state_switch_horizontal(),
    dash_forward()

def dash_backward_up():
    actions.user.game_state_switch_horizontal()
    dash_forward_up()

def dash_backward_down():
    actions.user.game_state_switch_horizontal()
    dash_backward_down()

def dash_demo_backward():
    actions.user.game_state_switch_horizontal(),
    dash_demo()

def jump_secondary():
    actions.user.game_key_hold("p", jump_secondary_ms)

def jump_primary():
    actions.user.game_key_hold("c", jump_primary_ms)

def use_move_mode():
    global parrot_config
    parrot_config = {
        **default_config,
        **move_config
    }
    refresh_ui(parrot_config, { "background_color": "C70039" })

def use_default_mode():
    global parrot_config
    parrot_config = default_config
    refresh_ui(parrot_config, { "background_color": "000000" })

def skip_scene():
    actions.user.game_stopper()
    actions.key("escape down c")

def return_map():
    actions.user.game_stopper()
    actions.key("escape up c c")

default_config = {
    "sh:th_100":  ("jump 1", jump_primary),
    "sh_stop":    ("", lambda: None),
    "ss:th_100":  ("jump 2", jump_secondary),
    "ss_stop":    ("", lambda: None),
    "ah":         ("left", actions.user.game_move_dir_hold_left),
    "oh":         ("right", actions.user.game_move_dir_hold_right),
    "ee":         ("stop", actions.user.game_stopper),
    "pop":        ("dash f", dash_forward),
    "mm":         ("dash f-down", dash_forward_down),
    "t":          ("dash f-up", dash_forward_up),
    "eh":         ("dash up", dash_up),
    "er":         ("dash down", dash_down),
    "palate":     ("dash demo", dash_demo),
    "tut <dash>": ("reverse <dash>"),
    "tut tut":    ("exit mode", actions.user.game_mode_disable),
    "tut pop":    ("", dash_backward),
    "tut palate": ("", dash_demo_backward),
    "tut t":      ("", dash_backward_up),
    "tut mm":     ("", dash_backward_down),
    "guh":        ("toggle down", lambda: actions.user.game_key_toggle("down")),
    "tut ee":     ("skip scene", skip_scene),
    "tut cluck":  ("return map", return_map),
    "cluck":      ("load", lambda: (actions.key("f8"), actions.user.game_stopper())),
    "cluck cluck":("save", lambda: actions.key("f7")),
    "cluck ee":   ("clear", lambda: actions.key("f4")),
    "cluck guh":  ("debug", lambda: actions.key("f6")),
    "foot 1":     ("grab"),
    "foot 2":     ("move mode"),
}
parrot_config = default_config

move_config = {
    "ah":         ("left", actions.user.game_move_dir_hold_left),
    "oh":         ("right", actions.user.game_move_dir_hold_right),
    "ee":         ("stop", actions.user.game_stopper),
    "guh":        ("down", actions.user.game_move_dir_hold_down),
    "eh":         ("up", actions.user.game_move_dir_hold_up),
    "t":          ("f-up", actions.user.game_move_dir_hold_up_horizontal),
    "mm":         ("f-down", actions.user.game_move_dir_hold_down_horizontal),
}

@ctx.action_class("user")
class Actions:
    def on_game_mode_enabled():
        show_ui(parrot_config)

    def on_game_mode_disabled():
        hide_ui()

pedal_center_up_job = None

def stop_move_mode():
    global pedal_center_up_job
    pedal_center_up_job = None
    unhighlight("foot_center")
    use_default_mode()

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        show_ui(parrot_config)

    def on_game_mode_disabled():
        hide_ui()

    def parrot_config():
        return parrot_config

    def pedal_left_down():
        # we manage highlighting here, but not the action
        # command mananged by playability app
        # it will hold "z", otherwise key gets untriggered every
        # time we issue another key with talon
        highlight("foot_left")

    def pedal_left_up():
        unhighlight("foot_left")

    def pedal_center_down():
        if pedal_center_up_job:
            cron.cancel(pedal_center_up_job)
            # do nothing - already running
        else:
            use_move_mode()
            highlight("foot_center")

    def pedal_center_up():
        global pedal_center_up_job
        pedal_center_up_job = cron.after("100ms", stop_move_mode)

@mod.action_class
class Actions:
    def game_celeste_set_jump_2(number: int):
        """set jump 2 ms"""
        global jump_secondary_ms
        jump_secondary_ms = number
        actions.user.ui_elements_set_text("jump2", f"{jump_secondary_ms}ms")
        actions.user.game_mode_enable()
