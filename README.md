# roku-talon-shared

This is shared set of Talon tools and scripts to help you play games, build UIs, move the mouse, setup parrot combos or dynamic noises. WIP. Each folder is considered a "package" with its own `manifest.json` file telling you what it contributes and depends on.

## Features
| Feature | Description | README |
| --- | --- | --- |
| `drag_mode` | Grid specializing in dragging between points with left, mid, and right click. WIP. | [README](drag_mode/README.md) |
| `dynamic_noises` | dynamic noises allow you to update noises like "pop" or "hiss" on the fly, programatically or to any spoken phrase e.g. saying "pop scroll down" to bind "scroll down" to noise "pop" | [README](dynamic_noises/README.md) |
| `game_tools` | Actions for playing games. Eventually with auto setup script. WIP. | [README](game_tools/README.md) |
| `mouse_move_adv` | Actions for moving the mouse to and from points. | [README](mouse_move_adv/README.md) |
| `parrot_config` | Quick and easy way to assign your parrot commands to combos, throttling, debounce, screen positions. Easy to swap out with other configs without using modes or tags. | [README](parrot_config/README.md) |
| `roku_games` | My personal game setups for reference. | [README](roku_games/README.md) |
| `ui_elements` | HTML/CSS (object oriented) like syntax for building UIs. Supports div, text, and most CSS properties such as margin, padding, flex_direction, etc... Supports custom ability to highlight divs by ID with an overlay color. WIP. | [README](ui_elements/README.md) |
| `vgamepad` | Talon integration with `vgamepad` for controlling video-games that require controller (xbox) input. | [README](vgamepad/README.md) |

## Partial checkout
If you want to checkout only a few of these tools, you can use `git sparse-checkout`

```sh
# Clone the repo
git clone git@github.com:rokubop/roku-talon-shared.git

# Change directory
cd roku-talon-shared

# Checkout only the tools you want
#
# WARNING: BE CAREFUL TO DO THIS IN THE CORRECT DIRECTORY
# THIS REMOVES ALL FOLDERS EXCEPT THE ONES YOU SPECIFY
git sparse-checkout set ui_elements mouse_move_adv

# checkout all tools
git sparse-checkout set drag_mode dynamic_noises game_tools mouse_move_adv parrot_config roku_games ui_elements vgamepad

# To reset so you see all tools
git sparse-checkout disable
```