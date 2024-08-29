from dataclasses import dataclass
from typing import Any, Optional
from talon import Module

mod = Module()

EVENT_ON_KEY = "on_key"
EVENT_KEY_PRESS = "press"
EVENT_KEY_HOLD = "hold"
EVENT_KEY_RELEASE = "release"

EVENT_ON_MOUSE = "on_mouse"
EVENT_MOUSE_CLICK = "click"
EVENT_MOUSE_HOLD = "hold"
EVENT_MOUSE_RELEASE = "release"

EVENT_ON_GAME_MODE = "on_game_mode_changed"
EVENT_GAME_MODE_DISABLED = "disabled"
EVENT_GAME_MODE_ENABLED = "enabled"

EVENT_ON_XBOX = "on_xbox"
EVENT_XBOX_HOLD = "hold"
EVENT_XBOX_RELEASE = "release"
EVENT_XBOX_DIR_CHANGE = "dir_change"
EVENT_XBOX_GEAR_CHANGE = "gear_change"

EVENT_PREFERRED_DIR_MODE_CHANGE = "preferred_dir_mode_change"

SUBJECT_LEFT_STICK = "left_stick"
SUBJECT_RIGHT_STICK = "right_stick"
SUBJECT_LEFT_TRIGGER = "left_trigger"
SUBJECT_RIGHT_TRIGGER = "right_trigger"
SUBJECT_DPAD = "dpad"

class GameEvent:
    def __init__(self):
        self.subscribers = []

    def register(self, callback):
        self.subscribers.append(callback)

    def unregister(self, callback):
        self.subscribers.remove(callback)

    def unregister_all(self):
        self.subscribers = []

class GameEventOnGameMode(GameEvent):
    def __init__(self):
        super().__init__()
        self.event_name = EVENT_ON_GAME_MODE
        self.locked_subscribers = []

    def register_locked(self, callback):
        self.locked_subscribers.append(callback)

    def fire_enabled(self):
        for callback in self.subscribers + self.locked_subscribers:
            callback(EVENT_GAME_MODE_ENABLED)

    def fire_disabled(self):
        for callback in self.subscribers + self.locked_subscribers:
            callback(EVENT_GAME_MODE_DISABLED)

class GameEventOnKey(GameEvent):
    def __init__(self):
        super().__init__()
        self.event_name = EVENT_ON_KEY

    def _fire(self, key: str, event_type: str):
        for callback in self.subscribers:
            callback(key, event_type)

    def fire_press(self, key: str): self._fire(key, EVENT_KEY_PRESS)
    def fire_hold(self, key: str): self._fire(key, EVENT_KEY_HOLD)
    def fire_release(self, key: str): self._fire(key, EVENT_KEY_RELEASE)

class GameEventOnMouse(GameEvent):
    def __init__(self):
        super().__init__()
        self.event_name = EVENT_ON_MOUSE

    def _fire(self, button: str, event_type: str):
        for callback in self.subscribers:
            callback(button, event_type)

    def fire_click(self, button): self._fire(button, EVENT_MOUSE_CLICK)
    def fire_hold(self, button): self._fire(button, EVENT_MOUSE_HOLD)
    def fire_release(self, button): self._fire(button, EVENT_MOUSE_RELEASE)

@dataclass
class GameXboxEvent:
    subject: str # specific button or left_stick, right_stick, left_trigger, right_trigger
    type: str
    value: Optional[Any]

class GameEventOnXbox(GameEvent):
    def __init__(self):
        super().__init__()
        self.event_name = EVENT_ON_XBOX

    def _fire(self, subject: str, type: str, value: Any = None):
        """
        Subject: the specific button or left_stick, right_stick, left_trigger, right_trigger
        Event type: hold, release, dir_change, gear_change
        Value: Optional value for the event
        """
        # print("GameEventOnXbox", self.subscribers, subject, type, value)
        for callback in self.subscribers:
            callback(GameXboxEvent(subject, type, value))

    def fire_left_stick_dir_change(self, xy: tuple[int, int]):
        self._fire(SUBJECT_LEFT_STICK, EVENT_XBOX_DIR_CHANGE, xy)

    def fire_right_stick_dir_change(self, xy: tuple[int, int]):
        self._fire(SUBJECT_RIGHT_STICK, EVENT_XBOX_DIR_CHANGE, xy)

    def fire_dpad_dir_hold_change(self, dir: str):
        self._fire(SUBJECT_DPAD, EVENT_XBOX_DIR_CHANGE, dir)

    def fire_trigger_hold(self, subject: str, gear: dict):
        self._fire(subject, EVENT_XBOX_HOLD, gear)

    def fire_trigger_gear_change(self, subject: str, gear: dict):
        self._fire(subject, EVENT_XBOX_GEAR_CHANGE, gear)

    def fire_button_hold(self, button: str):
        self._fire(button, EVENT_XBOX_HOLD)

    def fire_button_release(self, button: str):
        self._fire(button, EVENT_XBOX_RELEASE)

    def fire_preferred_dir_mode_change(self, subject: str, type: str):
        self._fire(subject, EVENT_PREFERRED_DIR_MODE_CHANGE, type)

event_on_mouse = GameEventOnMouse()
event_on_key = GameEventOnKey()
event_on_game_mode = GameEventOnGameMode()
event_on_xbox = GameEventOnXbox()

def event_unregister_all():
    event_on_mouse.unregister_all()
    event_on_key.unregister_all()
    event_on_game_mode.unregister_all()
    event_on_xbox.unregister_all()

@mod.action_class
class Actions:
    def game_event_register_on_game_mode(callback: callable, locked: bool = False):
        """
        events:
        ```py
        "on_game_mode", lambda state: # enabled/disabled
        ```
        """
        if locked:
            event_on_game_mode.register_locked(callback)
        else:
            event_on_game_mode.register(callback)

    def game_event_unregister_on_game_mode(callback: callable):
        """
        Unregister a callback for a specific game event.
        """
        event_on_game_mode.unregister(callback)

    def game_event_register_on_key(callback: callable):
        """
        events:
        ```py
        "on_key", lambda key, state: # press/hold/release
        ```
        """
        event_on_key.register(callback)

    def game_event_unregister_on_key(callback: callable):
        """
        Unregister a callback for a specific game event.
        """
        event_on_key.unregister(callback)

    def game_event_register_on_mouse(callback: callable):
        """
        events:
        ```py
        "on_mouse", lambda mouse, state: # click/hold/release
        ```
        """
        event_on_mouse.register(callback)

    def game_event_unregister_on_mouse(callback: callable):
        """
        Unregister a callback for a specific game event.
        """
        event_on_mouse.unregister(callback)

    def game_event_unregister_all():
        """Unregister all game events"""
        event_unregister_all()