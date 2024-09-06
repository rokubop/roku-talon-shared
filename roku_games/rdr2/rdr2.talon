.tar.app: rdr2
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
round: user.game_mouse_move_deg_180()
cam mid: user.game_mouse_move_reset_center_y()
look <user.game_dir>: user.game_mouse_move_deg_dynamic(game_dir)
look back: user.game_xbox_button_hold('right_thumb')

# add noise actions to vocabulary
pop {user.game_xbox_button}: skip()
wish {user.game_xbox_button}: skip()

{user.dynamic_noise_mode}: user.dynamic_noises_use_mode(dynamic_noise_mode)

# actions
weapon | gun: user.game_xbox_button_press('lb')
wheel: user.rdr2_wheel()
jump | greet: user.game_xbox_button_press('x')
reload | punch: user.game_xbox_button_press('b', 200)
aim | target | talk: user.game_xbox_button_hold('lt')
shoot: user.game_xbox_button_hold('rt', 200)
skin | loot | hitch: user.game_xbox_button_hold('y')
stow: user.game_xbox_button_hold('x')
pick: user.game_xbox_button_hold('lb')
call: user.game_xbox_button_press('dpad_up')
run: 
    user.game_xbox_left_stick_hold_dir("up")
    user.game_xbox_button_hold('a')
sell | satchel: user.game_xbox_button_hold('dpad_right')
hide: user.game_xbox_button_press('rb')
crouch: user.game_xbox_button_press('left_thumb')
scope: user.game_xbox_button_press('dpad_down')

(dead | dot | did) (eye | I): 
    user.game_xbox_button_press('right_thumb')
    user.game_xbox_button_press('left_thumb')
    
halt | stop:
    user.game_stopper()
    user.game_xbox_stopper()

^game exit$:                user.game_mode_disable()