from talon import Module, Context, actions, noise, speech_system
from dataclasses import dataclass
from typing import Optional, Literal
from .dynamic_noises_ui import (
    dynamic_noises_ui_element,
    show_tester_ui,
    hide_tester_ui
)
import time

mod = Module()
ctx = Context()

mod.list("dynamic_noise_mode", desc="Dynamic noise modes")

_dynamic_noises_enabled = False
_use_talon_noises = False
_use_speech_capture = False
_talon_noise_pop_init = False
_talon_noise_hiss_init = False
_speech_capture_enabled = False
event_subscribers = []
_talon_noises = ["pop", "hiss"]
EVENT_TYPE_CHANGE = "change"
EVENT_TYPE_ACTION = "action"
EVENT_TYPE_ACTION_STOP = "action_stop"
change_event_history = []

@dataclass
class DynamicActionEvent:
    type: Literal["change", "action", "action_stop"]
    name: str
    action_name: str
    error: bool = False

@dataclass
class DynamicActionCallback:
    name: str
    action: callable = lambda: None
    action_stop: Optional[callable] = lambda: None
    debounce: Optional[int] = None
    debounce_stop: Optional[int] = None
    throttle: Optional[int] = None

class DynamicAction:
    name: str
    current: DynamicActionCallback = None
    history: list[DynamicActionCallback]
    default: DynamicActionCallback = None
    alias: str = None

    def __init__(
        self,
        name: str,
        default_cb: DynamicActionCallback = None,
        alias: str = None
    ):
        self.name = name
        self.history = []
        self.alias = alias or name
        if default_cb:
            self.default = default_cb
            self.set(default_cb)

    def revert(self):
        if self.history:
            self.current = self.history.pop()

    def reset(self):
        self.current = self.default
        self.history = [self.default]

    def set(self, dynamic_action_callback: DynamicActionCallback):
        if self.current:
            self.history.append(self.current)
        self.history = self.history[-5:]
        self.current = dynamic_action_callback

        dynamic_noises_event_trigger(
            DynamicActionEvent(
                EVENT_TYPE_CHANGE,
                self.name,
                dynamic_action_callback.name,
            )
        )

    def set_default(self, dynamic_action_callback: DynamicActionCallback):
        self.default = dynamic_action_callback
        self.set(dynamic_action_callback)

    def execute(self):
        if self.current and self.current.action:
            try:
                self.current.action()
                dynamic_noises_event_trigger(
                    DynamicActionEvent(
                        EVENT_TYPE_ACTION,
                        self.name,
                        self.current.name,
                    )
                )
            except Exception as e:
                dynamic_noises_event_trigger(
                    DynamicActionEvent(
                        EVENT_TYPE_ACTION,
                        self.name,
                        self.current.name,
                        error=True
                    )
                )

    def execute_stop(self):
        if self.current and self.current.action_stop:
            self.current.action_stop()
            dynamic_noises_event_trigger(
                DynamicActionEvent(
                    EVENT_TYPE_ACTION_STOP,
                    self.name,
                    self.current.name,
                )
            )

@dataclass
class ChangeEventHistory:
    change_event: DynamicActionEvent
    timestamp: float

dynamic_noises_state: dict[str, DynamicAction] = {}

def separate_base_and_qualifier(name: str):
    if "_" in name:
        return name.split("_", 1)
    elif ":" in name:
        return name.split(":", 1)
    else:
        return name, ""

def dynamic_noises_set_class(
    name: str,
    dynamic_action_callback: DynamicActionCallback,
    default: bool = False,
    alias: str = None
):
    """Set a dynamic action"""
    global dynamic_noises_state
    if name not in dynamic_noises_state:
        dynamic_noises_state[name] = DynamicAction(name, alias=alias)
    if default:
        dynamic_noises_state[name].set_default(dynamic_action_callback)
    else:
        dynamic_noises_state[name].set(dynamic_action_callback)

def dynamic_noises_trigger(name: str):
    """Execute a dynamic action"""
    global dynamic_noises_state
    base_name, qualifier = separate_base_and_qualifier(name)
    if base_name in dynamic_noises_state:
        if qualifier == "stop":
            dynamic_noises_state[base_name].execute_stop()
        else:
            dynamic_noises_state[base_name].execute()
    else:
        print(f"Dynamic action {name} not found")

