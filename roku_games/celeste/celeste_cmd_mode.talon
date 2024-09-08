app: celeste
-
settings():
    key_hold = 64.0
    key_wait = 16.0
    user.game_mouse_calibrate_x_360 = 2139
    user.game_mouse_calibrate_y_90 = 542
    user.mouse_move_api = "windows"

^game [mode]$: user.game_mode_enable()
^game stop$: user.game_mode_disable()

<number>: user.game_celeste_set_jump_2(number)
