from talon import actions, Module, Context, cron, settings, app
from typing import Union
from .game_events import event_on_xbox, event_on_game_mode, EVENT_GAME_MODE_ENABLED

mod = Module()
ctx = Context()
ctx_game_xbox = Context()
ctx_game_xbox.matches = """
tag: user.game_xbox
"""

# for one word left, right, up, down
preferred_dir_mode_subject = "right_stick"
preferred_dir_mode_action_type = "hold"

def get_gear_value(subject: str, gear: int = 5):
    gears = settings.get(f"user.game_xbox_{subject}_gears")
    if not gears:
        return 5
    try:
        return float(gears.split(" ")[gear - 1])
    except KeyError:
        return 5

class GearState:
    gear: int
    value: float
    subject: str

    def __init__(self, subject: str):
        gear = settings.get(f"user.game_xbox_{subject}_default_gear")
        self.subject = subject
        self.set_gear(int(gear) if gear else 5)

    def set_gear(self, gear: Union[int, str]):
        self.gear = gear
        self.value = get_gear_value(self.subject, int(gear))

button_event_subscribers = []
dpad_hold_dir = None
left_stick_dir = (0, 0)
right_stick_dir = (0, 0)
gear_state = {}
held_buttons = set()
button_up_pending_jobs = {}
button_hold_time = None

LEFT_STICK = "left_stick"
RIGHT_STICK = "right_stick"
LEFT_TRIGGER = "left_trigger"
RIGHT_TRIGGER = "right_trigger"

def init_gear_states():
    global gear_state
    gear_state = {
        LEFT_STICK: GearState(LEFT_STICK),
        RIGHT_STICK: GearState(RIGHT_STICK),
        LEFT_TRIGGER: GearState(LEFT_TRIGGER),
        RIGHT_TRIGGER: GearState(RIGHT_TRIGGER),
    }

dir_to_xy = {
    "up": (0, 1),
    "down": (0, -1),
    "left": (-1, 0),
    "right": (1, 0),
    "back": (0, -1),
    "forward": (0, 1),
}

xbox_trigger_map = {
    "lt": LEFT_TRIGGER,
    "rt": RIGHT_TRIGGER,
    "l2": LEFT_TRIGGER,
    "r2": RIGHT_TRIGGER,
    LEFT_TRIGGER: LEFT_TRIGGER,
    RIGHT_TRIGGER: RIGHT_TRIGGER,
}

xbox_button_map = {
    "a": "a",
    "b": "b",
    "x": "x",
    "y": "y",
    "dpad_up": "dpad_up",
    "dpad_down": "dpad_down",
    "dpad_left": "dpad_left",
    "dpad_right": "dpad_right",
    "lb": "left_shoulder",
    "rb": "right_shoulder",
    "l1": "left_shoulder",
    "r1": "right_shoulder",
    "l3": "left_thumb",
    "r3": "right_thumb",
    "rt": "right_trigger",
    "lt": "left_trigger",
    "left_shoulder": "left_shoulder",
    "right_shoulder": "right_shoulder",
    "left_thumb": "left_thumb",
    "right_thumb": "right_thumb",
    "menu": "start",
    "start": "start",
    "view": "back",
    "back": "back",
    "guide": "guide",
    "xbox": "guide",
    **xbox_trigger_map,
}

def xbox_left_analog_hold_dir(dir: str | tuple, power: float = None):
    """Hold a left analog direction"""
    global left_stick_dir
    power = power or gear_state["left_stick"].value

    xy_dir = None

    if isinstance(dir, tuple):
        xy_dir = [0, 0]
        for single_dir in dir:
            single_xy = dir_to_xy[single_dir]
            xy_dir[0] += single_xy[0]
            xy_dir[1] += single_xy[1]
        xy_dir = tuple(xy_dir)
    else:
        xy_dir = dir_to_xy[dir]

    actions.user.vgamepad_left_stick(xy_dir[0] * power, xy_dir[1] * power)
    if left_stick_dir != xy_dir:
        event_on_xbox.fire_left_stick_dir_change(xy_dir)
    left_stick_dir = xy_dir

