from talon import Module, Context, actions
from .rdr2_ui import show_ui, hide_ui, update_pop, update_hiss

mod, ctx, ctx_game = Module(), Context(), Context()
# mod.apps.rdr2 = "os: windows\nand app.exe: /code.exe/i"
mod.apps.rdr2 = "os: windows\nand app.exe: /rdr2.exe/i"
ctx.matches = "os: windows\napp: rdr2"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

@mod.action_class
class Actions:
    def rdr2_wheel():
        """wheel"""
        actions.user.game_key_down("tab")
        actions.user.drag_mode_show()
        actions.user.dynamic_action_set_phrase("hiss", "tab")

@ctx_game.action_class("user")
class Actions:
    def on_game_state_change(state: dict):
        print("Game state change", state)

    def on_game_mode_enabled():
        print("Game mode enabled")
        actions.user.noise_register_dynamic_action_pop(
            "click",
            actions.user.game_mouse_click
        )
        actions.user.noise_register_dynamic_action_hiss(
            "stop",
            actions.user.game_stopper,
            alias="wish"
        )
        show_ui()

    def on_game_mode_disabled():
        print("Game mode disabled")
        actions.user.noise_unregister_dynamic_actions()
        hide_ui()