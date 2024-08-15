app: rdr2
mode: user.game
-
# keys
<user.letter>: user.game_key(letter)
<user.modifiers>: user.game_key(modifiers)
<user.function_key>: user.game_key(function_key)
<user.special_key>: user.game_key(special_key)
<user.symbol_key>: user.game_key(symbol_key)
<user.modifiers> <user.unmodified_key>: actions.key("{modifiers}-{unmodified_key}")
hold <user.keys>: user.game_key_down(keys)
hold <user.modifiers>: user.game_key_down(modifiers)
free <user.keys>: user.game_key_up(keys)
free <user.modifiers>: user.game_key_up(modifiers)
long <user.key>: user.game_key_hold(user.key, 1000)
touch | click: user.game_mouse_click()
trick: user.game_mouse_click_right()

# movement
go: user.game_move_dir_toggle('up')
go {user.game_dir}: user.game_move_dir_hold(game_dir)
back: user.game_move_dir_toggle('down')

{user.game_dir}: user.game_camera_continuous_dynamic(game_dir)
# {user.game_dir}: user.game_dir_preferred_action(game_dir)

# camera
cam {user.game_dir}: user.game_camera_continuous_dynamic(game_dir)
cam mid: user.game_reset_center_y()
look {user.game_dir}: user.game_camera_snap_dynamic(game_dir)
round: user.game_turn_180()

# misc
gear <number_small>: user.game_gear_for_last_action(number_small)
run: user.game_key_toggle("shift")
halt | stop: user.game_stopper()

^game exit$:                user.game_mode_disable()