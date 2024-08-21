app: rdr2
-
settings():
    user.game_mode_disables_command_mode = true
    user.game_xbox_left_stick_default_gear = 5
    user.game_xbox_left_stick_gears = ".2 .4 .6 .8 1"
    user.game_xbox_right_stick_default_gear = 3
    user.game_xbox_right_stick_gears = ".3 .5 .7 .9 1"
    user.game_xbox_left_trigger_default_gear = 5
    user.game_xbox_left_trigger_gears = ".2 .4 .6 .8 1"
    user.game_xbox_right_trigger_default_gear = 5
    user.game_xbox_right_trigger_gears = ".2 .4 .6 .8 1"
    user.game_xbox_button_hold = 50

    # mouse movement for quick direction snaps
    user.mouse_move_api = "windows"
    user.game_calibrate_x_360 = 6000
    user.game_calibrate_y_90 = 1500

^game [mode]$:                user.game_mode_enable()