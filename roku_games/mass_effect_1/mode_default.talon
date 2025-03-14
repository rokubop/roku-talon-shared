app: mass_effect_1
-
settings():
    speech.timeout = 0.05
    user.game_mouse_calibrate_x_360 = 1500
    user.game_mouse_calibrate_y_90 = 230
    key_hold = 64.0
    key_wait = 16.0
    user.mouse_move_api = "windows"

^game [mode]$: user.game_mode_enable()
