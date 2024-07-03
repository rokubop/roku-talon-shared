from talon import cron, ui
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.canvas import Canvas
from talon.screen import Screen
from talon.skia import RoundRect
from talon.types import Rect, Point2d
from typing import TypedDict, Optional, get_origin, get_args
from itertools import cycle
from dataclasses import dataclass, fields
import uuid

debug_draw_step_by_step = False
debug_points = False
debug_numbers = False
debug_current_step = 0
debug_start_step = 20
render_step = 0
ids = {}
builders_core = {}
state = {
    "highlighted": {},
    "text": {}
}

@dataclass
class BoxModelSpacing:
    top: int = 0
    right: int = 0
    bottom: int = 0
    left: int = 0

@dataclass
class BoxModelLayout:
    margin_spacing: BoxModelSpacing
    padding_spacing: BoxModelSpacing
    margin_rect: Rect
    padding_rect: Rect
    content_rect: Rect
    content_children_rect: Rect

    def __init__(self, x: int, y: int, margin_spacing: BoxModelSpacing, padding_spacing: BoxModelSpacing, width: int = None, height: int = None):
        self.margin_spacing = margin_spacing
        self.padding_spacing = padding_spacing
        self.margin_rect = Rect(x, y, 0, 0)
        self.padding_rect = Rect(x + margin_spacing.left, y + margin_spacing.top, width or 0, height or 0)
        content_x = x + margin_spacing.left + padding_spacing.left
        content_y = y + margin_spacing.top + padding_spacing.top
        content_width = width - padding_spacing.left - padding_spacing.right if width else 0
        content_height = height - padding_spacing.top - padding_spacing.bottom if height else 0
        self.content_rect = Rect(content_x, content_y, content_width, content_height)
        self.content_children_rect = Rect(self.content_rect.x, self.content_rect.y, 0, 0)

    def accumulate_dimensions(self, rect: Rect):
        grow_rect(self.content_children_rect, rect)
        grow_rect(self.content_rect, rect)
        self.padding_rect.width = self.content_rect.width + self.padding_spacing.left + self.padding_spacing.right
        self.padding_rect.height = self.content_rect.height + self.padding_spacing.top + self.padding_spacing.bottom
        self.margin_rect.width = self.padding_rect.width + self.margin_spacing.left + self.margin_spacing.right
        self.margin_rect.height = self.padding_rect.height + self.margin_spacing.top + self.margin_spacing.bottom

    def prepare_render(self, cursor: Point2d, flex_direction: str = "column", align_items: str = "flex_start", justify_content: str = "flex_start"):
        self.margin_rect.x = cursor.x
        self.margin_rect.y = cursor.y
        self.padding_rect.x = cursor.x + self.margin_spacing.left
        self.padding_rect.y = cursor.y + self.margin_spacing.top
        self.content_rect.x = cursor.x + self.margin_spacing.left + self.padding_spacing.left
        self.content_rect.y = cursor.y + self.margin_spacing.top + self.padding_spacing.top
        self.content_children_rect.x = self.content_rect.x
        self.content_children_rect.y = self.content_rect.y

        if flex_direction == "row":
            if justify_content == "center":
                self.content_children_rect.x = self.content_rect.x + self.content_rect.width // 2 - self.content_children_rect.width // 2
            elif justify_content == "flex_end":
                self.content_children_rect.x = self.content_rect.x + self.content_rect.width - self.content_children_rect.width
            if align_items == "center":
                self.content_children_rect.y = self.content_rect.y + self.content_rect.height // 2 - self.content_children_rect.height // 2
            elif align_items == "flex_end":
                self.content_children_rect.y = self.content_rect.y + self.content_rect.height - self.content_children_rect.height
        else:
            if justify_content == "center":
                self.content_children_rect.y = self.content_rect.y + self.content_rect.height // 2 - self.content_children_rect.height // 2
            elif justify_content == "flex_end":
                self.content_children_rect.y = self.content_rect.y + self.content_rect.height - self.content_children_rect.height
            if align_items == "center":
                self.content_children_rect.x = self.content_rect.x + self.content_rect.width // 2 - self.content_children_rect.width // 2
            elif align_items == "flex_end":
                self.content_children_rect.x = self.content_rect.x + self.content_rect.width - self.content_children_rect.width

@dataclass
class Margin(BoxModelSpacing):
    pass

@dataclass
class Padding(BoxModelSpacing):
    pass

def canvas_from_main_screen():
    """ui_main_screen"""
    screen: Screen = ui.main_screen()
    return Canvas.from_screen(screen)

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

