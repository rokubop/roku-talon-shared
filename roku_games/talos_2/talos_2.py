from talon import Module, Context, actions
from .talos_2_ui import talos_2_ui
import copy

mod = Module()
ctx = Context()

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.talos_2 = "os: windows\nand app.exe: /Talos2-Win64-Shipping.exe/i"
ctx.matches = "os: windows\napp: talos_2"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

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

state = {
    # actions
    "nn": {
        "value": 0,
        "labels": ["E", "hold E"]
    },
    "pop": {
        "value": 0,
        "labels": ["left click", "hold left click"]
    },
    "palate": {
        "value": 0,
        "labels": ["right click", "hold right click"]
    },
    "t": {
        "value": 0,
        "labels": ["toggle shift", "toggle down"]
    },
    "er": {
        "value": 0,
        "labels": ["space", "hold space"]
    },

    # movement
    "eh": {
        "value": 0,
        "labels": ["go", "up slow"]
    },
    "guh": {
        "value": 0,
        "labels": ["back", "turn 180"]
    },
    "ah": {
        "value": 0,
        "labels": ["left slow", "move left"]
    },
    "oh": {
        "value": 0,
        "labels": ["right slow", "move right"]
    },
    "ee": {
        "value": 0,
        "labels": ["stop", "hard stop"]
    },
    "hiss": {
        "value": 0,
        "labels": ["left strong", "left 90"]
    },
    "shush": {
        "value": 0,
        "labels": ["right strong", "right 90"]
    },
    "cluck": {
        "value": 0,
        "labels": ["game", "ui"]
    },
    "tut": {
        "labels": ["reset y"],
    },
    "tut tut": {
        "labels": ["exit"],
    },
    "tut <any>": {
        "labels": ["alt action once"],
    },
    "cluck <any>": {
        "labels": ["alt action toggle"],
    },
    "looking_down": {
        "value": False,
        "labels": []
    },
}

initial_state = copy.deepcopy(state)

def reset_state():
    global state
    state = copy.deepcopy(initial_state)

def get_number_state(key, alt=False):
    if alt:
        return 1 if state[key]["value"] == 0 else 0

    return state[key]["value"]

def on_palate(alt=False):
    if get_number_state("palate", alt) == 0:
        actions.user.game_mouse_click_right()
    else:
        actions.user.game_mouse_hold_right()

def on_pop(alt=False):
    if get_number_state("pop", alt) == 0:
        actions.user.game_mouse_click_left()
    else:
        actions.user.game_mouse_hold_left()

def on_eh(alt=False):
    if get_number_state("eh", alt) == 0:
        actions.user.game_wasd_hold_w()
    else:
        actions.user.game_mouse_move_continuous_up_10()

def on_guh(alt=False):
    if get_number_state("guh", alt) == 0:
        actions.user.game_wasd_hold_s()
    else:
        actions.user.game_mouse_move_deg_180()

def on_ah(alt=False):
    if get_number_state("ah", alt) == 0:
        actions.user.mouse_vectors("main", v=(-100, 0))
        # actions.user.game_mouse_move_continuous_left(2)
    else:
        actions.user.game_wasd_hold_a()

def on_oh(alt=False):
    if get_number_state("oh", alt) == 0:
        actions.user.mouse_vectors("main", v=(100, 0))
        # actions.user.game_mouse_move_continuous_right(2)
    else:
        actions.user.game_wasd_hold_d()

def on_ee(alt=False):
    actions.user.mouse_vectors_stop()
    # actions.user.mouse_vectors("main", v=(0, 0))
    if get_number_state("ee", alt) == 0:
        actions.user.game_stopper()
    else:
        actions.user.game_stop_all()

def on_hiss(alt=False):
    if get_number_state("hiss", alt) == 0:
        actions.user.game_mouse_move_continuous_left_10()
    else:
        actions.user.game_mouse_move_deg_left_90()

def on_hiss_stop(alt=False):
    if get_number_state("hiss", alt) == 0:
        actions.user.game_mouse_move_continuous_stop()
    else:
        pass

def on_shush(alt=False):
    if get_number_state("shush", alt) == 0:
        print("Active vectors:", actions.user.mouse_vectors_list())

        # 3. Get main state and create boost
        m = actions.user.mouse_vectors("main")
        print("Main vector state:", m)
        if m and m["v"] != (0, 0):
            actions.user.mouse_vectors(
                "main",
                a=(m["v"][0] * 4, m["v"][1] * 4),
                duration=300,
            )
        else:
            print("ERROR: Main vector has wrong velocity:", m["v"])
        # actions.user.game_mouse_move_continuous_right_10()
    else:
        actions.user.game_mouse_move_deg_right_90()

