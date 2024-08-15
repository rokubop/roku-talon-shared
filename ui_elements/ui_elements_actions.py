from talon import Module
from .ui_elements import UIBuilder, div, text, screen, css, button, input_text, ids, state, inputs, builders_core
from typing import Literal, List, Dict

mod = Module()

builders = {}

@mod.action_class
class Actions:
    def ui_elements(elements: List[str]) -> tuple[callable]:
        """
        Usage:
        ```py
        global ui

        # def show
        global ui
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

        # trigger update text
        actions.user.ui_elements_set_text("test", "Updated")

        # trigger highlight
        actions.user.ui_elements_highlight("box")
        actions.user.ui_elements_highlight_briefly("box")
        actions.user.ui_elements_unhighlight("box")

        # trigger get value
        actions.user.ui_elements_get_value("the_input")

        # def hide
        global ui
        ui.hide()
        ```
        """
        element_mapping: Dict[str, callable] = {
            'css': css,
            'div': div,
            'text': text,
            'screen': screen,
            'button': button,
            'input': input_text,
            'input_text': input_text,
            'text_input': input_text
        }
        return tuple(element_mapping[element] for element in elements)

    def ui_elements_screen(
        align: Literal["left", "center", "right", "top", "bottom"] = "center",
        justify_content: str = "center",
        align_items: str = "center",
        id: str = None,
        background_color: str = None,
        flex_direction: str = "column",
        highlight_color: str = None) -> UIBuilder:
        """
        DEPRECATED - use ui_elements instead
        Create a new UIBuilder instance with specific layout settings.

        Args:
            justify_content (str): How to justify content within the UI.
            align_items (str): How items should be aligned within the UI.
        """
        global builders

        if align == "left":
            align_items = "flex_start"
        elif align == "right":
            align_items = "flex_end"
        elif align == "top":
            justify_content = "flex_start"
        elif align == "bottom":
            justify_content = "flex_end"

        builders[id] = UIBuilder(
            justify_content=justify_content,
            align_items=align_items,
            width=1920,
            height=1080,
            background_color=background_color,
            flex_direction=flex_direction,
            highlight_color=highlight_color
        )

        return builders[id]

    def ui_builder_hide(id: str):
        """
        Hide the UI builder with the given ID.
        """
        global builders
        if id in builders:
            builders[id].hide()
        else:
            print(f"UI builder with ID {id} not found.")

    def ui_elements_hide_all():
        """Hide/close all currently active ui_elements"""
        for id in builders_core:
            builders_core[id].hide()

    def ui_builder_show(id: str):
        """
        Show the UI builder with the given ID.
        """
        global builders, builders_core
        if id in builders:
            builders[id].show()
        elif id in builders_core:
            builders_core[id].show()
        else:
            print(f"UI builder with ID {id} not found.")

    def ui_builder_get(id: str) -> UIBuilder:
        """
        Get the UI builder with the given ID.
        """
        global builders, builders_core
        if id in builders:
            return builders[id]
        elif id in builders_core:
            return builders_core[id]
        else:
            print(f"UI builder with ID {id} not found.")
            return None

    def ui_builder_get_id(id: str):
        """Get by ID"""
        return ids[id]

    def ui_builder_get_ids():
        """Get by ID"""
        return ids

    def ui_elements_get_value(id: str) -> str:
        """Get value of an input based on id"""
        input = inputs.get(id)
        if input:
            return input.value
        return None

    def ui_elements_set_text(id: str, value: str):
        """set text based on id"""
        global builders_core, ids, state
        if id in ids:
            for builder_id, builder in builders_core.items():
                if ids[id]["builder_id"] == builder_id:
                    builder.set_text(id, value)

    def ui_elements_highlight(id: str):
        """highlight based on id"""
        global builders_core, ids, state
        if id in ids:
            for builder_id, builder in builders_core.items():
                if ids[id]["builder_id"] == builder_id:
                    builder.highlight(id)

    def ui_elements_unhighlight(id: str):
        """unhighlight based on id"""
        global builders_core, ids, state
        if id in ids:
            for builder_id, builder in builders_core.items():
                if ids[id]["builder_id"] == builder_id:
                    builder.unhighlight(id)

    def ui_elements_highlight_briefly(id: str):
        """highlight briefly based on id"""
        global builders_core, ids, state
        if id in ids:
            for builder_id, builder in builders_core.items():
                if ids[id]["builder_id"] == builder_id:
                    builder.highlight_briefly(id)
