tag: user.game_3d_commands
mode: user.game
app: bg_3
# app: hi_fi_rush
-
# parrot(hiss): user.game_stopper()
# parrot(pop): user.game_mouse_click_left()

<user.letter>: key(letter)
<user.modifiers>: key(modifiers)
hold <user.keys>: key("{keys}:down")
hold <user.modifiers>: key("{modifiers}:down")

each:
    user.game_key("e")
    user.game_set_noise_mode("talker")
hold each:
    user.game_key("e:down")
talk:
    user.game_key("e")
    user.game_set_noise_mode("talker")
hook: user.game_key("q")
go left: user.game_move_dir_hold_a()
go right: user.game_move_dir_hold_d()
# [go] left: user.game_move_dir_hold_a()
# ^left$: user.game_move_dir_hold_a()
# [go] right: user.game_move_dir_hold_d()
# ^right$: user.game_move_dir_hold_d()
[go] back: user.game_move_dir_hold_s()
walk: user.game_move_dir_step_w()
walk left: user.game_move_dir_step_a()
walk right: user.game_move_dir_step_d()
walk back: user.game_move_dir_step_s()
go:
    user.game_on_go()
    user.game_move_dir_hold_w()
jump:
    key(space)
    user.game_set_noise_mode("jumper")
hit | fight:
    user.game_mouse_click_left()
    user.game_set_noise_mode("fighter")
heavy:
    user.game_mouse_click_right()
    user.game_set_noise_mode("heavy")
dash: user.game_key("shift")
^stop$: user.game_stopper()
stop: user.game_stopper()
crouch: user.game_key_toggle("ctrl")
run: user.game_key_toggle("shift")
# hop: user.game_jump_forward()
round: user.game_turn_180()
(cam | look) left:
    user.game_turn_left_90()
    user.game_set_noise_mode("fighter")
(cam | look) right:
    user.game_turn_right_90()
    user.game_set_noise_mode("fighter")
left: user.game_left_dynamic()
right: user.game_right_dynamic()
up: user.game_up_dynamic()
down: user.game_down_dynamic()
look (back | round): user.game_turn_180()
turn left: user.game_turn_left_continuous_5()
turn right: user.game_turn_right_continuous_5()
# left: user.game_turn_left_continuous_5()
# right: user.game_turn_right_continuous_5()
mid left: user.game_turn_left_45()
mid right: user.game_turn_right_45()
lil left: user.game_turn_left_15()
lil right: user.game_turn_right_15()
(tie | tiny) left: user.game_turn_left(2)
(tie | tiny) right: user.game_turn_right(2)
look up: user.game_look_up_continuous_5()
look down: user.game_look_down_continuous_5()
mid: user.game_reset_center_y()
exit: user.game_mode_disable()

# pop jump: user.game_set_noise_mode("jumper")
# pop fight: user.game_set_noise_mode("fighter")

clicker: user.game_set_noise_mode("clicker")
tracker: user.game_set_noise_mode("tracker")
pepper: user.game_set_noise_mode("pepper")
menu: user.game_set_noise_mode("menu")
dasher: user.game_set_noise_mode("dasher")
spammer: user.game_set_noise_mode("spammer")
mover: user.game_set_noise_mode("mover")
talker: user.game_set_noise_mode("talker")
fighter: user.game_set_noise_mode("fighter")
jumper: user.game_set_noise_mode("jumper")
repeater: user.game_set_noise_mode("repeater")
hooker: user.game_set_noise_mode("hooker")
# heavy: user.game_set_noise_mode("heavy")
jump fight: user.game_set_noise_mode("jump_fight")

# pop repeater
# hiss stopper
