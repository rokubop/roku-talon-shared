from talon import actions, cron

accent_color = "87ceeb"

history_list = []

def reset_history():
    global history_list
    history_list = []

def circle(color):
    svg, circle = actions.user.ui_elements_svg(["svg", "circle"])

    return svg()[
        circle(cx=12, cy=12, r=12, fill=color),
    ]

def green_circle():
    return circle("green")

def pink_circle():
    return circle("pink")

def blue_circle():
    return circle("blue")

def purple_circle():
    return circle("purple")

def square(color):
    svg, rect = actions.user.ui_elements_svg(["svg", "rect"])

    return svg()[
        rect(x=0, y=0, width=24, height=24, fill=color),
    ]

def red_square():
    return square("red")

command_icon_map = {
    "jump 1": pink_circle,
    "jump 2": pink_circle,
    "jump 3": pink_circle,
    "c": pink_circle,
    "left": green_circle,
    "right": green_circle,
    "up": green_circle,
    "down": green_circle,
    "stop": red_square,
    "load": purple_circle,
    "save": purple_circle,
    "clear": purple_circle,
    "debug": purple_circle,
    "restart chapter": purple_circle,
    "jump pause": purple_circle,
    "pause jump pause": purple_circle,
    "return map": purple_circle,
    "skip scene": purple_circle,
}

def command_name_to_icon(command_name):
    if command_name in command_icon_map:
        return command_icon_map[command_name]()
    else:
        return blue_circle()

def on_noise(noise, command_name):
    global history_list

    if "stop" in noise:
        return

    if len(history_list) >= 15:
        history_list = [(noise, command_name)]
    else:
        history_list.append((noise, command_name))

    actions.user.ui_elements_set_state("history_list", [*history_list])

def history_item(noise, command_name):
    div, text = actions.user.ui_elements(["div", "text"])

    return div(flex_direction="row", gap=16)[
        command_name_to_icon(command_name),
        text(noise, font_size=24),
        text(command_name, font_size=24),
    ]

def history_rollover():
    div, screen, state = actions.user.ui_elements(["div", "screen", "state"])
    history_list_state = state.get("history_list", [])

    print("history_list_state", history_list_state)

    return screen(align_items="flex_start", justify_content="flex_start", margin_top=300)[
        div(margin_left=48, padding=16)[
            div(gap=16)[
                *[history_item(noise, command_name) for noise, command_name in history_list_state]
            ],
        ],
    ]

def show_history_rollover():
    actions.user.ui_elements_show(history_rollover)
    actions.user.parrot_config_event_register(on_noise)

def hide_history_rollover():
    actions.user.parrot_config_event_unregister(on_noise)
    actions.user.ui_elements_hide(history_rollover)
    reset_history()