def xbox_right_analog_hold_dir(dir: str | tuple, power: float = None):
    """Hold a right analog direction"""
    global right_stick_dir
    power = power or gear_state["right_stick"].value

    xy_dir = None

    if isinstance(dir, tuple):
        xy_dir = [0, 0]
        for single_dir in dir:
            single_xy = dir_to_xy[single_dir]
            xy_dir[0] += single_xy[0]
            xy_dir[1] += single_xy[1]
        xy_dir = tuple(xy_dir)
    else:
        xy_dir = dir_to_xy[dir]

    actions.user.vgamepad_right_stick(xy_dir[0] * power, xy_dir[1] * power)
    if right_stick_dir != xy_dir:
        event_on_xbox.fire_right_stick_dir_change(xy_dir)
    right_stick_dir = xy_dir

def xbox_dpad_hold_dir(dir: str | tuple):
    """Hold a dpad direction"""
    global dpad_hold_dir
    dir_2 = None
    if isinstance(dir, tuple):
        dir_2 = dir[1]
        dir = dir[0]
    actions.user.vgamepad_dpad_dir_hold(dir)
    if dpad_hold_dir != dir:
        event_on_xbox.fire_dpad_dir_hold_change(dir)
    if dir_2:
        xbox_button_hold(f"dpad_{dir_2}")
    dpad_hold_dir = dir

def xbox_set_gear(subject: str, gear: Union[str, int]):
    print("set gear", subject, gear)
    gear_state[subject].set_gear(gear)
    event_on_xbox.fire_trigger_gear_change(subject, gear_state[subject])

def xbox_button_press(button: str, hold: int = None):
    global button_hold_time
    hold = hold or button_hold_time
    xbox_button_hold(button, hold)

def xbox_button_hold(button: str, hold: int = None):
    global button_up_pending_jobs, held_buttons
    button = xbox_button_map[button]
    if button in [LEFT_TRIGGER, RIGHT_TRIGGER]:
        # print("trigger hold", button, hold)
        xbox_trigger_hold(button, hold=hold)
        return

    if button_up_pending_jobs.get(button):
        cron.cancel(button_up_pending_jobs[button])
    held_buttons.add(button)
    actions.user.vgamepad_button_hold(button)
    event_on_xbox.fire_button_hold(button)

    # print("button hold", button, hold)
    if hold:
        button_up_pending_jobs[button] = cron.after(f"{hold}ms", lambda: xbox_button_release(button))

def xbox_button_release(button: str):
    global button_up_pending_jobs
    button = xbox_button_map[button]
    if button in [LEFT_TRIGGER, RIGHT_TRIGGER]:
        xbox_trigger_release(button)
        return

    actions.user.vgamepad_button_release(button)
    event_on_xbox.fire_button_release(button)
    button_up_pending_jobs[button] = None
    if button in held_buttons:
        held_buttons.remove(button)

def xbox_button_toggle(button: str):
    button = xbox_button_map[button]
    if button in held_buttons:
        xbox_button_release(button)
    else:
        xbox_button_hold(button)

def xbox_left_stick(x: float, y: float):
    global left_stick_dir
    actions.user.vgamepad_left_stick(x, y)
    if left_stick_dir != (x, y):
        event_on_xbox.fire_left_stick_dir_change((x, y))
    left_stick_dir = (x, y)

def xbox_right_stick(x: float, y: float):
    global right_stick_dir
    actions.user.vgamepad_right_stick(x, y)
    if right_stick_dir != (x, y):
        event_on_xbox.fire_right_stick_dir_change((x, y))
    right_stick_dir = (x, y)

