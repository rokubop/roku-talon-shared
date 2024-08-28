# Drag Grid/Mode

This is an experimental repository. Allows you drag from one point to another using left, middle, or right click. Flexible mouse movement to and from any point. hiss stopper for precision stops.

## Mode
| Command | Description |
| --- | --- |
| drag mode | Enable drag grid/mode with LMB default |
| pan mode | Enable pan grid/mode with MMB default |
| roll mode | Enable roll grid/mode with RMB default |
| grid hide | Hide the grid |

## Commands:
| Command | Description | Example |
| --- | --- | --- |
| \<T> | Click a target | sun plex |
| \<T> to \<T> | Drag from X to Y using current mode | sun plex to air bat |
| go \<T> | Move the mouse to a target smoothly | go sun plex |
| fly [to] \<T> | Start moving mouse toward X | fly to sun plex |
| fly \<dir> | Move the mouse in a direction | fly up, fly left, fly right, fly down |
| "hiss" noise | Stop movement immediately | |
| halt \| stop | Stop the mouse movement | |
| bring \<T> | Drag from a target to the current mouse position | bring sun plex |
| bring this to \<T> | Drag from the current mouse position to a target | bring this to sun plex |
| center \<T> | Move a target to the center of the screen | center sun plex |
| tick \<dir> | Move the mouse in a direction by a small increment | tick up, tick left |
| gear up | Increase the speed of the mouse movement | |
| gear down | Decrease the speed of the mouse movement | |

## Noises:
| Command | Description |
| --- | --- |
| hiss | Stop movement immediately |

## Layout
| Command | Description | Example |
| --- | --- | --- |
| more squares | Increase the number of squares in the grid | |
| less squares | Decrease the number of squares in the grid | |
| clear \<T> (to \| past) \<T> | Clear the grid between two targets | clear air bat to sun plex |
| clear line \<T> | Clear the horizontal line of the grid at the target | clear line sun plex |
| clear line \<T> past \<T> | Clear the horizontal lines of the targets from X to Y | clear line sun plex past air bat |
| take \<T> past \<T> | Omit all points except the area between two targets | take sun plex past air bat |
| grid reset | Reset the grid to the default state | |

## Includes
Modes:
```
user.drag_mode
```

Tags:
```
user.pan_mode
user.roll_mode
```

Settings:
```
user.drag_mode_exclude_chars
user.drag_mode_default_tile_size
user.drag_mode_tile_increment_size
user.drag_mode_offset_x_y
user.drag_mode_dynamic_noises_enabled
user.drag_mode_disable_dynamic_noises_on_grid_hide
```

Commands:
```
drag (mode | grid)
pan (mode | grid)
roll (mode | grid)
```

## Dependencies
- roku-talon-shared/mouse_move_adv
- roku-talon-shared/dynamic_noises
- roku-talon-shared/ui_elements