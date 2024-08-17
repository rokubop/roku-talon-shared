from talon import Module, actions
from typing import Any
import csv

mod = Module()

def get_words(ctx_game, game_words_csv_path):
    word_list = {}
    game_key_actions = {}
    with open(game_words_csv_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            action = row[0]
            alias = row[1] if len(row) > 1 else ''
            if alias:
                words = alias.split('|')
                for word in words:
                    if "game_button_" in action:
                        game_key_actions[word.strip()] = action
                    else:
                        word_list[word.strip()] = action
        print(f"Word list: {word_list}")
        ctx_game.lists["self.game_words"] = word_list
        ctx_game.lists["self.game_key_actions"] = game_key_actions

@mod.action_class
class Actions:
    def game_csv_game_words_setup(ctx_game: Any, game_words_csv_path: str):
        """setup csv game words"""
        get_words(ctx_game, game_words_csv_path)

    def game_word_to_action(word: str) -> str:
        """asdf"""
        if word == "game_xbox_b":
            actions.user.vgamepad_b()
        print(f"game_word_to_action: {word}")

    def game_key_actions(modifier: str, target: str) -> str:
        """asdf"""
        if modifier == "game_button_press":
            if target == "game_xbox_a":
                actions.user.vgamepad_a()
            elif target == "game_xbox_b":
                actions.user.vgamepad_b()
            elif target == "game_xbox_x":
                actions.user.vgamepad_x()
            elif target == "game_xbox_y":
                actions.user.vgamepad_y()
        print(f"game_key_actions: {modifier} {target}")