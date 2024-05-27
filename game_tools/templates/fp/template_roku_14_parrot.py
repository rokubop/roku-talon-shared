game_talon = '''\
app: {app_name}
-
settings():
    key_hold = 64.0
    key_wait = 16.0
    user.game_calibrate_x_360 = 2139
    user.game_calibrate_y_90 = 542
    user.mouse_move_api = "windows"

^game$:                     user.game_mode_enable()
^game mode$:                user.game_mode_enable()
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
parrot(nn):                 user.use_parrot_config("nn")
parrot(t):                  user.use_parrot_config("t")
'''

game_py = '''\
from talon import Module, Context, actions, ctrl

mod = Module()
ctx = Context()

mod.apps.{app_name} = r"""
os: {os}
and {app_context}
"""

ctx.matches = r"""
os: {os}
app: {app_name}
"""

ctx_game = Context()
ctx_game.matches = r"""
os: {os}
app: {app_name}
mode: user.game
"""

parrot_config = {{
    "eh":         ('forward', actions.user.game_move_dir_hold_w),
    "guh":        ("back", actions.user.game_move_dir_hold_s),
    "ah":         ("left", actions.user.game_move_dir_hold_a),
    "oh":         ("right", actions.user.game_move_dir_hold_d),
    "ee":         ("stop", actions.user.game_stopper),
    "pop":        ("L click", lambda: ctrl.mouse_click(0, hold=16000)),
    "cluck":      ("R click", lambda: ctrl.mouse_click(1, hold=16000)),
    "nn":         ("E", lambda: actions.key("e")),
    "palate":     ("jump", lambda: actions.key("space")),
    "t":          ("shift", lambda: actions.key("shift")),
    "shush":      ("look up", lambda: actions.user.mouse_move_continuous(0, -1, 5)),
    "shush_stop:db_1000": ("", lambda: actions.user.mouse_move_continuous_stop()),
    "hiss_stop:db_1000": ("", lambda: actions.user.mouse_move_continuous_stop()),
    "hiss":       ("look down", lambda: actions.user.mouse_move_continuous(0, 1, 5)),
    "er":         ("exit mode", actions.user.game_mode_disable),
    "tut":        ("reset y", actions.user.game_reset_center_y),
    "tut ah":     ("turn left", lambda: actions.user.game_turn_left_90()),
    "tut oh":     ("turn right", lambda: actions.user.game_turn_right_90()),
    "tut guh":    ("turn around", actions.user.game_turn_180),
    "tut ee":     ("F", lambda: actions.key("f")),
    "tut pop":    ("L click hold", lambda: ctrl.mouse_click(button=0, down=True)),
    "tut cluck":  ("R click hold", lambda: ctrl.mouse_click(button=2, down=True)),
    "tut shush":  ("space hold", lambda: actions.key("space:down")),
    "tut nn":     ("E hold", lambda: actions.key("e:down")),
    "tut palate": ("Q hold", lambda: actions.key("q:down")),
    "tut tut":    ("alt", lambda: actions.key("alt")),
}}

@ctx_game.action_class("user")
class Actions:
    def parrot_config():
        return parrot_config
'''