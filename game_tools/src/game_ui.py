# from talon import Module, actions, ui, cron, settings
# from talon.screen import Screen
# from talon.canvas import Canvas
# from talon.skia.canvas import Canvas as SkiaCanvas
# from talon.skia import RoundRect
# from talon.types import Rect, Point2d
# from pathlib import Path
# from itertools import islice
# import re
# from .game_create_files import has_game_files

# mod = Module()

# canvas_modal = None
# modal_left_x = 0
# modal_top_y = 0
# modal_width = 800
# modal_height = 500
# margin = 16
# y = 0
# x = 0
# text_size = 16
# text_gap = 16
# button_padding = 10
# buttons = {}
# debug_positions = False

# def get_app_name(text: str, max_len=20) -> str:
#     pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")
#     return "_".join(
#         list(islice(pattern.findall(text.replace(".exe", "")), max_len))
#     ).lower()

# def draw_title(c: SkiaCanvas, title: str):
#     global x, y, text_size
#     c.paint.color = f"ffffff"
#     c.paint.textsize = text_size
#     c.draw_text(title, x, y)

# def draw_line(c: SkiaCanvas):
#     global x, y, text_gap, modal_left_x, modal_width, margin
#     c.paint.stroke_width = 1
#     c.paint.color = f"ffffff99"
#     y += text_gap
#     c.draw_line(modal_left_x + margin, y, modal_left_x + modal_width - margin, y)

# def draw_center_text(c: SkiaCanvas, text: str, x: int, y: int):
#     text_rect = c.paint.measure_text(text)[1]
#     text_rect_default = c.paint.measure_text("ABC")[1]
#     c.draw_text(
#         text,
#         x + text_rect.x - text_rect.width / 2,
#         y - text_rect_default.y - text_rect_default.height / 2,
#     )

# def draw_key_value(c: SkiaCanvas, key: str, value: str):
#     global x, y, text_gap, text_size
#     y += text_gap + text_size
#     c.paint.color = f"ffffff"
#     text_rect = c.paint.measure_text(key)[1]
#     c.draw_text(key, x, y)
#     c.paint.color = f"FFD700"
#     c.paint.textsize = 16
#     c.draw_text(value, x + text_rect.width + text_gap, y)

# def add_button(c: SkiaCanvas, text: str, action: callable):
#     global text_size, text_gap, x, y, button_padding, buttons, debug_positions
#     if debug_positions:
#         c.paint.color = "ff0000"
#         c.draw_circle(x, y, 2)
#     text_width = c.paint.measure_text(text)[1].width
#     text_height = c.paint.measure_text("ABC")[1].height
#     button_rect = Rect(x, y, text_width + button_padding * 2, text_size + button_padding * 2)
#     rrect = RoundRect.from_rect(button_rect, x=10, y=10)
#     c.paint.style = c.paint.Style.FILL
#     c.paint.color = "FFD70011"
#     if buttons.get(text, {}).get("is_hovering", False):
#         c.paint.color = "FFD70033"
#     c.draw_rrect(rrect)
#     c.paint.color = "ffffff"
#     c.paint.style = c.paint.Style.STROKE
#     c.draw_rrect(rrect)
#     c.paint.style = c.paint.Style.FILL
#     draw_center_text(c, text, button_rect.x + button_rect.width / 2, button_rect.y + button_rect.height / 2)
#     if text not in buttons or buttons[text]["rect"] != button_rect:
#         buttons[text] = {
#             "rect": button_rect,
#             "is_hovering": False,
#             "action": action,
#         }
#     return button_rect

# def on_modal_update(c: SkiaCanvas):
#     global x, y, text_size, margin, text_gap, modal_left_x, modal_top_y, modal_width, modal_height
#     screen: Screen = ui.main_screen()
#     rect = screen.rect
#     screen_center = Point2d(rect.width / 2, rect.height / 2)
#     modal_top_y = screen_center.y - modal_height / 2
#     modal_left_x = screen_center.x - modal_width / 2
#     rect = Rect(modal_left_x, modal_top_y, modal_width, modal_height)

#     c.paint.style = c.paint.Style.FILL
#     shadow_rect = Rect(rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4)
#     c.paint.color = f"6082B633"
#     c.draw_rrect(RoundRect.from_rect(shadow_rect, x=12, y=12))
#     c.paint.color = f"00000099"
#     shadow_rect = Rect(rect.x - 1, rect.y - 1, rect.width + 2, rect.height + 2)
#     c.draw_rrect(RoundRect.from_rect(shadow_rect, x=11, y=11))

#     c.paint.stroke_width = 1
#     c.paint.color = f"333333"
#     c.paint.style = c.paint.Style.FILL
#     c.draw_rrect(RoundRect.from_rect(rect, x=10, y=10))

