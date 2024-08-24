from talon import Module

mod = Module()

mod.setting(
    "drag_mode_exclude_chars",
    type=str,
    default="",
    desc="Excluded characters from the drag mode grid e.g. 'ijl'",
)
mod.setting(
    "drag_mode_default_tile_size",
    type=int,
    default=60,
    desc="Default tile size for the drag mode grid",
)
mod.setting(
    "drag_mode_tile_increment_size",
    type=int,
    default=20,
    desc="Default tile size for the drag mode grid",
)
mod.setting(
    "drag_mode_offset_x_y",
    type=str,
    default="0 0",
    desc="Default offset for the drag mode grid",
)
mod.setting(
    "drag_mode_dynamic_actions_enabled",
    type=bool,
    default=True,
    desc="Enable dynamic actions for the hiss sound to stop",
)
mod.setting(
    "drag_mode_disable_dynamic_actions_on_grid_hide",
    type=bool,
    default=True,
    desc="Disable dynamic actions when exiting drag mode",
)