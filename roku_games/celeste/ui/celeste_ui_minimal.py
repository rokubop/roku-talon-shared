from talon import actions, cron

accent_color = "87ceeb"
live_keys_timeout = None

screen_style = {
    "id": "keys",
    "justify_content": "flex_end",
    "align_items": "flex_start",
    "highlight_color": f"{accent_color}88"
}

gamepad_style = {
    "flex_direction": "row",
    "gap": 8,
    "margin_bottom": 16,
    "margin_left": 16
}

key_style = {
    "padding": 8,
    "background_color": "333333dd",
    "flex_direction": "row",
    "justify_content": "center",
    "align_items": "center",
    "margin": 1,
    "width": 30,
    "height": 30,
}

def reset_live_keys():
    global live_keys_timeout
    actions.user.ui_elements_set_text("noise", "")
    actions.user.ui_elements_set_text("command", "")
    live_keys_timeout = None

def on_noise(noise, command_name):
    global live_keys_timeout
    if command_name:
        actions.user.ui_elements_set_text("noise", noise)
        actions.user.ui_elements_set_text("command", command_name)
        if live_keys_timeout:
            cron.cancel(live_keys_timeout)
        live_keys_timeout = cron.after("2s", reset_live_keys)

def live_text_ui():
    div, text = actions.user.ui_elements(["div", "text"])

    return div(margin_left=16)[
        text("", id="noise", font_size=30, font_weight="bold", color="FFFFFF"),
        text("", id="command", font_size=16, color="FFFFFF")
    ]

def on_key(key, state):
    if key in ["foot_left", "foot_center", "up", "down", "left", "right"]:
        if state == "press":
            actions.user.ui_elements_highlight_briefly(key)
        elif state == "hold":
            actions.user.ui_elements_highlight(key)
        elif state == "release":
            actions.user.ui_elements_unhighlight(key)

def keys_ui():
    div, text, screen = actions.user.ui_elements(["div", "text", "screen"])

    def key(key_name, text_content, width=30):
        return div(key_style, id=key_name, width=width)[
            text(text_content)
        ]

    def blank_key():
        return div(key_style, background_color="33333355")[text(" ")]

    def col():
        return div(flex_direction="column")

    def row():
        return div(flex_direction="row")

    return screen(screen_style)[
        div(gamepad_style)[
            row()[
                col()[
                    row()[blank_key(), key("up", "↑"), blank_key()],
                    row()[key("left", "←"), key("down", "↓"), key("right", "→")]
                ],
                col()[
                    row()[key("c", "jump"), key("p", "jump 2")],
                    row()[key("x", "dash"), key("t", "demo", width="100%")]
                ],
                col()[
                    key("foot_left", "foot1: grab", width="100%"),
                    key("foot_center", "foot2: move mode")
                ],
                live_text_ui()
            ],
        ]
    ]

def show_minimal_ui():
    actions.user.ui_elements_show(keys_ui)
    actions.user.game_event_register_on_key(on_key)
    actions.user.parrot_config_event_register(on_noise)

def hide_minimal_ui():
    actions.user.game_event_unregister_on_key(on_key)
    actions.user.parrot_config_event_unregister(on_noise)
    actions.user.ui_elements_hide_all()