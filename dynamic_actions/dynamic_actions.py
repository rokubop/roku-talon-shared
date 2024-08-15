from talon import Module, Context, actions, noise, speech_system, ctrl
from dataclasses import dataclass
from typing import Optional, TypedDict

mod = Module()
ctx = Context()

_talon_noise_pop_init = False
_talon_noise_hiss_init = False
_speech_capture_enabled = False

@dataclass
class DynamicActionCallback:
    name: str
    action: callable = lambda: None
    action_stop: Optional[callable] = lambda: None
    debounce: Optional[int] = None
    debounce_stop: Optional[int] = None
    throttle: Optional[int] = None
    once: Optional[bool] = False

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
        actions.user.on_dynamic_action_change(self.name, dynamic_action_callback.name)

    def set_default(self, dynamic_action_callback: DynamicActionCallback):
        self.default = dynamic_action_callback
        self.set(dynamic_action_callback)

    def execute(self):
        if self.current and self.current.action:
            print(self.current.name)
            self.current.action()

    def execute_stop(self):
        if self.current and self.current.action_stop:
            self.current.action_stop()

_dynamic_actions: dict[str, DynamicAction] = {}
_dynamic_actions_aliases: dict[str, str] = {}

def separate_base_and_qualifier(name: str):
    if "_" in name:
        return name.split("_", 1)
    elif ":" in name:
        return name.split(":", 1)
    else:
        return name, ""

def dynamic_action_set(name: str, dynamic_action_callback: DynamicActionCallback):
    """Set a dynamic action"""
    global _dynamic_actions
    if name not in _dynamic_actions:
        _dynamic_actions[name] = DynamicAction(name)
    _dynamic_actions[name].set(dynamic_action_callback)

def dynamic_action(name: str):
    """Execute a dynamic action"""
    global _dynamic_actions
    base_name, qualifier = separate_base_and_qualifier(name)
    if base_name in _dynamic_actions:
        if qualifier == "stop":
            _dynamic_actions[base_name].execute_stop()
        if base_name in _dynamic_actions:
            _dynamic_actions[base_name].execute()
    else:
        print(f"Dynamic action {name} not found")

def dynamic_action_set_default(name: str, dynamic_action_callback: DynamicActionCallback):
    """Set a default dynamic action"""
    global _dynamic_actions
    if name not in _dynamic_actions:
        _dynamic_actions[name] = DynamicAction(name)
    _dynamic_actions[name].set_default(dynamic_action_callback)
    actions.user.on_dynamic_action_change(name, dynamic_action_callback.name)

def dynamic_action_remove(name: str):
    """Remove a dynamic action"""
    global _dynamic_actions
    if name in _dynamic_actions:
        del _dynamic_actions[name]

def dynamic_action_init(
    name: str,
    action_name: str,
    action: callable = lambda: None,
    action_stop: callable = lambda: None,
    debounce_ms: int = None,
    debounce_stop_ms: int = None,
    throttle_ms: int = None,
    once: bool = False,
    alias: str = None
):
    """Init a dynamic action"""
    global _dynamic_actions
    cb = DynamicActionCallback(
        name=action_name,
        action=action,
        action_stop=action_stop,
        debounce=debounce_ms,
        debounce_stop=debounce_stop_ms,
        throttle=throttle_ms,
        once=once
    )
    if name not in _dynamic_actions:
        _dynamic_actions[name] = DynamicAction(name, alias=alias)
    _dynamic_actions[name].reset()
    _dynamic_actions[name].set_default(cb)

def noise_pop(_):
    print("doing dynamic action pop")
    dynamic_action("pop")

def noise_hiss(is_active):
    print("doing dynamic action hiss")
    if is_active:
        dynamic_action("hiss")
    else:
        dynamic_action("hiss_stop")

def spoken_word_is_dynamic_action(word):
    return word in _dynamic_actions or any(
        dynamic_action.alias == word
        for dynamic_action in _dynamic_actions.values()
    )

def on_phrase(d):
    parsed = d.get("parsed")
    if parsed:
        words = parsed._unmapped
        if words and len(words) > 1 and spoken_word_is_dynamic_action(words[0]):
            dynamic_action_word, words = words[0], words[1:]
            action_phrase = " ".join(words)
            cb = DynamicActionCallback(
                name=action_phrase,
                action=lambda: actions.mimic(action_phrase),
                action_stop=lambda: None
            )
            print(f"setting dynamic action {dynamic_action_word} to {action_phrase}")
            dynamic_action_set(dynamic_action_word, cb)

def start_speech_capture():
    global _speech_capture_enabled
    if not _speech_capture_enabled:
        _speech_capture_enabled = True
        speech_system.register("pre:phrase", on_phrase)

def stop_speech_capture():
    global _speech_capture_enabled
    speech_system.unregister("pre:phrase", on_phrase)
    _speech_capture_enabled = False

def test():
    print("test")
    ctrl.mouse_click(button=0, hold=16000)

