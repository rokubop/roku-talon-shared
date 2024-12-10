# WIP
game settings: user.game_settings()
# game create files:
#     user.game_ui_hide_game_modal_large()
#     user.game_create_files()
# game calibrate [ex]: user.game_mode_calibrate_x_enable()
# game calibrate why: user.game_mode_calibrate_y_enable()

# Testing if this is better if manually defined per context
# rather than always active
# game mode: user.game_mode_enable()

game [mode] exit: user.game_mode_disable()
game mode stop: user.game_mode_disable()
(stop | exit) game mode: user.game_mode_disable()