mode: user.drag_mode
-
###################
# Actions
###################
# air bat
^<user.drag_mode_target>$:
    user.drag_mode_move_mouse(drag_mode_target)
    mouse_click()
# "drag air bat to sun plex"
{user.drag_mode_mouse_button} <user.drag_mode_target> (to | past) <user.drag_mode_target>:
    user.drag_mode_drag_and_drop(drag_mode_target_1, drag_mode_target_2, drag_mode_mouse_button)
# "drag left"
^{user.drag_mode_mouse_button} {user.drag_mode_dir}$:
    user.drag_mode_mouse_drag(drag_mode_mouse_button)
    user.drag_mode_mouse_move_continuous_dir(drag_mode_dir)
# "drag air bat up", "pan sun plex down", "roll red harp left"
{user.drag_mode_mouse_button} <user.drag_mode_target> {user.drag_mode_dir}:
    user.drag_mode_move_mouse(drag_mode_target)
    user.drag_mode_mouse_drag(drag_mode_mouse_button)
    user.drag_mode_mouse_move_continuous_dir(drag_mode_dir)
# "air bat up"
<user.drag_mode_target> {user.drag_mode_dir}:
    user.drag_mode_move_mouse(drag_mode_target)
    user.drag_mode_mouse_move_continuous_dir(drag_mode_dir)
# "up", "left"
^{user.drag_mode_dir}$: user.drag_mode_mouse_move_continuous_dir(drag_mode_dir)
[bring] <user.drag_mode_target> (to | past) <user.drag_mode_target>:
    user.drag_mode_drag_and_drop(drag_mode_target_1, drag_mode_target_2)
bring <user.drag_mode_target>: user.drag_mode_bring(drag_mode_target)
bring <user.drag_mode_target> {user.drag_mode_dir}:
    user.drag_mode_move_mouse(drag_mode_target)
    user.drag_mode_mouse_drag()
    user.drag_mode_mouse_move_continuous_dir(drag_mode_dir)
bring this to <user.drag_mode_target>: user.drag_mode_bring_to(drag_mode_target)
center <user.drag_mode_target>: user.drag_mode_bring_to_center(drag_mode_target)
(go | hover) <user.drag_mode_target>: user.drag_mode_move_mouse_to_target(drag_mode_target)
go {user.drag_mode_dir}: user.drag_mode_mouse_move_continuous_dir(drag_mode_dir, 5)
go stop: user.drag_mode_stop()
fly [to] <user.drag_mode_target>: user.drag_mode_fly_towards(drag_mode_target)
fly {user.drag_mode_dir}: user.drag_mode_mouse_move_continuous_dir(drag_mode_dir)
fly stop: user.drag_mode_stop()
swipe {user.drag_mode_dir}:
    user.drag_mode_swipe_dir(drag_mode_dir)
swipe <user.drag_mode_target> {user.drag_mode_dir}:
    user.drag_mode_move_mouse(drag_mode_target)
    user.drag_mode_swipe_dir(drag_mode_dir)
tick: user.mouse_move_tick_last_direction()
tick down: user.mouse_move_tick(0, 1)
tick up: user.mouse_move_tick(0, -1)
tick left: user.mouse_move_tick(-1, 0)
tick right: user.mouse_move_tick(1, 0)
tick back: user.mouse_move_tick_reverse_last_direction()

gear up: user.mouse_move_continuous_speed_increase()
gear down: user.mouse_move_continuous_speed_decrease()

mouse stop: user.mouse_stop()
stop | halt: user.drag_mode_stop()

# "air bat then sun plex then red harp"
then <user.drag_mode_target> | <user.drag_mode_target> then:
    user.drag_mode_move_mouse(drag_mode_target)
    mouse_click()

################
# Layout actions
################
clear <user.drag_mode_target> (to | past) <user.drag_mode_target>:
    user.drag_mode_exclude_area_targets(drag_mode_target_1, drag_mode_target_2)
clear line <user.drag_mode_target>:
    user.drag_mode_exclude_line(drag_mode_target)
clear line <user.drag_mode_target> (to | past) <user.drag_mode_target>:
    user.drag_mode_exclude_line(drag_mode_target_1, drag_mode_target_2)
take <user.drag_mode_target> (to | past) <user.drag_mode_target>:
    user.drag_mode_isolate_area_targets(drag_mode_target_1 or drag_mode_target, drag_mode_target_2 or "")
grid (reset | full): user.drag_mode_reset()
less squares: user.drag_mode_more_squares()
more squares: user.drag_mode_less_squares()
grid bottom:
    user.drag_mode_reset()
    user.drag_mode_exclude_area_rect(0, 0, 1980, 800)
    user.drag_mode_show()
commands {user.drag_mode_dir}: user.drag_mode_show_commands(drag_mode_dir)
commands hide: user.ui_elements_hide_all()
commands show: user.drag_mode_show_commands()

################
# Mode actions
################
drag (grid | mode | off | hide): user.drag_mode_hide()
^grid (hide | close | off)$: user.drag_mode_hide()
^(hide | close) grid$: user.drag_mode_hide()

# <user.drag_mode_target_loop>:
#     user.drag_mode_move_to_target_loop(drag_mode_target_loop_list)

# {user.drag_mode_mouse_button} <user.drag_mode_target_loop>:
#     user.drag_mode_drag_to_target_loop(drag_mode_target_loop_list, drag_mode_mouse_button)