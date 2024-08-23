from talon import Module, Context, actions
from .rdr2_ui import show_ui, hide_ui

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.rdr2 = "os: windows\nand app.exe: /code.exe/i"
# mod.apps.rdr2 = "os: windows\nand app.exe: /rdr2.exe/i"
ctx.matches = "os: windows\napp: rdr2"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

def wheel_stop():
    actions.user.game_xbox_button_release("lb")
    actions.user.drag_mode_hide()

@mod.action_class
class Actions:
    def rdr2_wheel():
        """wheel"""
        actions.user.game_xbox_button_hold("lb")
        actions.user.drag_mode_show()
        actions.user.dynamic_action_set("hiss", "lb", wheel_stop)
        actions.user.dynamic_action_set("pop", "lb", wheel_stop)

def stop_all():
    actions.user.game_stopper()
    actions.user.game_xbox_stopper()

def register_dynamic_noises():
    actions.user.noise_register_dynamic_action_pop(
        action_name = "A",
        action = lambda: actions.user.game_xbox_button_press('a')
    )
    actions.user.noise_register_dynamic_action_hiss(
        action_name="stop",
        action = stop_all,
        alias = "wish"
    )

def on_mount():
    register_dynamic_noises()

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        print("Game mode enabled")
        actions.user.game_csv_game_words_setup(ctx_game, __file__)
        actions.user.game_xbox_gamepad_enable()
        show_ui(on_mount)

    def on_game_mode_disabled():
        actions.user.game_xbox_gamepad_disable()
        actions.user.noise_unregister_dynamic_actions()
        hide_ui()
        print("Game mode disabled")