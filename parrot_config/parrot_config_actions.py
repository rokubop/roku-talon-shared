from talon import Module, actions
from .parrot_config import (
    parrot_config_cycle_mode,
    parrot_config_get_mode,
    parrot_config_set_mode,
    parrot_config_noise,
    parrot_config_event_register,
    parrot_config_event_unregister,
)

mod = Module()

@mod.action_class
class Actions:
    def parrot_config_noise(name: str):
        """
        parrot noises should call this in order to use current `parrot_config`

        Example:
        ```talon
        parrot(pop):        user.parrot_config_noise("pop")
        parrot(hiss):       user.parrot_config_noise("hiss")
        parrot(hiss:stop):  user.parrot_config_noise("hiss_stop")
        ```
        """
        parrot_config_noise(name)

    def parrot_config():
        """
        Define your parrot config in a ctx here.

        Example:
        ```py
        parrot_config = {
            "pop":       ("pop", lambda: actions.mouse_click(0)),
            "hiss":      ("hiss", lambda: actions.scroll(1)),
            "hiss_stop": ("hiss", lambda: actions.scroll(-1)),
        }

        # or
        parrot_config = {
            "default": {
                "pop":       ("pop", lambda: actions.mouse_click(0)),
                "hiss":      ("hiss", lambda: actions.scroll(1)),
                ...
            },
            "other_mode": {
                "pop":       ("pop", lambda: actions.mouse_click(0)),
                "hiss":      ("hiss", lambda: actions.scroll(1)),
                ...
            },

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
        ```
        """
        return {}

    def parrot_config_set_mode(mode: str):
        """
        Change the current mode. Only applicable for parrot configs that define
        "default" and other modes.

        Example:
        ```py
        parrot_config = {
            "default": parrot_config_default,
            "other": {
                **parrot_config_default,
                **parrot_config_other,
            }
        }

        actions.user.parrot_config_mode("other")
        ```
        """
        parrot_config_set_mode(mode)

    def parrot_config_cycle_mode() -> str:
        """
        Cycle to the next mode. Only works if you have defined
        multiple modes in your `parrot_config`. Also returns the
        string value of the next mode.

        ```
        parrot_config = {
            "default": parrot_config_default,
            "other": {
                **parrot_config_default,
                **parrot_config_other,
            }
        }
        ```
        """
        return parrot_config_cycle_mode()

    def parrot_config_get_mode() -> str:
        """
        Get the current mode
        """
        return parrot_config_get_mode()

    def parrot_config_format_display(
        parrot_config: dict[str, tuple[str, callable]],
    ) -> tuple[list[str], list[str]]:
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

    def parrot_config_format_display_dict(
        parrot_config: dict[str, tuple[str, callable]] = None,
        mode: str = None,
    ) -> dict[str, callable]:
        """
        Format/prettify into dictionary of commands/action names
        ```
        display_dict = parrot_config_format_display(parrot_config)
        ```
        """
        if not parrot_config:
            parrot_config = actions.user.parrot_config()
        if "default" in parrot_config:
            if mode is None:
                mode = actions.user.parrot_config_get_mode()
            parrot_config = parrot_config.get(mode, parrot_config["default"])
        display_dict = {}

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
            display_dict[command] = action

        return display_dict

    def parrot_config_event_register(on_noise: callable):
        """
        Register noise event triggered from parrot_config
        ```py
        def on_noise(noise: str, command: str):
            print(noise, command)
        actions.user.parrot_config_event_register(on_noise)
        ```
        """
        parrot_config_event_register(on_noise)

    def parrot_config_event_unregister(on_noise: callable):
        """
        Unregister event set by actions.user.parrot_config_event_register
        """
        parrot_config_event_unregister(on_noise)