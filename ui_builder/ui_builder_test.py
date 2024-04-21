from talon import Module, actions, ui
from talon.screen import Screen
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia import RoundRect
from talon.types import Rect, Point2d
from typing import TypedDict
from dataclasses import dataclass
from .ui_builder_helpers import grow_rect

class UIOptionsDict(TypedDict):
    margin: int
    padding: int
    color: str
    bg_color: str
    align: str
    width: int
    height: int
    flex_direction: str
    justify: str

class UITextOptionsDict(UIOptionsDict):
    size: int
    bold: bool

@dataclass
class UIOptions:
    margin: int = 0
    padding: int = 0
    color: str = "white"
    bg_color: str = "black"
    align: str = "start"
    justify: str = "start"
    width: int = 0
    height: int = 0
    flex_direction: str = "column"
    gap: int = 16

@dataclass
class UITextOptions(UIOptions):
    size: int = 16
    bold: bool = False

class Cursor:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.virtual_x = 0
        self.virtual_y = 0

    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.virtual_x = x
        self.virtual_y = y

    def virtual_move_to(self, x, y):
        self.virtual_x = x
        self.virtual_y = y

    def __str__(self):
        return f"Cursor Position: ({self.x}, {self.y}, {self.virtual_x}, {self.virtual_y})"

class UIWithChildren:
    def __init__(self, options: UIOptions = None):
        self.options = options
        self.children = []

    def add_container(self, **kwargs: UIOptionsDict):
        container_options = UIOptions(**kwargs)
        container = UIContainer(container_options)
        container.cursor = Point2d(self.cursor.x, self.cursor.y)
        self.children.append(container)
        return container

    def add_text(self, text, **kwargs: UITextOptionsDict):
        text_options = UITextOptions(**kwargs)
        text = UIText(text, text_options)
        self.children.append(text)
        return text

class UIContainer(UIWithChildren):
    def __init__(self, options: UIOptions = None):
        super().__init__(options)
        self.content_rect = None
        self.padding_rect = None
        self.margin_rect = None

    def virtual_render(self, c: SkiaCanvas, cursor: Cursor):
        self.margin_rect = Rect(cursor.virtual_x, cursor.virtual_y, 0, 0)
        cursor.virtual_move_to(cursor.virtual_x + self.options.margin, cursor.virtual_y + self.options.margin)
        self.padding_rect = Rect(cursor.virtual_x, cursor.virtual_y, 0, 0)
        cursor.virtual_move_to(cursor.virtual_x + self.options.padding, cursor.virtual_y + self.options.padding)
        self.content_rect = Rect(cursor.virtual_x, cursor.virtual_y, 0, 0)
        for child in self.children:
            rect = child.virtual_render(c, cursor)
            if self.options.flex_direction == "column":
                cursor.virtual_move_to(cursor.virtual_x, cursor.virtual_y + rect.height + self.options.gap)
            elif self.options.flex_direction == "row":
                cursor.virtual_move_to(cursor.virtual_x + rect.width + self.options.gap, cursor.virtual_y)
            grow_rect(self.content_rect, rect)
        self.padding_rect.width = self.content_rect.width + self.options.padding * 2
        self.padding_rect.height = self.content_rect.height + self.options.padding * 2
        self.margin_rect.width = self.padding_rect.width + self.options.margin * 2
        self.margin_rect.height = self.padding_rect.height + self.options.margin * 2
        return self.margin_rect

    def render(self, c: SkiaCanvas, cursor: Cursor):
        cursor.move_to(self.padding_rect.x, self.padding_rect.y)
        c.paint.color = self.options.bg_color
        c.draw_rrect(RoundRect.from_rect(self.padding_rect))
        cursor.move_to(self.content_rect.x, self.content_rect.y)

        for child in self.children:
            rect = child.render(c, cursor)
            if self.options.flex_direction == "column":
                cursor.move_to(cursor.x, cursor.y + rect.height + self.options.gap)
            elif self.options.flex_direction == "row":
                cursor.move_to(cursor.x + rect.width + self.options.gap, cursor.y)
        return self.margin_rect

class UIText:
    def __init__(self, text: str, options: UITextOptions = None):
        self.options = options
        self.text = text
        self.text_width = None
        self.text_height = None

    def virtual_render(self, c: SkiaCanvas, cursor: Cursor):
        c.paint.textsize = self.options.size
        self.text_width = c.paint.measure_text(self.text)[1].width
        self.text_height = c.paint.measure_text("E")[1].height
        return Rect(cursor.virtual_x, cursor.virtual_y, self.text_width, self.text_height)

    def render(self, c: SkiaCanvas, cursor: Cursor):
        c.paint.color = self.options.color
        c.paint.textsize = self.options.size
        c.draw_text(self.text, cursor.x, cursor.y + self.text_height)
        return Rect(cursor.x, cursor.y, self.text_width, self.text_height)

class UIBuilder(UIWithChildren):
    def __init__(self, **kwargs: UIOptionsDict):
        super().__init__(UIOptions(**kwargs))
        self.canvas = None
        self.cursor = Cursor()

    def on_draw(self, c: SkiaCanvas):
        for child in self.children:
            child.virtual_render(c, self.cursor)
        for child in self.children:
            child.render(c, self.cursor)

    def show(self):
        if not self.canvas:
            screen: Screen = ui.main_screen()
            self.canvas = Canvas.from_screen(screen)
            self.canvas.register("draw", self.on_draw)
            self.canvas.freeze()

    def hide(self):
        if self.canvas:
            self.canvas.unregister("draw", self.on_draw)
            self.canvas.hide()
            self.canvas.close()
            self.canvas = None

mod = Module()

builder = None

@mod.action_class
class Actions:
    def ui_builder():
        """ui_builder"""
        return UIBuilder()

    def ui_builder_test():
        """ui_builder_test"""
        global builder
        builder = actions.user.ui_builder()
        window = builder.add_container(
            # width=100,
            # height=100,
            # padding=32,
            bg_color="222222",
            # align="center",
            # flex_direction="column",
            # justify="between"
        )
        box = window.add_container(
            bg_color="444444",
            padding=16,
            margin=16,
        )
        box.add_text("Hello World!")
        box.add_text("Goodbye World!")
        builder.show()

    def ui_builder_test_hide():
        """ui_builder_test"""
        global builder
        builder.hide()
        # window.add_text("Hello World!")
