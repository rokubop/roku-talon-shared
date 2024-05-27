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
background_color = "00000099"

default_box_size = 60
box_size = default_box_size

def on_grid_update(c: SkiaCanvas):
    global box_size, grid_pos_map, background_color
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
            c.paint.color = background_color
            c.draw_circle(x_pos, y_pos, 10)
            text, color = text[:2], text[2:]
            color = color_map.get(color, "ffffff")
            c.paint.color = color + "bb"
            draw_center_text(c, text, x_pos, y_pos)
            grid_pos_map[text] = Point2d(x_pos, y_pos)

def drag_grid_show():
    global canvas_grid
    drag_grid_hide()
    screen: Screen = ui.main_screen()
    canvas_grid = Canvas.from_screen(screen)
    canvas_grid.register("draw", on_grid_update)
    canvas_grid.freeze()

def drag_grid_hide():
    global canvas_grid, grid_pos_map
    if canvas_grid:
        canvas_grid.unregister("draw", on_grid_update)
        canvas_grid.hide()
        canvas_grid.close()
        canvas_grid = None
        grid_pos_map = {}

mod = Module()
mod.mode("drag_grid", "cursorless grid mode")

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
def drag_grid_target(m) -> list[str]:
    return "".join(m.letter_list)

@mod.capture(rule="<user.drag_grid_target> (to <user.drag_grid_target>)*")
def drag_grid_target_loop(m) -> list[str]:
    return m.drag_grid_target_list

def next_pos(target: str, drag: bool=False):
    pos = grid_pos_map[target]

    def callback(ev):
        if drag and ev.type == "stop":
            actions.mouse_click(button=0, up=True)

    return actions.user.mouse_move_to(pos.x, pos.y, callback_tick=callback)

def next_target(target: str, drag: bool=False):
    pos = grid_pos_map[target]
    return lambda: next_pos(target, drag)

builder = None

