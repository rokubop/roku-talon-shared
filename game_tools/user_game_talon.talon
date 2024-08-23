# WIP
# game setup: user.ui_show_game_modal_large()
# game create files:
#     user.ui_hide_game_modal_large()
#     user.game_create_files()
# game calibrate [ex]: user.game_mode_calibrate_x_enable()
# game calibrate why: user.game_mode_calibrate_y_enable()

game mode: user.game_mode_enable()
game [mode] exit: user.game_mode_disable()
game mode stop: user.game_mode_disable()
(stop | exit) game mode: user.game_mode_disable()