from talon import actions, cron

accent_color = "87ceeb"
live_text_keys_state = ""
pressed_keys = []
clear_pressed_keys_job = None
KEY_SIZE = 30

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
        "background_color": "333333dd",
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
        "margin": 1,
        "width": KEY_SIZE,
        "height": KEY_SIZE
    }

    def key(key_name, text_content, width=KEY_SIZE):
        return div(key_css, id=key_name, width=width)[
            text(text_content)
        ]

    def blank_key():
        return div(key_css, background_color="33333355")[text(" ")]

    return div(flex_direction="column")[
        div(flex_direction="row")[blank_key(), key("gamepad_dpad_up", "↑"), blank_key()],
        div(flex_direction="row")[key("gamepad_dpad_left", "←"), blank_key(), key("gamepad_dpad_right", "→")],
        div(flex_direction="row")[blank_key(), key("gamepad_dpad_down", "↓"), blank_key()]
    ]

def noises_ui():
    (div, text) = actions.user.ui_elements(["div", "text"])

    return div(flex_direction="row", gap=16, margin_top=12)[
        div(gap=8, width=150)[
            text("pop"),
            text("", id="pop", width=150, padding=8, font_size=20, font_weight="bold")
        ],
        div(gap=8, width=150)[
            text("hiss (wish)"),
            text("", id="hiss", width=150, padding=8, font_size=20, font_weight="bold")
        ]
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
    return div(background_color="FFFFFF66", width=300, height=2)

def show_hud_ui():
    (div, screen) = actions.user.ui_elements(["div", "screen"])

    ui_hud = screen(align_items="center", justify_content="flex_end")[
        div(background_color="00000066", border_radius=16, margin=16, margin_bottom=300, padding=16)[
            div(flex_direction="row", gap=16, justify_content="center", align_items="center")[
                div()[
                    cam_edges_ui(dpad_ui())
                ],
                div()[
                    cam_mode_ui(),
                    line_separator_ui(),
                    noises_ui()
                ],
                div()[
                    xbox_primary_buttons_ui(),
                ]
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
            actions.user.ui_elements_set_text("pop", event.action_name)
        elif event.name == "hiss" or event.name == "wish":
            actions.user.ui_elements_set_text("hiss", event.action_name)
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

def on_joystick_dir(joystick, coords):
    print(f"joystick: {joystick}, coords: {coords}")
    if joystick == "left_joystick":
        directions = {
            (-1, 0): "cam_left",
            (1, 0): "cam_right",
            (0, -1): "cam_up",
            (0, 1): "cam_down",
        }

        for direction in directions.values():
            actions.user.ui_elements_unhighlight(direction)

        if coords in directions:
            actions.user.ui_elements_highlight(directions[coords])

def show_ui():
    show_hud_ui()
    show_commands_ui()
    actions.user.game_event_register_on_key(on_key)
    actions.user.dynamic_actions_event_register(on_event)
    actions.user.mouse_move_dir_change_event_register(on_mouse_dir)
    actions.user.vgamepad_event_register_on_button(on_button)
    actions.user.vgamepad_event_register_joystick_dir_change(on_joystick_dir)

def hide_ui():
    actions.user.ui_elements_hide_all()
    actions.user.game_event_unregister_all()
    actions.user.dynamic_actions_event_unregister_all()
    actions.user.mouse_move_event_unregister_all()
    actions.user.vgamepad_event_unregister_all()
