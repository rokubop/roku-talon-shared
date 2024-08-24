# Changelog

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
- Removed `ui_builder_get_id` and `ui_builder_get_ids`. Use `ui_builder_get` instead.

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