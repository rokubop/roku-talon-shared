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
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()

def vgamepad_disable():
    global gamepad
    del gamepad

def vgamepad_button_down(button: str):
    button = button_map[button]
    held_buttons.add(button)
    gamepad.press_button(button=button)
    gamepad.update()
    vgamepad_event_trigger_on_button(button, EVENT_BUTTON_HOLD)

def vgamepad_button_up(button: str):
    button = button_map[button]
    held_buttons.remove(button)
    gamepad.release_button(button=button)
    gamepad.update()
    vgamepad_event_trigger_on_button(button, EVENT_BUTTON_RELEASE)

def vgamepad_button_press(button: str):
    vgamepad_button_down(button)
    cron.after(0.2, vgamepad_button_up, button)

def vgamepad_button(button: str, hold: int = None, down: bool = None, up: bool = None):
    if down:
        vgamepad_button_down(button)
    elif up:
        vgamepad_button_up(button)
    elif hold:
        vgamepad_button_down(button)
        cron.after(hold, vgamepad_button_up, button)
    else:
        vgamepad_button_press(button)

def left_joystick(x: float, y: float):
    global left_joystick_dir
    gamepad.left_joystick_float(x, y)
    gamepad.update()
    if left_joystick_dir != (x, y):
        vgamepad_event_trigger_on_dpad_dir_change(LEFT_JOYSTICK, (x, y))
    left_joystick_dir = (x, y)

def right_joystick(x: float, y: float):
    global right_joystick_dir
    gamepad.right_joystick_float(x, y)
    gamepad.update()
    if right_joystick_dir != (x, y):
        vgamepad_event_trigger_on_dpad_dir_change(RIGHT_JOYSTICK, (x, y))
    right_joystick_dir = (x, y)

def vgamepad_event_register_on_button(on_button: callable):
    button_event_subscribers.append(on_button)

def vgamepad_event_unregister_on_button(on_button: callable):
    button_event_subscribers.remove(on_button)

def vgamepad_event_trigger_on_button(button: str, state: str):
    for subscriber in button_event_subscribers:
        subscriber(button, state)

def vgamepad_event_register_on_dpad_dir_change(on_dpad_dir_change: callable):
    dpad_dir_change_event_subscribers.append(on_dpad_dir_change)

def vgamepad_event_unregister_on_dpad_dir_change(on_dpad_dir_change: callable):
    dpad_dir_change_event_subscribers.remove(on_dpad_dir_change)

def vgamepad_event_trigger_on_dpad_dir_change(joystick: str, coords: tuple):
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
    def vgamepad_button(button: str, hold: int = None, down: bool = None, up: bool = None): """vgamepad button"""; vgamepad_button(button, hold, down, up)
    def vgamepad_a(hold: int = None, down: bool = None, up: bool = None): """vgamepad a"""; vgamepad_button("a", hold, down, up)
    def vgamepad_b(hold: int = None, down: bool = None, up: bool = None): """vgamepad b"""; vgamepad_button("b", hold, down, up)
    def vgamepad_x(hold: int = None, down: bool = None, up: bool = None): """vgamepad x"""; vgamepad_button("x", hold, down, up)
    def vgamepad_y(hold: int = None, down: bool = None, up: bool = None): """vgamepad y"""; vgamepad_button("y", hold, down, up)
    def vgamepad_dpad_up(hold: int = None, down: bool = None, up: bool = None): """vgamepad dpad up"""; vgamepad_button("dpad_up", hold, down, up)
    def vgamepad_dpad_down(hold: int = None, down: bool = None, up: bool = None): """vgamepad dpad down"""; vgamepad_button("dpad_down", hold, down, up)
    def vgamepad_dpad_left(hold: int = None, down: bool = None, up: bool = None): """vgamepad dpad left"""; vgamepad_button("dpad_left", hold, down, up)
    def vgamepad_dpad_right(hold: int = None, down: bool = None, up: bool = None): """vgamepad dpad right"""; vgamepad_button("dpad_right", hold, down, up)
    def vgamepad_left_shoulder(hold: int = None, down: bool = None, up: bool = None): """vgamepad left shoulder"""; vgamepad_button("left_shoulder", hold, down, up)
    def vgamepad_right_shoulder(hold: int = None, down: bool = None, up: bool = None): """vgamepad right shoulder"""; vgamepad_button("right_shoulder", hold, down, up)
    def vgamepad_left_thumb(hold: int = None, down: bool = None, up: bool = None): """vgamepad left thumb"""; vgamepad_button("left_thumb", hold, down, up)
    def vgamepad_right_thumb(hold: int = None, down: bool = None, up: bool = None): """vgamepad right thumb"""; vgamepad_button("right_thumb", hold, down, up)
    def vgamepad_start(hold: int = None, down: bool = None, up: bool = None): """vgamepad start"""; vgamepad_button("start", hold, down, up)
    def vgamepad_back(hold: int = None, down: bool = None, up: bool = None): """vgamepad back"""; vgamepad_button("back", hold, down, up)
    def vgamepad_guide(hold: int = None, down: bool = None, up: bool = None): """vgamepad guide"""; vgamepad_button("guide", hold, down, up)
    def vgamepad_left_joystick(x: float, y: float): """left joystick"""; left_joystick(x, y)
    def vgamepad_left_joystick_dir_left(power: int = 1): """left joystick"""; left_joystick(-power, 0)
    def vgamepad_left_joystick_dir_right(power: int = 1): """left joystick"""; left_joystick(power, 0)
    def vgamepad_left_joystick_dir_up(power: int = 1): """left joystick"""; left_joystick(0, -power)
    def vgamepad_left_joystick_dir_down(power: int = 1): """left joystick"""; left_joystick(0, power)
    def vgamepad_right_joystick(x: float, y: float): """right joystick"""; right_joystick(x, y)
    def vgamepad_right_joystick_dir_left(power: int = 1): """right joystick"""; right_joystick(-power, 0)
    def vgamepad_right_joystick_dir_right(power: int = 1): """right joystick"""; right_joystick(power, 0)
    def vgamepad_right_joystick_dir_up(power: int = 1): """right joystick"""; right_joystick(0, -power)
    def vgamepad_right_joystick_dir_down(power: int = 1): """right joystick"""; right_joystick(0, power)
    def vgamepad_joystick_stop(): """joystick stop"""; left_joystick(0, 0); right_joystick(0, 0)
    def vgamepad_event_register_on_button(on_button: callable): """vgamepad event register on button"""; vgamepad_event_register_on_button(on_button)
    def vgamepad_event_unregister_on_button(on_button: callable): """vgamepad event unregister on button"""; vgamepad_event_unregister_on_button(on_button)
    def vgamepad_event_register_on_dpad_dir_change(on_dpad_dir_change: callable): """vgamepad event register on dpad dir change"""; vgamepad_event_register_on_dpad_dir_change(on_dpad_dir_change)
    def vgamepad_event_unregister_on_dpad_dir_change(on_dpad_dir_change: callable): """vgamepad event unregister on dpad dir change"""; vgamepad_event_unregister_on_dpad_dir_change(on_dpad_dir_change)
    def vgamepad_event_unregister_all(): """vgamepad event unregister all"""; vgamepad_event_unregister_all()
