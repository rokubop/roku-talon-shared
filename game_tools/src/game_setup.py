from talon import  Module, actions, ui, app
from itertools import islice
from pathlib import Path
import re
import os

mod = Module()
alt_color = False

BLUE = "42A5F5"

def get_app_name(text: str, max_len=20) -> str:
    pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")
    return "_".join(
        list(islice(pattern.findall(text.replace(".exe", "")), max_len))
    ).lower()

def get_app_context(active_app: ui.App) -> str:
    if app.platform == "mac":
        return f"app.bundle: {active_app.bundle}"
    if app.platform == "windows":
        exe_name = active_app.exe.split(os.path.sep)[-1]
        return f"app.exe: /{exe_name}/i"
    return f"app.name: {active_app.name}"

def get_scan_game_folders():
    scan_dirs = Path(__file__).parent.parent.parent / "roku_games"

    for part in scan_dirs.parts:
        if part == "talon":
            break
        scan_dirs = scan_dirs.relative_to(part)
    return [str(scan_dirs), str(scan_dirs)]

def game_settings_open():
    USER_GAMES_DIR = Path(__file__).parent.parent / "game_settings.py"
    actions.user.edit_text_file(USER_GAMES_DIR)
    actions.sleep("500ms")
    actions.edit.file_end()

def target_dir_open():
    print("open target dir")
    USER_GAMES_DIR = Path(__file__).parent.parent.parent / "roku_games"
    # os.system(f"open {USER_GAMES_DIR}")

    if app.platform == "windows":
        os.system(f"explorer {USER_GAMES_DIR}")
    elif app.platform == "mac":
        os.system(f"open {USER_GAMES_DIR}")
    else:
        os.system(f"xdg-open {USER_GAMES_DIR}")


def get_games(new_game):
    USER_GAMES_DIR = Path(__file__).parent.parent.parent / "roku_games"
    games = {}
    for x in USER_GAMES_DIR.iterdir():
        if x.is_dir():
            games[x.name] = {
                "name": x.name,
                "new": x.name == new_game
            }

    games[new_game] = {
        "name": new_game,
        "new": True
    }

    return games

def checkbox(selected):
    svg, rect, polyline = actions.user.ui_elements_svg(["svg", "rect", "polyline"])

    if selected:
        return svg(size=20)[
            rect(x=3, y=3, width=18, height=18, rx=2, ry=2, stroke=BLUE),
            polyline(points="20 6 9 17 4 12", stroke_width=3, stroke=BLUE),
        ]
    return svg(size=20)[
        rect(x=3, y=3, width=18, height=18, rx=2, ry=2),
    ]

def game_row(game_name, selected, on_toggle):
    global alt_color
    div, text, button = actions.user.ui_elements(["div", "text", "button"])

    bg = "222222" if alt_color else "333333"
    alt_color = not alt_color

    return div(flex_direction="row", align_items="center", border_color="555555", gap=4, padding=2, background_color=bg)[
        div(margin_right=8)[
            button(margin=0, padding=0, on_click=on_toggle)[
                checkbox(selected),
            ],
        ],
        div(flex=1)[
            text(game_name),
        ],
        button(flex_direction="row", align_items="center", gap=4, border_radius=2, on_click=game_settings_open)[
            text("Edit", color=BLUE),
        ],
        button(flex_direction="row", align_items="center", gap=4, border_radius=2, on_click=target_dir_open)[
            text("Open", color=BLUE),
        ],
    ]

def folder_row(game_name, is_new,):
    global alt_color
    div, text, icon = actions.user.ui_elements(["div", "text", "icon"])

    # bg = "222222" if alt_color else "333333"
    # bg = "222222"
    color = "FFCC00" if is_new else "FFFFFF"
    alt_color = not alt_color

    return div(flex_direction="row", align_items="center", border_color="555555", gap=4, padding=2)[
        div(margin_right=4)[
            icon("folder", size=20, color=color),
        ],
        div(flex=1)[
            text(game_name, color=color),
        ],
    ]

def scan_games_dir_row(dir):
    global alt_color
    div, text, button = actions.user.ui_elements(["div", "text", "button"])

    bg = "222222" if alt_color else "333333"
    alt_color = not alt_color

    return div(flex_direction="row", align_items="center", border_color="555555", gap=4, padding=2, background_color=bg)[
        text(dir, flex=1, padding_left=8),
        button(flex_direction="row", align_items="center", gap=4, border_radius=2, on_click=game_settings_open)[
            text("Edit", color=BLUE),
        ],
        button(flex_direction="row", align_items="center", gap=4, border_radius=2, on_click=target_dir_open)[
            text("Open", color=BLUE),
        ],
    ]

