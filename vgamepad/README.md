## vgamepad Talon integration
This will allow us to emulate and issue xbox controller actions. Only Windows and Linux are supported.

## Setup
The `vgamepad` repo is already included in the `.subtrees` folder (cloned from https://github.com/yannbouteiller/vgamepad), but we also must install the `vgamepad` package into our Talon environment.

**Required:**
1. Locate your `TALON_HOME` dir, where your `user` folder lives.
    - Windows: `~/AppData/Roaming/talon`
    - Linux: ?
2. Install the package
    - Windows: `[TALON_HOME]/venv/3.11/Scripts/pip.bat install vgamepad`
    - Linux: `[TALON_HOME]/bin/pip install vgamepad`
3. If using Linux, there is an additional step. See the README in the `vgamepad/.subtrees/vgamepad` folder.

Done! Now the `user.game_xbox_` actions should work from `game_tools` folder.

## Actions
```python
vgamepad_enable
vgamepad_disable
vgamepad_button
vgamepad_a
vgamepad_b
vgamepad_x
vgamepad_y
vgamepad_dpad_up
vgamepad_dpad_down
vgamepad_dpad_left
vgamepad_dpad_right
vgamepad_left_shoulder
vgamepad_right_shoulder
vgamepad_left_thumb
vgamepad_right_thumb
vgamepad_start
vgamepad_back
vgamepad_guide
vgamepad_left_joystick
vgamepad_left_joystick_dir_left
vgamepad_left_joystick_dir_right
vgamepad_left_joystick_dir_up
vgamepad_left_joystick_dir_down
vgamepad_right_joystick
vgamepad_right_joystick_dir_left
vgamepad_right_joystick_dir_right
vgamepad_right_joystick_dir_up
vgamepad_right_joystick_dir_down
vgamepad_joystick_stop
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