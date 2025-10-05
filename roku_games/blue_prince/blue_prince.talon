app: blue_prince
-
settings():
    key_hold = 64.0
    key_wait = 16.0
    user.game_mouse_calibrate_x_360 = 6000
    user.game_mouse_calibrate_y_90 = 2500
    user.mouse_move_api = "windows"

^game [mode]$: user.game_mode_enable()
