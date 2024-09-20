# Changelog

## Sep week 3, 2024
- Add `face_tester` package

## Sep week 2, 2024
- Stabalize `dynamic_noises` and `drag_mode` packages

BREAKING CHANGES
- Rename almost all game actions
  - `_key_down` and `_key_up` to `_key_hold` and `_key_release`
  > Reason: This is because "up" and "down" are very common keys in games
  - `game_turn_` to `game_mouse_move_deg_`
  > Reason: Indicate subject is mouse and what type of movement
  - `game_look_` to `game_mouse_move_deg_`
  > Reason: Indicate subject is mouse and what type of movement
  - `game_move_dir_` to `game_wasd_` and/or `game_arrows_`
  > Reason: use \{game}\_\{subject}\_\{type}\_\{action}\_\{value}
  > Subject in this case is the group of wasd or arrows
- Rename `user.dynamic_noises_use_mode` to `user.dynamic_noises_set_mode`
- Remove `user.use_parrot_config`. Use `user.parrot_config_noise` instead
  > Reason: packages should have the same prefix for every action

## Sep week 1, 2024
- Add `flex` for things like `flex: 1` for full width
- Added `border_bottom`, `border_top`, `border_left`, `border_right` to `ui_elements`

BREAKING CHANGES
- change various names in `mouse_move_adv` to `mouse_move_continuous_` or `mouse_move_smooth_`

## Aug week 5 2024
- Added manifest builder and manifests to every "package"
  to show actions, modes, settings, tags, and dependencies
- Add 'cam mode', 'go mode', 'pad mode' to set preferred dir
- Add hold pad commands
- Add left_thumb, right_thumb, view, guide, menu buttons for xbox
- Simplify and automate the noise mode binding process
- Fixed `ui_elements` not highlighting
- Fixed `text_input` not returning correct value
- Show red errors for bad noise bindings for `dynamic_actions`
- Add `ui_elements` components specific to game and noises. `game_ui_elements_` and `dynamic_actions_ui_element`

BREAKING CHANGES
- Rename `dynamic_actions_*` to `dynamic_noises_*`

## Fri Aug 23, 2024
### New Features
- Added `dynamic_actions` experimental folder for dynamic "pop" and "hiss"
- Added `vgamepad` integration for virtual xbox gamepad
- Added `user.game_xbox_` actions for xbox gamepad emulation
- Added `roku_games/rdr2` for Red Dead Redemption 2 using virtual xbox gamepad. Works with free version of Talon.
- Added `actions.user.ui_elements_hide_all`
- Added `actions.user.game_ui_elements_`
- Added better UI for drag mode and "hiss" stop support

### Breaking Changes
- Rename `actions.user.rt_mouse_move_delta` to `actions.user.mouse_move_delta_smooth`
- Removed `actions.user.ui_elements_screen`. Use `actions.user.ui_elements` instead.
- Removed `actions.user.ui_builder_show`. Use `.show()` instead.
- Removed `ui_elements_get_id` and `ui_elements_get_ids`. Use `ui_elements_get` instead.

## Sun Aug 4, 2024
ui_elements
- Add screen index param to screen ui_element
- Add input_text ui_element
- Add opacity property

game_tools
- Add mouse click actions + events to game_tools
- Add optional mouse hold for turn actions

drag_mode
- Add "center <target>"

parrot_config
- Add parrot events

roku_games
- Added celeste UI variations

## Sat Jul 20, 2024
- Add button to ui_elements