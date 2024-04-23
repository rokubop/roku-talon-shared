# Mouse Move Advanced (WIP)

Mouse movement actions for Talon using a delta (dx, dy) or position(s) (x, y) over a duration of time, with control over the easing type, API (Windows or Talon), and callbacks.

Easing Types:
- `linear`
- `ease_in_out`
- `ease_in`
- `ease_out`
- `instant`

| **Action** | **Description** |
|------------|-----------------|
| `user.mouse_move_adv` | Moves the mouse using a delta (dx, dy) starting from the current position, over a duration of time. |
| `user.mouse_move_adv_to` | Moves the mouse to a screen position (x, y) over a duration of time. |
| `user.mouse_move_adv_from` | Moves the mouse from a position (x, y) back to the current position over a duration of time. |
| `user.mouse_move_adv_from_to` | Moves the mouse from one point (x1, y1) to another (x2, y2) over a duration of time. |