def noise_pop(_):
    dynamic_noises_trigger("pop")

def noise_hiss(is_active):
    if is_active:
        dynamic_noises_trigger("hiss")
    else:
        dynamic_noises_trigger("hiss_stop")

def spoken_word_is_dynamic_action(word):
    return (_use_talon_noises and word in _talon_noises) or word in dynamic_noises_state or any(
        dynamic_action.alias == word
        for dynamic_action in dynamic_noises_state.values()
    )

def on_phrase(d):
    parsed = d.get("parsed")
    if parsed:
        words = parsed._unmapped
        if words and len(words) > 1 and spoken_word_is_dynamic_action(words[0]):
            dynamic_action_name, words = words[0], words[1:]
            action_phrase = " ".join(words)
            cb = DynamicActionCallback(
                name=action_phrase,
                action=lambda: actions.mimic(action_phrase),
                action_stop=lambda: None
            )
            dynamic_noises_set_class(dynamic_action_name, cb)

def start_speech_capture():
    global _speech_capture_enabled
    if not _speech_capture_enabled:
        _speech_capture_enabled = True
        speech_system.register("pre:phrase", on_phrase)

def stop_speech_capture():
    global _speech_capture_enabled
    if _speech_capture_enabled:
        speech_system.unregister("pre:phrase", on_phrase)
        _speech_capture_enabled = False

def dynamic_noises_event_register(on_event: callable):
    if on_event not in event_subscribers:
        event_subscribers.append(on_event)

    if change_event_history:
        for h in change_event_history:
            # if a change event happened in the last 5 seconds
            # then it was probably intended to be received,
            # so trigger it for the new subscriber
            if h.timestamp > time.perf_counter() - 5:
                on_event(h.change_event)

def dynamic_noises_event_unregister(on_event: callable):
    if on_event in event_subscribers:
        event_subscribers.remove(on_event)

def dynamic_noises_event_trigger(event: DynamicActionEvent):
    global change_event_history
    for subscriber in event_subscribers:
        subscriber(event)

    if event.type == EVENT_TYPE_CHANGE:
        # what about garbage collection?
        change_event_history.append(ChangeEventHistory(event, time.perf_counter()))
        change_event_history = change_event_history[-5:]

def dynamic_noises_set(
    name: str,
    action_name: str,
    action: callable,
    action_stop: callable = lambda: None,
    debounce_ms: int = None,
    debounce_stop_ms: int = None,
    throttle_ms: int = None,
    default: bool = False,
    phrase: str = None,
    alias: str = None
):
    global _talon_noise_pop_init, _talon_noise_hiss_init
    callback = None

    if not _dynamic_noises_enabled:
        print("dynamic noises not enabled. Enable using actions.user.dynamic_noises_enable()")
        return

    # if action[1] is None or not callable(action[1]):
    #     raise ValueError(
    #         f"\ndynamic_noises_set: action for '{name}' must be a callable (function or lambda).\n\n"
    #         f"Valid examples:\n"
    #         f'dynamic_noises_set_pop("jump", lambda: actions.key("space"))\n'
    #         f'dynamic_noises_set_hiss("jump", actions.user.game_mouse_click)\n'
    #         f'dynamic_noises_set("pop", "jump", lambda: actions.key("space"))\n\n'
    #         f"Invalid examples:\n"
    #         f'dynamic_noises_set_pop("jump", actions.key("space"))\n'
    #         f'dynamic_noises_set_hiss("jump", actions.key("space"))\n'
    #         f'dynamic_noises_set("pop", "jump", actions.user.game_mouse_click())\n'
    #     )

    if _use_talon_noises:
        if  name == "pop" and not _talon_noise_pop_init:
            _talon_noise_pop_init = True
            noise.register("pop", noise_pop)
        elif name == "hiss" and not _talon_noise_hiss_init:
            _talon_noise_hiss_init = True
            noise.register("hiss", noise_hiss)

    if phrase:
        callback = DynamicActionCallback(
            name=phrase,
            action=lambda: actions.mimic(phrase),
            action_stop=lambda: None
        )
    else:
        callback = DynamicActionCallback(
            name=action_name,
            action=action,
            action_stop=action_stop,
            debounce=debounce_ms,
            debounce_stop=debounce_stop_ms,
            throttle=throttle_ms,
        )
    dynamic_noises_set_class(name, callback, default, alias)

