from talon import actions, cron

history_list = []

def reset_history():
    global history_list
    history_list = []

def circle(color):
    svg, circle = actions.user.ui_elements_svg(["svg", "circle"])

    return svg(size=12)[
        circle(cx=12, cy=12, r=12, fill=color),
    ]

def green_circle():
    return circle("green")

def pink_circle():
    return circle("pink")

def blue_circle():
    return circle("3366ff")

def purple_circle():
    return circle("purple")

def square(color):
    svg, rect = actions.user.ui_elements_svg(["svg", "rect"])

    return svg(size=12)[
        rect(x=0, y=0, width=24, height=24, fill=color),
    ]

def mod(color):
    svg, rect = actions.user.ui_elements_svg(["svg", "rect"])

    return svg(size=12)[
        rect(x=0, y=0, width=8, height=24, fill=color),
    ]

def grab_mod():
    return mod("orange")

def side_b_mod():
    return mod("00ffcc")

def hold_jump_mod():
    return mod("a83273")

def red_square():
    return square("red")

def orange_square():
    return square("orange")

def teal_square():
    return square("00ffcc")

command_icon_map = {
    "jump 1": pink_circle,
    "jump 2": pink_circle,
    "jump 3": lambda: circle("a83273"),
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
    "grab": orange_square,
    "side b": teal_square,
}

def command_name_to_icon(command_name):
    if command_name in command_icon_map:
        return command_icon_map[command_name]()
    else:
        return blue_circle()

def append_history_log(action_name, command_name):
    global history_list

    grab = actions.user.ui_elements_get_state("grab")
    side_b = actions.user.ui_elements_get_state("side_b")
    hold_jump = actions.user.ui_elements_get_state("hold_jump")

    new_item = {
        "action": action_name,
        "command": command_name,
        "grab": True if grab or command_name == "grab" else False,
        "side_b": True if side_b or command_name == "side b" else False,
        "hold_jump": True if hold_jump or command_name == "jump 3" else False
    }

    if len(history_list) >= 20:
        history_list = [new_item]
    else:
        history_list.append(new_item)

    actions.user.ui_elements_set_state("history_list", [*history_list])

def on_noise(noise, command_name):
    if "stop" in noise:
        return

    append_history_log(noise, command_name)

def history_item(data):
    div, text = actions.user.ui_elements(["div", "text"])

    return div(flex_direction="row", align_items="center", width=200)[
        side_b_mod() if data["side_b"] else None,
        grab_mod() if data["grab"] else None,
        hold_jump_mod() if data["hold_jump"] else None,
        div(margin_right=16)[
            command_name_to_icon(data["command"]),
        ],
        div(flex_direction="row", width="100%", align_items="center", justify_content="space_between")[
            text(data["action"], font_size=16, font_weight="bold"),
            text(data["command"], font_size=16, font_weight="bold"),
        ]
    ]

def history_log():
    div, screen, state = actions.user.ui_elements(["div", "screen", "state"])
    history_list_state = state.get("history_list", [])

    return screen(flex_direction="row", align_items="flex_start", justify_content="flex_end")[
        div(margin_left=24, padding=16, margin_top=400, height=450, margin_right=30, background_color="00000099")[
            div(gap=8)[
                *[history_item(data) for data in history_list_state]
            ],
        ],
    ]

def show_history_log():
    actions.user.ui_elements_show(history_log)
    actions.user.parrot_config_event_register(on_noise)

def hide_history_log():
    actions.user.parrot_config_event_unregister(on_noise)
    actions.user.ui_elements_hide(history_log)
    reset_history()