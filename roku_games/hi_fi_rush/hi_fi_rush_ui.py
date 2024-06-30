from talon import actions

commands = None
accent_color = "87ceeb"

def show_commands(parrot_config, background_color="22266688"):
    global commands

    if commands:
        commands.hide()

    commands = actions.user.ui_elements_screen(
        id="parrot_commands",
        align_items="flex_end",
        justify_content="center",
    )
    container = commands.add_div(
        flex_direction="row",
        background_color=background_color,
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
    """Hide and destroy the commands UI"""
    global commands
    commands.hide()