import sys
from talon import Module, Context, actions
from pynput.mouse import Listener
from .zelda_totk_ui import show_ui, hide_ui
import time

mod, ctx, ctx_game = Module(), Context(), Context()

# Define the app context for Ryujinx
mod.apps.ryujinx = "os: windows\nand app.exe: /ryujinx.exe/i"
ctx.matches = "os: windows\napp: ryujinx"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

# Initialize mouse listener
listener = None

def on_move(x, y):
    """
    Capture the mouse movement and translate it to the right stick movements
    using the vgamepad abstraction.
    """
    screen_width = 1920
    screen_height = 1080

    # Scale mouse coordinates to [-1, 1] range
    x_scaled = (x / screen_width) * 2 - 1
    y_scaled = (y / screen_height) * 2 - 1

    # Apply a deadzone to prevent jitter when the mouse is near the center
    DEADZONE = 0.10
    if abs(x_scaled) < DEADZONE:
        x_scaled = 0
    if abs(y_scaled) < DEADZONE:
        y_scaled = 0

    # Clamp values to [-1.0, 1.0]
    x_scaled = max(-1.0, min(1.0, x_scaled))
    y_scaled = max(-1.0, min(1.0, y_scaled))

    # Call the vgamepad abstraction with the scaled values
    actions.user.vgamepad_right_stick(x_scaled, -y_scaled)  # Invert y for natural camera movement



default = {
    "pop": ("A", lambda: actions.user.game_xbox_button_press('a')),
    "hiss": ("stop", actions.user.game_stopper),
}

dynamic_noises = {
    "default": default,
    "mover": default,
    "battle": {
        **default,
        "pop": ("Y", lambda: actions.user.game_xbox_button_press('y')),
    }
}

@mod.action_class
class Actions:
    def pynput_mouse_map_right_stick_start():
        """Start the mouse listener"""
        global listener
        if actions.app.name() == "Ryujinx":  # Ensure it's only for Ryujinx
            listener = Listener(on_move=on_move)
            listener.start()
            print("Mouse listener started")

    def pynput_mouse_map_right_stick_stop():
        """Stop the mouse listener."""
        global listener
        if listener:
            listener.stop()
            print("Mouse listener stopped")
            listener = None

@ctx_game.action_class("user")
class Actions:
    def dynamic_noises():
        return dynamic_noises

    def on_game_mode_enabled():
        actions.user.game_csv_game_words_setup(ctx_game, __file__)
        actions.user.game_xbox_gamepad_enable()
        actions.user.dynamic_noises_enable()
        actions.user.pynput_mouse_map_right_stick_start()
        show_ui()

    def on_game_mode_disabled():
        actions.user.game_xbox_gamepad_disable()
        actions.user.dynamic_noises_disable()
        actions.user.pynput_mouse_map_right_stick_stop()
        hide_ui()
