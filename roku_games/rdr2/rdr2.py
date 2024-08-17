from talon import Module, Context, actions
from .rdr2_ui import show_ui, hide_ui, update_pop, update_hiss
import os

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.rdr2 = "os: windows\nand app.exe: /code.exe/i"
# mod.apps.rdr2 = "os: windows\nand app.exe: /rdr2.exe/i"
ctx.matches = "os: windows\napp: rdr2"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

@mod.action_class
class Actions:
    def rdr2_wheel():
        """wheel"""
        actions.user.game_key_down("tab")
        actions.user.drag_mode_show()
        actions.user.dynamic_action_set_phrase("hiss", "tab")

def stop_all():
    actions.user.game_stopper()
    actions.user.vgamepad_stopper()

@ctx_game.action_class("user")
class Actions:
    def on_game_state_change(state: dict):
        print("Game state change", state)

    def on_game_mode_enabled():
        print("Game mode enabled")
        game_words_path = os.path.join(os.path.dirname(__file__), 'game_words.csv')
        actions.user.game_csv_game_words_setup(ctx_game, game_words_path)
        actions.user.vgamepad_enable()
        actions.user.noise_register_dynamic_action_pop(
            "A",
            actions.user.vgamepad_a,
        )
        actions.user.noise_register_dynamic_action_hiss(
            "stop",
            stop_all,
            alias="wish"
        )
        show_ui()

    def on_game_mode_disabled():
        actions.user.vgamepad_disable()
        actions.user.noise_unregister_dynamic_actions()
        hide_ui()
        print("Game mode disabled")