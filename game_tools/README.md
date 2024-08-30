# Talon Game Tools (WIP)

This is an experimental repository for a full set of game actions and eventually automatically setting up a game for you. WIP.

## Commands

- (WIP - not for use yet) "game create files" command will automatically create a directory and talon files for you based on the game you currently have focused.
- (WIP - not for use yet) You can say "game calibrate" to start calibrating in-game for your x and y movement commands

## Actions
### Keys
| **Action**                     | **Action**                     | **Action**                     |
|--------------------------------|--------------------------------|--------------------------------|
| game_key                       | game_key_down                  | game_key_up                    |
| game_key_hold                  | game_key_toggle                | game_move_dir_hold_a           |
| game_move_dir_hold_d           | game_move_dir_hold_w           | game_move_dir_hold_s           |
| game_move_dir_hold_a_curved    | game_move_dir_hold_d_curved    | game_move_dir_hold_w_a         |
| game_move_dir_hold_w_d         | game_move_dir_hold_s_a         | game_move_dir_hold_s_d         |
| game_move_dir_hold_left        | game_move_dir_hold_right       | game_move_dir_hold_up          |
| game_move_dir_hold_down        | game_move_dir_hold_up_left     | game_move_dir_hold_up_right    |
| game_move_dir_hold_up_horizontal| game_move_dir_hold_down_left   | game_move_dir_hold_down_right  |
| game_move_dir_hold_down_horizontal| game_move_dir_hold_last_horizontal| game_move_dir_toggle_last_horizontal |
| game_move_dir_toggle_a         | game_move_dir_toggle_d         | game_move_dir_toggle_w         |
| game_move_dir_toggle_s         | game_move_dir_step_a           | game_move_dir_step_d           |


### Mouse

You will need these settings to be accurate for angles to work properly.

```
settings():
    user.game_calibrate_x_360 = 2300
    user.game_calibrate_y_90 = 500
    user.mouse_move_api = "windows"
    # user.mouse_move_api = "talon"
```

| **Action**                     | **Action**                     | **Action**                     |
|--------------------------------|--------------------------------|--------------------------------|
| game_mouse_click               | game_turn_right_continuous_10  | game_turn_right_continuous_20  |
| game_mouse_click_left          | game_turn_right_continuous_30  | game_turn_right_continuous_50  |
| game_mouse_click_right         | game_turn_right_continuous_100 | game_turn_left_continuous      |
| game_mouse_click_middle        | game_turn_left_continuous_5    | game_turn_left_continuous_10   |
| game_mouse_hold_left           | game_turn_left_continuous_20   | game_turn_left_continuous_30   |
| game_mouse_hold_right          | game_turn_left_continuous_50   | game_turn_left_continuous_100  |
| game_mouse_hold_middle         | game_turn_continuous_stop      | game_turn_180                  |
| game_turn_left_15              | game_turn_360                  | game_look_up_continuous        |
| game_turn_left_30              | game_look_up_continuous_5      | game_look_up_continuous_10     |
| game_turn_left_45              | game_look_up_continuous_20     | game_look_up_continuous_30     |
| game_turn_left_60              | game_look_up_continuous_50     | game_look_up_continuous_100    |
| game_turn_left_75              | game_look_down_continuous      | game_look_down_continuous_5    |
| game_turn_left_90              | game_look_down_continuous_10   | game_look_down_continuous_20   |
| game_turn_left                 | game_look_down_continuous_30   | game_look_down_continuous_50   |
| game_turn_right_15             | game_look_down_continuous_100  | game_look_continuous_stop      |
| game_turn_right_30             | game_look_up_15                | game_look_up_30                |
| game_turn_right_45             | game_look_up_45                | game_look_up_60                |
| game_turn_right_60             | game_look_up_75                | game_look_up_90                |
| game_turn_right_75             | game_look_up                   | game_look_down_15              |
| game_turn_right_90             | game_look_down_30              | game_look_down_45              |
| game_turn_right                | game_look_down_60              | game_look_down_75              |
| game_turn_right_continuous      | game_look_down_90              | game_look_down                 |
| game_turn_right_continuous_5    | game_reset_center_y            |                                |


### Other
| **Action** | **Action** | **Action** |
|------------|------------|------------|
| game_stopper | game_stop_all
| game_state_switch_horizontal | game_calibrate_x_360 | game_calibrate_y_90 |

### Xbox Gamepad

| **Action** | **Action** | **Action** |
|------------|------------|------------|
| game_xbox_gamepad_enable | game_xbox_left_stick_set_gear | game_xbox_trigger_set_gear |
| game_xbox_gamepad_disable | game_xbox_left_stick_stop | game_xbox_left_trigger |
| game_xbox_button_press | game_xbox_right_stick_hold_dir | game_xbox_left_trigger_hold |
| game_xbox_button_release | game_xbox_right_stick_set_gear | game_xbox_left_trigger_release |
| game_xbox_button_hold | game_xbox_right_stick_stop | game_xbox_left_trigger_set_gear |
| game_xbox_button_toggle | game_xbox_dpad_press_dir | game_xbox_right_trigger |
| game_xbox_stick_hold_dir | game_xbox_dpad_hold_only_dir | game_xbox_right_trigger_hold |
| game_xbox_stick_set_gear | game_xbox_trigger | game_xbox_right_trigger_release |
| game_xbox_stick_stop | game_xbox_trigger_hold | game_xbox_right_trigger_set_gear |
| game_xbox_left_stick_hold_dir | game_xbox_trigger_release | game_xbox_stopper |

### UI Elements

UI components built with `ui_elements` that you can place inside of other `ui_elements`. Automatically recieve state from game actions.

| **Action** | **Action** | **Action** |
|------------|------------|------------|
| game_ui_element_arrows_dpad (WIP) | game_ui_element_wasd_dpad (WIP) | game_ui_element_xbox_left_stick |
| game_ui_element_xbox_right_stick | game_ui_element_xbox_primary_buttons | game_ui_element_xbox_dpad |
| game_ui_element_xbox_left_trigger | game_ui_element_xbox_right_trigger |  game_ui_element_xbox_left_bumper |
| game_ui_element_xbox_right_bumper |

## Modes
`user.game`
`user.game_calibrating_x`
`user.game_calibrating_y`