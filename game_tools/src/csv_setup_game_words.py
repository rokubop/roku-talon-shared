from talon import Module
from typing import Any
import csv
import os

mod = Module()

def get_words(ctx_game, game_words_csv_path):
    game_dir = {}
    game_xbox_button = {}

    with open(game_words_csv_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            list_value = row[0]
            commands_str = row[1] if len(row) > 1 else ''
            if commands_str:
                commands = [command.strip() for command in commands_str.split('|')]

                if "xbox_button_" in list_value:
                    value = list_value.replace("xbox_button_", "")
                    for command in commands:
                        game_xbox_button[command] = value
                elif "dir_" in list_value:
                    value = list_value.replace("dir_", "")
                    if value == "forward":
                        value = "up"
                    elif value == "backward":
                        value = "down"
                    for command in commands:
                        game_dir[command] = value
                else:
                    print(f"Unknown prefix while parsing game_words.csv: {list_value}")

        ctx_game.lists["self.game_dir"] = game_dir
        ctx_game.lists["self.game_xbox_button"] = game_xbox_button

@mod.action_class
class Actions:
    def game_csv_game_words_setup(ctx_game: Any, current_file_path: str):
        """
        Parses `game_words.csv` file in you current directory, and will set up lists based on the values.

        Supported prefixes:
        `xbox_button_`, `dir_`

        Usage:

        `actions.user.game_csv_game_words_setup(ctx_game, __file__)`
        """
        game_words_path = os.path.join(os.path.dirname(current_file_path), 'game_words.csv')
        print(game_words_path)
        get_words(ctx_game, game_words_path)