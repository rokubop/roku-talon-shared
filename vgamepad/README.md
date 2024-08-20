## vgamepad Talon integration
This will allow us to emulate and issue xbox controller actions. Only Windows and Linux are supported. Used by the `game_tools` folder for `game_xbox_` actions.

## Setup
The `vgamepad` repo is already included in the `.subtrees` folder (cloned from https://github.com/yannbouteiller/vgamepad), but we also must install the `vgamepad` package into our Talon environment.

**Required:**
1. Locate your `TALON_HOME` dir.
    - Windows: `~/AppData/Roaming/talon`
    - Linux: ?
2. Using your terminal of choice, install the package using talon's pip.
    - Windows: `[TALON_HOME]/venv/3.11/Scripts/pip.bat install vgamepad`
    - Linux: `[TALON_HOME]/bin/pip install vgamepad`
3. If using Linux, there is an additional step. See the README in the `vgamepad/.subtrees/vgamepad` folder.

Done! Now the `user.game_xbox_` actions should work from `game_tools` folder.

## Actions
```python
vgamepad_enable
vgamepad_disable
vgamepad_button
vgamepad_left_joystick
vgamepad_right_joystick
vgamepad_event_register_on_button
vgamepad_event_unregister_on_button
vgamepad_event_register_on_dpad_dir_change
vgamepad_event_unregister_on_dpad_dir_change
vgamepad_event_unregister_all
```

## Additional info
`vgamepad` is included in the `.subtrees` folder, which was cloned from https://github.com/yannbouteiller/vgamepad.

> Virtual Gamepad (```vgamepad```) is a small python library that emulates XBox360 and DualShock4 gamepads on your system.
It enables controlling e.g. a video-game that requires analog input, directly from your python script.