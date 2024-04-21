from talon import Module, actions, ui
from talon.screen import Screen
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia import RoundRect
from talon.types import Rect, Point2d
from typing import TypedDict
from dataclasses import dataclass

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

def grow_rect(orig_rect: Rect, new_rect: Rect):
    if new_rect.x < orig_rect.x:
        orig_rect.width += orig_rect.x - new_rect.x
        orig_rect.x = new_rect.x
    if new_rect.y < orig_rect.y:
        orig_rect.height += orig_rect.y - new_rect.y
        orig_rect.y = new_rect.y
    if new_rect.x + new_rect.width > orig_rect.x + orig_rect.width:
        orig_rect.width = new_rect.x + new_rect.width - orig_rect.x
    if new_rect.y + new_rect.height > orig_rect.y + orig_rect.height:
        orig_rect.height = new_rect.y + new_rect.height - orig_rect.y

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
        self.rect = Rect(0, 0, self.options.width, self.options.height)

    def virtual_render(self):
        pass

    def render(self, c: SkiaCanvas, cursor: Cursor):
        for child in self.children:
            rect = child.virtual_render(c, cursor)
            if self.options.flex_direction == "column":
                cursor.virtual_move_to(cursor.virtual_x, cursor.virtual_y + rect.height + self.options.gap)
            elif self.options.flex_direction == "row":
                cursor.virtual_move_to(cursor.virtual_x + rect.width + self.options.gap, cursor.virtual_y)
            grow_rect(self.rect, rect)

        c.paint.color = self.options.bg_color
        c.draw_rrect(RoundRect.from_rect(self.rect))

        for child in self.children:
            rect = child.render(c, cursor)
            if self.options.flex_direction == "column":
                cursor.move_to(cursor.x, cursor.y + rect.height + self.options.gap)
            elif self.options.flex_direction == "row":
                cursor.move_to(cursor.x + rect.width + self.options.gap, cursor.y)
        return self.rect

    def rect(self):
        pass

class UIText:
    def __init__(self, text: str, options: UITextOptions = None):
        self.options = options
        self.text = text

    def virtual_render(self, c: SkiaCanvas, cursor: Cursor):
        c.paint.textsize = self.options.size
        text_width = c.paint.measure_text(self.text)[1].width
        text_height = c.paint.measure_text("E")[1].height
        return Rect(cursor.virtual_x, cursor.virtual_y, text_width, text_height)

    def render(self, c: SkiaCanvas, cursor: Cursor):
        c.paint.color = self.options.color
        c.paint.textsize = self.options.size
        text_width = c.paint.measure_text(self.text)[1].width
        text_height = c.paint.measure_text("E")[1].height
        c.draw_text(self.text, cursor.x, cursor.y + text_height)
        return Rect(cursor.x, cursor.y, text_width, text_height)

    def rect(self):
        pass

class UIBuilder(UIWithChildren):
    def __init__(self, **kwargs: UIOptionsDict):
        super().__init__(UIOptions(**kwargs))
        self.canvas = None
        self.cursor = Cursor()

    def on_draw(self, c: SkiaCanvas):
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
            bg_color="222222",
            # align="center",
            # flex_direction="column",
            # justify="between"
        )
        window.add_text("Hello World!")
        window.add_text("Goodbye World!")
        builder.show()

    def ui_builder_test_hide():
        """ui_builder_test"""
        global builder
        builder.hide()
        # window.add_text("Hello World!")
