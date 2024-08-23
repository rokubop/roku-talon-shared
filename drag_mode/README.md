# Drag Grid/Mode

This is an experimental repository. WIP. Likely will change in the future. Allows you drag from one point to another.

| Command | Description | Example |
| --- | --- | --- |
| drag mode | Enable drag grid/mode with LMB default | |
| pan mode | Enable pan grid/mode with MMB default | |
| roll mode | Enable roll grid/mode with RMB default | |
| X to Y | Drag from X to Y using current mode | sun plex to air bat |
| more squares | Increase the number of squares in the grid | |
| less squares | Decrease the number of squares in the grid | |
| grid hide \| hide grid | Hide the grid | |
| X | Click a target | sun plex |
| X then Y | Click two targets in sequence. **You** can chain as many as you want. | sun plex then air bat |
| clear X ( to \| past) Y | Clear the grid between two targets. So there isn't so much noise on your screen. | clear air bat to sun plex |
| bring X | Drag from a target to the current mouse position | bring sun plex |
| bring this to X | Drag from the current mouse position to a target | bring this to sun plex |
| fly to X | Start moving mouse toward X |
| fly up | Move the mouse up |
| fly down | Move the mouse down |
| fly left | Move the mouse left |
| fly right | Move the mouse right |
| (mouse | fly) stop | Stop the mouse movement |
| speedup | Increase the speed of the mouse movement |
| speeddown | Decrease the speed of the mouse movement |
| tick down | Tick mouse down |
| tick up | Tick mouse up |
| tick left | Tick mouse left |
| tick right | Tick mouse right |

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
```

Commands:
```
drag (mode | grid)
pan (mode | grid)
roll (mode | grid)
```