from talon import Module, actions, cron
import vgamepad as vg

mod = Module()

gamepad = None
EVENT_BUTTON_HOLD = "hold"
EVENT_BUTTON_RELEASE = "release"
button_event_subscribers = []
dpad_dir_change_event_subscribers = []
left_joystick_dir = (0, 0)
right_joystick_dir = (0, 0)
held_buttons = set()
button_up_pending_jobs = {}

button_map = {
    "a": vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    "b": vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    "x": vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    "y": vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
    "dpad_up": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    "dpad_down": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    "dpad_left": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    "dpad_right": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    "left_shoulder": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    "right_shoulder": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    "left_thumb": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
    "right_thumb": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
    "start": vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
    "back": vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    "guide": vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
}

LEFT_JOYSTICK = "left_joystick"
RIGHT_JOYSTICK = "right_joystick"

def vgamepad_enable():
    global gamepad
    gamepad = vg.VX360Gamepad()
    # gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    # gamepad.update()
    # gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    # gamepad.update()

def vgamepad_disable():
    global gamepad
    del gamepad

def vgamepad_button_down(button: str):
    global gamepad, button_up_pending_jobs, held_buttons
    if button_up_pending_jobs.get(button):
        cron.cancel(button_up_pending_jobs[button])
    held_buttons.add(button)
    gamepad.press_button(button_map[button])
    gamepad.update()
    vgamepad_event_trigger_on_button(button, EVENT_BUTTON_HOLD)

def vgamepad_button_up(button: str):
    global button_up_pending_jobs
    gamepad.release_button(button_map[button])
    gamepad.update()
    vgamepad_event_trigger_on_button(button, EVENT_BUTTON_RELEASE)
    button_up_pending_jobs[button] = None
    held_buttons.remove(button)

def vgamepad_button_press(button: str):
    vgamepad_button_down(button)
    button_up_pending_jobs[button] = cron.after("200ms", lambda: vgamepad_button_up(button))

def vgamepad_button(button: str, hold: int = None, down: bool = None, up: bool = None):
    if "trigger" in button:
        if button == "left_trigger":
            return trigger("left", hold, down, up)
        elif button == "right_trigger":
            return trigger("right", hold, down, up)

    if down:
        vgamepad_button_down(button)
    elif up:
        vgamepad_button_up(button)
    elif hold:
        vgamepad_button_down(button)
        button_up_pending_jobs[button] = cron.after(f"{hold}ms", lambda: vgamepad_button_up(button))
    else:
        vgamepad_button_press(button)

def vgamepad_dpad(button: str):
    directions = ["left", "right", "up", "down"]

    for direction in directions:
        if direction == button:
            vgamepad_button_down(f"dpad_{direction}")
        elif f"dpad_{direction}" in held_buttons:
            vgamepad_button_up(f"dpad_{direction}")

def vgamepad_stopper():
    left_joystick(0, 0)
    right_joystick(0, 0)
    if "dpad_left" in held_buttons:
        vgamepad_button_up("dpad_left")
    if "dpad_right" in held_buttons:
        vgamepad_button_up("dpad_right")
    if "dpad_up" in held_buttons:
        vgamepad_button_up("dpad_up")
    if "dpad_down" in held_buttons:
        vgamepad_button_up("dpad_down")

def left_joystick(x: float, y: float):
    global left_joystick_dir
    gamepad.left_joystick_float(x, y)
    gamepad.update()
    if left_joystick_dir != (x, y):
        vgamepad_event_trigger_joystick_dir_change(LEFT_JOYSTICK, (x, y))
    left_joystick_dir = (x, y)

def right_joystick(x: float, y: float):
    global right_joystick_dir
    gamepad.right_joystick_float(x, y)
    gamepad.update()
    if right_joystick_dir != (x, y):
        vgamepad_event_trigger_joystick_dir_change(RIGHT_JOYSTICK, (x, y))
    right_joystick_dir = (x, y)

def trigger_down(left_or_right: str, power: float = 1):
    global gamepad, button_up_pending_jobs, held_buttons
    button = f"{left_or_right}_trigger"
    if button_up_pending_jobs.get(button):
        cron.cancel(button_up_pending_jobs[button])
    held_buttons.add(button)
    getattr(gamepad, f"{left_or_right}_trigger_float")(power)
    gamepad.update()
    vgamepad_event_trigger_on_button(button, EVENT_BUTTON_HOLD)

