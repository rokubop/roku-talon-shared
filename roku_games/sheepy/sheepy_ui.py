from talon import actions

commands = None
keys = None
accent_color = "87ceeb"

def show_commands(parrot_config):
    global commands

    commands = actions.user.ui_builder_screen(
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
    keys = actions.user.ui_builder_screen(
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