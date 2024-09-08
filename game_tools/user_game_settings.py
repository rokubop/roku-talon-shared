from talon import Module
from typing import Union
from pathlib import Path

mod = Module()

# Where your game talon/python files will be
USER_GAMES_DIR = Path(__file__).parent.parent / "roku_games"
# USER_GAMES_DIR = Path(__file__).parent.parent / "my_repo" / "games"
# USER_GAMES_DIR = Path(__file__).parent.parent / "community" / "apps"
# USER_GAMES_DIR = Path(__file__).parent.parent / "community" / "games"
# USER_GAMES_DIR = Path(__file__).parent.parent / "knausj" / "apps"

mod.setting("game_mouse_calibrate_x_360", default=2000, type=int, desc="x amount that is equivalent to 360 degrees")
mod.setting("game_mouse_calibrate_y_90", default=500, type=int, desc="y amount that is equivalent to 90 degrees")
mod.setting("game_mouse_move_continuous_default_speed", default=5, type=int, desc="Default speed for continuous camera movement.")
mod.setting("game_mouse_move_continuous_gears", default="1 2 5 10 20", type=str, desc="Speeds for the camera gears.")
mod.setting("game_mouse_move_deg_default_angle", default=90, type=int, desc="Default angle for snapping the camera.")
mod.setting("game_mouse_move_deg_speed_ms", default=200, type=int, desc="Speed for snapping the camera.")
mod.setting("game_mouse_move_deg_gears", default="5 15 30 45 90", type=str, desc="Angles for snapping the camera.")
mod.setting("game_mode_disables_command_mode", default=True, type=bool, desc="Disable command mode when game mode is enabled.")
mod.setting("game_mouse_click_hold", default=16.0, type=Union[int, float], desc="Hold time for a click.")
mod.setting("game_xbox_button_hold", default=100, type=int, desc="The amount of time to hold a button before releasing it.")
mod.setting("game_xbox_left_stick_default_gear", default=5, type=int, desc="Default gear for the left stick")
mod.setting("game_xbox_left_stick_gears", default=".2 .4 .6 .8 1", type=str, desc="Gears for the left stick")
mod.setting("game_xbox_left_trigger_default_gear", default=5, type=int, desc="Default gear for the left trigger")
mod.setting("game_xbox_left_trigger_gears", default=".2 .4 .6 .8 1", type=str, desc="Gears for the left trigger")
mod.setting("game_xbox_right_stick_default_gear", default=5, type=int, desc="Default gear for the right stick")
mod.setting("game_xbox_right_stick_gears", default=".2 .4 .6 .8 1", type=str, desc="Gears for the right stick")
mod.setting("game_xbox_right_trigger_default_gear", default=5, type=int, desc="Default gear for the right trigger")
mod.setting("game_xbox_right_trigger_gears", default=".2 .4 .6 .8 1", type=str, desc="Gears for the right trigger")
mod.setting("game_xbox_preferred_dir_mode_subject", default="right_stick", type=str, desc="The preferred subject for the directionals")
mod.setting("game_xbox_preferred_dir_mode_action_type", default="hold", type=str, desc="The preferred action type for the preferred direction mode.")