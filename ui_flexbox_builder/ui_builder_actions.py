from talon import Module, actions
from .src.ui_builder import UIBuilder
from typing import Literal

mod = Module()

builder = None

@mod.action_class
class Actions:
    def ui_builder(id: str, align: Literal["left", "center", "right", "top", "bottom"] = "center"):
        """Create a new UIBuilder instance with specific layout settings."""
        return actions.user.ui_builder_screen(id, align)

    def ui_builder_screen(
        id: str,
        align: Literal["left", "center", "right", "top", "bottom"] = "center",
        justify_content: str = "center",
        align_items: str = "center",
        background_color: str = None,
        flex_direction: str = "column") -> UIBuilder:
        """
        Create a new UIBuilder instance with specific layout settings.

        Args:
            justify_content (str): How to justify content within the UI.
            align_items (str): How items should be aligned within the UI.
        """
        if align == "left":
            align_items = "flex_start"
        elif align == "right":
            align_items = "flex_end"
        elif align == "top":
            justify_content = "flex_start"
        elif align == "bottom":
            justify_content = "flex_end"

        return UIBuilder(
            justify_content=justify_content,
            align_items=align_items,
            width=1920,
            height=1080,
            background_color=background_color,
            flex_direction=flex_direction
        )

    def ui_builder_test_update():
        """ui_builder_test_update"""
        global builder
        builder.show()

    def ui_builder_test():
        """ui_builder_test"""
        global builder
        builder = actions.user.ui_builder(
            id="parrot_commands",
            align="bottom",
        )
        box = builder.add_div(
            opacity=0.9,
            background_color="222222",
            flex_direction="row",
            border_radius=4,
            border_color="444444",
            border_width=1,
            margin_bottom=48,
        )
        title = box.add_div(
            flex_direction="row",
            background_color="444444",
            padding=16,
            justify_content="center")
        title.add_text("Mode: ")
        title.add_text("Parrot", color="00FF00")
        contents = box.add_div(
            flex_direction="row",
            padding=16)

        for command, label in [
            ("ah", "left"),
            ("oh", "right"),
            ("ee", "stop"),
            ("nn", "jump"),
            ("palate", "ctrl"),
            ("t", "shift"),
            ("er", "exit mode yes indeed")
        ]:
            if label:
                contents.add_text(f"{command}: {label}")
        contents.add_text(
            "exit mode",
            color="FF0000",
            font_weight="bold")
        builder.show()

        # global builder
        # builder = actions.user.ui_builder_screen(
        #     justify_content="flex_end",
        #     align_items="center",
        # )

        # box = builder.add_flexbox(
        #     background_color="222222",
        #     margin_bottom=48,
        #     padding=16,
        #     gap=24,
        #     flex_direction="row",
        #     border_width=1,
        #     border_color="666666",
        #     border_radius=4,
        # )
        # box.add_text("Mode:")
        # box.add_text("Mouse Grid", color="00DD00")
        # box.add_text("|", color="666666")
        # box.add_text("fly <dir>")
        # box.add_text("|", color="666666")
        # box.add_text("fly stop")
        # box.add_text("|", color="666666")
        # box.add_text("tick [<dir>]")
        # box.add_text("|", color="666666")
        # box.add_text("<target> to <target>")
        # box.add_text("|", color="666666")
        # box.add_text("<target> <dir>")
        # box.add_text("|", color="666666")
        # box.add_text("grid hide")

        # bug - alignment off
        # box = builder.add_flexbox(
        #     background_color="222222",
        #     border_radius=4,
        #     padding=16,
        # )
        # box.add_text("Hello World!", size=32, color="dd6666")
        # box_2 = builder.add_flexbox(
        #     background_color="222222",
        #     border_radius=4,
        #     padding=16)
        # box_2.add_text("Hello World!", size=32, color="dd6666")

        # window = builder.add_flexbox(
        #     padding=16,
        #     background_color="222222",
        #     border_radius=4,
        # )
        # box = window.add_flexbox(
        #     background_color="444444",
        #     height=400,
        #     border_radius=4,
        #     padding=16,
        #     justify_content="flex_start",
        #     gap=32,
        #     align_items="center",
        #     flex_direction="column",
        # )
        # box.add_text("Hello World!", size=32, color="dd6666")
        # box.add_text("Goodbye World!", background_color="006600")
        # box.add_text(
        #     "Click Me!",
        #     background_color="666666",
        #     padding_y=16,
        #     padding_x=32,
        #     size=24,
        #     color="blue")
        # builder.show()

    def ui_builder_test_hide():
        """ui_builder_test"""
        global builder
        builder.hide()
