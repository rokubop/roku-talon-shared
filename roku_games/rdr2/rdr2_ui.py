from talon import actions, cron

accent_color = "87ceeb"
live_text_keys_state = ""
pressed_keys = []
clear_pressed_keys_job = None
KEY_SIZE = 25

def clear_pressed_keys():
    global pressed_keys, live_text_keys_state

    for key in pressed_keys:
        live_text_keys_state = live_text_keys_state.replace(f"{key} ", "")

    pressed_keys = []
    actions.user.ui_elements_set_text("live_text_keys", live_text_keys_state)

def on_key(key, state):
    global live_text_keys_state, clear_pressed_keys_job

    if state == "press":
        actions.user.ui_elements_highlight_briefly(key)
        live_text_keys_state += f"{key} "
        pressed_keys.append(key)
    elif state == "hold":
        actions.user.ui_elements_highlight(key)
        live_text_keys_state += f"{key} "
    elif state == "release":
        actions.user.ui_elements_unhighlight(key)
        live_text_keys_state = live_text_keys_state.replace(f"{key} ", "")

    actions.user.ui_elements_set_text("live_text_keys", live_text_keys_state)

    if clear_pressed_keys_job:
        cron.cancel(clear_pressed_keys_job)
    clear_pressed_keys_job = cron.after("200ms", clear_pressed_keys)

def cam_edges_ui(children):
    (div, text) = actions.user.ui_elements(["div", "text"])

    return div(flex_direction="row")[
        div(flex_direction="column")[
            div(width=5, height=5, margin=1)[text(" ", font_size=5)],
            div(id="cam_left", width=5, height=KEY_SIZE*2+1, margin=1)[text(" ", font_size=5)],
            div(width=5, height=5, margin=1)[text(" ", font_size=5)],
        ],
        div(flex_direction="column")[
            div(id="cam_up", width=KEY_SIZE*3+3, height=5, margin=1)[text(" ", font_size=5)],
            children,
            div(id="cam_down", width=KEY_SIZE*3+3, height=5, margin=1)[text(" ", font_size=5)],
        ],
        div(flex_direction="column")[
            div(width=5, height=5, margin=1)[text(" ", font_size=5)],
            div(id="cam_right", width=5, height=KEY_SIZE*2+1, margin=1)[text(" ", font_size=5)],
            div(width=5, height=5, margin=1)[text(" ", font_size=5)],
        ],
    ]

def dpad_ui():
    (div, text) = actions.user.ui_elements(["div", "text"])

    key_css = {
        "padding": 8,
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
        "width": KEY_SIZE,
        "height": KEY_SIZE
    }

    def key(key_name, text_content, width=KEY_SIZE):
        return div(key_css, id=key_name, width=width, background_color="333333dd")[
            text(text_content)
        ]

    def blank_key():
        return div(key_css)[text(" ")]

    def blank_middle_key():
        return div(key_css, background_color="333333dd")[text(" ")]

    return div(flex_direction="column")[
        div(flex_direction="row")[blank_key(), key("gamepad_dpad_up", "↑"), blank_key()],
        div(flex_direction="row")[key("gamepad_dpad_left", "←"), blank_middle_key(), key("gamepad_dpad_right", "→")],
        div(flex_direction="row")[blank_key(), key("gamepad_dpad_down", "↓"), blank_key()]
    ]

def noises_ui():
    (div, text) = actions.user.ui_elements(["div", "text"])

    return div(flex_direction="column", gap=8)[
        div(id="pop", flex_direction="row", width=150, padding=8, border_width=1, border_color="FFFFFF33", border_radius=4)[
            text("pop"),
            text("", id="pop_value", color=accent_color)
        ],
        div(id="hiss", flex_direction="row", width=150, padding=8, border_width=1, border_color="FFFFFF33", border_radius=4)[
            text("hiss"),
            text("", id="hiss_value", color=accent_color)
        ]
    ]

def stick_ui(left_or_right : str):
    (div, text) = actions.user.ui_elements(["div", "text"])

    key_css = {
        "padding": 8,
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
        "border_radius": KEY_SIZE,
        "width": KEY_SIZE,
        "height": KEY_SIZE
    }

    def key(key_name, text_content, width=KEY_SIZE):
        return div(key_css, id=key_name, width=width, background_color="333333cc")[
            text(text_content)
        ]

    def blank_key():
        return div(key_css)[text(" ")]

    return div(flex_direction="column", background_color="333333dd", border_radius=100, padding=1)[
        div(flex_direction="row")[blank_key(), key(f"{left_or_right}_stick_up", " "), blank_key()],
        div(flex_direction="row")[key(f"{left_or_right}_stick_left", " "), blank_key(), key(f"{left_or_right}_stick_right", " ")],
        div(flex_direction="row")[blank_key(), key(f"{left_or_right}_stick_down", " "), blank_key()]
    ]

