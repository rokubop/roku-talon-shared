from talon import Module, Context

mod = Module()
ctx = Context()

ctx_game = Context()
ctx_game.matches = "mode: user.game"
mod.mode("game", "game play mode")
mod.mode("game_calibrating_x", "calibrating x")
mod.mode("game_calibrating_y", "calibrating y")

mod.tag("game_xbox", desc="game xbox")
mod.list("game_xbox_button", desc="xbox buttons")
mod.list("game_xbox_stick", desc="xbox stick left or right")
mod.list("game_xbox_left_stick", desc="xbox left stick")
mod.list("game_xbox_right_stick", desc="xbox right stick")
mod.list("game_xbox_trigger", desc="xbox trigger left or right")
mod.list("game_xbox_left_trigger", desc="xbox left trigger name")
mod.list("game_xbox_right_trigger", desc="xbox right trigger name")
mod.list("game_xbox_dpad", desc="xbox dpad name")
mod.list("game_dir", desc="Game dir e.g. left right up down back forward")
mod.list("game_gear", desc="Game gear for various dynamic values, spoken form 1 to 5")

ctx.lists["user.game_dir"] = {
    "left"
    "right",
    "up",
    "down",
    "back",
    "forward",
}
ctx.lists["user.game_gear"] = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
}

@mod.capture(rule="{user.game_dir} [{user.game_dir}]")
def game_dir(m) -> str:
    """
    a one or two word direction e.g. left, right, left right, up, down, back, back left, etc..
    """
    return tuple(m.game_dir_list) if len(m) == 2 else m.game_dir
