from talon import Module, Context, actions, cron
from .ui.index import show_ui, hide_ui, refresh_ui

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.celeste = "os: windows\nand app.exe: /Celeste.exe/i"
ctx.matches = "os: windows\napp: celeste"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

jump_primary_ms = 300

def dash_forward_up():
    actions.user.game_dir_hold_last_horizontal()
    actions.user.game_key_hold("up", 100),
    actions.user.game_key("x")

def dash_forward_down():
    actions.user.game_dir_hold_last_horizontal()
    actions.user.game_key_hold("down", 100),
    actions.user.game_key("x")

def dash_forward():
    actions.user.game_dir_hold_last_horizontal()
    actions.user.game_key("x")

def dash_up():
    actions.user.game_arrows_hold_up(),
    actions.user.game_key("x")

def dash_down():
    actions.user.game_arrows_hold_down(),
    actions.user.game_key("x")

def dash_demo():
    actions.user.game_dir_hold_last_horizontal()
    actions.user.game_key("t")

def dash_backward():
    actions.user.game_state_switch_horizontal(),
    dash_forward()

def dash_backward_up():
    actions.user.game_state_switch_horizontal()
    dash_forward_up()

def dash_backward_down():
    actions.user.game_state_switch_horizontal()
    dash_forward_down()

def dash_demo_backward():
    actions.user.game_state_switch_horizontal(),
    dash_demo()

def jump_primary():
    actions.user.game_key_hold("c", jump_primary_ms)

def use_move_mode():
    global parrot_config
    parrot_config = {
        **default_config,
        **move_config
    }
    # refresh_ui(parrot_config, "C70039")

def use_default_mode():
    global parrot_config
    parrot_config = default_config
    # refresh_ui(parrot_config, "000000")

def skip_scene():
    actions.user.game_stopper()
    actions.key("escape down c")

def return_map():
    actions.user.game_stopper()
    actions.key("escape up c c")

def restart_chapter():
    actions.user.game_stopper()
    actions.user.game_key_sequence("escape up up c c", 100)

default_config = {
    "sh:th_90":   ("jump 1", jump_primary),
    "sh_stop":    ("", lambda: None),
    "ss":         ("jump 2", lambda: actions.user.game_key_hold("p")),
    "ss_stop:db_20":("", lambda: actions.user.game_key_release("p")),
    "ah":         ("left", actions.user.game_arrows_hold_left),
    "oh":         ("right", actions.user.game_arrows_hold_right),
    "ee":         ("stop", actions.user.game_stopper),
    "pop":        ("dash f", dash_forward),
    "mm":         ("dash f down", dash_forward_down),
    "t":          ("dash f up", dash_forward_up),
    "eh":         ("dash up", dash_up),
    "er":         ("dash down", dash_down),
    "palate":     ("dash demo", dash_demo),
    "tut <dash>": ("reverse <dash>"),
    "guh":        ("toggle down", lambda: actions.user.game_key_toggle("down")),
    "tut tut":    ("exit mode", actions.user.game_mode_disable),
    "tut pop":    ("dash b", dash_backward),
    "tut palate": ("dash b demo", dash_demo_backward),
    "tut t":      ("dash b up", dash_backward_up),
    "tut mm":     ("dash b down", dash_backward_down),
    "tut ee":     ("skip scene", skip_scene),
    "tut cluck":  ("return map", return_map),
    "cluck":      ("load", lambda: (actions.key("f8"), actions.user.game_stopper())),
    "cluck cluck":("save", lambda: actions.key("f7")),
    "cluck ee":   ("clear", lambda: actions.key("f4")),
    "cluck guh":  ("debug", lambda: actions.key("f6")),
    "cluck pop":  ("restart chapter", restart_chapter),
    "foot 1":     ("grab"),
    "foot 2":     ("move mode"),
}
parrot_config = default_config

move_config = {
    "ah":         ("left", actions.user.game_arrows_hold_left),
    "oh":         ("right", actions.user.game_arrows_hold_right),
    "ee":         ("stop", actions.user.game_stopper),
    "guh":        ("down", actions.user.game_arrows_hold_down),
    "eh":         ("up", actions.user.game_arrows_hold_up),
    "t":          ("f-up", actions.user.game_arrows_hold_up_horizontal),
    "mm":         ("f-down", actions.user.game_arrows_hold_down_horizontal),
    "palate":     ("short up", lambda: actions.user.game_key_hold("up", 30)),
    "pop":        ("short down", lambda: actions.user.game_key_hold("down", 30)),
    "sh:th_100":  ("c", lambda: actions.user.game_key("c")),
    "sh_stop":    ("", lambda: None),
    "ss:th_100":  ("x", lambda: actions.user.game_key("x")),
    "ss_stop":    ("", lambda: None),
}

pedal_center_up_job = None

def stop_move_mode():
    global pedal_center_up_job
    pedal_center_up_job = None
    actions.user.ui_elements_unhighlight("foot_center")
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
        actions.user.ui_elements_highlight("foot_left")

    def pedal_left_up():
        actions.user.ui_elements_unhighlight("foot_left")

    def pedal_center_down():
        if pedal_center_up_job:
            cron.cancel(pedal_center_up_job)
            # do nothing - already running
        else:
            use_move_mode()
            actions.user.ui_elements_highlight("foot_center")

    def pedal_center_up():
        global pedal_center_up_job
        pedal_center_up_job = cron.after("100ms", stop_move_mode)