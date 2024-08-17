app: rdr2
mode: user.game
-

# gamepad(dpad_up):           "up"
# gamepad(dpad_down):         "down"
# gamepad(dpad_left):         "left"
# gamepad(dpad_right):        "right"

# gamepad(west:down):         "wd"
# gamepad(west:up):           "wu"
# gamepad(north:down):        "nd"
# gamepad(north:up):          "nu"
# gamepad(east:down):         "east"
# gamepad(east:up):           "eastup"
# gamepad(south:down):        "Southdown"
# gamepad(south:up):          "Southup"

green: user.vgamepad_a()
blue: user.vgamepad_b()
red: user.vgamepad_x()
yell: user.vgamepad_y()
left: user.vgamepad_left()
right: user.vgamepad_right()
up: user.vgamepad_up()
down: user.vgamepad_down()
go left: user.vgamepad_left()
go right: user.vgamepad_right()
go up: user.vgamepad_up()
go down: user.vgamepad_down()

# gamepad(select):            user.quick_pick_show()
# gamepad(start):             user.command_dictation_mode_toggle()

# gamepad(l1):                user.go_back()
# gamepad(r1):                user.go_forward()

# gamepad(l2:change):         user.gamepad_scroll(0, value*-1)
# gamepad(r2:change):         user.gamepad_scroll(0, value)

# gamepad(left_xy):           user.gamepad_scroll(x, y*-1)
# gamepad(l3):                user.gamepad_scroll_slow_toggle()

# gamepad(right_xy:repeat):   user.gamepad_mouse_move(x, y*-1)
# gamepad(r3):

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
gallop:
    user.game_key("w")
    sleep(100ms)
    user.game_move_dir_hold_w()
whoa there:
    user.game_key("ctrl")
    user.game_key("ctrl")
mount | unmount: user.game_key("e")
pick up: user.game_key_hold("r", 200)
wheel: user.rdr2_wheel()

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