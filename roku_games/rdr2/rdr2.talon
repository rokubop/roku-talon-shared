app: rdr2
mode: user.game
-
# movement
go: user.game_move_dir_toggle('up')
go {user.game_dir}: user.game_move_dir_hold(game_dir)
back: user.game_move_dir_toggle('down')

# {user.game_dir}: user.game_dir_preferred_action(game_dir)

# camera
cam {user.game_dir}: user.game_camera_continuous_dynamic(game_dir)
cam mid: user.game_reset_center_y()
look {user.game_dir}: user.game_camera_snap_dynamic(game_dir)
round: user.game_turn_180()
# check {user.game_dir}: user.game_camera_action_dir("camera_snap_angle_temporary", game_dir)
# comb {user.game_dir}: user.game_camera_action_dir("camera_scan_lines_pattern", game_dir)
# wave {user.game_dir}: user.game_camera_action_dir("camera_scan_wave_pattern", game_dir)

# keys
# change this to game keys
long <user.key>: user.game_key_hold(user.key, 1000)
hold <user.key>: user.game_key_hold(user.key, 1000)

# misc
gear <number_small>: user.game_gear_for_last_action(number_small)
run: user.game_key_toggle("shift")
halt | stop: user.game_stopper()

^game exit$:                user.game_mode_disable()

pop <phrase>: skip()
hiss <phrase>: skip()