app: hi_fi_rush
-
settings():
    speech.timeout = 0.05
    user.game_mouse_calibrate_x_360 = 3080
    user.game_mouse_calibrate_y_90 = 542
    key_hold = 64.0
    key_wait = 0.0
    user.game_key_repeat_wait = 16.0
    user.mouse_move_api = "windows"
    user.mouse_move_continuous_speed_default = 6

^game [mode]$:              user.game_mode_enable()