def on_shush_stop(alt=False):
    if get_number_state("shush", alt) == 0:
        actions.user.game_mouse_move_continuous_stop()
    else:
        pass

def on_nn(alt=False):
    if get_number_state("nn", alt) == 0:
        actions.user.game_key("e")
    else:
        actions.user.game_key_hold("e")

def on_t(alt=False):
    if get_number_state("t", alt) == 0:
        actions.user.game_key_toggle("shift")
    else:
        if state["looking_down"]["value"]:
            actions.user.game_mouse_move_deg_up_45()
        else:
            actions.user.game_mouse_move_deg_down_45()
        state["looking_down"]["value"] = not state["looking_down"]["value"]

def on_er(alt=False):
    if get_number_state("er", alt) == 0:
        actions.user.game_key("space")
    else:
        actions.user.game_key_hold("space")

def toggle_state(key):
    global state
    if key == "looking_down":
        return

    new_state = state.copy()
    new_state[key] = state[key].copy()
    new_state[key]["value"] = 1 if state[key]["value"] == 0 else 0
    actions.user.ui_elements_set_state("game_state", new_state)

    state = new_state
    globals()[f"on_{key}"]()

    # state[key]["value"] = 1 if state[key]["value"] == 0 else 0
    # globals()[f"on_{key}"]()

    # new_state = state.copy()
    # new_state[key] = state[key].copy()  # only deep-copy the changed subdict
    # actions.user.ui_elements_set_state("game_state", new_state)

def trigger_alt_once(key):
    if key == "looking_down" or key == "cluck":
        return
    else:
        globals()[f"on_{key}"](alt=True)

def toggle_mode():
    global parrot_config
    if state["cluck"]["value"] == 0:
        parrot_config = {
            **actions.user.parrot_mode_v6_config(),
            "default": {
                **actions.user.parrot_mode_v6_config()["default"],
                "cluck": (label("cluck"), toggle_mode),
                "tut tut": (label("tut tut"), actions.user.game_mode_disable),
            },
        }
        state["cluck"]["value"] = 1
    else:
        parrot_config = game_config
        state["cluck"]["value"] = 0

def toggle(key): return (f"toggle {key}", lambda: toggle_state(key))

def alt(key): return (f"alt {key}", lambda: trigger_alt_once(key))

def label(key):
    return ", ".join(state[key]["labels"])

def use_a_or_b(key):
    return (
        label(key),
        lambda alt=False: globals()[f"on_{key}"](alt)
    )

game_config = {
    # actions
    "nn":         use_a_or_b("nn"),
    "pop":        use_a_or_b("pop"),
    "palate":     use_a_or_b("palate"),
    "t":          use_a_or_b("t"),
    "er":         use_a_or_b("er"),

    # movement
    "eh":         use_a_or_b("eh"),
    "guh":        use_a_or_b("guh"),
    "ah":         use_a_or_b("ah"),
    "oh":         use_a_or_b("oh"),
    "ee":         use_a_or_b("ee"),
    "hiss":       use_a_or_b("hiss"),
    "hiss_stop":  ("", on_hiss_stop),
    "shush":      use_a_or_b("shush"),
    "shush_stop": ("", on_shush_stop),

    # special
    "tut":        ("reset y", actions.user.game_mouse_move_reset_center_y),
    "tut tut":    ("exit", actions.user.game_mode_disable),
    "cluck":      ("game, ui", toggle_mode),
    "cluck ah":   toggle("ah"),
    "cluck oh":   toggle("oh"),
    "cluck ee":   toggle("ee"),
    "cluck t":    toggle("t"),
    "cluck pop":  toggle("pop"),
    "cluck palate": toggle("palate"),
    "cluck eh":   toggle("eh"),
    "cluck guh":  toggle("guh"),
    "cluck hiss": toggle("hiss"),
    "cluck shush":toggle("shush"),
    "cluck nn":   toggle("nn"),
    "cluck er":   toggle("er"),
    "tut ah":     alt("ah"),
    "tut oh":     alt("oh"),
    "tut ee":     alt("ee"),
    "tut guh":    alt("guh"),
    "tut eh":     alt("eh"),
    "tut hiss":   alt("hiss"),
    "tut shush":  alt("shush"),
    "tut nn":     alt("nn"),
    "tut er":     alt("er"),
    "tut t":      alt("t"),
    "tut pop":    alt("pop"),
    "tut palate": alt("palate"),
}

parrot_config = game_config

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        reset_state()
        actions.user.ui_elements_show(talos_2_ui, initial_state={
            "game_state": state.copy(),
        })

    def on_game_mode_disabled():
        actions.user.ui_elements_hide_all()

    def parrot_config():
        return parrot_config