from talon import Module, Context, actions
from .rdr2_ui import show_ui, hide_ui, update_pop, update_hiss

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.rdr2 = "os: windows\nand app.exe: /code.exe/i"
# mod.apps.rdr2 = "os: windows\nand app.exe: /rdr2.exe/i"
ctx.matches = "os: windows\napp: rdr2"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

@ctx_game.action_class("user")
class Actions:
    def on_game_state_change(state: dict):
        print("Game state change", state)

    def on_dynamic_action_change(name: str, action_name: str):
        print("***************Dynamic action change", name, action_name)
        if name == "pop":
            update_pop(action_name)
        elif name == "hiss" or name == "wish":
            update_hiss(action_name)

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
        # actions.user.noise_register_dynamic_action_hiss(
        #     "toggle right",
        #     actions.user.game_mouse_toggle_right,
        #     alias="wish"
        # )
        show_ui()

    def on_game_mode_disabled():
        print("Game mode disabled")
        actions.user.noise_unregister_dynamic_actions()
        hide_ui()