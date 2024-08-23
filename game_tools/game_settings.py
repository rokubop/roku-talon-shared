from talon import Module
from typing import Union

mod = Module()

_settings = {
    "game_calibrate_x_360": (2000, int, "x amount that is equivalent to 360 degrees"),
    "game_calibrate_y_90": (500, int, "y amount that is equivalent to 90 degrees"),
    "game_camera_continuous_default_speed": (5, int, "Default speed for continuous camera movement."),
    "game_camera_continuous_gear_speeds": ("1 2 5 10 20", str, "Speeds for the camera gears."),
    "game_camera_snap_default_angle": (90, int, "Default angle for snapping the camera."),
    "game_camera_snap_speed_ms": (200, int, "Speed for snapping the camera."),
    "game_mode_disables_command_mode": (True, bool, "Disable command mode when game mode is enabled."),
    "game_mouse_click_hold": (16.0, Union[int, float], "Hold time for a click."),
    "game_xbox_button_hold": (100, int, "The amount of time to hold a button before releasing it."),
    "game_xbox_left_stick_default_gear": (5, int, "Default gear for the left stick"),
    "game_xbox_left_stick_gears": (".2 .4 .6 .8 1", str, "Gears for the left stick"),
    "game_xbox_left_trigger_default_gear": (5, int, "Default gear for the left trigger"),
    "game_xbox_left_trigger_gears": (".2 .4 .6 .8 1", str, "Gears for the left trigger"),
    "game_xbox_right_stick_default_gear": (5, int, "Default gear for the right stick"),
    "game_xbox_right_stick_gears": (".2 .4 .6 .8 1", str, "Gears for the right stick"),
    "game_xbox_right_trigger_default_gear": (5, int, "Default gear for the right trigger"),
    "game_xbox_right_trigger_gears": (".2 .4 .6 .8 1", str, "Gears for the right trigger")
}

for name, (default, type, desc) in _settings.items():
    mod.setting(name, desc=desc, type=type, default=default)