import sys
from talon import Module, Context, cron

mod, ctx_mac = Module(), Context()
ctx_mac.matches = "os: mac"

button_map = {}
gamepad = None

# not available on macOS
if sys.platform != "darwin":
    import vgamepad as vg

    xbox_button_map = {
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

    button_map = xbox_button_map

def vgamepad_enable():
    global gamepad
    if not gamepad:
        try:
            gamepad = vg.VX360Gamepad()
        except:
            print("""
                Failed to enable vgamepad. Make sure vgamepad is installed to use xbox controller emulation.
                Or delete this folder if you don't need/want this.
                See the README in roku-talon-shared/vgamepad for more information.
            """)

def vgamepad_disable():
    global gamepad
    gamepad = None

def vgamepad_button_hold(button: str):
    if gamepad:
        gamepad.press_button(button_map[button])
        gamepad.update()

def vgamepad_button_release(button: str):
    if gamepad:
        gamepad.release_button(button_map[button])
        gamepad.update()

def left_stick(x: float, y: float):
    if gamepad:
        gamepad.left_joystick_float(x, y)
        gamepad.update()

def right_stick(x: float, y: float):
    if gamepad:
        gamepad.right_joystick_float(x, y)
        gamepad.update()

def left_trigger(power: float):
    if gamepad:
        gamepad.left_trigger_float(power)
        gamepad.update()

def right_trigger(power: float):
    global job
    if gamepad:
        gamepad.right_trigger_float(power)
        gamepad.update()

def dpad_dir_hold(dir: str):
    if gamepad:
        for direction in ["left", "right", "up", "down"]:
            if direction == dir:
                gamepad.press_button(button_map[f"dpad_{direction}"])
            else:
                gamepad.release_button(button_map[f"dpad_{direction}"])
        gamepad.update()

def not_supported():
    print("vgamepad is not supported on macOS.")

@mod.action_class
class Actions:
    def vgamepad_enable(): """vgamepad enable. Required before gamepad actions work."""; vgamepad_enable()
    def vgamepad_disable(): """vgamepad disable"""; vgamepad_disable()
    def vgamepad_button_hold(button: str):
        """
        vgamepad hold button. You must manually release the button with `actions.user.vgamepad_button_release`.

        **values**: "a", "b", "x", "y", "dpad_up", "dpad_down", "dpad_left",
        "dpad_right", "left_shoulder", "right_shoulder", "left_thumb",
        "right_thumb", "start", "back", "guide"
        """
        vgamepad_button_hold(button)
    def vgamepad_button_release(button: str): """vgamepad release button"""; vgamepad_button_release(button)
    def vgamepad_dpad_dir_hold(dir: str): """vgamepad dpad hold dir mutually exclusive - up, down, left, right"""; dpad_dir_hold(dir)
    def vgamepad_left_trigger(power: float): """left trigger"""; left_trigger(power)
    def vgamepad_right_trigger(power: float): """right trigger"""; right_trigger(power)
    def vgamepad_left_stick(x: float, y: float): """left analog stick"""; left_stick(x, y)
    def vgamepad_right_stick(x: float, y: float): """right analog joystick"""; right_stick(x, y)

@ctx_mac.action_class("user")
class MacActions:
    def vgamepad_enable(): not_supported()
    def vgamepad_disable(): not_supported()
    def vgamepad_button_hold(button: str): not_supported()
    def vgamepad_button_release(button: str): not_supported()
    def vgamepad_dpad_dir_hold(dir: str): not_supported()
    def vgamepad_left_trigger(power: float): not_supported()
    def vgamepad_right_trigger(power: float): not_supported()
    def vgamepad_left_stick(x: float, y: float): not_supported()
    def vgamepad_right_stick(x: float, y: float): not_supported()