#     c.paint.color = f"ffffff66"
#     c.paint.style = c.paint.Style.STROKE
#     c.draw_rrect(RoundRect.from_rect(rect, x=10, y=10))
#     c.paint.style = c.paint.Style.FILL

#     x = modal_left_x + margin
#     y = modal_top_y + margin + text_size

#     draw_title(c, "Game Tools")
#     draw_line(c)
#     USER_GAMES_DIR = Path(__file__).parent.parent / "user_games"
#     draw_key_value(c, "User game directory", str(USER_GAMES_DIR))
#     active_app = ui.active_app()
#     app_name = get_app_name(active_app.name)
#     draw_key_value(c, "Current game", app_name)
#     has_files = (USER_GAMES_DIR / app_name).exists()
#     draw_key_value(c, "Has game files", str(has_files))
#     c.paint.color = "ffffff"
#     y += text_gap + text_size
#     c.draw_text('"Create game files"', x, y)
#     y += text_gap + text_size
#     c.draw_text('"Calibrate x"', x, y)
#     y += text_gap + text_size
#     c.draw_text('"Calibrate y"', x, y)
#     if not has_files:
#         y += text_gap + text_size
#         c.draw_text(f"No game folder found for {app_name}.", x, y)
#         y += text_gap + text_size
#         c.draw_text(f"Say \"game create\"", x, y)
#     y += text_gap + text_size
#     button_rect = add_button(c, "Game create files", game_ui_hide_game_modal_large)
#     x = x + button_rect.width + text_gap
#     button_rect =add_button(c, "Game change folder", game_ui_hide_game_modal_large)
#     x = x + button_rect.width + text_gap
#     button_rect =add_button(c, "Game tools close", game_ui_hide_game_modal_large)

# def on_mouse(e):
#     global canvas_modal
#     print(e)
#     print(e.event)
#     if e.event == "mousemove":
#         for data in buttons.values():
#             hovering = data["rect"].contains(e.gpos)
#             if data["is_hovering"] != hovering:
#                 data["is_hovering"] = hovering
#                 canvas_modal.freeze()
#     elif e.event == "mousedown":
#         for data in buttons.values():
#             hovering = data["rect"].contains(e.gpos)
#             if data["is_hovering"]:
#                 data["action"]()

# def game_ui_show_game_modal_large():
#     global canvas_modal
#     game_ui_hide_game_modal_large()
#     screen: Screen = ui.main_screen()
#     rect = screen.rect
#     print(rect.width, rect.height)
#     canvas_modal = Canvas.from_screen(screen)
#     canvas_modal.blocks_mouse = True
#     canvas_modal.register("draw", on_modal_update)
#     canvas_modal.register("mouse", on_mouse)
#     canvas_modal.freeze()


# def game_ui_hide_game_modal_large():
#     global canvas_modal
#     if canvas_modal:
#         canvas_modal.unregister("draw", on_modal_update)
#         canvas_modal.unregister("mouse", on_mouse)
#         canvas_modal.hide()
#         canvas_modal.close()
#         canvas_modal = None

# def game_settings_open():
#     USER_GAMES_DIR = Path(__file__).parent.parent / "user_game_settings.py"
#     actions.user.edit_text_file(USER_GAMES_DIR)
#     actions.sleep("500ms")
#     actions.edit.file_end()

# builder = None

# def get_path_prefix():
#     USER_GAMES_DIR = Path(__file__).parent.parent / "user_games"
#     for part in USER_GAMES_DIR.parts:
#         if part == "talon":
#             break
#         USER_GAMES_DIR = USER_GAMES_DIR.relative_to(part)
#     return str(USER_GAMES_DIR)

# def get_path_text(id: str, path_prefix:str, app_name: str) -> str:
#     NEW_FOLDER = f"{path_prefix}/{app_name}"
#     if id == "root":
#         return NEW_FOLDER
#     elif id == "talon":
#         return f"{NEW_FOLDER}/{app_name}.talon"
#     elif id == "py":
#         return f"{NEW_FOLDER}/{app_name}.py"

# def on_path_text_change(value: str):
#     app_name = get_path_prefix()
#     actions.user.ui_elements_set_text("root", get_path_text("root", app_name, value))
#     actions.user.ui_elements_set_text("talon", get_path_text("talon", app_name, value))
#     actions.user.ui_elements_set_text("py", get_path_text("py", app_name, value))

