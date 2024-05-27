from talon import Module
from .parrot_config import use_parrot_config

mod = Module()

@mod.action_class
class Actions:
    def use_parrot_config(sound: str):
        """
        Call this with your sounds to use the current `ctx` `parrot_config`

        Example:
        ```talon
        parrot(pop):        user.use_parrot_config("pop")
        parrot(hiss):       user.use_parrot_config("hiss")
        parrot(hiss:stop):  user.use_parrot_config("hiss_stop")
        ```
        """
        use_parrot_config(sound)

    def parrot_config():
        """
        Return the parrot configuration for the current context
        Default should be `{}`. Override this in your
        preferred contexts.

        Example:
        ```py
        parrot_config = {
            "pop":       ("pop", lambda: actions.mouse_click(0)),
            "hiss":      ("hiss", lambda: actions.scroll(1)),
            "hiss_stop": ("hiss", lambda: actions.scroll(-1)),
        }

        @ctx.action_class("user")
        class user_actions:
            def parrot_config():
                return parrot_config
        ```

        Options:
        ```py
        "noise noise"   - combo results in action
        "noise@left"    - action at the left side of the screen
        "noise@right"   - action at the right side of the screen
        "noise@up"      - action at the top side of the screen
        "noise@down"    - action at the bottom side of the screen
        "noise:th_100"  - throttle of 100ms (triggered once every 100ms)
        "noise:th"      - default throttle
        "noise:db_100"  - debounce of 100ms (triggered after 100ms of continuous noise)
        "noise:db"      - default debounce
        "noise:db@left" - action at left side of screen, debounce of 100ms
        ```
        """
        return {}