def xbox_trigger_hold(button: str, power: float = None, hold: int = None):
    global button_up_pending_jobs, held_buttons
    # print("trigger hold", button, power, hold)
    power = power or gear_state[button].value
    # print("power", power)
    if button_up_pending_jobs.get(button):
        cron.cancel(button_up_pending_jobs[button])
    held_buttons.add(button)
    # print("vtrigger hold", button, power)
    getattr(actions.user, f"vgamepad_{button}")(power)
    event_on_xbox.fire_trigger_hold(button, gear_state[button])

    if hold:
        button_up_pending_jobs[button] = cron.after(f"{hold}ms", lambda: xbox_trigger_release(button))

def xbox_trigger_release(button):
    global button_up_pending_jobs
    getattr(actions.user, f"vgamepad_{button}")(0)
    event_on_xbox.fire_button_release(button)
    button_up_pending_jobs[button] = None
    if button in held_buttons:
        held_buttons.remove(button)

def xbox_preferred_dir_mode(dir: str | tuple, type: str = None):
    type = type or preferred_dir_mode_action_type
    if preferred_dir_mode_subject == "left_stick":
        xbox_left_analog_hold_dir(dir)
    elif preferred_dir_mode_subject == "right_stick":
        xbox_right_analog_hold_dir(dir)
    elif preferred_dir_mode_subject == "dpad":
        if type == "press":
            if isinstance(dir, tuple):
                for single_dir in dir:
                    xbox_button_press(f"dpad_{single_dir}")
            else:
                xbox_button_press(f"dpad_{dir}")
        elif type == "hold":
            xbox_dpad_hold_dir(dir)

def xbox_preferred_dir_mode_set(subject: str, type: str):
    global preferred_dir_mode_subject, preferred_dir_mode_action_type
    preferred_dir_mode_subject = subject
    preferred_dir_mode_action_type = type
    event_on_xbox.fire_preferred_dir_mode_change(subject, type)

def xbox_stop_all():
    xbox_left_stick(0, 0)
    xbox_right_stick(0, 0)
    for button in list(held_buttons):
        actions.user.vgamepad_button_release(button)
    held_buttons.clear()

def xbox_stopper():
    """Perform general purpose stopper based on priority"""
    global dpad_hold_dir
    if right_stick_dir != (0, 0):
        xbox_right_stick(0, 0)
        return

    xbox_left_stick(0, 0)
    for button in list(held_buttons):
        xbox_button_release(button)
    held_buttons.clear()
    if dpad_hold_dir:
        xbox_button_release(f"dpad_{dpad_hold_dir}")
        dpad_hold_dir = None

def xbox_mode_enable():
    actions.user.vgamepad_enable()
    ctx.tags = ["user.game_xbox"]

def xbox_mode_disable():
    actions.user.vgamepad_disable()
    ctx.tags = []

@mod.action_class
class Actions:
    def game_event_register_on_xbox_event(callback: callable):
        """
        ```
        def on_gamepad_event(event: Any):
            print(event.subject, event.type, event.value)

        actions.user.game_event_register_on_xbox_event(on_gamepad_event)
        ```
        """
        event_on_xbox.register(callback)

    def game_event_unregister_on_xbox_event(callback: callable):
        """
        Unregister a callback for a specific game event.
        """
        event_on_xbox.unregister(callback)

    def game_event_unregister_all_on_xbox_event():
        """
        Unregister all callbacks for a specific game event.
        """
        event_on_xbox.unregister_all()

@ctx_game_xbox.action_class("user")
class Actions:
    def game_stopper():
        xbox_stopper()
        actions.next() # mouse/keys

def game_mode_setup():
    global button_hold_time, preferred_dir_mode_action_type, preferred_dir_mode_subject
    # TODO: This isn't necessary for games without xbox controls
    button_hold_time = settings.get("user.game_xbox_button_hold")
    init_gear_states()
    preferred_dir_mode_action_type = settings.get("user.game_xbox_preferred_dir_mode_action_type")
    preferred_dir_mode_subject = settings.get("user.game_xbox_preferred_dir_mode_subject")

def on_game_mode(state):
    if state == EVENT_GAME_MODE_ENABLED:
        game_mode_setup()

def on_ready():
    game_mode_setup()
    event_on_game_mode.register_locked(on_game_mode)

app.register("ready", on_ready)