@mod.action_class
class Actions:
    def drag_grid_show():
        """Show the grid"""
        drag_grid_show()
        actions.user.drag_grid_show_commands()
        actions.mode.enable("user.drag_grid")

    def drag_grid_hide():
        """Hide the grid"""
        drag_grid_hide()
        actions.user.mouse_move_continuous_stop()
        actions.user.mouse_move_stop()
        actions.user.drag_grid_hide_commands()
        actions.mode.disable("user.drag_grid")

    def drag_grid_move_mouse(target: str):
        """Move the mouse to the grid position"""
        pos = grid_pos_map[target]
        actions.mouse_move(pos.x, pos.y)
        actions.user.mouse_move_continuous_stop()

    def cursorless_move_mouse_to_target(target: str):
        """Move the mouse to the grid position"""
        pos = grid_pos_map[target]
        actions.user.mouse_move_to(pos.x, pos.y)

    def drag_grid_fly_towards(target: str):
        """Move the mouse to the grid position"""
        pos = grid_pos_map[target]
        actions.user.mouse_move_continuous_towards(pos.x, pos.y)

    def drag_grid_more_squares():
        """Increase the number of squares"""
        global box_size
        box_size += 20
        if canvas_grid:
            canvas_grid.freeze()

    def drag_grid_less_squares():
        """Decrease the number of squares"""
        global box_size
        box_size -= 20
        if canvas_grid:
            canvas_grid.freeze()


    def drag_grid_move_to_target_loop(targets: list[list[str]]):
        """Move the mouse to the grid position"""
        actual_targets = targets[0]
        pos = grid_pos_map[actual_targets[0]]
        actions.user.mouse_move_to(pos.x, pos.y)
        for target in islice(actual_targets, 1, None):
            actions.user.mouse_move_queue(next_target(target))

    def drag_grid_drag_to_target_loop(targets: list[list[str]], button: int = 0):
        """Move the mouse to the grid position"""
        actual_targets = targets[0]
        pos = grid_pos_map[actual_targets[0]]
        actions.user.mouse_move_to(pos.x, pos.y, callback_tick=lambda ev: ctrl.mouse_click(button=button, down=True) if ev.type == "stop" else None)
        for i, target in enumerate(islice(actual_targets, 1, None)):
            if i == len(actual_targets) - 1:
                actions.user.mouse_move_queue(next_target(target, True))
            else:
                actions.user.mouse_move_queue(next_target(target))

    def drag_grid_drag_and_drop(target_one: str, target_two: str, button: int = 0):
        """Drag and drop from target one to target two"""
        actions.user.drag_grid_move_mouse(target_one)
        ctrl.mouse_click(button=button, down=True)
        def release(ev):
            if ev.type == "stop":
                ctrl.mouse_click(button=button, up=True)
        pos_one = grid_pos_map[target_one]
        pos_two = grid_pos_map[target_two]
        actions.user.mouse_move_from_to(pos_one.x, pos_one.y, pos_two.x, pos_two.y, callback_tick=release)

    def drag_grid_exclude_area_targets(target_one: str, target_two: str):
        """Exclude the grid of numbers from target one to target two"""
        global grid_exclude_regions
        if canvas_grid:
            pos_one = grid_pos_map[target_one]
            pos_two = grid_pos_map[target_two]
            grid_exclude_regions.append(Rect(pos_one.x, pos_one.y, pos_two.x - pos_one.x + 1, pos_two.y - pos_one.y + 1))
            canvas_grid.freeze()

    def drag_grid_isolate_area_targets(target_one: str, target_two: str):
        """Isolate the grid of numbers from target one to target two"""
        global grid_include_regions
        if canvas_grid:
            pos_one = grid_pos_map[target_one]
            pos_two = grid_pos_map[target_two]
            grid_include_regions.append(Rect(pos_one.x, pos_one.y, pos_two.x - pos_one.x + 1, pos_two.y - pos_one.y + 1))
            canvas_grid.freeze()

    def drag_grid_exclude_area_rect(x: int, y: int, width: int, height: int):
        """Exclude the grid of numbers with a rectangle"""
        global grid_exclude_regions
        grid_exclude_regions.append(Rect(x, y, width, height))
        if canvas_grid:
            canvas_grid.freeze()

    def drag_grid_exclude_line(target_one: str, target_two: str = None):
        """Exclude the grid of numbers with a line"""
        global grid_exclude_regions
        if canvas_grid:
            pos_one = grid_pos_map[target_one]
            pos_two = grid_pos_map[target_two] if target_two else grid_pos_map[target_one]
            grid_exclude_regions.append(Rect(0, pos_one.y, 1920, pos_two.y - pos_one.y + 1))
            canvas_grid.freeze()

    def drag_grid_bring(target: str, button: int = 0):
        """Bring the target to current mouse position"""
        (x, y) = ctrl.mouse_pos()
        target_pos = grid_pos_map[target]
        # actions.user.drag_grid_move_mouse(target)
        def release(ev):
            if ev.type == "stop":
                ctrl.mouse_click(button=button, up=True)

        def moved(ev):
            if ev.type == "stop":
                ctrl.mouse_click(button=button, down=True)
                actions.user.mouse_move_from_to(target_pos.x, target_pos.y, x, y, 200, callback_tick=release)

        actions.user.mouse_move_to(target_pos.x, target_pos.y, 200, callback_tick=moved)

    def drag_grid_bring_to(target: str, button: int = 0):
        """Bring the target to current mouse position"""
        (x, y) = ctrl.mouse_pos()
        target_pos = grid_pos_map[target]
        def release(ev):
            if ev.type == "stop":
                ctrl.mouse_click(button=button, up=True)

        ctrl.mouse_click(button=button, down=True)
        actions.user.mouse_move_from_to(x, y, target_pos.x, target_pos.y, callback_tick=release)


    def drag_grid_reset():
        """Reset the grid"""
        global grid_exclude_regions, grid_include_regions, box_size, default_box_size
        box_size = default_box_size
        grid_exclude_regions = []
        grid_include_regions = []
        actions.user.mouse_move_continuous_stop()
        actions.user.mouse_move_stop()
        if canvas_grid:
            canvas_grid.freeze()

    def drag_grid_stop():
        """Reset the grid"""
        actions.user.mouse_move_continuous_stop()
        actions.user.mouse_move_stop()

    def drag_grid_show_commands():
        """Show the grid commands"""
        global builder

        builder = actions.user.ui_html_builder_screen(
            justify_content="flex_end",
            align_items="center",
        )

        box = builder.add_flexbox(
            background_color="222222",
            margin_bottom=48,
            padding=16,
            flex_direction="column",
            justify_content="center",
            align_items="center",
            border_width=1,
            border_color="666666",
            border_radius=4,
        )
        top = box.add_flexbox(
            flex_direction="row",
            gap=12,
            align_items="center",
        )
        top.add_text("Mode:")
        top.add_text("Drag Grid", color="87CEEB", bold=True)
        top.add_text("|", color="666666")
        top.add_text("Drag X to Y (LMB)")
        top.add_text("|", color="666666")
        top.add_text("Pan X to Y (MMB)")
        top.add_text("|", color="666666")
        top.add_text("Roll X to Y (RMB)")
        top.add_text("|", color="666666")
        # top.add_text("<T> = Target")
        # top.add_text("fly <dir>")
        # top.add_text("|", color="666666")
        # top.add_text("fly to <T>")
        # top.add_text("|", color="666666")
        # top.add_text("fly stop")
        # top.add_text("|", color="666666")
        # top.add_text("tick [<dir>]")
        # top.add_text("|", color="666666")
        # top.add_text("<T> to <T>")
        # top.add_text("|", color="666666")
        # top.add_text("<T> <dir>")
        top.add_text("|", color="666666")
        top.add_text("(more | less) squares")
        top.add_text("|", color="666666")
        top.add_text("grid hide", color="DD2222", bold=True)

        builder.show()

    def drag_grid_hide_commands():
        """Hide the grid commands"""
        global builder
        if builder:
            builder.hide()
            builder = None

ctx = Context()
ctx.matches = r"""
mode: user.drag_grid
"""