def cam_mode_ui():
    (div, text) = actions.user.ui_elements(["div", "text"])

    return div(flex_direction="row", gap=16, height=20, align_items="center", justify_content="center", margin_bottom=12)[
        text("<dir> mode:"),
        text("cam", font_weight="bold", margin_bottom=3),
    ]

def live_text_keys_ui():
    (div, text) = actions.user.ui_elements(["div", "text"])

    return div()[
        text("", id="live_text_keys", font_size=20, font_weight="bold")
    ]

def xbox_primary_buttons_ui():
    (div, text) = actions.user.ui_elements(["div", "text"])

    GREEN = "88d61a"
    RED = "d61a1a"
    BLUE = "1a1ad6"
    YELLOW = "d6d61a"

    key_css = {
        "padding": 8,
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
        "margin": 1,
        "width": KEY_SIZE,
        "height": KEY_SIZE
    }

    def button(key_name, text_content, color, width=KEY_SIZE):
        return div(
            key_css,
            id=key_name,
            width=width,
            highlight_color=color,
            background_color=f"{color}55",
            border_radius=KEY_SIZE
        )[
            text(text_content)
        ]

    def blank_area():
        return div(key_css)[text(" ")]

    return div(flex_direction="column")[
        div(flex_direction="row")[blank_area(), button("gamepad_y", "Y", YELLOW), blank_area()],
        div(flex_direction="row")[button("gamepad_x", "X", BLUE), blank_area(), button("gamepad_b", "B", RED)],
        div(flex_direction="row")[blank_area(), button("gamepad_a", "A", GREEN), blank_area()]
    ]

def line_separator_ui():
    (div, text) = actions.user.ui_elements(["div", "text"])
    return div(background_color="FFFFFF66", width=120, height=2)

def show_hud_ui():
    (div, screen, text) = actions.user.ui_elements(["div", "screen", "text"])

    ui_hud = screen(align_items="center", justify_content="flex_end")[
        div(background_color="00000066", border_radius=16, margin=16, margin_bottom=300, padding=16, border_width=1, border_color="FF0000aa")[
            div(flex_direction="row", gap=16)[
                div()[
                    text("pad", margin_bottom=16),
                    dpad_ui()
                ],
                div()[
                    div(flex_direction="row", margin_bottom=16, gap=8)[
                        text("go"),
                        text("5", id="go_power", color=accent_color),
                    ],
                    stick_ui("left"),
                ],
                div()[
                    div(flex_direction="row", margin_bottom=16, gap=8)[
                        text("cam"),
                        text("5", id="cam_power", color=accent_color),
                    ],
                    stick_ui("right"),
                ],
                div()[
                    text("buttons", margin_bottom=16),
                    xbox_primary_buttons_ui(),
                ],
                div()[
                    text("triggers / bumpers", margin_bottom=16),
                    div(flex_direction="column", gap=8)[
                        div(flex_direction="row", gap=8)[
                            div(id="left_trigger", flex_direction="row", padding=8, border_radius=4, background_color="333333dd", width=60, gap=8, justify_content="center")[
                                text("LT"),
                                text("5", id="left_trigger_power", color=accent_color),
                            ],
                            div(id="right_trigger", flex_direction="row", padding=8, border_radius=4, background_color="333333dd", width=60, gap=8, justify_content="center")[
                                text("RT"),
                                text("5", id="right_trigger_power", color=accent_color),
                            ]
                        ],
                        div(flex_direction="row", gap=8)[
                            div(id="gamepad_left_shoulder", flex_direction="row", padding=8, border_radius=4, background_color="333333dd", width=60, justify_content="center")[
                                text("LB")
                            ],
                            div(id="gamepad_right_shoulder", flex_direction="row", padding=8, border_radius=4, background_color="333333dd", width=60, justify_content="center")[
                                text("RB"),
                            ]
                        ]
                    ]
                ],
                div()[
                    text("noises", margin_bottom=16),
                    # cam_mode_ui(),
                    # line_separator_ui(),
                    noises_ui()
                ],
            ],
            live_text_keys_ui()
        ],
    ]

    ui_hud.show()

commands = [
    "<key>",
    "hold <key>",
    "free <key>",
    "long <key>",
    "go",
    "go <dir>",
    "<dir>",
    "back",
    "cam <dir>",
    "cam mid",
    "look <dir>",
    "round",
    "gear <num>",
    "click",
    "trick",
    "run",
    "halt",
    "stop",
    "game exit"
]