def parse_box_model(model_type: BoxModelSpacing, **kwargs) -> BoxModelSpacing:
    model = model_type()
    model_name = model_type.__name__.lower()
    model_name_x = f'{model_name}_x'
    model_name_y = f'{model_name}_y'

    if model_name in kwargs:
        all_sides_value = kwargs[model_name]
        model.top = model.right = model.bottom = model.left = all_sides_value

    if model_name_x in kwargs:
        model.left = model.right = kwargs[model_name_x]
    if model_name_y in kwargs:
        model.top = model.bottom = kwargs[model_name_y]

    for side in ['top', 'right', 'bottom', 'left']:
        side_key = f'{model_name}_{side}'
        if side_key in kwargs:
            setattr(model, side, kwargs[side_key])

    return model

class UIOptionsDict(TypedDict):
    id: str
    align: str
    background_color: str
    border_color: str
    border_radius: int
    border_width: int
    bottom: int
    color: str
    flex_direction: str
    justify_content: str
    align_items: str
    height: int
    justify: str
    left: int
    margin: Margin
    padding: Padding
    right: int
    top: int
    width: int

class UITextOptionsDict(UIOptionsDict):
    id: str
    font_size: int
    font_weight: str

VALID_PROPS = (
    set(UIOptionsDict.__annotations__.keys())
    .union(set(UITextOptionsDict.__annotations__.keys()))
)

class UIOptions:
    id: str = None
    align: str = "start"
    background_color: str = None
    border_color: str = "red"
    border_radius: int = 0
    border_width: int = 0
    bottom: Optional[int] = None
    top: Optional[int] = None
    left: Optional[int] = None
    right: Optional[int] = None
    color: str = "white"
    flex_direction: str = "column"
    gap: int = None
    height: int = 0
    justify: str = "flex_start"
    justify_content: str = "flex_start"
    align_items: str = "flex_start"
    margin: Margin = Margin(0, 0, 0, 0)
    padding: Padding = Padding(0, 0, 0, 0)
    width: int = 0

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.padding = parse_box_model(Padding, **{k: v for k, v in kwargs.items() if 'padding' in k})
        self.margin = parse_box_model(Margin, **{k: v for k, v in kwargs.items() if 'margin' in k})

@dataclass
class UITextOptions(UIOptions):
    id: str = None
    font_size: int = 16
    font_weight: str = "normal"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    def add_child(self, child):
        if isinstance(child, tuple):
            for c in child:
                self.children.append(c)
        else:
            self.children.append(child)

    def __getitem__(self, children=None):
        if children is None:
            children = []
        if not isinstance(children, list):
            children = [children]
        for child in children:
            self.add_child(child)
        return self

    def add_div(self, **kwargs: UIOptionsDict):
        return self.add_flexbox(**kwargs)

    def add_flexbox(self, **kwargs: UIOptionsDict):
        container_options = UIOptions(**kwargs)
        container = UIBox(container_options)
        container.cursor = Point2d(self.cursor.x, self.cursor.y)
        self.children.append(container)
        return container

    def add_text(self, text, **kwargs: UITextOptionsDict):
        text_options = UITextOptions(**kwargs)
        text = UIText(text, text_options)
        self.children.append(text)
        return text

