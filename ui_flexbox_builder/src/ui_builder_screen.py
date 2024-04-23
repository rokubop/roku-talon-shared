from talon import Module, actions, ui
from talon.screen import Screen
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas

def canvas_from_main_screen():
    """ui_main_screen"""
    screen: Screen = ui.main_screen()
    return Canvas.from_screen(screen)