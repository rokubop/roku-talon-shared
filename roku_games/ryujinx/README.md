# Red Dead Redemption 2

## Setup
1. Since this depends on almost everything in `roku-talon-shared`, make sure you have that inside your `[TALON_HOME]/user` directory.
2. Make sure you have the `vgamepad` installed. Follow the instructions in the [roku-talon-shared/vgamepad/README.md](https://github.com/rokubop/roku-talon-shared/tree/main/vgamepad/) to install it.
3. When inside the game, say "game" or "game mode" to enable the game mode.
4. To exit game mode, say "game exit".

## Commands
| Command | Description |
| --- | --- |
| `game mode` | Enable RDR2 game mode |
| `game exit` | Exit RDR2 game mode |

See [game_words.csv](game_words.csv) for xbox button names.

See [rdr2.talon](rdr2.talon) for the full list of commands.

### Optional Additional Setup
1. (Optional) You can move the `rdr2` directory somewhere else if you like. As long as it's inside your `[TALON_HOME]/user` directory, and as long as you have `roku-talon-shared` in your `[TALON_HOME]/user` directory.
2. (Optional) Edit `rdr2/game_words.csv` for xbox controller button names
3. (Optional) Add new commands to `rdr2/rdr2.talon` and `rdr2/rdr2.py` as needed.
4. (Optional) You can change the UI if you like in `rdr2/rdr2_ui.py`.
5. (Optional) Adjust any settings like speech timeout in `rdr2/rdr2_settings.py`.

## Dependencies

- Free version of Talon
- Windows or linux required (does not work for mac), because of `vgamepad` dependency
- `roku-talon-shared` in your `[TALON_HOME]/user` directory
- `vgamepad` needs to be manually installed by following the instructions in the [roku-talon-shared/vgamepad/README.md](https://github.com/rokubop/roku-talon-shared/tree/main/vgamepad/) so that we can use xbox controller emulation. This is necessary to enable aim assist in the game.

## Known Issues
- RDR2 limits keyboard presses outside of the game, making it very difficult to update talon files while the game is running. https://www.reddit.com/r/reddeadredemption2/comments/1dsrrn7/keyboard_input_delay_when_tabbed_out_of_rdr2/