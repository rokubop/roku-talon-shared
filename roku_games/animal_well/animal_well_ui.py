from talon import actions

commands = None
keys = None
accent_color = "87ceeb"

def show_commands(parrot_config):
    global commands

    (div, screen, text) = actions.user.ui_elements(['div', 'screen', 'text'])
    (cmds, acts) = actions.user.parrot_config_format_display(parrot_config)

    commands = screen(align_items="flex_start", justify_content="flex_start")[
        div(flex_direction="row", margin_top=48, padding=16, gap=16)[
            div(gap=8)[
                text("sound", font_weight="bold"),
                *(text(command) for command in cmds)
            ],
            div(gap=8)[
                text("action", font_weight="bold"),
                *(text(action, color=accent_color) for action in acts)
            ]
        ]
    ]

    commands.show()

def hide_commands():
    global commands
    commands.hide()

def show_keys():
    global keys
    keys = actions.user.ui_elements_screen(
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
        div = container.add_div(key, id=key_name, width=width)
        div.add_text(key_name)

    def add_blank_key(container):
        div = container.add_div(key, background_color="33333355")
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