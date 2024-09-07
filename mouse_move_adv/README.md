# Mouse Move Advanced (WIP)

This is an experimental repository. WIP. action names may change in the future. This is used for helping you turn in game and drag commands.

Mouse movement actions for Talon using a delta (dx, dy) or position(s) (x, y) over a duration of time, with control over the easing type, API (Windows or Talon), and callbacks.

## Actions

| **Action** | **Description** |
|------------|-----------------|
| `mouse_move_continuous` | Move the mouse continuously given a unit vector. |
| `mouse_move_continuous_towards` | Move the mouse continuously towards an xy screen position. |
| `mouse_move_continuous_stop` | Stop continuous mouse movement with optional debounce. l|
| `mouse_move_continuous_speed_increase` | Increase the speed of a current continuous movement.|
| `mouse_move_continuous_speed_decrease` | Decrease the speed of a current continuous movement.|
| `mouse_move_smooth_delta` | Move the mouse over a delta with control over the curve type, duration, mouse api type, and callback. |
| `mouse_move_smooth_delta_degrees` | Move the mouse by a number of degrees over a duration. |
| `mouse_move_smooth_from_to` | Move the mouse from one point to another over a duration. |
| `mouse_move_smooth_to` | Move the mouse to a point over a duration. |
| `mouse_move_smooth_from` | Move the mouse from a point to the current mouse position over a duration. |
| `mouse_move_smooth_queue` | Add to movement queue, executed after next mouse_stop. |
| `mouse_move_tick` | Jump the mouse a short distance in a specific direction. |
| `mouse_move_tick_down` | Jump the mouse a short distance down. |
| `mouse_move_tick_left` | Jump the mouse a short distance left. |
| `mouse_move_tick_right` | Jump the mouse a short distance right. |
| `mouse_move_tick_up` | Jump the mouse a short distance up. |
| `mouse_move_tick_last_direction` | Jump the mouse a short distance in the same direction of the last continuous movement. |
| `mouse_move_tick_reverse_last_direction` | Jump the mouse a short distance in the opposite direction of the last continuous movement. |
| `mouse_move_info` | Get mouse movement info |
| `mouse_move_event_dir_change_register` | Register callback event for mouse_move_dir_change. Will trigger when direction changes. |
| `mouse_move_event_dir_change_unregister` | Unregister event set by actions.user.mouse_move_event_dir_change_register. |
| `mouse_move_event_register` | Register callback event for mouse movement. Will trigger when movement starts or stops. |
| `mouse_move_event_unregister` | Unregister event set by actions.user.mouse_move_event_register. |
| `mouse_move_event_unregister_all` | Unregister all mouse movement events. |

## Settings
| **Setting** | **Type** | **Default** | **Description** |
|-------------|----------|-------------|-----------------|
| `mouse_move_api` | "talon" or "windows" | "talon" | Mouse API to use for mouse movement - talon or windows |
| `mouse_move_calibrate_x_360` | int | 2000 | The number of units to move the mouse to turn 360 degrees. |
| `mouse_move_calibrate_y_90` | int | 500 | The number of units to move the mouse to look up 90 degrees. |
| `mouse_move_continuous_speed_default` | int | 2 |  |
| `mouse_move_smooth_duration` | int | 200 |  |
| `mouse_move_tick_distance` | int | 50 |  |

## Dependencies
none