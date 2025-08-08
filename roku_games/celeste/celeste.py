from talon import Module, Context, actions, cron, ctrl
from .ui.celeste_ui import show_ui, hide_ui
from .ui.components.history_log import append_history_log
import time
from pynput import keyboard

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.celeste = "os: windows\nand app.exe: /Celeste.exe/i"
ctx.matches = "os: windows\napp: celeste"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

def release_down():
    if actions.user.game_key_is_held("down"):
        actions.user.game_key_release("down")

def dash_forward_down():
    actions.user.game_dir_hold_last_horizontal()
    actions.user.game_key_hold("down", 150, retrigger=False)
    actions.user.game_key("x")

def dash_forward_up():
    release_down()
    actions.user.game_dir_hold_last_horizontal()
    actions.user.game_key_hold("up", 150),
    actions.user.game_key("x")

def dash_forward():
    release_down()
    actions.user.game_dir_hold_last_horizontal()
    actions.user.game_key("x")

def dash_up():
    release_down()
    actions.user.game_arrows_hold_up(),
    actions.user.game_key("x")

def dash_down():
    actions.user.game_arrows_hold_down(),
    actions.user.game_key("x")

def dash_demo():
    release_down()
    actions.user.game_dir_hold_last_horizontal()
    actions.user.game_key("t")

def dash_backward():
    actions.user.game_state_switch_horizontal()
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
    actions.user.game_key_hold("c", 300)

def jump_primary_backward():
    actions.user.game_state_switch_horizontal()
    actions.user.game_dir_hold_last_horizontal()
    actions.user.game_key_hold("c", 300)

def use_move_mode():
    global parrot_config
    parrot_config = {
        **default_config,
        **move_config
    }

def use_default_mode():
    global parrot_config
    parrot_config = default_config

def skip_scene():
    actions.user.game_stopper()
    actions.key("escape down c")

def return_map():
    actions.user.game_stopper()
    actions.key("escape up c c")

def restart_chapter():
    actions.user.game_stopper()
    actions.user.game_key_sequence("escape up up c c", 100)

def jump_pause():
    actions.user.game_key("c")
    actions.user.game_key("escape")

def pause_jump_pause():
    actions.user.game_key("escape")
    actions.sleep("50ms")
    actions.user.game_key("p") # second jump bound to "p"
    actions.user.game_key("escape")

# def test():
#     actions.user.game_key_hold("c", 200)
#     cron.after("208ms", lambda: actions.user.game_key_hold("c", 200))

default_config = {
    "sh:th_90":   ("jump 1", jump_primary),
    # "sh:th_90":   ("jump 1", test),
    "sh_stop":    ("", lambda: None),
    "ss":         ("jump 2", lambda: actions.user.game_key_hold("p")),
    "ss_stop":    ("", lambda: actions.user.game_key_release("p")),
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
    "tut sh":     ("jump b", jump_primary_backward),
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
    "cluck sh":   ("jump pause", jump_pause),
    "cluck ss":   ("pause jump pause", pause_jump_pause),
    "foot 1":     ("grab"),
    "foot 2":     ("move mode"),
    "foot 3":     ("jump 3")
}
parrot_config = default_config

move_config = {
    "ah":         ("left", actions.user.game_arrows_hold_left),
    "oh":         ("right", actions.user.game_arrows_hold_right),
    "ee":         ("stop", actions.user.game_stopper),
    "guh":        ("down", actions.user.game_arrows_hold_down),
    "eh":         ("up", actions.user.game_arrows_hold_up),
    "er":         ("r click", actions.user.game_mouse_click_right),
    "t":          ("f-up", actions.user.game_arrows_hold_up_horizontal),
    "mm":         ("f-down", actions.user.game_arrows_hold_down_horizontal),
    "palate":     ("short up", lambda: actions.user.game_key_hold("up", 30)),
    "pop":        ("short down", lambda: actions.user.game_key_hold("down", 30)),
    "tut":        ("tab", lambda: actions.user.game_key("tab")),
    "tut t":      ("b-up", lambda: (
        actions.user.game_state_switch_horizontal(),
        actions.user.game_arrows_hold_up_horizontal()
    )),
    "tut mm":     ("b-down", lambda: (
        actions.user.game_state_switch_horizontal(),
        actions.user.game_arrows_hold_down_horizontal()
    )),
    "sh:th_100":  ("c", lambda: actions.user.game_key("c")),
    "sh_stop":    ("", lambda: None),
    "ss:th_100":  ("x", lambda: actions.user.game_key("x")),
    "ss_stop":    ("", lambda: None),
    "cluck":      ("escape", lambda: actions.user.game_key("escape")),
}

def stop_move_mode():
    global pedal_center_up_job
    pedal_center_up_job = None
    use_default_mode()
    actions.user.ui_elements_unhighlight("foot_center")
    # actions.user.ui_elements_set_state("side_b", False)

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        # actions.user.ui_elements_set_state("parrot_config", parrot_config)
        show_ui()
        actions.user.pynput_pedal_enable()

    def on_game_mode_disabled():
        hide_ui()
        actions.user.pynput_pedal_disable()

    def parrot_config():
        return parrot_config

    def pynput_pedal_left_down():
        actions.user.game_key_hold("z", release_on_stop=False)
        # append_history_log("pedal 1", "grab")
        # actions.user.ui_elements_set_state("grab", True)
        actions.user.ui_elements_highlight("foot_left")

    def pynput_pedal_left_up():
        actions.user.game_key_release("z")
        # actions.user.ui_elements_set_state("grab", False)
        actions.user.ui_elements_unhighlight("foot_left")

    def pynput_pedal_middle_down():
        use_move_mode()
        # append_history_log("pedal 2", "side b")
        # actions.user.ui_elements_set_state("side_b", True)
        actions.user.ui_elements_highlight("foot_center")

    def pynput_pedal_middle_up():
        stop_move_mode()

    def pynput_pedal_right_down():
        actions.user.game_key_hold("p", release_on_stop=False)
        # append_history_log("pedal 3", "jump 3")
        # actions.user.ui_elements_set_state("hold_jump", True)
        actions.user.ui_elements_highlight("foot_right")

    def pynput_pedal_right_up():
        actions.user.game_key_release("p")
        # actions.user.ui_elements_set_state("hold_jump", False)
        actions.user.ui_elements_unhighlight("foot_right")

    def pedal_left_down(): actions.skip()
    def pedal_left_up(): actions.skip()
    def pedal_center_down(): actions.skip()
    def pedal_center_up(): actions.skip()
    def pedal_right_down(): actions.skip()
    def pedal_right_up(): actions.skip()