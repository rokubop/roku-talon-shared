from talon import Module, actions, app

mod = Module()

ui_elements_register_on_lifecycle_init = False
game_event_register_on_xbox_event_init = False
accent_color_default = "87ceeb"

def game_ui_elements_keys_dpad(wasd: bool = False, size: int = 30):
    (div, text) = actions.user.ui_elements(["div", "text"])

    key_css = {
        "padding": 8,
        "background_color": "333333dd",
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
        "margin": 1,
        "width": size,
        "height": size
    }

    def key(key_name, text_content, width=size):
        return div(key_css, id=key_name, width=width)[
            text(text_content)
        ]

    def blank_key():
        return div(key_css, background_color="33333355")[text(" ")]

    def row():
        return div(flex_direction="row")

    key_up = key("w", "W") if wasd else key("up", "↑")
    key_left = key("a", "A") if wasd else key("left", "←")
    key_down = key("s", "S") if wasd else key("down", "↓")
    key_right = key("d", "D") if wasd else key("right", "→")

    return div(flex_direction="column")[
        row()[blank_key(), key_up, blank_key()],
        row()[key_left, key_down, key_right]
    ]

def xbox_stick_ui(
    subject: str,
    label: str,
    size : int = 30,
    accent_color: str = None,
):
    (div, text) = actions.user.ui_elements(["div", "text"])
    accent_color = accent_color or accent_color_default

    key_css = {
        "padding": 8,
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
        "border_radius": size,
        "width": size,
        "height": size
    }

    def key(key_name, text_content, width=size):
        return div(key_css, id=key_name, width=width, background_color="333333cc")[
            text(text_content)
        ]

    def blank_key():
        return div(key_css)[text(" ")]

    return div()[
        div(flex_direction="row", margin_bottom=16, gap=8)[
            text(label),
            text("5", id=f"{subject}_gear", color=accent_color),
        ],
        div(flex_direction="column", background_color="333333dd", border_radius=100, padding=1)[
            div(flex_direction="row")[
                blank_key(), key(f"{subject}_up", " "), blank_key()
            ],
            div(flex_direction="row")[
                key(f"{subject}_left", " "), blank_key(), key(f"{subject}_right", " ")
            ],
            div(flex_direction="row")[
                blank_key(), key(f"{subject}_down", " "), blank_key()
            ]
        ]
    ]

def xbox_primary_buttons_ui(label: str, size : int = 30):
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
        "width": size,
        "height": size
    }

    def button(key_name, text_content, color, width=size):
        return div(
            key_css,
            id=key_name,
            width=width,
            highlight_color=color,
            background_color=f"{color}55",
            border_radius=size
        )[
            text(text_content)
        ]

    def blank_area():
        return div(key_css)[text(" ")]

    return div()[
        text(label, margin_bottom=16),
        div(flex_direction="column")[
            div(flex_direction="row")[
                blank_area(), button("gamepad_y", "Y", YELLOW), blank_area()
            ],
            div(flex_direction="row")[
                button("gamepad_x", "X", BLUE), blank_area(), button("gamepad_b", "B", RED)
            ],
            div(flex_direction="row")[
                blank_area(), button("gamepad_a", "A", GREEN), blank_area()
            ]
        ]
    ]

def xbox_dpad_ui(label: str, size : int = 30):
    (div, text) = actions.user.ui_elements(["div", "text"])

    key_css = {
        "padding": 8,
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
        "width": size,
        "height": size
    }

    def key(key_name, text_content, width=size):
        return div(key_css, id=key_name, width=width, background_color="333333dd")[
            text(text_content)
        ]

    def blank_key():
        return div(key_css)[text(" ")]

    def blank_middle_key():
        return div(key_css, background_color="333333dd")[text(" ")]

    return div()[
        text(label, margin_bottom=16),
        div(flex_direction="column")[
            div(flex_direction="row")[
                blank_key(), key("gamepad_dpad_up", "↑"), blank_key()
            ],
            div(flex_direction="row")[
                key("gamepad_dpad_left", "←"),
                blank_middle_key(),
                key("gamepad_dpad_right", "→")
            ],
            div(flex_direction="row")[
                blank_key(), key("gamepad_dpad_down", "↓"), blank_key()
            ]
        ]
    ]

