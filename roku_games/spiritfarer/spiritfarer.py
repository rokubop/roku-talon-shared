from talon import Module, Context, actions
from .ui.spiritfarer_ui import show_ui, hide_ui

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.spiritfarer = "os: windows\nand app.exe: /spiritfarer.exe/i"
ctx.matches = "os: windows\napp: spiritfarer"
ctx_game.matches = f"{ctx.matches}\nmode: user.game"

def mode_cycle():
    new_mode = actions.user.parrot_config_cycle_mode()
    actions.user.ui_elements_set_state("parrot_config", parrot_config[new_mode])

default_config = {
    "sh:th_90":   ("space long", lambda: actions.user.game_key_hold("space", 300)),
    "sh_stop":    ("", lambda: None),
    "ss":         ("space short", lambda: actions.user.game_key_hold("space")),
    "ss_stop:db_50":("", lambda: actions.user.game_key_release("space")),
    "ah":         ("dir left", actions.user.game_arrows_hold_left),
    "oh":         ("dir right", actions.user.game_arrows_hold_right),
    "eh":         ("dir up", actions.user.game_arrows_hold_up),
    "guh":        ("dir down", actions.user.game_arrows_hold_down),
    "ee":         ("stop", actions.user.game_stopper),
    "pop":        ("1", lambda: actions.user.game_key("1")),
    "t":          ("2", lambda: actions.user.game_key("2")),
    "mm":         ("e", lambda: actions.user.game_key("e")),
    "palate_click": ("tab", lambda: actions.user.game_key("tab")),
    "er":         ("r", lambda: actions.user.game_key("r")),
    "cluck":      ("mode cycle", mode_cycle),
    "tut":        ("escape", lambda: actions.user.game_key("escape")),
    "tut er":     ("hold r", lambda: actions.user.game_key_hold("r")),
    "tut mm":     ("hold e", lambda: actions.user.game_key_hold("e")),
    "tut sh":     ("space hold", lambda: actions.user.game_key_hold("space")),
    "tut tut":    ("exit", actions.user.game_mode_disable),
}

key_press_config = {
    **default_config,
    "ah":         ("left", lambda: actions.user.game_key("left")),
    "oh":         ("right", lambda: actions.user.game_key("right")),
    "eh":         ("up", lambda: actions.user.game_key("up")),
    "guh":        ("down", lambda: actions.user.game_key("down")),
}

parrot_config = {
    "default": default_config,
    "key_press": key_press_config,
}

@ctx_game.action_class("user")
class Actions:
    def on_game_mode_enabled():
        actions.user.ui_elements_set_state("parrot_config", default_config)
        show_ui()

    def on_game_mode_disabled():
        hide_ui()

    def parrot_config():
        return parrot_config