def dynamic_noises_use_mode(mode: str):
    dynamic_noises = actions.user.dynamic_noises()
    if not dynamic_noises:
        raise ValueError(f"Tried to set noise mode '{mode}' but def dynamic_noises() is not defined. Define def dynamic_noises in your ctx.")

    if not mode in dynamic_noises:
        raise ValueError(f"Noise mode '{mode}' not found in def dynamic_noises(). Available modes: {list(dynamic_noises.keys())}")

    for noise, action in dynamic_noises[mode].items():
        if noise == "on_enable":
            action()
            continue

        if not isinstance(action, (list, tuple)):
            raise ValueError(f"Action for noise '{noise}' is not a tuple or list: {action}")

        if len(action) != 2:
            raise ValueError(f"Action tuple for noise '{noise}' does not have exactly 2 elements: {action}")

        if not callable(action[1]):
            raise ValueError(
                f"\nThe action for '{noise}' must be a callable (function or lambda).\n\n"
                f"Valid examples:\n"
                f'"pop": ("E", lambda: actions.user.game_key("e")),\n'
                f'"pop": ("L click", actions.user.game_mouse_click_left),\n\n'
                f"Invalid examples:\n"
                f'"pop": ("E", actions.user.game_key("e")),\n'
                f'"pop": ("L click", actions.user.game_mouse_click_left())\n'
            )

        dynamic_noises_set(noise, action_name=action[0], action=action[1])

def dynamic_noises_enable(
    talon_noises: bool = True,
    speech_capture: bool = True
):
    global _dynamic_noises_enabled
    global _use_talon_noises
    global _use_speech_capture
    global _talon_noise_hiss_init
    global _talon_noise_pop_init

    if not _dynamic_noises_enabled:
        _dynamic_noises_enabled = True
        _talon_noise_pop_init = False
        _talon_noise_hiss_init = False
        _use_talon_noises = talon_noises
        _use_speech_capture = speech_capture
        if _use_talon_noises:
            ctx.tags = ["user.dynamic_noises_talon_noise_override"]

        if _use_speech_capture:
            start_speech_capture()

        dynamic_noises = actions.user.dynamic_noises()
        if dynamic_noises:
            if not "default" in dynamic_noises:
                raise ValueError(
                    f'\ndef dynamic_noises should must contain a "default" mode\n\n'
                    f"Example:\n"
                    f"def dynamic_noises():\n"
                    f"    return {{\n"
                    f'        "default": {{\n'
                    f'            "pop": ("click", actions.mouse_click),\n'
                    f'            "hiss": ("scroll down", lambda: actions.mouse_scroll(50))\n'
                    f"        }},\n"
                    f'        "repeater": {{\n'
                    f'            "pop": ("repeat", actions.core.repeat_phrase),\n'
                    f'            "hiss": ("None", actions.skip)\n'
                    f"        }}\n"
                    f"    }}\n"
                )

            dynamic_noises_use_mode("default")
            ctx.lists["user.dynamic_noise_mode"] = list(dynamic_noises.keys())

def dynamic_noises_disable():
    global _dynamic_noises_enabled
    global _talon_noise_pop_init
    global _talon_noise_hiss_init
    global dynamic_noises_state

    if _talon_noise_pop_init:
        noise.unregister("pop", noise_pop)
        _talon_noise_pop_init = False

    if _talon_noise_hiss_init:
        noise.unregister("hiss", noise_hiss)
        _talon_noise_hiss_init = False

    ctx.tags = []
    ctx.lists["user.dynamic_noise_mode"] = []
    _dynamic_noises_enabled = False
    dynamic_noises_state.clear()
    stop_speech_capture()

