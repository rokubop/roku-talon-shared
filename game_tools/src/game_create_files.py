import os
import re
from itertools import islice
from pathlib import Path
from ..templates.fp.template_roku_14_parrot import game_talon, game_mode_talon, game_py
from ..user_game_settings import USER_GAMES_DIR
from talon import Module, actions, app, ui

mod = Module()

active_app = None

@mod.action_class
class Actions:
    def prep_game_create_files():
        """Prepare to create a new directory with talon and python context files for the current application"""
        global active_app
        active_app = ui.active_app()

    def game_create_files(platform_suffix: str = None):
        """Create a new directory with talon and python context files for the current application"""
        global active_app
        app = active_app or ui.active_app()
        print('hello world')
        app_name = get_app_name(active_app.name)
        app_dir = USER_GAMES_DIR / app_name

        game_talon_template = game_talon.format(app_name=app_name)
        game_mode_talon_template = game_mode_talon.format(app_name=app_name)
        game_py_template = get_python_template(active_app, app_name)

        if not app_dir.is_dir():
            os.mkdir(app_dir)

        file = app_dir / f"{app_name}.talon"
        create_file(file, game_talon_template)
        file = app_dir / f"{app_name}_mode.talon"
        create_file(file, game_mode_talon_template)
        file = app_dir / f"{get_platform_filename(app_name, platform_suffix)}.py"
        create_file(file, game_py_template)
        active_app = None

def get_python_template(active_app: ui.App, app_name: str) -> str:
    return game_py.format(
        app_name=app_name,
        os=app.platform,
        app_context=get_app_context(active_app),
    )

def get_platform_filename(app_name: str, platform_suffix: str = None) -> str:
    if platform_suffix:
        return f"{app_name}_{platform_suffix}"
    return app_name


def get_app_context(active_app: ui.App) -> str:
    if app.platform == "mac":
        return f"app.bundle: {active_app.bundle}"
    if app.platform == "windows":
        return f"app.exe: {active_app.exe.split(os.path.sep)[-1]}"
    return f"app.name: {active_app.name}"


def get_app_name(text: str, max_len=20) -> str:
    pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")
    return "_".join(
        list(islice(pattern.findall(text.replace(".exe", "")), max_len))
    ).lower()


def create_file(path: Path, content: str) -> bool:
    if path.is_file():
        actions.app.notify(f"Application context file '{path}' already exists")
        return False

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

    return True

def has_game_files() -> bool:
    app = active_app or ui.active_app()
    app_name = get_app_name(app.name)
    app_dir = USER_GAMES_DIR / app_name
    return app_dir.is_dir() and any(app_dir.iterdir())
