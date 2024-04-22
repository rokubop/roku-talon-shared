from talon import Module, actions
from .ui_builder import UIBuilder

mod = Module()

builder = None

@mod.action_class
class Actions:
    def ui_builder(justify_content: str = "start", align_items: str = "start", background_color: str = None):
        """
        Create a new UIBuilder instance with specific layout settings.

        Args:
            justify_content (str): How to justify content within the UI.
            align_items (str): How items should be aligned within the UI.
        """
        return UIBuilder(
            justify_content=justify_content,
            align_items=align_items,
            width=1920,
            height=1080,
            background_color=background_color
        )

    def ui_builder_test():
        """ui_builder_test"""
        global builder
        builder = actions.user.ui_builder(
            justify_content="flex_end",
            align_items="center",
            background_color="111111"
        )
        window = builder.add_container(
            padding=16,
            background_color="222222",
            border_radius=4,
        )
        box = window.add_container(
            background_color="444444",
            border_radius=4,
            padding=16,
        )
        box.add_text("Hello World!", size=32, color="dd6666")
        box.add_text("Goodbye World!")
        box.add_text(
            "Click Me!",
            background_color="666666",
            padding_y=16,
            padding_x=32,
            size=24,
            color="blue")
        builder.show()

    def ui_builder_test_hide():
        """ui_builder_test"""
        global builder
        builder.hide()
