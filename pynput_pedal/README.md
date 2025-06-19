# pynput pedal

Provides pedal context actions that don't trigger unwanted repeats or releases while pressing other keys with Talon.

Workaround for Talon issue https://github.com/talonvoice/talon/issues/684

## Setup

1. Locate your TALON_HOME dir
```sh
# mac and linux
cd ~/.talon

# windows
cd ~/AppData/Roaming/talon
```

2. Download or clone this repository into your Talon `user` directory.
```sh
cd user
git clone https://github.com/rokubop/pyntput_pedal.git
```

3. Install `pynput` using Talon's pip. This is a lightweight cross-platform package that allows us to listen to keyboard and mouse events.
```sh
cd ..

# Windows and Mac
venv/[current-talon-python-version]/Scripts/pip.bat install pynput

# Linux
bin/pip install pynput
```

4. Change these values in `pynput_pedal.py` to match the keys your pedal is assigned to. If you want to omit a defintion, then use `None` for the value.
```
LEFT_PEDAL_KEY = '*'
MIDDLE_PEDAL_KEY = '-'
RIGHT_PEDAL_KEY = '+'
```

5. Setup a `Context` with the following actions that you want. These will not activate until you manually enable `actions.user.pynput_pedal_enable`

```py
from talon import Context

ctx = Context()

ctx.action_class("user"):
    def pynput_pedal_left_down():
        # your code here

    def pynput_pedal_left_up():
        # your code here

    def pynput_pedal_middle_down():
        # your code here

    def pynput_pedal_middle_up():
        # your code here

    def pynput_pedal_right_down():
        # your code here

    def pynput_pedal_right_up():
        # your code here
```

6. Finally, call `actions.user.pynput_pedal_enable()` to have `pynput` start listening to pedal events, and use `actions.user.pynput_pedal_disable()` to stop listening.

Done! 🎉