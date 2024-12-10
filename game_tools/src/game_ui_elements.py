from talon import Module, actions, Context, registry, settings

mod = Module()
ctx = Context()

ui_elements_register_on_lifecycle_init = False
listening_for_xbox_events = False
listening_for_key_events = False
game_event_register_on_xbox_event_init = False
game_event_register_on_keys_init = False
include_key_events = False
include_xbox_events = False
accent_color_default = "87ceeb"
list_names = {}
expected_keys = set()

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

def game_ui_elements_keys_dpad(wasd: bool = False, size: int = 30, props: dict = {}):
    div, text = actions.user.ui_elements(["div", "text"])
    if wasd:
        expected_keys.update(["w", "a", "s", "d"])
    else:
        expected_keys.update(["up", "down", "left", "right"])

    key_css = {
        "padding": 8,
        "background_color": "333333",
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
        "margin": 1,
        "width": size,
        "height": size,
        "opacity": props.get("opacity") or 0.7
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

    return div(props, flex_direction="column")[
        row()[blank_key(), key_up, blank_key()],
        row()[key_left, key_down, key_right]
    ]

def game_key_ui(key_name: str, text_content: str, size: int = 30, props: dict = {}):
    div, text = actions.user.ui_elements(["div", "text"])
    expected_keys.add(key_name)

    key_css = {
        "padding": 8,
        "background_color": "333333",
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
        "margin": 1,
        "width": size,
        "height": size,
        "opacity": 0.7,
        **props
    }

    return div(key_css, id=key_name)[
        text(text_content)
    ]

def xbox_stick_ui(
    subject: str,
    label: str,
    size : int = 30,
    accent_color: str = None,
):
    div, text = actions.user.ui_elements(["div", "text"])
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
    div, text = actions.user.ui_elements(["div", "text"])

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
            highlight_color=f"{color}77",
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
    div, text = actions.user.ui_elements(["div", "text"])

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
    div, text = actions.user.ui_elements(["div", "text"])
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
    div, text = actions.user.ui_elements(["div", "text"])
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
    div, text = actions.user.ui_elements(["div", "text"])

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

def on_key(key, state):
    if state == "press":
        actions.user.ui_elements_highlight_briefly(key)
    elif state == "hold":
        actions.user.ui_elements_highlight(key)
    elif state == "release":
        actions.user.ui_elements_unhighlight(key)

def on_key_new(key, state):
    if state == "press":
        actions.user.ui_elements_highlight_briefly(key)
    elif state == "hold":
        actions.user.ui_elements_highlight(key)
    elif state == "release":
        actions.user.ui_elements_unhighlight(key)

def on_trigger(event):
    if event.type == "hold":
        actions.user.ui_elements_highlight(event.subject)
    elif event.type == "release":
        actions.user.ui_elements_unhighlight(event.subject)
    elif event.type == "gear_change":
        gear_state = event.value
        actions.user.ui_elements_set_text(f"{event.subject}_gear", gear_state.gear)

def on_xbox_event(event):
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

def register_live_keys():
    actions.user.game_event_register_on_key(on_key_new)

def unregister_live_keys():
    actions.user.game_event_unregister_on_key(on_key_new)

def on_xbox_ui_mount():
    actions.user.game_event_register_on_xbox_event(on_xbox_event)
    preferred_dir_mode_subject = settings.get("user.game_xbox_preferred_dir_mode_subject")
    if preferred_dir_mode_subject:
        actions.user.ui_elements_highlight(f"{preferred_dir_mode_subject}_preferred", f"{GREEN}55")

def on_xbox_ui_unmount():
    global listening_for_xbox_events
    actions.user.game_event_unregister_all_on_xbox_event()
    listening_for_xbox_events = False

def use_game_xbox():
    global listening_for_xbox_events

    if not listening_for_xbox_events:
        listening_for_xbox_events = True
        # user lists are dynamic so fetch at this time
        list_names["left_stick"] = get_first_list_key("user.game_xbox_left_stick")
        list_names["right_stick"] = get_first_list_key("user.game_xbox_right_stick")
        list_names["dpad"] = get_first_list_key("user.game_xbox_dpad")

        actions.user.ui_elements_register_effect(on_xbox_ui_mount, on_xbox_ui_unmount, [])

def on_keys_ui_mount():
    actions.user.game_event_register_on_key(on_key_new)

def on_keys_ui_unmount():
    global listening_for_key_events
    actions.user.game_event_unregister_on_key(on_key_new)
    listening_for_key_events = False

def use_game_keys():
    global listening_for_key_events

    if not listening_for_key_events:
        listening_for_key_events = True
        actions.user.ui_elements_register_effect(on_keys_ui_mount, on_keys_ui_unmount, [])

@mod.action_class
class Actions:
    def game_use_live_keys_effect():
        """Use game keys effect - compatible with ui_elements. """
        use_game_keys()

    def game_ui_register_live_keys():
        """Register game keys - compatible with ui_elements"""
        register_live_keys()

    def game_ui_unregister_live_keys():
        """Unregister game keys - compatible with ui_elements"""
        unregister_live_keys()

    def game_ui_element_arrows(size: int = 30, props: dict = None):
        """game ui element arrows dpad"""
        use_game_keys()
        return game_ui_elements_keys_dpad(wasd=False, size=size, props=props)

    def game_ui_element_wasd(size: int = 30, props: dict = None):
        """game ui element WASD dpad"""
        use_game_keys()
        return game_ui_elements_keys_dpad(wasd=True, size=size, props=props)

    def game_ui_element_key(key_name: str, text_content: str, size: int = 30, props: dict = None):
        """game ui element key"""
        use_game_keys()
        return game_key_ui(key_name, text_content, size, props)

    def game_ui_element_xbox_left_stick(label: str = None, size: int = 30, accent_color: str = None):
        """game ui element xbox left stick"""
        use_game_xbox()
        return xbox_stick_ui("left_stick", label, size, accent_color)

    def game_ui_element_xbox_right_stick(label: str = None, size: int = 30, accent_color: str = None):
        """game ui element xbox right stick"""
        use_game_xbox()
        return xbox_stick_ui("right_stick", label, size, accent_color)

    def game_ui_element_xbox_primary_buttons(label: str = "buttons", size: int = 30):
        """game ui element xbox primary buttons"""
        use_game_xbox()
        return xbox_primary_buttons_ui(label, size)

    def game_ui_element_xbox_center_buttons(label: str = "buttons", size: int = 20):
        """game ui element xbox center buttons"""
        use_game_xbox()
        return xbox_center_buttons_ui(size)

    def game_ui_element_xbox_dpad(label: str = None, size: int = 30):
        """game ui element xbox dpad"""
        use_game_xbox()
        return xbox_dpad_ui(label, size)

    def game_ui_element_xbox_left_trigger(label: str = "LT", size: int = 30):
        """game ui element xbox left trigger"""
        use_game_xbox()
        return xbox_trigger_ui("left_trigger", label, size)

    def game_ui_element_xbox_right_trigger(label: str = "RT", size: int = 30):
        """game ui element xbox right trigger"""
        use_game_xbox()
        return xbox_trigger_ui("right_trigger", label, size)

    def game_ui_element_xbox_left_bumper(label: str = "LB", size: int = 30):
        """game ui element xbox left bumper"""
        use_game_xbox()
        return xbox_bumper_ui("left_shoulder", label, size)

    def game_ui_element_xbox_right_bumper(label: str = "RB", size: int = 30):
        """game ui element xbox right bumper"""
        use_game_xbox()
        return xbox_bumper_ui("right_shoulder", label, size)