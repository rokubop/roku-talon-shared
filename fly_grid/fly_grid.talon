mode: user.fly_grid
-
^<user.fly_grid_target>$:
    user.fly_grid_move_mouse(fly_grid_target)
    mouse_click()
then <user.fly_grid_target> | <user.fly_grid_target> then:
    user.fly_grid_move_mouse(fly_grid_target)
    mouse_click()
[move | drag | bring] <user.fly_grid_target> (to | past) <user.fly_grid_target>:
    user.fly_grid_drag_and_drop(fly_grid_target_1, fly_grid_target_2)
^grid (hide | close | off)$: user.fly_grid_hide()
^(hide | close) grid$:      user.fly_grid_hide()
clear <user.fly_grid_target> (to | past) <user.fly_grid_target>:
    user.fly_grid_exclude_area_targets(fly_grid_target_1, fly_grid_target_2)
clear line <user.fly_grid_target>:
    user.fly_grid_exclude_line(fly_grid_target)
clear line <user.fly_grid_target> (to | past) <user.fly_grid_target>:
    user.fly_grid_exclude_line(fly_grid_target_1, fly_grid_target_2)
take <user.fly_grid_target> (to | past) <user.fly_grid_target>:
    user.fly_grid_isolate_area_targets(fly_grid_target_1 or fly_grid_target, fly_grid_target_2 or "")
grid (reset | full):        user.fly_grid_reset()
less squares:               user.fly_grid_more_squares()
more squares:               user.fly_grid_less_squares()
grid bottom:
    user.fly_grid_reset()
    user.fly_grid_exclude_area_rect(0, 0, 1980, 800)
    user.fly_grid_show()
grid left:
    user.fly_grid_reset()
    user.fly_grid_exclude_area_rect(0, 0, 1000, 800)
    user.fly_grid_show()
bring this to <user.fly_grid_target>: user.fly_grid_bring_to(fly_grid_target)
bring <user.fly_grid_target>: user.fly_grid_bring(fly_grid_target)
hover <user.fly_grid_target>: user.cursorless_move_mouse_to_target(fly_grid_target)
fly to <user.fly_grid_target>: user.fly_grid_fly_towards(fly_grid_target)
fly stop:                   user.fly_grid_stop()
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
