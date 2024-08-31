mode: user.drag_mode
-
^<user.drag_mode_target>$:
    user.drag_mode_move_mouse(drag_mode_target)
    mouse_click()
then <user.drag_mode_target> | <user.drag_mode_target> then:
    user.drag_mode_move_mouse(drag_mode_target)
    mouse_click()

drag <user.drag_mode_target> (to | past) <user.drag_mode_target>:
    user.drag_mode_drag_and_drop(drag_mode_target_1, drag_mode_target_2, 0)
pan <user.drag_mode_target> (to | past) <user.drag_mode_target>:
    user.drag_mode_drag_and_drop(drag_mode_target_1, drag_mode_target_2, 2)
roll <user.drag_mode_target> (to | past) <user.drag_mode_target>:
    user.drag_mode_drag_and_drop(drag_mode_target_1, drag_mode_target_2, 1)

center <user.drag_mode_target>: user.drag_mode_bring_to_center(drag_mode_target, 0)

<user.drag_mode_target> (to | past) <user.drag_mode_target>:
    user.drag_mode_drag_and_drop(drag_mode_target_1, drag_mode_target_2, 0)

# <user.drag_mode_target_loop>:
#     user.drag_mode_move_to_target_loop(drag_mode_target_loop_list)

# drag <user.drag_mode_target_loop>:
#     user.drag_mode_drag_to_target_loop(drag_mode_target_loop_list, 0)
# pan <user.drag_mode_target_loop>:
#     user.drag_mode_drag_to_target_loop(drag_mode_target_loop_list, 2)
# roll <user.drag_mode_target_loop>:
#     user.drag_mode_drag_to_target_loop(drag_mode_target_loop_list, 1)

swipe <user.drag_mode_target> left:
    user.drag_mode_move_mouse(drag_mode_target)
    user.mouse_move_delta_smooth(-200, 0)

drag (grid | mode | off | hide): user.drag_mode_hide()
^grid (hide | close | off)$: user.drag_mode_hide()
^(hide | close) grid$: user.drag_mode_hide()

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

bring this to <user.drag_mode_target>: user.drag_mode_bring_to(drag_mode_target)
bring <user.drag_mode_target>: user.drag_mode_bring(drag_mode_target)
(go | hover) <user.drag_mode_target>: user.drag_mode_move_mouse_to_target(drag_mode_target)

fly [to] <user.drag_mode_target>: user.drag_mode_fly_towards(drag_mode_target)
fly up: user.mouse_move_continuous(0, -1)
fly down: user.mouse_move_continuous(0, 1)
fly left: user.mouse_move_continuous(-1, 0)
fly right: user.mouse_move_continuous(1, 0)
fly stop: user.drag_mode_stop()
mouse stop: user.mouse_stop()
stop | halt: user.drag_mode_stop()

tick: user.mouse_move_tick_last_direction()
tick down: user.mouse_move_tick_direction(0, 1)
tick up: user.mouse_move_tick_direction(0, -1)
tick left: user.mouse_move_tick_direction(-1, 0)
tick right: user.mouse_move_tick_direction(1, 0)
tick back: user.mouse_move_tick_reverse_last_direction()
gear up: user.mouse_move_speed_increase()
gear down: user.mouse_move_speed_decrease()

<user.drag_mode_target> up:
    user.drag_mode_move_mouse(drag_mode_target)
    user.mouse_move_continuous(0, -1)
<user.drag_mode_target> down:
    user.drag_mode_move_mouse(drag_mode_target)
    user.mouse_move_continuous(0, 1)
<user.drag_mode_target> left:
    user.drag_mode_move_mouse(drag_mode_target)
    user.mouse_move_continuous(-1, 0)
<user.drag_mode_target> right:
    user.drag_mode_move_mouse(drag_mode_target)
    user.mouse_move_continuous(1, 0)
