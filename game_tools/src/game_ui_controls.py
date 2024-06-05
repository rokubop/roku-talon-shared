from talon import actions

commands = None
keys = None
accent_color = "87ceeb"
global_options = None

def get_align_justify(options):
    if "align" not in options:
        return "flex_start", "flex_start"

    align_items = "center"
    justify_content = "center"

    if "right" in options.get("align"):
        align_items = "flex_end"
    elif "left" in options.get("align"):
        align_items = "flex_start"

    if "bottom" in options.get("align"):
        justify_content = "flex_end"
    elif "top" in options.get("align"):
        justify_content = "flex_start"

    return align_items, justify_content

def show_commands():
    global commands, global_options

    parrot_config = None
    try:
        parrot_config = actions.user.parrot_config()
    except AttributeError:
        pass

    font_size = global_options.get("font_size", 16)
    accent_color = global_options.get("accent_color", "87ceeb")
    gap = font_size
    half_gap = gap // 2

    commands = actions.user.ui_html_builder_screen(
        id="game_ui",
        align_items=global_options["align_items"],
        justify_content=global_options["justify_content"],
    )
    container = commands.add_div(
        id="commands",
        margin_left=global_options["margin_left"],
        margin_top=global_options["margin_top"],
        flex_direction="row",
        padding=16,
        gap=gap,
        background_color=global_options.get("background_color"),
    )
    commands_column = container.add_div(gap=half_gap)
    commands_column.add_text("sound", font_weight="bold", font_size=font_size)
    for command, (action, _) in parrot_config.items():
        if action == "":
            continue
        command = command.split(":")[0]
        commands_column.add_text(command, font_size=font_size)

    actions_column = container.add_div(gap=half_gap)
    actions_column.add_text("action", font_weight="bold", color=accent_color, font_size=font_size)
    for command, (action, _) in parrot_config.items():
        if action == "":
            continue
        actions_column.add_text(action, color=accent_color, font_size=font_size)

    commands.show()

def hide_commands():
    global commands, global_options
    commands.hide()

def show_dpad():
    global keys, commands

    commands_box_model = actions.user.ui_builder_get_id("commands")["box_model"]
    accent_color = global_options.get("accent_color", "87ceeb")

    keys = actions.user.ui_html_builder_screen(
        id="dpad",
        justify_content=global_options["justify_content"],
        align_items=global_options["align_items"],
        highlight_color=f"{accent_color}88",
    )
    gamepad = keys.add_div(
        flex_direction="row",
        gap=0,
        margin_top=commands_box_model.margin_rect.height,
        margin_left=global_options["margin_left"] + 16,
    )
    dpad = gamepad.add_div(
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
    keys.show()

    print('ok', keys.get_ids())

def hide_keys():
    keys.hide()

def show_ui(options):
    global global_options
    global_options = options

    align_items, justify_content = get_align_justify(options)
    global_options["align_items"] = align_items
    global_options["justify_content"] = justify_content

    margin_left, margin_top = options.get("offset", (0, 0))
    global_options["margin_left"] = margin_left
    global_options["margin_top"] = margin_top

    show_commands()
    show_dpad()

def hide_ui():
    hide_commands()
    hide_keys()

def highlight(id):
    keys.highlight(id)

def unhighlight(id):
    keys.unhighlight(id)

def highlight_briefly(id):
    keys.highlight_briefly(id)

def ui_dpad_left():
    highlight("A")
    unhighlight("W")
    unhighlight("S")
    unhighlight("D")

def ui_dpad_right():
    highlight("D")
    unhighlight("W")
    unhighlight("S")
    unhighlight("A")

def ui_dpad_up():
    highlight("W")
    unhighlight("A")
    unhighlight("S")
    unhighlight("D")

def ui_dpad_down():
    highlight("S")
    unhighlight("W")
    unhighlight("A")
    unhighlight("D")

def ui_dpad_stop():
    unhighlight("W")
    unhighlight("A")
    unhighlight("S")
    unhighlight("D")
