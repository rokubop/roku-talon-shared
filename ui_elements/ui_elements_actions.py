from talon import Module
from typing import List, Dict
from .ui_elements import (
    UIBuilder,
    div,
    text,
    screen,
    css,
    button,
    input_text,
    inputs,
    builders_core,
    builder_child_id_action,
    event_register_on_lifecycle,
    event_unregister_on_lifecycle
)

mod = Module()

@mod.action_class
class Actions:
    def ui_elements(elements: List[str]) -> tuple[callable]:
        """
        Usage:
        ```py
        # def show
        (div, text, screen, button, input_text) = actions.user.ui_elements(["div", "text", "screen", "button", "input_text"])
        ui = screen(align_items="flex_end", justify_content="center")[
            div(id="box", padding=16, background_color="FF000088")[
                text("Hello world", color="FFFFFF"),
                text("Test", id="test", font_size=24),
                input_text(id="the_input"),
                button("Click me", on_click=lambda: print("Clicked"))
            ]
        ]
        ui.show()

        # def hide and destroy
        actions.user.ui_elements_hide_all()

        # trigger update text
        actions.user.ui_elements_set_text("test", "Updated")

        # trigger highlight
        actions.user.ui_elements_highlight("box")
        actions.user.ui_elements_highlight_briefly("box")
        actions.user.ui_elements_unhighlight("box")

        # trigger get value
        actions.user.ui_elements_get_value("the_input")
        ```
        """
        element_mapping: Dict[str, callable] = {
            'css': css, # deprecated, just use a dict
            'div': div,
            'text': text,
            'screen': screen,
            'button': button,
            'input': input_text,
            'input_text': input_text,
            'text_input': input_text
        }
        return tuple(element_mapping[element] for element in elements)

    def ui_elements_screen():
        """
        Only the screen ui element. Has .show() method.
        Give it an id if you want to specifically hide it
        later with actions.user.ui_elements_hide(id)
        """
        return screen

    def ui_elements_hide(id: str):
        """Hide and destroys a ui_element based on the id assigned to the screen ui_element"""
        global builders_core
        if id in list[builders_core]:
            builders_core[id].hide()

    def ui_elements_hide_all():
        """Hide and destroys all currently active ui_elements"""
        for id in list[builders_core]:
            builders_core[id].hide()

    def ui_elements_set_text(id: str, value: str):
        """set text based on id"""
        builder_child_id_action(id, "set_text", value)

    def ui_elements_highlight(id: str):
        """highlight based on id"""
        builder_child_id_action(id, "highlight")

    def ui_elements_unhighlight(id: str):
        """unhighlight based on id"""
        builder_child_id_action(id, "unhighlight")

    def ui_elements_highlight_briefly(id: str):
        """highlight briefly based on id"""
        builder_child_id_action(id, "highlight_briefly")

    def ui_builder_get(id: str) -> UIBuilder:
        """
        Get the UI builder with the given ID. Only for
        informational purposes. Not for mutation.
        """
        global builders_core
        if id in list[builders_core]:
            return builders_core[id]
        else:
            print(f"UI builder with ID {id} not found.")
            return None

    def ui_elements_get_value(id: str) -> str:
        """Get value of an input based on id"""
        input = inputs.get(id)
        if input:
            return input.value
        return None

    def ui_elements_register_on_lifecycle(callback: callable):
        """Register a callback to be called on mount or unmount"""
        event_register_on_lifecycle(callback)

    def ui_elements_unregister_on_lifecycle(callback: callable):
        """Unregister a lifecycle callback"""
        event_unregister_on_lifecycle(callback)
