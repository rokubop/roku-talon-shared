from talon import Module, actions
from typing import Any
import csv

mod = Module()

# {user.game_modifier_dir} {user.game_dir}: user.game_dir_with_modifier(game_dir_modifier, game_dir)
# {user.game_modifier_button} {user.game_buttons}: user.game_button_with_modifier(game_key_actions, game_words)
# {user.game_modifier_power} <number_small>: user.game_power_with_modifier(game_power_modifier, game_power)
# {user.game_dir}: user.game_dir_preferred_mode(game_dir)

def get_words(ctx_game, game_words_csv_path):
    # word_list = {}
    # game_key_actions = {}
    # game_modifier_dir = {}
    # game_modifier_button = {}
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

        ctx_game.lists["self.game_dir"] = game_dir
        ctx_game.lists["self.game_xbox_button"] = game_xbox_button

@mod.action_class
class Actions:
    def game_csv_game_words_setup(ctx_game: Any, game_words_csv_path: str):
        """setup csv game words"""
        get_words(ctx_game, game_words_csv_path)