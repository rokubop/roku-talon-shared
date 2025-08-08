from talon import Module, actions
from pynput import keyboard

mod = Module()

LEFT_PEDAL_KEY = '*'
MIDDLE_PEDAL_KEY = '-'
RIGHT_PEDAL_KEY = '+'

hold_state = {
    LEFT_PEDAL_KEY: False,
    MIDDLE_PEDAL_KEY: False,
    RIGHT_PEDAL_KEY: False
}

def on_pynput_press(key):
    try:
        if key.char in hold_state and not hold_state[key.char]:
            hold_state[key.char] = True
            if key.char == LEFT_PEDAL_KEY:
                actions.user.pynput_pedal_left_down()
            elif key.char == MIDDLE_PEDAL_KEY:
                actions.user.pynput_pedal_middle_down()
            elif key.char == RIGHT_PEDAL_KEY:
                actions.user.pynput_pedal_right_down()
    except AttributeError:
        pass

def on_pynput_release(key):
    try:
        if key.char in hold_state:
            if key.char == LEFT_PEDAL_KEY:
                actions.user.pynput_pedal_left_up()
            elif key.char == MIDDLE_PEDAL_KEY:
                actions.user.pynput_pedal_middle_up()
            elif key.char == RIGHT_PEDAL_KEY:
                actions.user.pynput_pedal_right_up()
            hold_state[key.char] = False
    except AttributeError:
        pass

@mod.action_class
class Actions:
    def pynput_pedal_enable():
        """Enable the pynput pedal."""
        global listener
        listener = keyboard.Listener(
            on_press=on_pynput_press,
            on_release=on_pynput_release
        )
        listener.start()

    def pynput_pedal_disable():
        """Disable the pynput pedal."""
        global listener
        if listener:
            listener.stop()
            listener = None

    def pynput_pedal_left_down():
        """Define your left pedal down action in a ctx"""
        actions.skip()

    def pynput_pedal_left_up():
        """Define your left pedal up action in a ctx"""
        actions.skip()

    def pynput_pedal_middle_down():
        """Define your middle pedal down action in a ctx"""
        actions.skip()

    def pynput_pedal_middle_up():
        """Define your middle pedal up action in a ctx"""
        actions.skip()

    def pynput_pedal_right_down():
        """Define your right pedal down action in a ctx"""
        actions.skip()

    def pynput_pedal_right_up():
        """Define your right pedal up action in a ctx"""
        actions.skip()