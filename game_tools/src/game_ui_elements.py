from talon import Module, actions, Context, registry, settings

mod = Module()
ctx = Context()

ui_elements_register_on_lifecycle_init = False
game_event_register_on_xbox_event_init = False
include_key_events = False
include_xbox_events = False
accent_color_default = "87ceeb"
list_names = {}

GREEN = "88d61a"
RED = "d61a1a"
BLUE = "1a1ad6"
YELLOW = "d6d61a"

def get_first_list_key(list_name: str):
    list_key_values = list(registry.lists[list_name])[0]
    if list_key_values:
        first_key = next(iter(list_key_values), None)
        return first_key

def get_key_from_list(list_name: str, value: str):
    list_key_values = list(registry.lists[list_name])[0]
    if list_key_values:
        key = next((key for key, val in list_key_values.items() if val == value), None)
        return key

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
    label = label or list_names[subject]
    gear = settings.get(f"user.game_xbox_{subject}_default_gear") or 5

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
            text(text_content, font_size=size//2)
        ]

    def blank_key(id: str = ""):
        return div(key_css, id=id)[text(" ")]

    thumb = "left_thumb" if subject == "left_stick" else "right_thumb"

    return div()[
        div(flex_direction="row", margin_bottom=16, gap=8)[
            text(label),
            text(gear, id=f"{subject}_gear", color=accent_color),
            div(id=f"{subject}_preferred", width=12, height=12, border_radius=12)[text(" ")]
        ],
        div(id=subject, flex_direction="column", background_color="333333dd", border_radius=100, padding=1)[
            div(flex_direction="row")[
                blank_key(), key(f"{subject}_up", " "), blank_key()
            ],
            div(flex_direction="row")[
                key(f"{subject}_left", " "), blank_key(thumb), key(f"{subject}_right", " ")
            ],
            div(flex_direction="row")[
                blank_key(), key(f"{subject}_down", " "), blank_key()
            ]
        ]
    ]

def xbox_primary_buttons_ui(label: str, size : int = 30):
    (div, text) = actions.user.ui_elements(["div", "text"])

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
            text(text_content, font_size=size//2)
        ]

    def blank_area():
        return div(key_css)[text(" ")]

    return div()[
        text(label, margin_bottom=16),
        div(flex_direction="column")[
            div(flex_direction="row")[
                blank_area(), button("y", "Y", YELLOW), blank_area()
            ],
            div(flex_direction="row")[
                button("x", "X", BLUE), blank_area(), button("b", "B", RED)
            ],
            div(flex_direction="row")[
                blank_area(), button("a", "A", GREEN), blank_area()
            ]
        ]
    ]

def xbox_center_buttons_ui(size : int):
    (div, text) = actions.user.ui_elements(["div", "text"])

    container_css = {
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
        "gap": 16,
    }

    css = {
        "width": size,
        "height": size,
        "border_radius": size,
        "border_width": 1,
        "border_color": "FFFFFF33",
        "background_color": "33333333",
    }

    return div(container_css)[
        div(css, id="back")[text(" ")],
        div(css, id="guide", border_color=f"{GREEN}55", highlight_color=f"{GREEN}55")[text(" ")],
        div(css, id="start")[text(" ")]
    ]

def xbox_dpad_ui(label: str, size : int = 30):
    (div, text) = actions.user.ui_elements(["div", "text"])
    label = label or list_names["dpad"]

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
        div(flex_direction="row", margin_bottom=16, gap=8)[
            text(label),
            div(id="dpad_preferred", width=12, height=12, border_radius=12)[text(" ")],
        ],
        div(flex_direction="column")[
            div(flex_direction="row")[
                blank_key(), key("dpad_up", "↑"), blank_key()
            ],
            div(flex_direction="row")[
                key("dpad_left", "←"),
                blank_middle_key(),
                key("dpad_right", "→")
            ],
            div(flex_direction="row")[
                blank_key(), key("dpad_down", "↓"), blank_key()
            ]
        ]
    ]

def xbox_trigger_ui(subject: str, label: str, size : int = 30, accent_color: str = None):
    (div, text) = actions.user.ui_elements(["div", "text"])
    accent_color = accent_color or accent_color_default
    gear = settings.get(f"user.game_xbox_{subject}_default_gear") or 5

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
        text(gear, id=f"{subject}_gear", color=accent_color),
    ]

