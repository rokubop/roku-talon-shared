# Ryujinx(ZELDA)
Adapted from original work done by [rokubop](https://github.com/rokubop/roku-talon-shared) for [rdr2](https://github.com/rokubop/roku-talon-shared/tree/main/roku_games/rdr2). With a few changes now it works with ryujinx switch emulator, specifically set up for Zelda totk in this case.

Thanks rokubop.

## Setup
1. Since this depends on almost everything in `roku-talon-shared`, make sure you have that inside your `[TALON_HOME]/user` directory.
2. Make sure you have the `vgamepad` installed. Follow the instructions in the [roku-talon-shared/vgamepad/README.md](https://github.com/rokubop/roku-talon-shared/tree/main/vgamepad/) to install it.
3. ***Important New Step*** Since native ryujinx mouse input for right stick was not working I used `pynput` to map mouse input to `vgamepad` right stick. Install `pynput` with Talon's pip (package installer for python). Using your terminal of choice...

Windows (If your TALON_HOME is ~/AppData/Roaming/talon):
`~/AppData/Roaming/talon/venv/3.11/Scripts/pip.bat install pynput`

Linux:`[TALON_HOME]/bin/pip install pynput`

4. When inside the game, say "game" or "game mode" to enable the game mode.
5. To exit game mode, say "game exit".

## Commands
| Command | Description |
| --- | --- |
| `game mode` | Enable game mode |
| `game exit` | Exit  game mode |

See [game_words.csv](game_words.csv) for xbox button names.

See [ryujinx_totk.talon](ryujinx_totk.talon) for the full list of commands.

### Optional Additional Setup
1. (Optional) You can move the `ryujinx` directory somewhere else if you like. As long as it's inside your `[TALON_HOME]/user` directory, and as long as you have `roku-talon-shared` in your `[TALON_HOME]/user` directory.
2. (Optional) Edit `ryujinx/game_words.csv` for xbox controller button names
3. (Optional) Add new commands to `ryujinx/ryujinx_totk.talon` and `ryujinx/ryujinx_totk.py` as needed.
4. (Optional) You can change the UI if you like in `ryujinx/ryujinx_totk_ui.py`.
5. (Optional) Adjust any settings like speech timeout in `ryujinx/ryujinx_totk_settings.py`.

## Dependencies

- Free version of Talon
- Windows or linux required (does not work for mac), because of `vgamepad` dependency
- `roku-talon-shared` in your `[TALON_HOME]/user` directory
- `vgamepad` needs to be manually installed by following the instructions in the [roku-talon-shared/vgamepad/README.md](https://github.com/rokubop/roku-talon-shared/tree/main/vgamepad/) so that we can use xbox controller emulation. This is necessary to enable aim assist in the game.
- `Ryujinx` switch emulator https://github.com/Ryujinx/Ryujinx/wiki/Ryujinx-Setup-&-Configuration-Guide
- `pynput` talon integration 