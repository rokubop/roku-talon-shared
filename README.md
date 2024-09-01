# roku-talon-shared

This is shared set of Talon tools and scripts to help you play games, build UIs, make complex swappable parrot configs easily. WIP.

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

## Installation
Clone this repository in your Talon `/user` directory.

```bash
git clone git@github.com:rokubop/roku-talon-shared.git
```

If you only want to use a specific set of tools, you can use `git sparse-checkout` to specify which folders you want to include.

```bash
cd roku-talon-shared
git sparse-checkout init
```

This will make this repository empty except for the root files. Now you need to add what you want.

For example if you only want `ui_elements` and `mouse_move_adv`, you can do the following:

```bash
git sparse-checkout set ui_elements mouse_move_adv
```

If you want to add additional folders later, you can do the following:

```bash
git sparse-checkout add drag_mode
```

If you want to remove a folder(s) later, you need to define the entire set again excluding the folder you want to remove:

```bash
git sparse-checkout set ui_elements
```

To disable sparse-checkout and get all the files back:
```bash
git sparse-checkout disable
```

See git documentation on sparse-checkout for more information.