# @mod.action_class
# class Actions:
#     def game_ui_show_calibrate_x():
#         """Show the calibrate x modal"""
#         current_value = settings.get("user.mouse_move_calibrate_x_360")
#         builder = actions.user.ui_flexbox_builder({
#             'id': 'main',
#             'align': 'top_left',
#             'margin_left': 200,
#             'margin_top': 200,
#         })
#         builder.add_title('Calibrate X')
#         builder.add_text('Place your cursor on a point on the screen and calibrate')
#         builder.add_gap(-12)
#         builder.add_text('the number that equals a 360 degree turn.')
#         builder.add_gap(8)
#         builder.add_text("2000", id="calibration_value", size=24)
#         builder.add_gap(16)
#         builder.add_text('You can say: ', color="dddddd")
#         builder.add_gap(-8)
#         builder.add_text('"<number>", "plus <number>", or "minus <number>"')
#         builder.add_gap(-8)
#         builder.add_text(f'Example: "{current_value}", "plus 300", "minus 22"', color="888888")
#         builder.add_gap(24)
#         builder.add_button_group([
#             {
#                 'text': 'Calibrate save',
#                 'action': lambda: None,
#             },
#             {
#                 'text': 'Calibrate y',
#                 'action': lambda: None,
#             },
#             {
#                 'text': 'Calibrate close',
#                 'action': actions.user.game_ui_hide_game_modal_large
#             },
#         ])
#         builder.show()

#     def game_ui_show_calibrate_y():
#         """Show the calibrate y modal"""
#         current_value = settings.get("user.mouse_move_calibrate_y_90")
#         builder = actions.user.ui_flexbox_builder({
#             'id': 'main',
#             'align': 'top_left',
#             'margin_left': 200,
#             'margin_top': 200,
#         })
#         builder.add_title('Calibrate Y')
#         builder.add_text('Say numbers until it correctly centers the cursor vertically.')
#         builder.add_gap(-12)
#         builder.add_text('the number that equals a 360 degree turn.')
#         builder.add_gap(8)
#         builder.add_text("500", id="calibration_value", size=24)
#         builder.add_gap(16)
#         builder.add_text('You can say: ', color="dddddd")
#         builder.add_gap(-8)
#         builder.add_text('"<number>", "plus <number>", or "minus <number>"')
#         builder.add_gap(-8)
#         builder.add_text(f'Example: "{current_value}", "plus 100", "minus 22"', color="888888")
#         builder.add_gap(24)
#         builder.add_button_group([
#             {
#                 'text': 'Calibrate save',
#                 'action': lambda: None,
#             },
#             {
#                 'text': 'Calibrate x',
#                 'action': lambda: None,
#             },
#             {
#                 'text': 'Calibrate close',
#                 'action': actions.user.game_ui_hide_game_modal_large
#             },
#         ])
#         builder.show()

#     def game_ui_calibrate_update(dx: int):
#         """Update the calibrate value"""
#         actions.user.ui_flexbox_builder_update({
#             'id': 'main',
#             'components': [{
#                 'id': 'calibration_value',
#                 'text': str(round(dx))
#             }]
#         })

#     def game_ui_show_game_modal_large():
#         """Show the game modal"""
#         actions.skip() # not implemented yet

#     def game_ui_hide_game_modal_large():
#         """Hide the game modal"""
#         actions.skip() # not implemented yet

#     def game_ui_show_game_help():
#         """Show the game setup success modal"""
#         builder = actions.user.ui_flexbox_builder({
#             'id': 'main',
#             'align': 'center',
#             'width': 400,
#         })
#         builder.add_title('Game Help')
#         builder.add_gap()
#         builder.add_text('You can say:', margin_bottom=8)
#         builder.add_text('First time setup (while focused game):', margin_bottom=-8)
#         builder.add_link_group([
#             {
#                 'text': 'Game setup',
#                 'action': actions.user.game_ui_show_game_modal_large
#             }
#         ])
#         if has_game_files():
#             builder.add_gap(-8)
#             builder.add_text('Game files already setup', color="00FF00", size=14)
#         builder.add_gap()
#         builder.add_text('Editing commands:', margin_bottom=-8)
#         builder.add_link_group([
#             {
#                 'text': 'Game edit commands',
#                 'action': lambda: None,
#             },
#             {
#                 'text': 'Game edit parrot',
#                 'action': lambda: None,
#             },
#         ])
#         builder.add_gap()
#         builder.add_text('Show/hide commands:', margin_bottom=-8)
#         builder.add_link_group([
#             {
#                 'text': 'Game show commands',
#                 'action': lambda: None,
#             },
#             {
#                 'text': 'Game hide commands',
#                 'action': lambda: None,
#             },
#         ])
#         builder.add_gap()
#         builder.add_text('Calibrate 360 x or 90 y:', margin_bottom=-8)
#         builder.add_link_group([
#             {
#                 'text': 'Game calibrate x',
#                 'action': lambda: None,
#             },
#             {
#                 'text': 'Game calibrate y',
#                 'action': lambda: None,
#             },
#         ])
#         builder.add_gap(24)
#         builder.add_button({
#             'text': 'Game help close',
#             'primary': True,
#             'action': actions.user.game_ui_hide_game_modal_large,
#         })
#         builder.show()