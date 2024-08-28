app: rdr2
-
settings():
    speech.timeout = 0.05
    key_hold = 64.0
    key_wait = 16.0

    user.game_mode_disables_command_mode = true
    user.game_xbox_left_stick_default_gear = 5
    user.game_xbox_left_stick_gears = ".2 .4 .6 .8 1"
    user.game_xbox_right_stick_default_gear = 3
    user.game_xbox_right_stick_gears = ".4 .5 .6 .7 1"
    user.game_xbox_left_trigger_default_gear = 5
    user.game_xbox_left_trigger_gears = ".2 .4 .6 .8 1"
    user.game_xbox_right_trigger_default_gear = 5
    user.game_xbox_right_trigger_gears = ".2 .4 .6 .8 1"
    user.game_xbox_button_hold = 100

    # mouse movement for quick direction snaps
    user.mouse_move_api = "windows"
    user.game_calibrate_x_360 = 6000
    user.game_calibrate_y_90 = 1500

    # exclude chars that have "hiss" sound
    user.drag_mode_exclude_chars = "giosvxz"
    user.drag_mode_default_tile_size = 80
    user.drag_mode_disable_dynamic_noises_on_grid_hide = false

^game [mode]$:                user.game_mode_enable()