class UIBox(UIWithChildren):
    def __init__(self, options: UIOptions = None):
        super().__init__(options)
        self.box_model: BoxModelLayout = None
        self.type = "box"
        self.id = self.options.id or None
        self.debug_number = 0
        self.debug_color = "red"
        self.debug_colors = iter(cycle(["red", "green", "blue", "yellow", "purple", "orange", "cyan", "magenta"]))

    def virtual_render(self, c: SkiaCanvas, cursor: Cursor):
        self.box_model = BoxModelLayout(cursor.virtual_x, cursor.virtual_y, self.options.margin, self.options.padding, self.options.width, self.options.height)
        cursor.virtual_move_to(self.box_model.content_children_rect.x, self.box_model.content_children_rect.y)
        last_cursor = Point2d(cursor.virtual_x, cursor.virtual_y)
        for i, child in enumerate(self.children):
            gap = self.options.gap or 0
            if self.options.gap is None and child.type == "text" and self.children[i - 1].type == "text":
                gap = 16
            a_cursor = Point2d(cursor.virtual_x, cursor.virtual_y)
            rect = child.virtual_render(c, cursor)
            cursor.virtual_move_to(a_cursor.x, a_cursor.y)
            if i != len(self.children) - 1:
                if self.options.flex_direction == "column":
                    cursor.virtual_move_to(cursor.virtual_x, cursor.virtual_y + rect.height + gap)
                elif self.options.flex_direction == "row":
                    cursor.virtual_move_to(cursor.virtual_x + rect.width + gap, cursor.virtual_y)
            self.box_model.accumulate_dimensions(rect)

        cursor.virtual_move_to(last_cursor.x, last_cursor.y)

        return self.box_model.margin_rect

    def draw_debug_number(self, c: SkiaCanvas, cursor: Cursor, new_color = False):
        if new_color:
            self.debug_color = next(self.debug_colors)

        c.paint.color = self.debug_color
        self.debug_number += 1

        c.draw_text(str(self.debug_number), cursor.x, cursor.y)

    def render(self, c: SkiaCanvas, cursor: Cursor, builder_options: any):
        global ids, debug_current_step, render_step, debug_numbers, debug_points, debug_draw_step_by_step
        render_step += 1
        if debug_current_step and render_step >= debug_current_step:
            return self.box_model.margin_rect

        self.box_model.prepare_render(cursor, self.options.flex_direction, self.options.align_items, self.options.justify_content)
        if self.id:
            ids[self.id] = {
                "box_model": self.box_model,
                "options": self.options,
                "builder_id": builder_options["id"]
            }
        cursor.move_to(self.box_model.padding_rect.x, self.box_model.padding_rect.y)

        if debug_points:
            c.paint.color = "red"
            c.draw_circle(cursor.x, cursor.y, 2)
        if debug_numbers:
            self.draw_debug_number(c, cursor)

        if self.options.border_width:
            c.paint.color = self.options.border_color
            c.paint.style = c.paint.Style.STROKE
            bordered_rect = Rect(
                self.box_model.padding_rect.x - self.options.border_width,
                self.box_model.padding_rect.y - self.options.border_width,
                self.box_model.padding_rect.width + self.options.border_width * 2,
                self.box_model.padding_rect.height + self.options.border_width * 2)

            if self.options.border_radius:
                c.draw_rrect(RoundRect.from_rect(bordered_rect, x=self.options.border_radius, y=self.options.border_radius))
            else:
                c.draw_rect(bordered_rect)
        c.paint.style = c.paint.Style.FILL

        if self.options.background_color:
            c.paint.color = self.options.background_color
            if self.options.border_radius:
                c.draw_rrect(RoundRect.from_rect(self.box_model.padding_rect, x=self.options.border_radius, y=self.options.border_radius))
            else:
                c.draw_rect(self.box_model.padding_rect)


        cursor.move_to(self.box_model.content_children_rect.x, self.box_model.content_children_rect.y)

        # if debug_draw_step_by_step:
        #     render_step += 1
        #     if debug_current_step and render_step >= debug_current_step:
        #         return self.box_model.margin_rect
        # if debug_points:
        #     c.paint.color = "red"
        #     c.draw_circle(cursor.x, cursor.y, 2)
        # if debug_numbers:
        #     self.draw_debug_number(c, cursor)

        if self.options.flex_direction == "row":
            if self.options.align_items == "center":
                cursor.move_to(cursor.x, cursor.y + self.box_model.content_children_rect.height // 2)
            elif self.options.align_items == "flex_end":
                cursor.move_to(cursor.x, cursor.y + self.box_model.content_children_rect.height)
        else:
            if self.options.align_items == "center":
                cursor.move_to(cursor.x + self.box_model.content_children_rect.width // 2, cursor.y)
            elif self.options.align_items == "flex_end":
                cursor.move_to(cursor.x + self.box_model.content_children_rect.width, cursor.y)

        # if debug_points:
        #     c.paint.color = "red"
        #     c.draw_circle(cursor.x, cursor.y, 2)
        # if debug_numbers:
        #     self.draw_debug_number(c, cursor)

        last_cursor = Point2d(cursor.x, cursor.y)
        for i, child in enumerate(self.children):
            if debug_draw_step_by_step:
                render_step += 1
                if debug_current_step and render_step >= debug_current_step:
                    continue

            if self.options.flex_direction == "row":
                if self.options.align_items == "center":
                    cursor.move_to(cursor.x, cursor.y - child.box_model.margin_rect.height // 2)
                elif self.options.align_items == "flex_end":
                    cursor.move_to(cursor.x, cursor.y - child.box_model.margin_rect.height)
            elif self.options.flex_direction == "column":
                if self.options.align_items == "center":
                    cursor.move_to(cursor.x - child.box_model.margin_rect.width // 2, cursor.y)
                elif self.options.align_items == "flex_end":
                    cursor.move_to(cursor.x - child.box_model.margin_rect.width, cursor.y)

            # if debug_points:
            #     c.paint.color = "red"
            #     c.draw_circle(cursor.x, cursor.y, 2)
            # if debug_numbers:
            #     self.draw_debug_number(c, cursor, new_color=True)

            child_last_cursor = Point2d(cursor.x, cursor.y)
            rect = child.render(c, cursor, builder_options)
            cursor.move_to(child_last_cursor.x, child_last_cursor.y)

            if i == len(self.children) - 1:
                break

            if debug_draw_step_by_step:
                render_step += 1
                if debug_current_step and render_step >= debug_current_step:
                    continue

            gap = self.options.gap or 0
            if self.options.gap is None and child.type == "text" and self.children[i + 1].type == "text":
                gap = 16

            if self.options.flex_direction == "row":
                if self.options.align_items == "center":
                    cursor.move_to(cursor.x, cursor.y + child.box_model.margin_rect.height // 2)
                elif self.options.align_items == "flex_end":
                    cursor.move_to(cursor.x, cursor.y + child.box_model.margin_rect.height)
                cursor.move_to(cursor.x + rect.width + gap, cursor.y)
            else:
                if self.options.align_items == "center":
                    cursor.move_to(cursor.x + child.box_model.margin_rect.width // 2, cursor.y)
                elif self.options.align_items == "flex_end":
                    cursor.move_to(cursor.x + child.box_model.margin_rect.width, cursor.y)
                cursor.move_to(cursor.x, cursor.y + rect.height + gap)

            # if debug_points:
            #     c.paint.color = "red"
            #     c.draw_circle(cursor.x, cursor.y, 2)
            # if debug_numbers:
            #     self.draw_debug_number(c, cursor)

        # if debug_draw_step_by_step:
        #     render_step += 1
        #     if debug_current_step and render_step >= debug_current_step:
        #         return self.box_model.margin_rect

        cursor.move_to(last_cursor.x, last_cursor.y)

        # if debug_points:
        #     c.paint.color = "red"
        #     c.draw_circle(cursor.x, cursor.y, 2)
        # if debug_numbers:
        #     self.draw_debug_number(c, cursor)

        return self.box_model.margin_rect

class UIText:
    def __init__(self, text: str, options: UITextOptions = None):
        self.options = options
        self.id = self.options.id
        self.text = text
        self.type = "text"
        self.text_width = None
        self.text_height = None
        self.box_model = None
        self.debug_number = 0
        self.debug_color = "red"
        self.debug_colors = iter(cycle(["red", "green", "blue", "yellow", "purple", "orange", "cyan", "magenta"]))

        if self.options.gap is None:
            self.options.gap = 16

    def draw_debug_number(self, c: SkiaCanvas, cursor: Cursor, new_color = False):
        if new_color:
            self.debug_color = next(self.debug_colors)

        c.paint.color = self.debug_color
        self.debug_number += 1

        c.draw_text(str(self.debug_number), cursor.x, cursor.y)

    def virtual_render(self, c: SkiaCanvas, cursor: Cursor):
        self.box_model = BoxModelLayout(cursor.virtual_x, cursor.virtual_y, self.options.margin, self.options.padding, self.options.width, self.options.height)
        cursor.virtual_move_to(self.box_model.content_children_rect.x, self.box_model.content_children_rect.y)
        c.paint.textsize = self.options.font_size
        c.paint.font.embolden = True if self.options.font_weight == "bold" else False
        self.text_width = c.paint.measure_text(self.text)[1].width
        self.text_height = c.paint.measure_text("E")[1].height
        self.box_model.accumulate_dimensions(Rect(cursor.virtual_x, cursor.virtual_y, self.text_width, self.text_height))
        return self.box_model.margin_rect

    def render(self, c: SkiaCanvas, cursor: Cursor, builder_options: dict[str, any]):
        global ids, state, debug_current_step, render_step, debug_points, debug_numbers, debug_draw_step_by_step
        render_now = True

        if debug_draw_step_by_step:
            render_step += 1
            if debug_current_step and render_step >= debug_current_step:
                return self.box_model.margin_rect

        self.box_model.prepare_render(cursor, self.options.flex_direction, self.options.align_items, self.options.justify_content)

        if self.id:
            ids[self.id] = {
                "box_model": self.box_model,
                "options": self.options,
                "builder_id": builder_options["id"]
            }
            if not state["text"].get(self.id):
                state["text"][self.id] = self.text
            render_now = False
        cursor.move_to(self.box_model.padding_rect.x, self.box_model.padding_rect.y)

        if debug_points:
            c.paint.color = "red"
            c.draw_circle(cursor.x, cursor.y, 2)
        if debug_draw_step_by_step:
            render_step += 1
            if debug_current_step and render_step >= debug_current_step:
                return self.box_model.margin_rect
        if debug_numbers:
            self.draw_debug_number(c, cursor)

        if self.options.background_color:
            c.paint.color = self.options.background_color

            if self.options.border_radius:
                options = RoundRect.from_rect(self.box_model.padding_rect, x=self.options.border_radius, y=self.options.border_radius)
                c.draw_rrect(options)
            else:
                c.draw_rect(self.box_model.padding_rect)

        cursor.move_to(self.box_model.content_children_rect.x, self.box_model.content_children_rect.y)
        if self.id:
            ids[self.id]["cursor"] = {
                "x": cursor.x,
                "y": cursor.y + self.text_height
            }

        if render_now:
            draw_text_simple(c, self.text, self.options, cursor.x, cursor.y + self.text_height)
        # if debug_points:
        #     c.paint.color = "red"
        #     c.draw_circle(cursor.x, cursor.y, 2)
        # if debug_draw_step_by_step:
        #     render_step += 1
        #     if debug_current_step and render_step >= debug_current_step:
        #         return self.box_model.margin_rect
        # if debug_numbers:
        #     self.draw_debug_number(c, cursor)

        return self.box_model.margin_rect

def draw_text_simple(c, text, options, x, y):
    c.paint.color = options.color
    c.paint.textsize = options.font_size
    c.paint.font.embolden = True if options.font_weight == "bold" else False
    c.draw_text(str(text), x, y)

class UIBuilder(UIBox):
    def __init__(self, **options: UIOptionsDict):
        self.cursor = Cursor()
        self.static_canvas = None
        self.dynamic_canvas = None
        self.highlight_canvas = None
        self.unhighlight_jobs = {}
        self.highlight_color = options.get("highlight_color")
        opts = UIOptions(**options or {})
        super().__init__(opts)
        if not self.id:
            self.id = uuid.uuid4()
        self.builder_options = {
            "id": options.get("id") or self.id
        }

    def on_draw_static(self, c: SkiaCanvas):
        self.virtual_render(c, self.cursor)
        self.render(c, self.cursor, self.builder_options)
        self.dynamic_canvas.freeze()

    def on_draw_dynamic(self, c: SkiaCanvas):
        global state
        for id in state["text"]:
            if id in ids:
                if ids[id]["builder_id"] == self.id:
                    options = ids[id]["options"]
                    cursor = ids[id]["cursor"]
                    draw_text_simple(c, state["text"][id], options, cursor["x"], cursor["y"])
            else:
                print(f"Could not update state on ID {id}. ID not found.")

    def on_draw_highlight(self, c: SkiaCanvas):
        global state
        for id in state["highlighted"]:
            if id in ids:
                if ids[id]["builder_id"] == self.id:
                    box_model = ids[id]["box_model"]
                    c.paint.color = state["highlighted"][id]
                    c.paint.style = c.paint.Style.FILL
                    c.draw_rect(box_model.padding_rect)
            else:
                print(f"Could not highlight ID {id}. ID not found.")

    def show(self):
        global debug_current_step, render_step, debug_start_step, debug_draw_step_by_step

        if debug_draw_step_by_step:
            if self.static_canvas:
                render_step = 0
                debug_current_step += 1

            else:
                render_step = 0
                debug_current_step = debug_start_step

        if self.static_canvas:
            self.cursor = Cursor()
            self.static_canvas.freeze()
            self.dynamic_canvas.freeze()
            self.highlight_canvas.freeze()
        else:
            self.static_canvas = canvas_from_main_screen()
            self.static_canvas.register("draw", self.on_draw_static)
            self.static_canvas.freeze()

            self.dynamic_canvas = canvas_from_main_screen()
            self.dynamic_canvas.register("draw", self.on_draw_dynamic)
            self.dynamic_canvas.freeze()

            self.highlight_canvas = canvas_from_main_screen()
            self.highlight_canvas.register("draw", self.on_draw_highlight)
            self.highlight_canvas.freeze()

    def get_ids(self):
        return ids

    def set_text(self, id: str, text: str):
        global state
        state["text"][id] = text
        if self.dynamic_canvas:
            self.dynamic_canvas.freeze()

    def highlight(self, id: str, color_alpha: str = None):
        global state
        state["highlighted"][id] = color_alpha or self.highlight_color or "FFFFFF88"
        self.highlight_canvas.freeze()

    def unhighlight(self, id: str):
        global state
        if id in state["highlighted"]:
            state["highlighted"].pop(id)

            if self.unhighlight_jobs.get(id):
                cron.cancel(self.unhighlight_jobs[id][0])
                self.unhighlight_jobs[id][1]()
                self.unhighlight_jobs[id] = None

            self.highlight_canvas.freeze()

    def highlight_briefly(self, id: str, color_alpha: str = None, duration: int = 150):
        self.highlight(id, color_alpha)
        pending_unhighlight = lambda: self.unhighlight(id)
        self.unhighlight_jobs[id] = (cron.after(f"{duration}ms", pending_unhighlight), pending_unhighlight)

    def hide(self):
        """Hide and destroy the UI builder."""
        global ids, state

        if self.static_canvas:
            self.static_canvas.unregister("draw", self.on_draw_static)
            self.static_canvas.hide()
            self.static_canvas.close()
            self.static_canvas = None

            self.dynamic_canvas.unregister("draw", self.on_draw_dynamic)
            self.dynamic_canvas.hide()
            self.dynamic_canvas.close()
            self.dynamic_canvas = None

            self.highlight_canvas.unregister("draw", self.on_draw_highlight)
            self.highlight_canvas.hide()
            self.highlight_canvas.close()
            self.highlight_canvas = None

        # state["text"] = {}
        # ids = {}

@dataclass
class UIProps:
    id: str
    align: str
    background_color: str
    border_color: str
    border_radius: int
    border_width: int
    bottom: int
    top: int
    left: int
    right: int
    color: str
    flex_direction: str
    font_size: int
    font_weight: str
    gap: int
    height: int
    highlight_color: str
    justify: str
    justify_content: str
    align_items: str
    margin: int
    margin_top: int
    margin_right: int
    margin_bottom: int
    margin_left: int
    padding: int
    padding_top: int
    padding_right: int
    padding_bottom: int
    padding_left: int
    width: int

VALID_PROPS = {f.name for f in fields(UIProps)}
EXPECTED_TYPES = {f.name: f.type for f in fields(UIProps)}

def resolve_type(type_hint):
    if get_origin(type_hint) is Optional:
        return get_args(type_hint)[0]
    return type_hint

def get_props(props, additional_props):
    all_props = None
    if props is None:
        all_props = additional_props
    elif not additional_props:
        all_props = props
    else:
        all_props = {**props, **additional_props}

    invalid_props = set(all_props.keys()) - VALID_PROPS
    if invalid_props:
        raise ValueError(
            f"\nInvalid CSS prop: {', '.join(invalid_props)}\n\n"
            f"Valid CSS props are:\n"
            f"{', '.join(VALID_PROPS)}"
        )

    type_errors = []
    for key, value in all_props.items():
        expected_type = EXPECTED_TYPES[key]
        if not isinstance(value, expected_type):
            type_errors.append(f"{key}: expected {expected_type.__name__}, got {type(value).__name__}")

    if type_errors:
        raise ValueError(
            f"\nInvalid CSS prop type:\n" +
            "\n".join(type_errors)
        )

    return all_props

class UIElementsProxy:
    def __init__(self, func):
        self.func = func

    def __getitem__(self, item):
        raise TypeError(f"You must call {self.func.__name__}() before declaring children. Use {self.func.__name__}()[..] instead of {self.func.__name__}[..].")

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

# ui_elements
def screen(props=None, **additional_props):
    global builders_core
    options = get_props(props, additional_props)
    builder = UIBuilder(
        width=1920,
        height=1080,
        **options
    )
    builders_core[builder.id] = builder
    return builder

def div(props=None, **additional_props):
    options = get_props(props, additional_props)
    box_options = UIOptions(**options)
    return UIBox(box_options)

def text(content, props=None, **additional_props):
    options = get_props(props, additional_props)
    text_options = UITextOptions(**options)
    return UIText(content, text_options)

def css(props=None, **additional_props):
    return get_props(props, additional_props)

div = UIElementsProxy(div)
text = UIElementsProxy(text)
screen = UIElementsProxy(screen)
css = UIElementsProxy(css)