@mod.action_class
class Actions:
    def dynamic_action(name: str):
        """Execute a dynamic action e.g. `actions.user.dynamic_action("pop")`"""
        dynamic_action(name)

    def dynamic_action_set(
        name: str,
        action_name: str,
        action: callable,
        action_stop: callable = lambda: None,
        debounce_ms: int = None,
        debounce_stop_ms: int = None,
        throttle_ms: int = None,
        once: bool = False
    ):
        """
        Update a dynamic action with a new action
        Example:
        ```py
        actions.user.dynamic_action_set(
            "pop",
            "jump",
            lambda: actions.key("space"),
        )
        ```
        ```py
        actions.user.dynamic_action_set(
            "hiss",
            "jump",
            lambda: actions.key("space:down"),
            lambda: actions.key("space:up"),
        )
        ```
        """
        cb = DynamicActionCallback(
            name=action_name,
            action=action,
            action_stop=action_stop,
            debounce=debounce_ms,
            debounce_stop=debounce_stop_ms,
            throttle=throttle_ms,
            once=once
        )
        dynamic_action_set(name, cb)

    def dynamic_action_set_phrase(
        name: str,
        phrase: str,
        once: bool = False
    ):
        """
        Update a dynamic action using a phrase to mimic
        Example:
        ```py
        actions.user.dynamic_action_set_phrase(
            "pop",
            "again"
        )
        ```
        """
        cb = DynamicActionCallback(
            name=phrase,
            action=lambda: actions.mimic(phrase),
            action_stop=lambda: None
        )
        dynamic_action_set(name, cb)

    def register_dynamic_actions():
        """
        Starts listening for phrases of the dynamic action name
        and will bind the phrase to the action when spoken. Should
        be used for generic commands or parrot noises.

        Use `noise_register_dynamic_action_pop` and `noise_register_dynamic_action_hiss`
        instead for talon noise registration.
        """
        start_speech_capture()

    def unregister_dynamic_actions():
        """
        Stops listening for phrases of the dynamic action name.
        Should be used for generic commands or parrot noises.

        Use `noise_unregister_dynamic_actions` instead for talon noise registration.
        """
        stop_speech_capture()

    def noise_register_dynamic_action_pop(
        action_name: str,
        action: callable,
        once: bool = False,
        alias: str = None
    ):
        """
        Noise register dynamic pop using Talon's noise.register.
        Sets context to disable Talon's default noise callback.
        """
        global _talon_noise_pop_init
        dynamic_action_init(
            "pop",
            action_name,
            action,
            once=once,
            alias=alias
        )
        if not _talon_noise_pop_init:
            noise.register("pop", noise_pop)
            _talon_noise_pop_init = True
            start_speech_capture()
        ctx.tags = ["user.dynamic_actions_talon_noise_override"]

    def noise_register_dynamic_action_hiss(
        action_name: str,
        action: callable = lambda: None,
        action_stop: callable = lambda: None,
        debounce_ms: int = None,
        debounce_stop_ms: int = None,
        throttle_ms: int = None,
        once: bool = False,
        alias: str = None
    ):
        """
        Noise register dynamic hiss using Talon's noise.register.
        Sets context to disable Talon's default noise callback.
        """
        global _talon_noise_hiss_init
        dynamic_action_init(
            "hiss",
            action_name,
            action,
            action_stop,
            debounce_ms,
            debounce_stop_ms,
            throttle_ms,
            once,
            alias
        )
        if not _talon_noise_hiss_init:
            noise.register("hiss", noise_hiss)
            _talon_noise_hiss_init = True
            start_speech_capture()
        ctx.tags = ["user.dynamic_actions_talon_noise_override"]

    def noise_unregister_dynamic_actions():
        """
        Unregister Talon noise dynamic actions for pop and hiss.
        Restore Talon's default noise callbacks.
        """
        global _talon_noise_pop_init, _talon_noise_hiss_init
        noise.unregister("pop", noise_pop)
        noise.unregister("hiss", noise_hiss)
        ctx.tags = []
        _talon_noise_pop_init = False
        _talon_noise_hiss_init = False
        dynamic_action_remove("pop")
        dynamic_action_remove("hiss")
        if not _dynamic_actions:
            stop_speech_capture()

    def dynamic_noises_toggle():
        """
        Toggle dynamic talon noises on or off. Used if you don't care about
        setting default actions and just want to toggle them on or off.
        """
        if _talon_noise_pop_init or _talon_noise_hiss_init:
            actions.user.noise_unregister_dynamic_actions()
            print("Dynamic noises disabled")
        else:
            actions.user.noise_register_dynamic_action_pop(
                "click",
                test
            )
            actions.user.noise_register_dynamic_action_hiss("none", alias="wish")
            print("Dynamic noises enabled")

    def on_dynamic_action_change(name: str, action_name: str):
        """ctx callback on noise change"""
        print(f"on dynamic action change {name} {action_name}")
        actions.skip()