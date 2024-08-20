from talon import actions, Module
from typing import Union, Any
from dataclasses import dataclass
from .game_core import event_subscribers

mod = Module()

@dataclass
class GameXboxEvent:
    subject: str
    type: str
    value: Any

xbox_power = {
    "left_stick": 1,
    "right_stick": 1,
    "left_trigger": 1,
    "right_trigger": 1,
}

xbox_dir_hold_left_analog_dir_map = {
    "up": lambda power: actions.user.vgamepad_left_joystick(0, power),
    "down": lambda power: actions.user.vgamepad_left_joystick(0, -power),
    "left": lambda power: actions.user.vgamepad_left_joystick(-power, 0),
    "right": lambda power: actions.user.vgamepad_left_joystick(power, 0),
}

xbox_dir_hold_right_analog_dir_map = {
    "up": lambda power: actions.user.vgamepad_right_joystick(0, power),
    "down": lambda power: actions.user.vgamepad_right_joystick(0, -power),
    "left": lambda power: actions.user.vgamepad_right_joystick(-power, 0),
    "right": lambda power: actions.user.vgamepad_right_joystick(power, 0),
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
    "lt": "left_trigger",
    "rt": "right_trigger",
    "l1": "left_shoulder",
    "r1": "right_shoulder",
    "l2": "left_trigger",
    "r2": "right_trigger",
    "l3": "left_thumb",
    "r3": "right_thumb",
    "left_shoulder": "left_shoulder",
    "right_shoulder": "right_shoulder",
    "left_thumb": "left_thumb",
    "right_thumb": "right_thumb",
    "left_trigger": "left_trigger",
    "right_trigger": "right_trigger",
    "start": "start",
    "back": "back",
    "guide": "guide",
}

def xbox_dir_hold_left_analog(dir: str, power: float = None):
    """Hold a left analog direction"""
    xbox_dir_hold_left_analog_dir_map[dir](power or xbox_power["left_stick"])

def xbox_dir_hold_right_analog(dir: str, power: float = None):
    """Hold a right analog direction"""
    xbox_dir_hold_right_analog_dir_map[dir](power or xbox_power["right_stick"])

def xbox_dir_hold_dpad(dir: str):
    """Hold a dpad direction"""
    actions.user.vgamepad_button("dpad_up", up=True)
    actions.user.vgamepad_button("dpad_down", up=True)
    actions.user.vgamepad_button("dpad_left", up=True)
    actions.user.vgamepad_button("dpad_right", up=True)
    actions.user.vgamepad_button(f"dpad_{dir}", down=True)

def xbox_set_power(subject: str, power: Union[str, int, float]):
    power = float(power)
    if subject not in xbox_power:
        raise ValueError(f"xbox_set_power subject must be one of {xbox_power.keys()}. Got {subject}")
    if power < 0 or power > 1:
        raise ValueError(f"xbox_set_power power must be between 0 and 1.0. Got {power}")
    xbox_power[subject] = power
    actions.user.game_event_trigger_on_xbox_gamepad_event(subject, "power", power)

def xbox_button(button: str, hold: int = None, down: bool = None, up: bool = None):
    button = xbox_button_map[button]
    if button in ["left_trigger", "right_trigger"]:
        getattr(actions.user, f"game_xbox_{button}")()
    else:
        actions.user.vgamepad_button(button, hold, down, up)

def xbox_button_hold(button: str, hold: int = None):
    if hold:
        xbox_button(button, hold=hold)
    else:
        xbox_button(button, down=True)

@mod.action_class
class Actions:
    def game_event_register_on_xbox_gamepad_event(callback: callable):
        """
        ```
        def on_gamepad_event(event: Any):
            print(event.subject, event.event_type, event.value)

        actions.user.game_event_register_on_xbox_gamepad_event(on_gamepad_event)
        ```
        """
        global event_subscribers
        if "on_xbox" not in event_subscribers:
            event_subscribers["on_xbox"] = []
        event_subscribers["on_xbox"].append(callback)

    def game_event_unregister_on_xbox_gamepad_event(callback: callable):
        """
        Unregister a callback for a specific game event.
        """
        global event_subscribers
        if "on_xbox" in event_subscribers:
            event_subscribers["on_xbox"].remove(callback)
            if not event_subscribers["on_xbox"]:
                del event_subscribers["on_xbox"]

    def game_event_trigger_on_xbox_gamepad_event(subject: str, type: str, value: Any):
        """
        Trigger an event and call all registered callbacks.
        """
        global event_subscribers
        if "on_xbox" in event_subscribers:
            for callback in event_subscribers["on_xbox"]:
                callback(GameXboxEvent(subject, type, value))