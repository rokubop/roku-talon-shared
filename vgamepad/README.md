## vgamepad Talon integration
This will allow us to emulate Xbox360 gamepad actions with Talon. Only Windows and Linux are supported.

Used by the `game_tools` folder for `game_xbox_` actions.

## Setup
1. Locate your `TALON_HOME` dir, on windows this is `~/AppData/Roaming/talon`. You can say "talon home" to get the path.
2. Clone `roku-talon-shared` into your `[TALON_HOME]/user` folder. If you already have it, then you are done with this step.

    From your terminal of choice, navigate to your `[TALON_HOME]/user` folder and run the following command:
    ```
    git clone https://github.com/rokubop/roku-talon-shared.git
    ```
    Or if you don't want to use git, you can copy the files manually.
3. In addition to cloning the files, we must also install `vgamepad` with Talon's `pip` (package installer for python). Using your terminal of choice...

    Windows (If your TALON_HOME is `~/AppData/Roaming/talon`)
    ```
    ~/AppData/Roaming/talon/venv/3.11/Scripts/pip.bat install vgamepad
    ```

    Linux:
    ```
    [TALON_HOME]/bin/pip install vgamepad
    ```

   ### Windows only
   It will  prompt you to install ViGEmBus by Nefarius Software Solutions. Install ViGEmBus. vgamepad is a wrapper around Nefarius' Virtual Gamepad Emulation framework which you can read about here (https://github.com/nefarius/ViGEmBus)

   ### Linux only
    Additional setup is required for Linux. See the [README](https://github.com/rokubop/roku-talon-shared/tree/main/vgamepad/.subtrees/vgamepad/README.md) in the `vgamepad/.subtrees/vgamepad` folder.

4. Done! Now the `user.game_xbox_` actions should work from `game_tools` folder.

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