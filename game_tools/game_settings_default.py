from talon import Module

mod = Module()

# camera
mod.setting("game_camera_actions_enabled", type=bool, default=False)
mod.setting("game_camera_continuous_default_speed", type=int, default=5)
mod.setting("game_camera_continuous_gear_speeds", type=str, default="1 2 5 10 20")
mod.setting("game_camera_stop_on_move", type=bool, default=True)
mod.setting("game_camera_snap_default_angle", type=int, default=90)
mod.setting("game_camera_snap_gear_angles", type=str, default="3 10 25 45 90")
mod.setting("game_camera_snap_gear_angles", type=str, default="3 10 25 45 90")
mod.setting("game_camera_snap_speed_ms", type=int, default=200)
mod.setting("game_move_stop_requires_camera_stop_first", type=bool, default=True)

# noises
mod.setting("game_dynamic_noises_enabled", type=bool, default=False)
mod.setting("game_dynamic_noises_hiss_enabled", type=bool, default=True)
mod.setting("game_dynamic_noises_pop_enabled", type=bool, default=True)

# movement
mod.setting("game_movement_actions_enabled", type=bool, default=False)
mod.setting("game_use_awsd_for_arrows", type=bool, default=False)
mod.setting("game_curved_left_and_right", type=bool, default=False)

# ui
mod.setting("game_ui_enabled", type=bool, default=False)
mod.setting("game_ui_show_actions", type=bool, default=True)
mod.setting("game_ui_show_dynamic_noises", type=bool, default=True)
mod.setting("game_ui_show_gear_actions", type=bool, default=True)
mod.setting("game_ui_show_held_keys", type=bool, default=True)
mod.setting("game_ui_show_key_actions", type=bool, default=True)
mod.setting("game_ui_show_last_command", type=bool, default=True)
mod.setting("game_ui_show_live_dpad", type=bool, default=True)
mod.setting("game_ui_show_mouse_click", type=bool, default=True)