mode: user.drag_grid
-
^<user.drag_grid_target>$:
    user.drag_grid_move_mouse(drag_grid_target)
    mouse_click()
then <user.drag_grid_target> | <user.drag_grid_target> then:
    user.drag_grid_move_mouse(drag_grid_target)
    mouse_click()

drag <user.drag_grid_target> (to | past) <user.drag_grid_target>:
    user.drag_grid_drag_and_drop(drag_grid_target_1, drag_grid_target_2, 0)
pan <user.drag_grid_target> (to | past) <user.drag_grid_target>:
    user.drag_grid_drag_and_drop(drag_grid_target_1, drag_grid_target_2, 2)
roll <user.drag_grid_target> (to | past) <user.drag_grid_target>:
    user.drag_grid_drag_and_drop(drag_grid_target_1, drag_grid_target_2, 1)

<user.drag_grid_target_loop>:
    user.drag_grid_move_to_target_loop(drag_grid_target_loop_list)

drag <user.drag_grid_target_loop>:
    user.drag_grid_drag_to_target_loop(drag_grid_target_loop_list, 0)
pan <user.drag_grid_target_loop>:
    user.drag_grid_drag_to_target_loop(drag_grid_target_loop_list, 2)
roll <user.drag_grid_target_loop>:
    user.drag_grid_drag_to_target_loop(drag_grid_target_loop_list, 1)

swipe <user.drag_grid_target> left:
    user.drag_grid_move_mouse(drag_grid_target)
    user.rt_mouse_move_delta(-200, 0)

drag grid:                  user.drag_grid_hide()
^grid (hide | close | off)$: user.drag_grid_hide()
^(hide | close) grid$:      user.drag_grid_hide()

clear <user.drag_grid_target> (to | past) <user.drag_grid_target>:
    user.drag_grid_exclude_area_targets(drag_grid_target_1, drag_grid_target_2)
clear line <user.drag_grid_target>:
    user.drag_grid_exclude_line(drag_grid_target)
clear line <user.drag_grid_target> (to | past) <user.drag_grid_target>:
    user.drag_grid_exclude_line(drag_grid_target_1, drag_grid_target_2)

take <user.drag_grid_target> (to | past) <user.drag_grid_target>:
    user.drag_grid_isolate_area_targets(drag_grid_target_1 or drag_grid_target, drag_grid_target_2 or "")
grid (reset | full):        user.drag_grid_reset()
less squares:               user.drag_grid_more_squares()
more squares:               user.drag_grid_less_squares()
grid bottom:
    user.drag_grid_reset()
    user.drag_grid_exclude_area_rect(0, 0, 1980, 800)
    user.drag_grid_show()
grid left:
    user.drag_grid_reset()
    user.drag_grid_exclude_area_rect(0, 0, 1000, 800)
    user.drag_grid_show()

bring this to <user.drag_grid_target>: user.drag_grid_bring_to(drag_grid_target)
bring <user.drag_grid_target>: user.drag_grid_bring(drag_grid_target)
hover <user.drag_grid_target>: user.cursorless_move_mouse_to_target(drag_grid_target)

fly to <user.drag_grid_target>: user.drag_grid_fly_towards(drag_grid_target)
fly stop:                   user.drag_grid_stop()
fly up:                     user.mouse_move_continuous(0, -1)
fly down:                   user.mouse_move_continuous(0, 1)
fly left:                   user.mouse_move_continuous(-1, 0)
fly right:                  user.mouse_move_continuous(1, 0)
# tick vs take
tick:                       user.mouse_tick_last_direction()
tick down:                  user.mouse_tick_direction(0, 1)
tick up:                    user.mouse_tick_direction(0, -1)
tick left:                  user.mouse_tick_direction(-1, 0)
tick right:                 user.mouse_tick_direction(1, 0)
tick back:                  user.mouse_tick_reverse_last_direction()
speedup:                    user.mouse_speed_increase()
slowdown:                   user.mouse_speed_decrease()

<user.drag_grid_target> up:
    user.drag_grid_move_mouse(drag_grid_target)
    user.mouse_move_continuous(0, -1)
<user.drag_grid_target> down:
    user.drag_grid_move_mouse(drag_grid_target)
    user.mouse_move_continuous(0, 1)
<user.drag_grid_target> left:
    user.drag_grid_move_mouse(drag_grid_target)
    user.mouse_move_continuous(-1, 0)
<user.drag_grid_target> right:
    user.drag_grid_move_mouse(drag_grid_target)
    user.mouse_move_continuous(1, 0)
