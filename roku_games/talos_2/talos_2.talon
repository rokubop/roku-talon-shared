app: talos_2
-
settings():
    speech.timeout = 0.05
    user.game_mouse_calibrate_x_360 = 2413
    user.game_mouse_calibrate_y_90 = 1160
    key_hold = 64.0
    key_wait = 0.0
    user.game_key_repeat_wait = 16.0
    user.mouse_move_api = "windows"

^game [mode]$: user.game_mode_enable()
