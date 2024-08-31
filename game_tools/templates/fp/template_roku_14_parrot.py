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
parrot(eh):                 user.parrot_config_noise("eh")
parrot(guh):                user.parrot_config_noise("guh")
parrot(ah):                 user.parrot_config_noise("ah")
parrot(oh):                 user.parrot_config_noise("oh")
parrot(ee):                 user.parrot_config_noise("ee")
parrot(hiss):               user.parrot_config_noise("hiss")
parrot(hiss:stop):          user.parrot_config_noise("hiss_stop")
parrot(shush):              user.parrot_config_noise("shush")
parrot(shush:stop):         user.parrot_config_noise("shush_stop")
parrot(palate_click):       user.parrot_config_noise("palate")
parrot(tut):                user.parrot_config_noise("tut")
parrot(cluck):              user.parrot_config_noise("cluck")
parrot(pop):                user.parrot_config_noise("pop")
parrot(er):                 user.parrot_config_noise("er")
parrot(nn):                 user.parrot_config_noise("mm")
parrot(t):                  user.parrot_config_noise("t")
'''

game_py = '''\
from talon import Module, Context, actions
from .{app_name}_ui import show_ui, hide_ui

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

    def on_game_mode_enabled():
        show_ui(parrot_config)

    def on_game_mode_disabled():
        hide_ui()
'''

game_ui_py = '''\
from talon import actions

ui_commands = None
accent_color = "87ceeb"

def show_ui(parrot_config):
    global ui_commands
    (commands, acts) = actions.user.parrot_config_format_display(parrot_config)
    (div, text, screen) = actions.user.ui_elements(["div", "text", "screen"])

    ui_commands = screen(align_items="flex_end", justify_content="flex_start")[
        div(background_color="00000066", margin=16, margin_right=32, padding=16)[
            div(flex_direction="row", gap=16)[
                div(gap=8)[
                    text("sound", font_weight="bold"),
                    *(text(command) for command in commands),
                ],
                div(gap=8)[
                    text("actions", font_weight="bold", color=accent_color),
                    *(text(action, color=accent_color) for action in acts),
                ]
            ]
        ],
    ]
    ui_commands.show()

def hide_ui():
    global ui
    ui_commands.hide()
'''