# Mouse Move Advanced (WIP)

This is an experimental repository. WIP. action names may change in the future. This is used for helping you turn in game and drag commands.

Mouse movement actions for Talon using a delta (dx, dy) or position(s) (x, y) over a duration of time, with control over the easing type, API (Windows or Talon), and callbacks.

## Actions

| **Action** | **Description** |
|------------|-----------------|
| `mouse_move_delta_smooth` | Move the mouse over a delta with control over the curve type, duration, mouse api type, and callback. |
| `mouse_move_from_to` | Move the mouse from one point to another over a duration. |
| `mouse_move_to` | Move the mouse to a point over a duration. |
| `mouse_move_from` | Move the mouse from a point over a duration. |
| `mouse_move_delta_degrees` | Move the mouse by a number of degrees over a duration. |
| `mouse_move_queue` | Add to movement queue, executed after next mouse_stop. |
| `mouse_move_continuous` | Move the mouse continuously given a unit vector. |
| `mouse_move_continuous_towards` | Move the mouse continuously towards an xy screen position. |
| `mouse_move_continuous_stop` | Stop continuous mouse movement with optional debounce. l|
| `mouse_move_tick_last_direction` | Jump the mouse a short distance in the same direction of the last continuous movement. |
| `mouse_move_tick_reverse_last_direction` | Jump the mouse a short distance in the opposite direction of the last continuous movement. |
| `mouse_move_tick_direction` | Jump the mouse a short distance in a specific direction. |
| `mouse_move_speed_increase` | Increase the speed of a current continuous movement.|
| `mouse_move_speed_decrease` | Decrease the speed of a current continuous movement.|
| `mouse_move_info` | Get mouse movement info |
| `mouse_move_event_register` | Register callback event for mouse movement. Will trigger when movement starts or stops. |
| `mouse_move_event_unregister` | Unregister event set by actions.user.mouse_move_event_register. |
| `mouse_move_dir_change_event_register` | Register callback event for mouse_move_dir_change. Will trigger when direction changes. |
| `mouse_move_dir_change_event_unregister` | Unregister event set by actions.user.mouse_move_dir_change_event_register. |
| `mouse_move_event_unregister_all` | Unregister all mouse movement events. |

## Settings
| **Setting** | **Type** | **Default** | **Description** |
|-------------|----------|-------------|-----------------|
| `mouse_move_api` | "talon" or "windows" | "talon" | Mouse API to use for mouse movement - talon or windows |

## Dependencies
none