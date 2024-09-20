app: ryujinx
mode: user.game
-

# directions
<user.game_dir>: user.game_xbox_preferred_dir_mode(game_dir)
{user.game_xbox_left_stick}: user.game_xbox_left_stick_hold_dir("up")
{user.game_xbox_left_stick} <user.game_dir>: user.game_xbox_left_stick_hold_dir(game_dir)
{user.game_xbox_right_stick} <user.game_dir>: user.game_xbox_right_stick_hold_dir(game_dir)
{user.game_xbox_stick} {user.game_gear}: user.game_xbox_stick_set_gear(game_xbox_stick, game_gear)
{user.game_xbox_trigger} {user.game_gear}: user.game_xbox_trigger_set_gear(game_xbox_trigger, game_gear)
{user.game_xbox_dpad} {user.game_dir}: user.game_xbox_dpad_press_dir(game_dir)
hold {user.game_xbox_dpad} {user.game_dir}: user.game_xbox_dpad_hold_only_dir(game_dir)
hold <user.game_dir>: user.game_xbox_preferred_dir_mode(game_dir, "hold")

{user.game_xbox_left_stick} mode: user.game_xbox_preferred_dir_mode_set(game_xbox_left_stick)
{user.game_xbox_right_stick} mode: user.game_xbox_preferred_dir_mode_set(game_xbox_right_stick)
{user.game_xbox_dpad} mode: user.game_xbox_preferred_dir_mode_set(game_xbox_dpad, "press")

# buttons
[tap] {user.game_xbox_button}: user.game_xbox_button_press(game_xbox_button)
long {user.game_xbox_button}: user.game_xbox_button_hold(game_xbox_button, 1000)
longer {user.game_xbox_button}: user.game_xbox_button_hold(game_xbox_button, 4000)
hold {user.game_xbox_button}: user.game_xbox_button_hold(game_xbox_button)
free {user.game_xbox_button}: user.game_xbox_button_release(game_xbox_button)

# append a postfix to hold the button
# e.g. instead of "yank" say "yankee"
# e.g. instead of "bat" say "batter"
# e.g. instead of "ratch" say "ratcher"
{user.game_xbox_button} (ye | he | her | er | at): user.game_xbox_button_hold(game_xbox_button)
Erie | airy | error: user.game_xbox_button_hold("a")

# other camera actions
#round: user.game_turn_180()
#cam mid: user.game_reset_center_y()
#look <user.game_dir>: user.game_camera_snap_dynamic(game_dir)

# add noise actions to vocabulary
pop {user.game_xbox_button}: skip()
wish {user.game_xbox_button}: skip()

{user.dynamic_noise_mode}: user.dynamic_noises_use_mode(dynamic_noise_mode)

# actions
run:
    user.game_xbox_left_stick_hold_dir("up")
    user.game_xbox_button_hold('b', 3200)
jump: user.game_xbox_button_press('x')
attack: user.game_xbox_button_press('y')
aim: user.game_xbox_button_hold('lt')
shoot: user.game_xbox_button_hold('rt')
crouch: user.game_xbox_button_press('left_thumb')
scoper: user.game_xbox_button_press('right_thumb')
call: user.game_xbox_button_press('dpad_down')
throw: user.game_xbox_button_hold('rb')
# Change right hand ability
ultra hand: 
    user.game_xbox_button_hold('lb', 800)
    sleep(0.6)
    user.game_xbox_right_stick_hold_dir('left', 5)
    sleep(0.9)
    user.game_xbox_right_stick_stop()
ascend:
    user.game_xbox_button_hold('lb', 800)
    sleep(0.6)
    user.game_xbox_right_stick_hold_dir('down', 5)
    sleep(0.9)
    user.game_xbox_right_stick_stop()
fuse:
    user.game_xbox_button_hold('lb', 800)
    sleep(0.6)
    user.game_xbox_right_stick_hold_dir('up', 5)
    sleep(0.9)
    user.game_xbox_right_stick_stop()
recall:
    user.game_xbox_button_hold('lb', 800)
    sleep(0.6)
    user.game_xbox_right_stick_hold_dir('right', 5)
    sleep(0.9)
    user.game_xbox_right_stick_stop()
# Whilst using ultra hand
rotate: user.game_xbox_button_hold('rb')
twist: user.game_xbox_button_press('dpad_right')
flip: user.game_xbox_button_press('dpad_down')
unstick:
    user.game_xbox_right_stick_hold_dir('right', 5)
    sleep(0.2)
    user.game_xbox_right_stick_hold_dir('left', 5)
    sleep(0.2)
    user.game_xbox_right_stick_hold_dir('right', 5)
    sleep(0.2)
    user.game_xbox_right_stick_hold_dir('left', 5)
    sleep(0.2)
    user.game_xbox_right_stick_stop()
# Opens quick menu
item: user.game_xbox_button_hold('dpad_up')
weapon: user.game_xbox_button_hold('dpad_right')
purah: user.game_xbox_button_press('view')

stop:
    user.game_stopper()
    user.game_xbox_stopper()
game hide:
    user.ui_elements_hide_all()

^game exit$:                user.game_mode_disable()