def show_commands_ui():
    global ui_commands
    (div, text, screen) = actions.user.ui_elements(["div", "text", "screen"])

    ui_commands = screen(align_items="flex_end", justify_content="center")[
        div(background_color="00000066", margin=16, margin_right=32, padding=16)[
            div(flex_direction="row", gap=16)[
                div(gap=8)[
                    text("commands", font_weight="bold"),
                    *(text(command) for command in commands),
                ],
            ]
        ],
    ]

    ui_commands.show()

def update_pop(new_action_name):
    actions.user.ui_elements_set_text("pop", new_action_name)

def update_hiss(new_action_name):
    actions.user.ui_elements_set_text("hiss", new_action_name)

def on_event(event):
    if event.type == "change":
        if event.name == "pop":
            actions.user.ui_elements_set_text("pop_value", event.action_name)
        elif event.name == "hiss" or event.name == "wish":
            actions.user.ui_elements_set_text("hiss_value", event.action_name)
    elif event.type == "action":
        if event.name == "pop":
            actions.user.ui_elements_highlight_briefly("pop")
        elif event.name == "hiss" or event.name == "wish":
            actions.user.ui_elements_highlight("hiss")
    elif event.type == "action_stop" and event.name == "hiss":
        actions.user.ui_elements_unhighlight("hiss")

def on_mouse_dir(x: float, y: float):
    directions = {
        (-1, 0): "cam_left",
        (1, 0): "cam_right",
        (0, -1): "cam_up",
        (0, 1): "cam_down",
    }

    for direction in directions.values():
        actions.user.ui_elements_unhighlight(direction)

    if x < 0:
        actions.user.ui_elements_highlight(directions[(-1, 0)])
    elif x > 0:
        actions.user.ui_elements_highlight(directions[(1, 0)])

    if y < 0:
        actions.user.ui_elements_highlight(directions[(0, -1)])
    elif y > 0:
        actions.user.ui_elements_highlight(directions[(0, 1)])

def on_button(button, state):
    if state == "hold":
        actions.user.ui_elements_highlight(f"gamepad_{button}")
    elif state == "release":
        actions.user.ui_elements_unhighlight(f"gamepad_{button}")

def on_joystick_dir(subject, coords):
    print(f"subject: {subject}, coords: {coords}")
    directions = {
        (-1, 0): "stick_left",
        (1, 0): "stick_right",
        (0, -1): "stick_down",
        (0, 1): "stick_up",
    }

    for direction in directions.values():
        if subject == "left_stick":
            actions.user.ui_elements_unhighlight(f"left_{direction}")
        elif subject == "right_stick":
            actions.user.ui_elements_unhighlight(f"right_{direction}")

    if coords in directions:
        if subject == "left_stick":
            actions.user.ui_elements_highlight(f"left_{directions[coords]}")
        elif subject == "right_stick":
            actions.user.ui_elements_highlight(f"right_{directions[coords]}")

def on_stick(event):
    if event.type == "gear_change":
        gear_state = event.value
        if event.subject == "right_stick":
            actions.user.ui_elements_set_text("cam_power", gear_state.gear)
        elif event.subject == "left_stick":
            actions.user.ui_elements_set_text("go_power", gear_state.gear)
    elif event.type == "dir_change":
        on_joystick_dir(event.subject, event.value)

def on_trigger(event):
    if event.type == "hold":
        actions.user.ui_elements_highlight(event.subject)
    elif event.type == "release":
        actions.user.ui_elements_unhighlight(event.subject)
    elif event.type == "gear_change":
        gear_state = event.value
        actions.user.ui_elements_set_text(f"{event.subject}_power", gear_state.gear)

def on_xbox_event(event):
    print(f"on_xbox_event: {event}")
    if event.subject == "right_stick" or event.subject == "left_stick":
        on_stick(event)
    elif event.subject == "left_trigger" or event.subject == "right_trigger":
        on_trigger(event)
    else:
        if event.type == "hold":
            actions.user.ui_elements_highlight(f"gamepad_{event.subject}")
        elif event.type == "release":
            actions.user.ui_elements_unhighlight(f"gamepad_{event.subject}")

def show_ui():
    show_hud_ui()
    show_commands_ui()
    actions.user.game_event_register_on_key(on_key)
    actions.user.game_event_register_on_xbox_gamepad_event(on_xbox_event)
    actions.user.dynamic_actions_event_register(on_event)

def hide_ui():
    actions.user.ui_elements_hide_all()
    actions.user.game_event_unregister_all()
    actions.user.dynamic_actions_event_unregister_all()
