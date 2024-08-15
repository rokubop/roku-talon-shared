app: rdr2
# mode: user.game
-
settings():
    # key_hold = 64.0
    # key_wait = 16.0
    # user.game_mouse_click_hold = 64.0

    # movement settings
    user.game_movement_actions_enabled = true
    user.game_use_awsd_for_arrows = true
    user.game_curved_left_and_right = false

    # camera settings
    user.game_camera_actions_enabled = true
    user.mouse_move_api = "windows"
    user.game_calibrate_x_360 = 6000
    user.game_calibrate_y_90 = 3000
    user.game_camera_continuous_default_speed = 5
    user.game_camera_continuous_gear_speeds = "1 2 5 10 20"
    user.game_camera_stop_on_move = true
    user.game_camera_snap_default_angle = 90
    user.game_camera_snap_gear_angles = "3 10 25 45 90"
    user.game_camera_snap_speed_ms = 200
    user.game_move_stop_requires_camera_stop_first = true

    # Talon noise settings (not parrot)
    user.game_dynamic_noises_enabled = true
    user.game_dynamic_noises_pop_enabled = true
    user.game_dynamic_noises_hiss_enabled = true

    # UI
    user.game_ui_enabled = true
    user.game_ui_show_dynamic_noises = true
    user.game_ui_show_actions = true
    user.game_ui_show_key_actions = true
    user.game_ui_show_gear_actions = true
    user.game_ui_show_live_dpad = true
    user.game_ui_show_held_keys = true
    user.game_ui_show_last_command = true

^game [mode]$:                user.game_mode_enable()