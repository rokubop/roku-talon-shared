from talon import Module, Context, actions, ui, cron, settings, ctrl
from talon.screen import Screen
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia import RoundRect
from talon.types import Rect, Point2d
from pathlib import Path
from itertools import islice
import re

canvas_grid = None
def generate_char_combo():
    ord_a = ord('a')
    ord_z = ord('z')
    colors = ["", "g", "r", "b", "p", "y"]
    for color in colors:
        for letter_one in range(ord_a, ord_z + 1):
            for letter_two in range(ord_a, ord_z + 1):
                yield chr(letter_one) + chr(letter_two) + color

def draw_center_text(c: SkiaCanvas, text: str, x: int, y: int):
    text_rect = c.paint.measure_text(text)[1]
    text_rect_default = c.paint.measure_text("ABC")[1]
    c.draw_text(
        text,
        x + text_rect.x - text_rect.width / 2,
        y - text_rect_default.y - text_rect_default.height / 2,
    )

grid_pos_map = {}
grid_exclude_regions = []
grid_include_regions = []

color_map = {
    "g": "00ff00",
    "r": "ff0000",
    "b": "0000ff",
    "p": "ff00ff",
    "y": "ffff00",
}

default_box_size = 60
box_size = default_box_size

def on_grid_update(c: SkiaCanvas):
    global box_size
    screen: Screen = ui.main_screen()
    rect = screen.rect
    box_size_half = box_size // 2
    c.paint.textsize = 16
    columns = int(rect.width // box_size)
    rows = int(rect.height // box_size)
    c.paint.color = "ffffff99"
    char_combo_generator = generate_char_combo()
    for y in range(rows):
        for x in range(columns):
            skip = False
            x_pos = x * box_size + box_size_half
            y_pos = y * box_size + box_size_half
            for region in grid_include_regions:
                if not region.contains(Point2d(x_pos, y_pos)):
                    skip = True
            for region in grid_exclude_regions:
                if region.contains(Point2d(x_pos, y_pos)):
                    skip = True
            if skip:
                continue
            text = next(char_combo_generator)
            c.paint.color = "00000099"
            c.draw_circle(x_pos, y_pos, 10)
            text, color = text[:2], text[2:]
            color = color_map.get(color, "ffffff")
            c.paint.color = color + "bb"
            draw_center_text(c, text, x_pos, y_pos)
            grid_pos_map[text] = Point2d(x_pos, y_pos)

def cursorless_grid_show():
    global canvas_grid
    cursorless_grid_hide()
    screen: Screen = ui.main_screen()
    rect = screen.rect
    canvas_grid = Canvas.from_screen(screen)
    canvas_grid.register("draw", on_grid_update)
    canvas_grid.freeze()

def cursorless_grid_hide():
    global canvas_grid, grid_pos_map
    if canvas_grid:
        canvas_grid.unregister("draw", on_grid_update)
        canvas_grid.hide()
        canvas_grid.close()
        canvas_grid = None
        grid_pos_map = {}

mod = Module()
mod.mode("cursorless_grid", "cursorless grid mode")

def get_pos_for_target(target: str) -> Point2d:
    screen: Screen = ui.main_screen()
    rect = screen.rect
    box_size = 60
    box_size_half = box_size // 2
    columns = int(rect.width // box_size)
    rows = int(rect.height // box_size)
    char_combo_generator = generate_char_combo()
    for y in range(rows):
        for x in range(columns):
            text = next(char_combo_generator)
            if text == target:
                return Point2d(x * box_size + box_size_half, y * box_size + box_size_half)
    return Point2d(0, 0)

@mod.capture(rule="<user.letter> <user.letter>")
def cursorless_grid_target(m) -> list[str]:
    return "".join(m.letter_list)

@mod.action_class
class Actions:
    def cursorless_grid_show():
        """Show the grid"""
        cursorless_grid_show()
        actions.mode.enable("user.cursorless_grid")

    def cursorless_grid_hide():
        """Hide the grid"""
        cursorless_grid_hide()
        actions.mode.disable("user.cursorless_grid")

    def cursorless_grid_move_mouse(target: str):
        """Move the mouse to the grid position"""
        pos = grid_pos_map[target]
        actions.mouse_move(pos.x, pos.y)

    def cursorless_move_mouse_to_target(target: str):
        """Move the mouse to the grid position"""
        pos = grid_pos_map[target]
        actions.user.mouse_move_adv_to(pos.x, pos.y)

    def cursorless_grid_more_squares():
        """Increase the number of squares"""
        global box_size
        box_size += 20
        if canvas_grid:
            canvas_grid.freeze()

    def cursorless_grid_less_squares():
        """Decrease the number of squares"""
        global box_size
        box_size -= 20
        if canvas_grid:
            canvas_grid.freeze()

    def cursorless_grid_drag_and_drop(target_one: str, target_two: str):
        """Drag and drop from target one to target two"""
        actions.user.cursorless_grid_move_mouse(target_one)
        ctrl.mouse_click(button=0, down=True)
        def release(ev):
            if ev.type == "stop":
                ctrl.mouse_click(button=0, up=True)
        pos_one = grid_pos_map[target_one]
        pos_two = grid_pos_map[target_two]
        actions.user.mouse_move_adv_from_to(pos_one.x, pos_one.y, pos_two.x, pos_two.y, callback_tick=release)

    def cursorless_grid_exclude_area_targets(target_one: str, target_two: str):
        """Exclude the grid of numbers from target one to target two"""
        global grid_exclude_regions
        if canvas_grid:
            pos_one = grid_pos_map[target_one]
            pos_two = grid_pos_map[target_two]
            grid_exclude_regions.append(Rect(pos_one.x, pos_one.y, pos_two.x - pos_one.x + 1, pos_two.y - pos_one.y + 1))
            canvas_grid.freeze()

    def cursorless_grid_isolate_area_targets(target_one: str, target_two: str):
        """Isolate the grid of numbers from target one to target two"""
        global grid_include_regions
        if canvas_grid:
            pos_one = grid_pos_map[target_one]
            pos_two = grid_pos_map[target_two]
            grid_include_regions.append(Rect(pos_one.x, pos_one.y, pos_two.x - pos_one.x + 1, pos_two.y - pos_one.y + 1))
            canvas_grid.freeze()

    def cursorless_grid_exclude_area_rect(x: int, y: int, width: int, height: int):
        """Exclude the grid of numbers with a rectangle"""
        global grid_exclude_regions
        grid_exclude_regions.append(Rect(x, y, width, height))
        if canvas_grid:
            canvas_grid.freeze()

    def cursorless_grid_exclude_line(target_one: str, target_two: str = None):
        """Exclude the grid of numbers with a line"""
        global grid_exclude_regions
        if canvas_grid:
            pos_one = grid_pos_map[target_one]
            pos_two = grid_pos_map[target_two] if target_two else grid_pos_map[target_one]
            grid_exclude_regions.append(Rect(0, pos_one.y, 1920, pos_two.y - pos_one.y + 1))
            canvas_grid.freeze()

    def cursorless_grid_bring(target: str):
        """Bring the target to current mouse position"""
        (x, y) = ctrl.mouse_pos()
        target_pos = grid_pos_map[target]
        # actions.user.cursorless_grid_move_mouse(target)
        def release(ev):
            if ev.type == "stop":
                ctrl.mouse_click(button=0, up=True)

        def moved(ev):
            if ev.type == "stop":
                ctrl.mouse_click(button=0, down=True)
                actions.user.mouse_move_adv_from_to(target_pos.x, target_pos.y, x, y, 200, callback_tick=release)

        actions.user.mouse_move_adv_to(target_pos.x, target_pos.y, 200, callback_tick=moved)

    def cursorless_grid_bring_to(target: str):
        """Bring the target to current mouse position"""
        (x, y) = ctrl.mouse_pos()
        target_pos = grid_pos_map[target]
        def release(ev):
            if ev.type == "stop":
                ctrl.mouse_click(button=0, up=True)

        ctrl.mouse_click(button=0, down=True)
        actions.user.mouse_move_adv_from_to(x, y, target_pos.x, target_pos.y, callback_tick=release)


    def cursorless_grid_reset():
        """Reset the grid"""
        global grid_exclude_regions, grid_include_regions, box_size, default_box_size
        box_size = default_box_size
        grid_exclude_regions = []
        grid_include_regions = []
        if canvas_grid:
            canvas_grid.freeze()

ctx = Context()
ctx.matches = r"""
mode: user.cursorless_grid
"""