def game_setup_ui(props):
    elements = ["screen", "div", "text", "button", "icon", "input_text", "state"]
    screen, div, text, button, icon, input_text, state = actions.user.ui_elements(elements)

    games, set_games = state.use("games")
    new_game_name, set_new_game_name = state.use("new_game_name", props["app_name"])

    def on_game_name_change(e):
        set_new_game_name(e.value)
        new_games = games.copy()
        for game in games.values():
            if game["new"]:
                new_games.pop(game["name"])
                new_games[e.value] = {
                    "name": e.value,
                    "new": True
                }
                break
        set_games(new_games)

    def on_toggle(game):
        def fn(e):
            set_games({
                **games,
                game: not games[game]
            })
        return fn

    return screen(justify_content="center", align_items="center")[
        div(draggable=True, background_color="272727", border_radius=8, min_width=600, min_height=400, border_width=1)[
            div(drag_handle=True, flex_direction='row', justify_content="space_between", align_items="center", border_bottom=1, border_color="555555")[
                text("Game setup", font_size=24, padding=16),
                button(on_click=actions.user.ui_elements_hide_all)[
                    icon("close", size=20, padding=6),
                ],
            ],
            div(padding=16, gap=16, overflow_y="auto", max_height=400)[
                text("Step 1 of 3", font_size=20),
                div(flex_direction="column", margin_top=16)[
                    div(flex_direction="column", gap=16)[
                        text('New app name', font_size=18),
                        input_text(id="game_name", autofocus=True, on_change=on_game_name_change, font_size=20, border_radius=4, background_color="444444", value=props["app_name"]),
                    ],
                ],
                div(gap=16, margin_top=16)[
                    text("The following code will be used to define the app", font_size=18),
                    div(background_color="111111", border_radius=4)[
                        div(flex_direction="row", justify_content="space_between")[
                            div(gap=12, padding=16)[
                                div(flex_direction="row")[
                                    text('mod.apps.', font_family="consolas", color="CCCCCC"),
                                    text(new_game_name, font_family="consolas", color="FFCC00"),
                                    text(' = r"""', font_family="consolas", color="CCCCCC"),
                                ],
                                text(f'os: {props["os"]}', font_family="consolas", color="CCCCCC"),
                                text(f'and {props["app_context"]}', font_family="consolas", color="CCCCCC"),
                                text('"""', font_family="consolas", color="CCCCCC"),
                            ],
                            div()[
                                button()[icon("copy", color="CCCCCC")]
                            ]
                        ],
                    ],
                ],
                div(flex_direction="column", gap=12, margin_top=16)[
                    div(flex_direction="row", align_items="center")[
                        text("Your Talon games folder", font_size=18),
                        button(on_click=game_settings_open)[
                            text("Change", color=BLUE),
                        ],
                        button(on_click=target_dir_open)[
                            text("Open", color=BLUE),
                        ],
                    ],
                    text('This is where the new game folder will be created', font_size=14),
                    div(background_color="111111", border_radius=4, flex_direction="row")[
                        text(props["target_dir"], font_family="consolas", color="CCCCCC", padding=16),
                        button()[icon("copy", color="CCCCCC")]
                    ],
                    div(border_width=1, padding=8, background_color="222222")[
                        folder_row(props["target_dir_shorthand"], False),
                        div(flex_direction="row")[
                            div(width=1, margin_top=4, margin_bottom=4, margin_left=8, margin_right=8, background_color="666666"),
                            div(flex_direction="column")[
                                *[folder_row(game_name, data["new"]) for game_name, data in sorted(games.items())],
                            ]
                        ],
                    ],
                ],
                # div(flex_direction="column", padding=16)[
                #     text("Scan folders for games & templates", font_size=20, margin_bottom=16),
                #     div(border_width=1)[
                #         *[scan_games_dir_row(scan_dir) for scan_dir in props["scan_dirs"]],
                #     ],
                # ],
                # div(flex_direction="column", padding=16)[
                #     text("Copy from existing game", font_size=20, margin_bottom=16),
                #     div(border_width=1)[
                #         *[game_row(game, selected, on_toggle(game)) for game, selected in games.items()],
                #     ],
                # ],
                div(flex_direction="row", justify_content="flex_end", gap=16, padding_top=8)[
                    button("Cancel",
                        font_weight="normal",
                        on_click=actions.user.ui_elements_hide_all,
                        border_width=1,
                        border_radius=4,
                        padding=12,
                        padding_left=24,
                        padding_right=24
                    ),
                    button("Continue",
                        on_click=actions.user.ui_elements_hide_all,
                        background_color=BLUE if any(game for game in games.values()) else "444444",
                        border_radius=4,
                        padding=12,
                        padding_left=24,
                        padding_right=24
                    )
                ]
            ]
        ]
    ]

@mod.action_class
class Actions:
    def game_setup():
        """Setup a new game"""
        active_app = ui.active_app()
        app_name = get_app_name(active_app.name)
        games = get_games(app_name)

        actions.user.ui_elements_toggle(
            game_setup_ui,
            props={
                "app_name": app_name,
                "app_context": get_app_context(active_app),
                "os": app.platform,
                "scan_dirs": get_scan_game_folders(),
                "target_dir": Path(__file__).parent.parent.parent / "roku_games",
                "target_dir_shorthand": "roku_games",
            },
            initial_state={
                "games": games
            })


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