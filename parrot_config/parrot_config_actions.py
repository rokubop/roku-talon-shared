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
        "noise"         - default
        "noise noise"   - combo results in action
        "noise:th_100"  - throttle of 100ms (triggered once every 100ms)
        "noise:th"      - default throttle
        "noise:db_100"  - debounce of 100ms (triggered after 100ms of continuous noise)
        "noise:db"      - default debounce
        "noise@left"    - action at the left side of the screen
        "noise@right"   - action at the right side of the screen
        "noise@up"      - action at the top side of the screen
        "noise@down"    - action at the bottom side of the screen
        ```
        """
        return {}

    def parrot_config_format_display(parrot_config: dict[str, tuple[str, callable]]) -> tuple[list[str], list[str]]:
        """
        Format/prettify into commands/actions
        ```
        (cmds, acts) = parrot_config_format_display(parrot_config)
        ```
        """
        cmds, acts = [], []

        for command, action_tuple in parrot_config.items():
            if isinstance(action_tuple, tuple):
                if len(action_tuple) == 0:
                    continue
                action = action_tuple[0]
            else:
                action = action_tuple

            if action == "":
                continue
            command = command.split(":")[0]
            cmds.append(command)
            acts.append(action)

        return (cmds, acts)
