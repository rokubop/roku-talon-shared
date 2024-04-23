mode: user.cursorless_grid
-
^<user.cursorless_grid_target>$:
    user.cursorless_grid_move_mouse(cursorless_grid_target)
    mouse_click()
then <user.cursorless_grid_target> | <user.cursorless_grid_target> then:
    user.cursorless_grid_move_mouse(cursorless_grid_target)
    mouse_click()
[move | drag | bring] <user.cursorless_grid_target> (to | past) <user.cursorless_grid_target>:
    user.cursorless_grid_drag_and_drop(cursorless_grid_target_1, cursorless_grid_target_2)
^grid (hide | close | off)$: user.cursorless_grid_hide()
^(hide | close) grid$:      user.cursorless_grid_hide()
clear <user.cursorless_grid_target> (to | past) <user.cursorless_grid_target>:
    user.cursorless_grid_exclude_area_targets(cursorless_grid_target_1, cursorless_grid_target_2)
clear line <user.cursorless_grid_target>:
    user.cursorless_grid_exclude_line(cursorless_grid_target)
clear line <user.cursorless_grid_target> (to | past) <user.cursorless_grid_target>:
    user.cursorless_grid_exclude_line(cursorless_grid_target_1, cursorless_grid_target_2)
take <user.cursorless_grid_target> (to | past) <user.cursorless_grid_target>:
    user.cursorless_grid_isolate_area_targets(cursorless_grid_target_1 or cursorless_grid_target, cursorless_grid_target_2 or "")
grid (reset | full):        user.cursorless_grid_reset()
less squares:               user.cursorless_grid_more_squares()
more squares:               user.cursorless_grid_less_squares()
grid bottom:
    user.cursorless_grid_reset()
    user.cursorless_grid_exclude_area_rect(0, 0, 1980, 800)
    user.cursorless_grid_show()
grid left:
    user.cursorless_grid_reset()
    user.cursorless_grid_exclude_area_rect(0, 0, 1000, 800)
    user.cursorless_grid_show()
bring this to <user.cursorless_grid_target>: user.cursorless_grid_bring_to(cursorless_grid_target)
bring <user.cursorless_grid_target>: user.cursorless_grid_bring(cursorless_grid_target)
hover <user.cursorless_grid_target>: user.cursorless_move_mouse_to_target(cursorless_grid_target)