def xbox_bumper_ui(subject: str, label: str, size : int = 30):
    (div, text) = actions.user.ui_elements(["div", "text"])

    return div(
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
        actions.user.ui_elements_highlight(button)
    elif state == "release":
        actions.user.ui_elements_unhighlight(button)


def on_stick_dir(subject, coords):
    x, y = coords

    for direction in ["up", "down", "left", "right"]:
        actions.user.ui_elements_unhighlight(f"{subject}_{direction}")

    if x < 0:
        actions.user.ui_elements_highlight(f"{subject}_left")
    if x > 0:
        actions.user.ui_elements_highlight(f"{subject}_right")
    if y < 0:
        actions.user.ui_elements_highlight(f"{subject}_down")
    if y > 0:
        actions.user.ui_elements_highlight(f"{subject}_up")

def on_stick(event):
    if event.type == "gear_change":
        gear_state = event.value
        actions.user.ui_elements_set_text(f"{event.subject}_gear", gear_state.gear)
    elif event.type == "dir_change":
        on_stick_dir(event.subject, event.value)

def on_dpad_dir(dir):
    for direction in ["up", "down", "left", "right"]:
        actions.user.ui_elements_unhighlight(f"dpad_{direction}")

    actions.user.ui_elements_highlight(f"dpad_{dir}")

def on_trigger(event):
    if event.type == "hold":
        actions.user.ui_elements_highlight(event.subject)
    elif event.type == "release":
        actions.user.ui_elements_unhighlight(event.subject)
    elif event.type == "gear_change":
        gear_state = event.value
        actions.user.ui_elements_set_text(f"{event.subject}_gear", gear_state.gear)

def on_xbox_event(event):
    # print(f"on_xbox_event: {event}")
    if event.type == "preferred_dir_mode_change":
        actions.user.ui_elements_unhighlight("left_stick_preferred")
        actions.user.ui_elements_unhighlight("right_stick_preferred")
        actions.user.ui_elements_unhighlight("dpad_preferred")
        actions.user.ui_elements_highlight(f"{event.subject}_preferred", f"{GREEN}55")
    elif event.subject == "right_stick" or event.subject == "left_stick":
        on_stick(event)
    elif event.subject == "left_trigger" or event.subject == "right_trigger":
        on_trigger(event)
    elif event.subject == "dpad" and event.type == "dir_change":
        on_dpad_dir(event.value)
    else:
        if event.type == "hold":
            color = GREEN if event.subject == "guide" else None
            actions.user.ui_elements_highlight(event.subject, color)
        elif event.type == "release":
            actions.user.ui_elements_unhighlight(event.subject)

def on_ui_lifecycle(event):
    global ui_elements_register_on_lifecycle_init
    global game_event_register_on_xbox_event_init
    global include_xbox_events, include_key_events

    ids_to_check = ["dpad_up", "left_stick", "right_stick", "left_trigger", "a"]
    children_ids = event.children_ids

    if not any(id in children_ids for id in ids_to_check):
        # different UI that we don't care about
        return

    if event.type == "mount":
        if include_xbox_events and not game_event_register_on_xbox_event_init:
            game_event_register_on_xbox_event_init = True
            actions.user.game_event_register_on_xbox_event(on_xbox_event)
            preferred_dir_mode_subject = settings.get("user.game_xbox_preferred_dir_mode_subject")
            if preferred_dir_mode_subject:
                actions.user.ui_elements_highlight(f"{preferred_dir_mode_subject}_preferred", f"{GREEN}55")
    elif event.type == "unmount":
        if include_xbox_events and game_event_register_on_xbox_event_init:
            game_event_register_on_xbox_event_init = False
            include_xbox_events = False
            actions.user.game_event_unregister_all_on_xbox_event()
        if ui_elements_register_on_lifecycle_init:
            ui_elements_register_on_lifecycle_init = False
            actions.user.ui_elements_unregister_on_lifecycle(on_ui_lifecycle)

def events_init(type: str):
    global ui_elements_register_on_lifecycle_init, include_key_events, include_xbox_events
    if type == "keys":
        include_key_events = True
    elif type == "xbox":
        include_xbox_events = True
        list_names["left_stick"] = get_first_list_key("user.game_xbox_left_stick")
        list_names["right_stick"] = get_first_list_key("user.game_xbox_right_stick")
        list_names["dpad"] = get_first_list_key("user.game_xbox_dpad")

    if not ui_elements_register_on_lifecycle_init:
        ui_elements_register_on_lifecycle_init = True
        actions.user.ui_elements_register_on_lifecycle(on_ui_lifecycle)

@mod.action_class
class Actions:
    def game_ui_element_arrows(size: int = 30, props: dict = None):
        """game ui element arrows dpad"""
        events_init("keys")
        return game_ui_elements_keys_dpad(wasd=False, size=size)

    def game_ui_element_wasd(size: int = 30):
        """game ui element WASD dpad"""
        events_init("keys")
        return game_ui_elements_keys_dpad(wasd=True, size=size)

    def game_ui_element_xbox_left_stick(label: str = None, size: int = 30, accent_color: str = None):
        """game ui element xbox left stick"""
        events_init("xbox")
        return xbox_stick_ui("left_stick", label, size, accent_color)

    def game_ui_element_xbox_right_stick(label: str = None, size: int = 30, accent_color: str = None):
        """game ui element xbox right stick"""
        events_init("xbox")
        return xbox_stick_ui("right_stick", label, size, accent_color)

    def game_ui_element_xbox_primary_buttons(label: str = "buttons", size: int = 30):
        """game ui element xbox primary buttons"""
        events_init("xbox")
        return xbox_primary_buttons_ui(label, size)

    def game_ui_element_xbox_center_buttons(label: str = "buttons", size: int = 20):
        """game ui element xbox center buttons"""
        events_init("xbox")
        return xbox_center_buttons_ui(size)

    def game_ui_element_xbox_dpad(label: str = None, size: int = 30):
        """game ui element xbox dpad"""
        events_init("xbox")
        return xbox_dpad_ui(label, size)

    def game_ui_element_xbox_left_trigger(label: str = "LT", size: int = 30):
        """game ui element xbox left trigger"""
        events_init("xbox")
        return xbox_trigger_ui("left_trigger", label, size)

    def game_ui_element_xbox_right_trigger(label: str = "RT", size: int = 30):
        """game ui element xbox right trigger"""
        events_init("xbox")
        return xbox_trigger_ui("right_trigger", label, size)

    def game_ui_element_xbox_left_bumper(label: str = "LB", size: int = 30):
        """game ui element xbox left bumper"""
        events_init("xbox")
        return xbox_bumper_ui("left_shoulder", label, size)

    def game_ui_element_xbox_right_bumper(label: str = "RB", size: int = 30):
        """game ui element xbox right bumper"""
        events_init("xbox")
        return xbox_bumper_ui("right_shoulder", label, size)