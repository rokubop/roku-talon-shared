app: stray
-
settings():
    key_hold = 64.0
    key_wait = 16.0
    user.game_calibrate_x_360 = 2300
    user.game_calibrate_y_90 = 500
    user.mouse_move_api = "windows"

^game [mode]$: user.game_mode_enable()
