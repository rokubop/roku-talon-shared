from talon import Module, Context, actions

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.hollow_knight = "os: windows\nand app.exe: hollow_knight.exe"
ctx.matches = "os: windows\napp: hollow_knight"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

parrot_config = {
    "eh":         ('forward', actions.user.game_move_dir_hold_up),
    "guh":        ("back", actions.user.game_move_dir_hold_down),
    "ah":         ("left", actions.user.game_move_dir_hold_left),
    "oh":         ("right", actions.user.game_move_dir_hold_right),
    "ee":         ("stop", actions.user.game_stopper),
    "cluck":      ("a", lambda: actions.user.game_key("a")),
    "mm":         ("jump long", lambda: actions.user.game_key_hold("z", 500)),
    "palate":     ("dash", lambda: actions.user.game_key("c")),
    "t":          ("shift", lambda: actions.user.game_key("tab")),
    "shush":      ("jump", lambda: actions.user.game_key_down("z")),
    "shush_stop:db_200": ("", lambda: actions.user.game_key_up("z")),
    "hiss:th_100":("", lambda: actions.user.game_key("x")),
    "hiss_stop":  ("", lambda: None),
    "er":         ("exit mode", actions.user.game_mode_disable),
    "tut t":      ("map", lambda: actions.user.game_key_down("tab")),
    "tut cluck":  ("hold a", lambda: actions.user.game_key_down("a")),
}

game_ui = {
    "show": True,
    "show_commands": True,
    "show_dpad": True,
    "show_last_keypress": True,
    "align": "top_left",
    "offset": (16, 40),
    "font_size": 16,
    "primary_color": "ffffff",
    "accent_color": "87ceeb",
    "background_color": None,
    "use_parrot_config": True,
    "commands": [],
}

@ctx_game.action_class("user")
class Actions:
    def game_ui():
        return game_ui

    def parrot_config():
        return parrot_config
