from talon import Module
from typing import Any
import csv
import os

mod = Module()

valid_dir_csv_keys = [
    "dir_left",
    "dir_right",
    "dir_up",
    "dir_down",
    "dir_forward",
    "dir_backward"
]

valid_xbox_csv_keys = [
    "xbox_button_a",
    "xbox_button_b",
    "xbox_button_x",
    "xbox_button_y",
    "xbox_button_lb",
    "xbox_button_rb",
    "xbox_button_guide",
    "xbox_button_menu",
    "xbox_button_view",
    "xbox_button_left_thumb",
    "xbox_button_right_thumb",
    "xbox_left_trigger",
    "xbox_right_trigger",
    "xbox_dpad",
    "xbox_left_stick",
    "xbox_right_stick"
]

valid_csv_keys = ["list_value"] + valid_xbox_csv_keys + valid_dir_csv_keys

def get_words(ctx_game, game_words_csv_path):
    game_dir = {}
    has_xbox_button = False
    game_xbox_button = {}
    game_xbox_stick = {}
    game_xbox_left_stick = {}
    game_xbox_right_stick = {}
    game_xbox_trigger = {}
    game_xbox_left_trigger = {}
    game_xbox_right_trigger = {}
    game_xbox_dpad = {}

    with open(game_words_csv_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            list_value = row[0]
            commands_str = row[1] if len(row) > 1 else ''
            if commands_str:
                commands = [command.strip() for command in commands_str.split('|')]

                if list_value not in valid_csv_keys:
                        print(f"Invalid key in game_words.csv: {list_value}\n\n")
                        print(f"Valid keys: {valid_csv_keys}")
                        continue

                def add_to_list(list, value):
                    for command in commands:
                        list[command] = value

                if "xbox_" in list_value:
                    has_xbox_button = True

                    if "xbox_button_" in list_value:
                        value = list_value.replace("xbox_button_", "")
                        add_to_list(game_xbox_button, value)
                    elif "xbox_left_stick" in list_value:
                        value = list_value.replace("xbox_", "")
                        add_to_list(game_xbox_stick, "left")
                        add_to_list(game_xbox_left_stick, value)
                    elif "xbox_right_stick" in list_value:
                        value = list_value.replace("xbox_", "")
                        add_to_list(game_xbox_stick, "right")
                        add_to_list(game_xbox_right_stick, value)
                    elif "xbox_left_trigger" in list_value:
                        value = list_value.replace("xbox_", "")
                        add_to_list(game_xbox_trigger, "left")
                        add_to_list(game_xbox_button, value)
                        add_to_list(game_xbox_left_trigger, value)
                    elif "xbox_right_trigger" in list_value:
                        value = list_value.replace("xbox_", "")
                        add_to_list(game_xbox_trigger, "right")
                        add_to_list(game_xbox_button, value)
                        add_to_list(game_xbox_right_trigger, value)
                    elif "xbox_dpad" in list_value:
                        value = list_value.replace("xbox_", "")
                        add_to_list(game_xbox_dpad, value)
                elif "dir_" in list_value:
                    value = list_value.replace("dir_", "")
                    if value == "forward":
                        value = "up"
                    elif value == "backward":
                        value = "down"
                    add_to_list(game_dir, value)
                elif list_value == "list_value":
                    continue
                else:
                    print(f"Unknown prefix while parsing game_words.csv: {list_value}")

        ctx_game.lists["self.game_dir"] = game_dir
        if has_xbox_button:
            ctx_game.lists["self.game_xbox_button"] = game_xbox_button
            ctx_game.lists["self.game_xbox_stick"] = game_xbox_stick
            ctx_game.lists["self.game_xbox_left_stick"] = game_xbox_left_stick
            ctx_game.lists["self.game_xbox_right_stick"] = game_xbox_right_stick
            ctx_game.lists["self.game_xbox_trigger"] = game_xbox_trigger
            ctx_game.lists["self.game_xbox_left_trigger"] = game_xbox_left_trigger
            ctx_game.lists["self.game_xbox_right_trigger"] = game_xbox_right_trigger
            ctx_game.lists["self.game_xbox_dpad"] = game_xbox_dpad

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