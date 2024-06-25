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

def jump_secondary():
    actions.user.game_key_hold("p", jump_secondary_ms)

def jump_primary():
    actions.user.game_key_hold("c", jump_primary_ms)

def set_secondary_jump_duration(duration_ms: int):
    global jump_secondary_ms
    jump_secondary_ms = duration_ms

def use_feather_parrot_config():
    global parrot_config
    parrot_config = {
        **default_config,
        **move_config
    }
    refresh_ui(parrot_config, { "background_color": "C70039" })

def use_default_parrot_config():
    global parrot_config
    parrot_config = default_config
    refresh_ui(parrot_config, { "background_color": "000000" })

default_config = {
    "ah":         ("left", actions.user.game_move_dir_hold_left),
    "oh":         ("right", actions.user.game_move_dir_hold_right),
    "ee":         ("stop", actions.user.game_stopper),
    "guh":        ("toggle down", lambda: actions.user.game_key_toggle("down")),
    "eh":         ("dash up", dash_up),
    "t":          ("dash FUP", dash_forward_up),
    "mm":         ("dash FDOWN", dash_forward_down),
    "er":         ("dash DOWN", dash_down),
    "pop":        ("dash F", dash_forward),
    "palate":     ("dash demo", dash_demo),
    "shush:th_100":("jump 1", jump_primary),
    "shush_stop": ("", lambda: None),
    "hiss:th_100":("jump 2", jump_secondary),
    "hiss_stop":  ("", lambda: None),
    "tut t":      ("map", lambda: actions.user.game_key_down("tab")),
    "tut tut":    ("exit mode", actions.user.game_mode_disable),
    "tut eh":     ("up", actions.user.game_move_dir_hold_up),
    "tut guh":    ("down", actions.user.game_move_dir_hold_down),
    "tut pop":    ("", lambda: (
        actions.user.game_state_switch_horizontal(),
        dash_forward())),
    "tut palate":     ("", lambda: (
        actions.user.game_state_switch_horizontal(),
        dash_demo())),
    "tut t":      ("", lambda: (
        actions.user.game_state_switch_horizontal(),
        dash_forward_up())),
    "tut mm":     ("", lambda: (
        actions.user.game_state_switch_horizontal(),
        dash_forward_down())),
    "tut ee":     ("skip scene", lambda: actions.key("escape down c")),
    "tut cluck":  ("return map", lambda: actions.key("escape up c c")),
    "cluck":      ("load", lambda: (actions.key("f8"), actions.user.game_stopper())),
    "cluck cluck":("save", lambda: actions.key("f7")),
    "cluck ee":   ("clear", lambda: actions.key("f4")),
    "cluck guh":  ("debug", lambda: actions.key("f6")),
    "foot_pedal_L": ("grab", lambda: None),
    "foot_pedal_M": ("move mode", lambda: None),
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

feather_stop_job = None

def stop_feather_mode():
    global feather_stop_job
    feather_stop_job = None
    unhighlight("foot_center")
    use_default_parrot_config()

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        show_ui(parrot_config)

    def on_game_mode_disabled():
        hide_ui()

    def parrot_config():
        return parrot_config

    def pedal_left_down():
        # command mananged by playability app
        # hold "z", otherwise key gets untriggered every
        # time we issue another key with talon
        highlight("foot_left")

    def pedal_left_up():
        unhighlight("foot_left")

    def pedal_center_down():
        if feather_stop_job:
            cron.cancel(feather_stop_job)
            # do nothing - already running
        else:
            use_feather_parrot_config()
            highlight("foot_center")

    def pedal_center_up():
        global feather_stop_job
        feather_stop_job = cron.after("100ms", stop_feather_mode)

@mod.action_class
class Actions:
    def game_celeste_set_jump_2(number: int):
        """set jump 2 ms"""
        global jump_secondary_ms
        print(f"set jump2 to {number}")
        jump_secondary_ms = number
        actions.user.game_mode_enable()

    def game_celeste_set_flex_key(action_name: str):
        """set flex key"""
        global flex
        flex = action_name
