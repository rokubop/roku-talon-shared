game_talon = '''\
app: {app_name}
-
settings():
    key_hold = 64.0
    key_wait = 16.0
    user.game_calibrate_x_360 = 2139
    user.game_calibrate_y_90 = 542
    user.mouse_move_api = "windows"

^game [mode]$:                user.game_mode_enable()
'''

game_mode_talon = '''\
app: {app_name}
mode: user.game
-
<phrase>:                   skip()
parrot(eh):                 user.use_parrot_config("eh")
parrot(guh):                user.use_parrot_config("guh")
parrot(ah):                 user.use_parrot_config("ah")
parrot(oh):                 user.use_parrot_config("oh")
parrot(ee):                 user.use_parrot_config("ee")
parrot(hiss):               user.use_parrot_config("hiss")
parrot(hiss:stop):          user.use_parrot_config("hiss_stop")
parrot(shush):              user.use_parrot_config("shush")
parrot(shush:stop):         user.use_parrot_config("shush_stop")
parrot(palate_click):       user.use_parrot_config("palate")
parrot(tut):                user.use_parrot_config("tut")
parrot(cluck):              user.use_parrot_config("cluck")
parrot(pop):                user.use_parrot_config("pop")
parrot(er):                 user.use_parrot_config("er")
parrot(nn):                 user.use_parrot_config("mm")
parrot(t):                  user.use_parrot_config("t")
'''

game_py = '''\
from talon import Module, Context, actions

mod, ctx, ctx_game = Module(), Context(), Context()
mod.apps.{app_name} = "os: {os}\\nand {app_context}"
ctx.matches = "os: {os}\\napp: {app_name}"
ctx_game.matches = f"{{ctx.matches}}\\nmode: user.game"

parrot_config = {{
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
}}

@ctx_game.action_class("user")
class Actions:
    def parrot_config():
        return parrot_config
'''