def trigger_up(left_or_right: str):
    global button_up_pending_jobs
    button = f"{left_or_right}_trigger"
    gamepad.left_trigger_float(0)
    gamepad.update()
    vgamepad_event_trigger_on_button(button, EVENT_BUTTON_RELEASE)
    button_up_pending_jobs[button] = None
    held_buttons.remove(button)

def trigger_toggle(left_or_right: str, power: float = 1):
    if f"{left_or_right}_trigger" in held_buttons:
        trigger_up(left_or_right)
    else:
        trigger_down(left_or_right, power)

def trigger(left_or_right: str, hold: int = None, down: bool = None, up: bool = None, power: float = 1):
    if down:
        trigger_down(left_or_right, power)
    elif up:
        trigger_up(left_or_right)
    elif hold:
        trigger_down(left_or_right, power)
        button_up_pending_jobs[f"{left_or_right}_trigger"] = cron.after(f"{hold}ms", lambda: trigger_up(left_or_right))
    else:
        trigger_toggle(left_or_right, power)

def vgamepad_event_register_on_button(on_button: callable):
    button_event_subscribers.append(on_button)

def vgamepad_event_unregister_on_button(on_button: callable):
    button_event_subscribers.remove(on_button)

def vgamepad_event_trigger_on_button(button: str, state: str):
    print(f"button: {button}, state: {state}")
    for subscriber in button_event_subscribers:
        subscriber(button, state)

def vgamepad_event_register_joystick_dir_change(on_dpad_dir_change: callable):
    dpad_dir_change_event_subscribers.append(on_dpad_dir_change)

def vgamepad_event_unregister_joystick_dir_change(on_dpad_dir_change: callable):
    dpad_dir_change_event_subscribers.remove(on_dpad_dir_change)

def vgamepad_event_trigger_joystick_dir_change(joystick: str, coords: tuple):
    print(f"joystick: {joystick}, coords: {coords}")
    for subscriber in dpad_dir_change_event_subscribers:
        subscriber(joystick, coords)

def vgamepad_event_unregister_all():
    global button_event_subscribers, dpad_dir_change_event_subscribers
    button_event_subscribers = []
    dpad_dir_change_event_subscribers = []

@mod.action_class
class Actions:
    def vgamepad_enable(): """vgamepad enable. Must be done before vgamepad inputs will work."""; vgamepad_enable()
    def vgamepad_disable(): """vgamepad disable"""; vgamepad_disable()
    def vgamepad_button(button: str, hold: int = None, down: bool = None, up: bool = None):
        """
        vgamepad button

        **values:** a, b, x, y, dpad_up, dpad_down, dpad_left, dpad_right,
        left_shoulder, right_shoulder, left_thumb, right_thumb, start, back, guide
        """
        vgamepad_button(button, hold, down, up)
    def vgamepad_button_down(button: str): """vgamepad button down"""; vgamepad_button_down(button)
    def vgamepad_button_up(button: str): """vgamepad button up"""; vgamepad_button_up(button)
    def vgamepad_button_hold(button: str, hold: int): """vgamepad button hold"""; vgamepad_button(button, hold)
    def vgamepad_left_trigger(power: int = 1, hold: int = None, down: bool = None, up: bool = None): """left trigger"""; trigger("left", hold, down, up, power)
    def vgamepad_right_trigger(power: int = 1, hold: int = None, down: bool = None, up: bool = None): """right trigger"""; trigger("right", hold, down, up, power)
    def vgamepad_left_joystick(x: float, y: float): """left joystick"""; left_joystick(x, y)
    def vgamepad_right_joystick(x: float, y: float): """right joystick"""; right_joystick(x, y)
    def vgamepad_stopper(): """stop movement"""; vgamepad_stopper()
    def vgamepad_event_register_on_button(on_button: callable): """vgamepad event register on button"""; vgamepad_event_register_on_button(on_button)
    def vgamepad_event_unregister_on_button(on_button: callable): """vgamepad event unregister on button"""; vgamepad_event_unregister_on_button(on_button)
    def vgamepad_event_register_joystick_dir_change(on_dpad_dir_change: callable): """vgamepad event register on dpad dir change"""; vgamepad_event_register_joystick_dir_change(on_dpad_dir_change)
    def vgamepad_event_unregister_joystick_dir_change(on_dpad_dir_change: callable): """vgamepad event unregister on dpad dir change"""; vgamepad_event_unregister_joystick_dir_change(on_dpad_dir_change)
    def vgamepad_event_unregister_all(): """vgamepad event unregister all"""; vgamepad_event_unregister_all()
