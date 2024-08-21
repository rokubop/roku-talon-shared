app: rdr2
mode: user.game
-

# directions
{user.game_dir}: user.game_xbox_right_stick_hold_dir(game_dir)
go: user.game_xbox_left_stick_hold_dir("up")
go {user.game_dir}: user.game_xbox_left_stick_hold_dir(game_dir)
go {user.game_gear}: user.game_xbox_left_stick_set_gear(game_gear)
cam {user.game_dir}: user.game_xbox_right_stick_hold_dir(game_dir)
cam {user.game_gear}: user.game_xbox_right_stick_set_gear(game_gear)

# buttons
[tap] {user.game_xbox_button}: user.game_xbox_button_press(game_xbox_button)
long {user.game_xbox_button}: user.game_xbox_button_hold(game_xbox_button, 1000)
longer {user.game_xbox_button}: user.game_xbox_button_hold(game_xbox_button, 4000)
hold {user.game_xbox_button}: user.game_xbox_button_hold(game_xbox_button)
free {user.game_xbox_button}: user.game_xbox_button_release(game_xbox_button)

# triggers
latch {user.game_gear}: user.game_xbox_left_trigger_set_gear(game_gear)
ratch {user.game_gear}: user.game_xbox_right_trigger_set_gear(game_gear)

# actions
weapon: user.game_xbox_button_press('lb')
wheel: user.rdr2_wheel()
reload | punch: user.game_xbox_button_press('x', 200)
aim: user.game_xbox_button_hold('lt')
shoot: user.game_xbox_button_hold('rt', 200)
pick: user.game_xbox_button_hold('lb')
call: user.game_xbox_button_press('dpad_up')
run: user.game_xbox_button_hold('a')

cam mid: user.game_reset_center_y()
look {user.game_dir}: user.game_camera_snap_dynamic(game_dir)
round: user.game_turn_180()

# gear <number_small>: user.game_gear_for_last_action(number_small)
halt | stop: user.game_stopper()

# [{user.game_modifier_button}] (dodge | block | jump | climb): user.vgamepad_x()

# gallop:
#     user.game_key("w")
#     sleep(100ms)
#     user.game_move_dir_hold_w()
# whoa there:
#     user.game_key("ctrl")
#     user.game_key("ctrl")
# mount | unmount: user.game_key("e")
# pick up: user.game_key_hold("r", 200)

# movement
# go: user.game_move_dir_toggle('up')
# go {user.game_dir}: user.game_move_dir_hold(game_dir)
# back: user.game_move_dir_toggle('down')

# {user.game_dir}: user.game_camera_continuous_dynamic(game_dir)
# {user.game_dir}: user.game_dir_preferred_action(game_dir)

# camera
# cam {user.game_dir}: user.game_camera_continuous_dynamic(game_dir)

# run: user.game_key_toggle("shift")

^game exit$:                user.game_mode_disable()