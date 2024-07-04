app: talos_2
-
settings():
    speech.timeout = 0.05
    user.game_calibrate_x_360 = 4521
    user.game_calibrate_y_90 = 1110
    key_hold = 64.0
    key_wait = 16.0
    user.mouse_move_api = "windows"

^game [mode]$: user.game_mode_enable()
