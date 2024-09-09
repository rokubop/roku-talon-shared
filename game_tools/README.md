# Talon Game Tools (WIP)

This is an experimental repository for a full set of game actions and eventually automatically setting up a game for you. WIP.

## Actions
### Keys
| **Action**                     | **Action**                     | **Action**                     |
|---------------------------------|---------------------------------|---------------------------------|
| game_key                        | game_key_hold                  | game_key_release                |
| game_key_toggle                 | game_wasd_hold                 | game_wasd_hold_a                |
| game_wasd_hold_a_curved         | game_wasd_hold_d               | game_wasd_hold_d_curved         |
| game_wasd_hold_s                | game_wasd_hold_s_a             | game_wasd_hold_s_d              |
| game_wasd_hold_w                | game_wasd_hold_w_a             | game_wasd_hold_w_d              |
| game_wasd_toggle                | game_wasd_toggle_a             | game_wasd_toggle_d              |
| game_wasd_toggle_s              | game_wasd_toggle_w             | game_arrows_hold                |
| game_arrows_hold_down           | game_arrows_hold_down_horizontal| game_arrows_hold_down_left       |
| game_arrows_hold_down_right     | game_arrows_hold_left          | game_arrows_hold_right          |
| game_arrows_hold_up             | game_arrows_hold_up_horizontal | game_arrows_hold_up_left        |
| game_arrows_hold_up_right       | game_dir_hold_last_horizontal  | game_dir_toggle_last_horizontal |



### Mouse

You will need these settings to be accurate for angles to work properly.

```
settings():
    user.game_mouse_calibrate_x_360 = 2300
    user.game_mouse_calibrate_y_90 = 500
    user.mouse_move_api = "windows"
    # user.mouse_move_api = "talon"
```

| **Action**                     | **Action**                     | **Action**                     |
|---------------------------------|---------------------------------|---------------------------------|
| game_mouse_click               | game_mouse_move_continuous_right_10  | game_mouse_move_continuous_right_20  |
| game_mouse_click_left          | game_mouse_move_continuous_right_30  | game_mouse_move_continuous_right_5   |
| game_mouse_click_right         | game_mouse_move_continuous_left      | game_mouse_move_continuous_left_5    |
| game_mouse_click_middle        | game_mouse_move_continuous_left_10   | game_mouse_move_continuous_left_20   |
| game_mouse_hold_left           | game_mouse_move_continuous_left_30   | game_mouse_move_continuous_left_100  |
| game_mouse_hold_right          | game_mouse_move_continuous_stop      | game_mouse_move_deg_180              |
| game_mouse_hold_middle         | game_mouse_move_deg_360              | game_mouse_move_continuous_up        |
| game_mouse_move_deg_left_15    | game_mouse_move_continuous_up_5      | game_mouse_move_continuous_up_10     |
| game_mouse_move_deg_left_30    | game_mouse_move_continuous_up_20     | game_mouse_move_continuous_up_30     |
| game_mouse_move_deg_left_45    | game_mouse_move_continuous_down      | game_mouse_move_continuous_down_5    |
| game_mouse_move_deg_left_90    | game_mouse_move_continuous_down_10   | game_mouse_move_continuous_down_20   |
| game_mouse_move_deg_left       | game_mouse_move_continuous_down_30   | game_mouse_move_reset_center_y       |
| game_mouse_move_deg_right_15   | game_mouse_move_deg_up_15            | game_mouse_move_deg_up_30            |
| game_mouse_move_deg_right_30   | game_mouse_move_deg_up_45            | game_mouse_move_deg_up_90            |
| game_mouse_move_deg_right_45   | game_mouse_move_deg_down_15          | game_mouse_move_deg_down_30          |
| game_mouse_move_deg_right_90   | game_mouse_move_deg_down_45          | game_mouse_move_deg_down_75          |
| game_mouse_move_deg_right      | game_mouse_move_deg_down_90          | game_mouse_move_deg_down             |

### Other
| **Action** | **Action** | **Action** |
|------------|------------|------------|
| game_stopper | game_stop_all
| game_state_switch_horizontal | game_mouse_calibrate_x_360 | game_mouse_calibrate_y_90 |

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
| game_ui_element_arrows (WIP) | game_ui_element_wasd (WIP) | game_ui_element_xbox_left_stick |
| game_ui_element_xbox_right_stick | game_ui_element_xbox_primary_buttons | game_ui_element_xbox_dpad |
| game_ui_element_xbox_left_trigger | game_ui_element_xbox_right_trigger |  game_ui_element_xbox_left_bumper |
| game_ui_element_xbox_right_bumper |

## Modes
`user.game`
`user.game_calibrating_x`
`user.game_calibrating_y`

## Dependencies
- `roku-talon-shared/mouse_move_adv`
- `roku-talon-shared/vgamepad` if you use the `game_xbox_` actions
- `roku-talon-shared/ui_elements` if you use the `game_ui_element_` actions

See `manifest.json` for details.