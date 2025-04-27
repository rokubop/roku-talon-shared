app: portal_revolution
-
settings():
    speech.timeout = 0.05
    user.game_mouse_calibrate_x_360 = 3000
    user.game_mouse_calibrate_y_90 = 800
    key_hold = 64.0
    key_wait = 16.0
    user.mouse_move_api = "windows"

^game [mode]$: user.game_mode_enable()
