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
from talon import Module, Context, actions, ctrl
from .{app_name}_ui import show_ui, hide_ui, highlight, highlight_briefly, unhighlight


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

def up():
    actions.user.game_move_dir_hold_up()
    highlight("W")
    unhighlight("S")
    unhighlight("A")
    unhighlight("D")

def down():
    actions.user.game_move_dir_hold_down()
    highlight("S")
    unhighlight("W")
    unhighlight("A")
    unhighlight("D")

def left():
    actions.user.game_move_dir_hold_left()
    highlight("A")
    unhighlight("W")
    unhighlight("S")
    unhighlight("D")

def right():
    actions.user.game_move_dir_hold_right()
    highlight("D")
    unhighlight("W")
    unhighlight("S")
    unhighlight("A")

def stop():
    actions.user.game_stopper()
    unhighlight("W")
    unhighlight("S")
    unhighlight("A")
    unhighlight("D")

parrot_config = {{
    "eh":         ('forward', up),
    "guh":        ("back", down),
    "ah":         ("left", left),
    "oh":         ("right", right),
    "ee":         ("stop", stop),
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

@ctx.action_class("user")
class Actions:
    def game_mode_enable():
        show_ui(parrot_config)
        actions.next()

@ctx_game.action_class("user")
class Actions:
    def game_mode_disable():
        hide_ui()
        actions.next()

    def parrot_config():
        return parrot_config
'''

ui_py = '''\
from talon import actions

commands = None
keys = None
accent_color = "87ceeb"

def show_commands(parrot_config):
    global commands

    commands = actions.user.ui_html_builder_screen(
        id="parrot_commands",
        align_items="flex_start",
        justify_content="flex_start",
    )
    container = commands.add_div(
        margin_top=48,
        flex_direction="row",
        padding=16,
        gap=16,
    )
    commands_column = container.add_div(gap=8)
    commands_column.add_text("sound", font_weight="bold")
    for command, (action, _) in parrot_config.items():
        if action == "":
            continue
        command = command.split(":")[0]
        commands_column.add_text(command)

    actions_column = container.add_div(gap=8)
    actions_column.add_text("action", font_weight="bold", color=accent_color)
    for command, (action, _) in parrot_config.items():
        if action == "":
            continue
        actions_column.add_text(action, color=accent_color)

    commands.show()

def hide_commands():
    global commands
    commands.hide()

def show_keys():
    global keys
    keys = actions.user.ui_html_builder_screen(
        id="keys",
        justify_content="flex_start",
        align_items="flex_start",
        highlight_color=f"{accent_color}88",
    )
    gamepad = keys.add_div(
        flex_direction="row",
        gap=0,
        margin_top=325,
        margin_left=16
    )
    dpad = gamepad.add_div(
        flex_direction="column",
    )
    keyboard = gamepad.add_div(
        flex_direction="column",
    )

    key = {
        "padding": 8,
        "background_color": "333333dd",
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
        "margin": 1,
        "width": 30,
        "height": 30,
    }
    def add_key(container, key_name, width=30):
        opts = {**key, 'id': key_name, 'width': width}
        div = container.add_div(**opts)
        div.add_text(key_name)

    def add_blank_key(container):
        div = container.add_div(**{**key, "background_color":"33333355"})
        div.add_text(" ")

    first_row = dpad.add_div(flex_direction="row")
    add_blank_key(first_row)
    add_key(first_row, "W")
    add_blank_key(first_row)

    second_row = dpad.add_div(flex_direction="row")
    add_key(second_row, "A")
    add_key(second_row, "S")
    add_key(second_row, "D")

    first_row = keyboard.add_div(flex_direction="row")
    add_key(first_row, "SH", 60)
    add_key(first_row, "E")

    second_row = keyboard.add_div(flex_direction="row")
    add_key(second_row, "CT", 45)
    add_key(second_row, "SP", 45)

    keys.show()

def hide_keys():
    keys.hide()

def show_ui(parrot_config):
    show_commands(parrot_config)
    show_keys()

def hide_ui():
    hide_commands()
    hide_keys()

def highlight(id):
    keys.highlight(id)

def unhighlight(id):
    keys.unhighlight(id)

def highlight_briefly(id):
    keys.highlight_briefly(id)
'''