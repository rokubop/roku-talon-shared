# Changelog

## Sat Aug 31, 2024
- Added manifest builder and manifests to every "package"
  to show actions, modes, settings, tags, and dependencies

## Tue Aug 27-28, 2024
- Add 'cam mode', 'go mode', 'pad mode' to set preferred dir
- Add hold pad commands
- Add left_thumb, right_thumb, view, guide, menu buttons for xbox
- Simplify and automate the noise mode binding process

Breaking Changes
- Rename `dynamic_actions_*` to `dynamic_noises_*`

## Sun Aug 25, 2024
- Fixed `ui_elements` not highlighting
- Fixed `text_input` not returning correct value
- Show red errors for bad noise bindings for `dynamic_actions`
- Add `ui_elements` components specific to game and noises. `game_ui_elements_` and `dynamic_actions_ui_element`

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