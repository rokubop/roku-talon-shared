app: spiritfarer
-
settings():
    key_hold = 64.0
    key_wait = 0.0
    user.game_key_repeat_wait = 16.0

^game [mode]$: user.game_mode_enable()
^game stop$: user.game_mode_disable()