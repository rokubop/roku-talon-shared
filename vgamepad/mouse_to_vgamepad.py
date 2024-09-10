import sys
from talon import Module, Context, actions, cron
from pynput.mouse import Listener

mod = Module()
ctx_mac = Context()
ctx_mac.matches = "os: mac"

listener = None  # Global listener variable
sensitivity = (9, 9)  # Increased sensitivity for more responsive movement
dead_zone = 0.60  # A small dead zone for filtering out minor movements
last_position = (3, 3)  # Hold the last stick position
stop_job = None  # Job to stop sending right stick input after inactivity

def get_input(x, y):
    """Get mouse input and scale it."""
    print(f"Raw mouse coordinates: x={x}, y={y}")
    input_x = (x / 1280) * 2 - 1  # Adjust according to screen width
    input_y = (y / 720) * 2 - 1  # Adjust according to screen height
    print(f"Scaled input values: x={input_x}, y={input_y}")
    return input_x, input_y

def is_movement_significant(x, y):
    """Check if the mouse movement is significant enough to update the stick."""
    return abs(x) > dead_zone or abs(y) > dead_zone

def on_move(x, y):
    """Handle mouse movement and map it directly to the right stick input."""
    global last_position, stop_job

    # Cancel the previous stop job if it's scheduled
    if stop_job:
        cron.cancel(stop_job)

    input_x, input_y = get_input(x, y)
    scaled_x = input_x * sensitivity[0]
    scaled_y = input_y * sensitivity[1]

    if is_movement_significant(scaled_x - last_position[0], scaled_y - last_position[1]):
        print(f"Moving right stick to: x={scaled_x}, y={scaled_y}")
        actions.user.vgamepad_right_stick(scaled_x, scaled_y)
        last_position = (scaled_x, scaled_y)

    # Schedule a new stop job to reset the stick after 100ms of inactivity
    stop_job = cron.after("100ms", actions.user.stop_sending_stick)

@mod.action_class
class Actions:
    def stop_sending_stick():
        """Stop sending stick input due to inactivity."""
        print("Stopping stick input due to inactivity")
        actions.user.vgamepad_right_stick(0, 0)  # Reset stick to center

    def pynput_mouse_map_right_stick_start():
        """Start the mouse listener."""
        global listener
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
g