def xbox_trigger_ui(subject: str, label: str, size : int = 30, accent_color: str = None):
    (div, text) = actions.user.ui_elements(["div", "text"])
    accent_color = accent_color or accent_color_default

    return div(
        id=subject,
        flex_direction="row",
        padding=8,
        border_radius=4,
        background_color="333333dd",
        width=size*2,
        gap=8,
        justify_content="center"
    )[
        text(label),
        text("5", id=f"{subject}_gear", color=accent_color),
    ]

def xbox_bumpber_ui(subject: str, label: str, size : int = 30):
    (div, text) = actions.user.ui_elements(["div", "text"])

    div(
        id=subject,
        flex_direction="row",
        padding=8,
        border_radius=4,
        background_color="333333dd",
        width=size*2,
        justify_content="center"
    )[
        text(label)
    ]

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
    # print(f"on_xbox_event: {event}")
    if event.subject == "right_stick" or event.subject == "left_stick":
        on_stick(event)
    elif event.subject == "left_trigger" or event.subject == "right_trigger":
        on_trigger(event)
    else:
        if event.type == "hold":
            actions.user.ui_elements_highlight(f"gamepad_{event.subject}")
        elif event.type == "release":
            actions.user.ui_elements_unhighlight(f"gamepad_{event.subject}")

def on_ui_lifecycle(event):
    global ui_elements_register_on_lifecycle_init
    global game_event_register_on_xbox_event_init

    if event.type == "mount":
        if not game_event_register_on_xbox_event_init:
            print("on_ui_lifecycle mount")
            game_event_register_on_xbox_event_init = True
            actions.user.game_event_register_on_xbox_event(on_xbox_event)
    elif event.type == "unmount":
        print("on_ui_lifecycle unmount")
        if game_event_register_on_xbox_event_init:
            game_event_register_on_xbox_event_init = False
            actions.user.game_event_unregister_all_on_xbox_event()
        if ui_elements_register_on_lifecycle_init:
            ui_elements_register_on_lifecycle_init = False
            actions.user.ui_elements_unregister_on_lifecycle(on_ui_lifecycle)

def events_init():
    global ui_elements_register_on_lifecycle_init
    if not ui_elements_register_on_lifecycle_init:
        ui_elements_register_on_lifecycle_init = True
        print("events_init")
        actions.user.ui_elements_register_on_lifecycle(on_ui_lifecycle)

@mod.action_class
class Actions:
    def game_ui_element_arrows_dpad(size: int = 30):
        """game ui element arrows dpad"""
        events_init()
        return game_ui_elements_keys_dpad(wasd=False, size=size)

    def game_ui_element_wasd_dpad(size: int = 30):
        """game ui element WASD dpad"""
        events_init()
        return game_ui_elements_keys_dpad(wasd=True, size=size)

    def game_ui_element_xbox_left_stick(label: str, size: int = 30, accent_color: str = None):
        """game ui element xbox left stick"""
        events_init()
        return xbox_stick_ui("left_stick", label, size, accent_color)

    def game_ui_element_xbox_right_stick(label: str, size: int = 30, accent_color: str = None):
        """game ui element xbox right stick"""
        events_init()
        return xbox_stick_ui("right_stick", label, size, accent_color)

    def game_ui_element_xbox_primary_buttons(size: int = 30):
        """game ui element xbox primary buttons"""
        events_init()
        return xbox_primary_buttons_ui(size)

    def game_ui_element_xbox_dpad(size: int = 30):
        """game ui element xbox dpad"""
        events_init()
        return xbox_dpad_ui(size)

    def game_ui_element_xbox_left_trigger(label: str, size: int = 30):
        """game ui element xbox left trigger"""
        events_init()
        return xbox_trigger_ui("left_trigger", label, size)

    def game_ui_element_xbox_right_trigger(label: str, size: int = 30):
        """game ui element xbox right trigger"""
        events_init()
        return xbox_trigger_ui("right_trigger", label, size)

    def game_ui_element_xbox_left_bumper(label: str, size: int = 30):
        """game ui element xbox left bumper"""
        events_init()
        return xbox_bumpber_ui("left_shoulder", label, size)

    def game_ui_element_xbox_right_bumper(label: str, size: int = 30):
        """game ui element xbox right bumper"""
        events_init()
        return xbox_bumpber_ui("right_shoulder", label, size)