## vgamepad Talon integration
This will allow us to emulate Xbox360 gamepad actions with Talon. Only Windows and Linux are supported.

Used by the `game_tools` folder for `game_xbox_` actions.

## Setup
1. Locate your `TALON_HOME` dir.
    - Windows: `~/AppData/Roaming/talon`
    - Linux: ?
2. Put this repo inside your `[TALON_HOME]/user` folder. The [vgamepad repo](https://github.com/yannbouteiller/vgamepad) is already included in the `.subtrees` folder, but we also must install the `vgamepad` package into our Talon environment.
3. Using your terminal of choice, install the package using Talon's pip.
    - Windows: `[TALON_HOME]/venv/3.11/Scripts/pip.bat install vgamepad`
    - Linux: `[TALON_HOME]/bin/pip install vgamepad`
4. If using Linux, there is an additional step. See the README in the `vgamepad/.subtrees/vgamepad` folder.

Done! Now the `user.game_xbox_` actions should work from `game_tools` folder.

The below low level actions are available, but it is recommended to use the `game_xbox_` actions instead.

## Actions
| Action | Description |
| --- | --- |
| `vgamepad_enable` | Enables Virtual Xbox360 gamepad. Required before gamepad actions work. |
| `vgamepad_disable` |
| `vgamepad_button_hold` | Starts pressing a button (no effect if already pressed). Note: The GUIDE button is not available on Linux. You must manually release the button with `actions.user.vgamepad_button_release`.|
| `vgamepad_button_release` | Releases a button (no effect if already released) |
| `vgamepad_dpad_dir_hold` | Mutually exclusive direction hold of dpad. |
| `vgamepad_left_trigger` | Sets the value of the left trigger. float between 0.0 and 1.0 (0.0 = trigger released) |
| `vgamepad_right_trigger` | Sets the value of the left trigger. float between 0.0 and 1.0 (0.0 = trigger released) |
| `vgamepad_left_stick` | Sets the values of the X and Y axis for the left joystick. float between -1.0 and 1.0 (0 = neutral position) |
| `vgamepad_right_stick` | Sets the values of the X and Y axis for the left joystick. float between -1.0 and 1.0 (0 = neutral position) |

## Additional info
`vgamepad` is included in the `.subtrees` folder, which was cloned from https://github.com/yannbouteiller/vgamepad.

> Virtual Gamepad (```vgamepad```) is a small python library that emulates XBox360 and DualShock4 gamepads on your system.
It enables controlling e.g. a video-game that requires analog input, directly from your python script.