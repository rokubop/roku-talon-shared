app: sheepy
-
settings():
    key_hold = 64.0
    speech.timeout = 0.05

^game [mode]$: user.game_mode_enable()

# live split timer
game start: key(space keypad_1)