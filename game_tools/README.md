# Talon Game Tools (WIP)

This is an experimental repository for a full set of game actions and eventually automatically setting up a game for you. WIP.

## Commands

- "game create files" command will automatically create a directory and talon files for you based on the game you currently have focused, at the directory based on `game_tools/user_game_settings`, using template `game_tools/templates/fp/template_roku_14_parrot.py`. I plan to make this more configurable in the future.
- You can say "game calibrate" to start calibrating in-game for your x and y movement commands (third person or first person game). You'll need to copy the values to the respective code in your talon file for that game:
```
settings():
    user.game_calibrate_x_360 = 2300
    user.game_calibrate_y_90 = 500
```

## Actions
| **Action** |
|------------|
| game_key |
| game_key_down |
| game_key_up |
| game_key_hold |
| game_key_toggle |
| game_mouse_click |
| game_mouse_click_left |
| game_mouse_click_right |
| game_mouse_click_middle |
| game_mouse_hold_left |
| game_mouse_hold_right |
| game_mouse_hold_middle |
| game_move_dir_hold_a |
| game_move_dir_hold_d |
| game_move_dir_hold_w |
| game_move_dir_hold_s |
| game_move_dir_hold_a_curved |
| game_move_dir_hold_d_curved |
| game_move_dir_hold_w_a |
| game_move_dir_hold_w_d |
| game_move_dir_hold_s_a |
| game_move_dir_hold_s_d |
| game_move_dir_hold_left |
| game_move_dir_hold_right |
| game_move_dir_hold_up |
| game_move_dir_hold_down |
| game_move_dir_hold_up_left |
| game_move_dir_hold_up_right |
| game_move_dir_hold_up_horizontal |
| game_move_dir_hold_down_left |
| game_move_dir_hold_down_right |
| game_move_dir_hold_down_horizontal |
| game_move_dir_hold_last_horizontal |
| game_move_dir_toggle_last_horizontal |
| game_move_dir_toggle_a |
| game_move_dir_toggle_d |
| game_move_dir_toggle_w |
| game_move_dir_toggle_s |
| game_move_dir_step_a |
| game_move_dir_step_d |
| game_move_dir_step_w |
| game_move_dir_step_s |
| game_stopper |
| game_stop_all |
| game_turn_left_15 |
| game_turn_left_30 |
| game_turn_left_45 |
| game_turn_left_60 |
| game_turn_left_75 |
| game_turn_left_90 |
| game_turn_left |
| game_turn_right_15 |
| game_turn_right_30 |
| game_turn_right_45 |
| game_turn_right_60 |
| game_turn_right_75 |
| game_turn_right_90 |
| game_turn_right |
| game_turn_right_continuous |
| game_turn_right_continuous_5 |
| game_turn_right_continuous_10 |
| game_turn_right_continuous_20 |
| game_turn_right_continuous_30 |
| game_turn_right_continuous_50 |
| game_turn_right_continuous_100 |
| game_turn_left_continuous |
| game_turn_left_continuous_5 |
| game_turn_left_continuous_10 |
| game_turn_left_continuous_20 |
| game_turn_left_continuous_30 |
| game_turn_left_continuous_50 |
| game_turn_left_continuous_100 |
| game_turn_continuous_stop |
| game_turn_180 |
| game_turn_360 |
| game_look_up_continuous |
| game_look_up_continuous_5 |
| game_look_up_continuous_10 |
| game_look_up_continuous_20 |
| game_look_up_continuous_30 |
| game_look_up_continuous_50 |
| game_look_up_continuous_100 |
| game_look_down_continuous |
| game_look_down_continuous_5 |
| game_look_down_continuous_10 |
| game_look_down_continuous_20 |
| game_look_down_continuous_30 |
| game_look_down_continuous_50 |
| game_look_down_continuous_100 |
| game_look_continuous_stop |
| game_look_up_15 |
| game_look_up_30 |
| game_look_up_45 |
| game_look_up_60 |
| game_look_up_75 |
| game_look_up_90 |
| game_look_up |
| game_look_down_15 |
| game_look_down_30 |
| game_look_down_45 |
| game_look_down_60 |
| game_look_down_75 |
| game_look_down_90 |
| game_look_down |
| game_reset_center_y |
| game_state_switch_horizontal |
| game_calibrate_x_360 |
| game_calibrate_y_90 |