@mod.action_class
class Actions:
    def dynamic_noises_enable(
        talon_noises: bool = True,
        speech_capture: bool = True
    ):
        """
        Enable dynamic noises - Do this before setting dynamic noises

        - `talon_noises`: when "pop" or "hiss" is referenced,
        it uses Talon's `noise.register`. Set this to `False` if
        you want to manually trigger "pop" or "hiss" using parrot
        noises to trigger `dynamic_noises_trigger("pop")` for example.

        - `speech_capture`: Allows you to set dynamic noises
        by saying "{noise name} {any phrase}"
        """
        dynamic_noises_enable(talon_noises, speech_capture)

    def dynamic_noises_disable():
        """
        Unregister dynamic noises and restore Talon's default
        noises if applicable.
        """
        dynamic_noises_disable()

    def dynamic_noises_set(
        name: str,
        action_name: str,
        action: callable,
        action_stop: callable = lambda: None,
        debounce_ms: int = None,
        debounce_stop_ms: int = None,
        throttle_ms: int = None,
        default: bool = False,
        phrase: str = None,
        alias: str = None
    ):
        """
        Update a dynamic action with a new action
        Example:
        ```py
        actions.user.dynamic_noises_set(
            "pop",
            "jump",
            lambda: actions.key("space"),
        )
        ```
        ```py
        actions.user.dynamic_noises_set(
            "hiss",
            "jump",
            lambda: actions.key("space:down"),
            lambda: actions.key("space:up"),
        )
        ```
        """
        dynamic_noises_set(name, action_name, action, action_stop, debounce_ms, debounce_stop_ms, throttle_ms, default, phrase, alias)

    def dynamic_noises_set_hiss(
        action_name: str,
        action: callable,
        action_stop: callable = lambda: None,
        debounce_ms: int = None,
        debounce_stop_ms: int = None,
        throttle_ms: int = None,
        default: bool = False,
        phrase: str = None,
        alias: str = None
    ):
        """Set hiss dynamic action"""
        dynamic_noises_set("hiss", action_name, action, action_stop, debounce_ms, debounce_stop_ms, throttle_ms, default, phrase, alias)

    def dynamic_noises_set_pop(
        action_name: str,
        action: callable,
        action_stop: callable = lambda: None,
        debounce_ms: int = None,
        debounce_stop_ms: int = None,
        throttle_ms: int = None,
        default: bool = False,
        phrase: str = None,
        alias: str = None
    ):
        """Set pop dynamic action"""
        dynamic_noises_set("pop", action_name, action, action_stop, debounce_ms, debounce_stop_ms, throttle_ms, default, phrase, alias)

    def dynamic_noises_trigger(name: str):
        """Execute a dynamic action e.g. `actions.user.dynamic_noises_trigger("pop")`"""
        dynamic_noises_trigger(name)

    def dynamic_noises_event_register(on_event: callable):
        """
        Register callback event for dynamic_noises. Will trigger
        when a dynamic action is changed or executed, or stopped.

        ```py
        def on_event(event):
            print(event.type, event.name, event.action_name)
        actions.user.dynamic_noises_event_register(on_event)
        ```
        """
        dynamic_noises_event_register(on_event)

    def dynamic_noises_event_unregister(on_event: callable):
        """
        Unregister event set by actions.user.dynamic_noises_event_register
        """
        dynamic_noises_event_unregister(on_event)

    def dynamic_noises_event_unregister_all():
        """
        Unregister all dynamic noises events
        """
        global event_subscribers
        event_subscribers = []

    def dynamic_noises_tester_toggle(enable: bool = None):
        """
        Toggle noise tester with UI
        """
        global _dynamic_noises_enabled, _use_talon_noises, _use_speech_capture
        if _dynamic_noises_enabled or enable == False:
            print("Disabling dynamic noises")
            dynamic_noises_disable()
            hide_tester_ui()
        else:
            print("Enabling dynamic noises")
            dynamic_noises_enable()
            actions.user.dynamic_noises_set_pop("click", lambda: actions.mouse_click(0))
            actions.user.dynamic_noises_set_hiss("none", lambda: None)
            show_tester_ui()

    def dynamic_noises_ui_element():
        """
        Show dynamic noises UI
        """
        return dynamic_noises_ui_element()

    def dynamic_noises_use_mode(mode: str):
        """
        Use dynamic noise mode matching your definitions from `def dynamic_noises()`
        """
        dynamic_noises_use_mode(mode)

    def dynamic_noises():
        """
        Return dynamic noise modes
        """
        return {}