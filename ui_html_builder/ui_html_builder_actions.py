from talon import Module
from .ui_html_builder import UIBuilder
from typing import Literal

mod = Module()

builders = {}

@mod.action_class
class Actions:
    def ui_builder_screen(
        id: str,
        align: Literal["left", "center", "right", "top", "bottom"] = "center",
        justify_content: str = "center",
        align_items: str = "center",
        background_color: str = None,
        flex_direction: str = "column",
        highlight_color: str = None) -> UIBuilder:
        """
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

    def ui_builder_show(id: str):
        """
        Show the UI builder with the given ID.
        """
        global builders
        if id in builders:
            builders[id].show()
        else:
            print(f"UI builder with ID {id} not found.")

    def ui_builder_get(id: str) -> UIBuilder:
        """
        Get the UI builder with the given ID.
        """
        global builders
        if id in builders:
            return builders[id]
        else:
            print(f"UI builder with ID {id} not found.")
            return None