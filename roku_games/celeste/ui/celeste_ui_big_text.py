from talon import actions, cron

ui_noise_command = None
accent_color = "87ceeb"

live_keys_timeout = None

key_style = {
    "padding": 8,
    "background_color": "333333",
    "flex_direction": "row",
    "justify_content": "center",
    "align_items": "center",
    "margin": 1,
    "width": 60,
    "height": 60,
    "opacity": 0.5,
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

def ui_noise_command():
    (screen, div, text) = actions.user.ui_elements(["screen", "div", "text"])

    return  screen()[
        div(padding=40, margin_top=130, margin_left=50)[
            text("", id="noise", font_size=140, font_weight="bold", color="FFFFFF"),
            text("", id="command", font_size=60, margin_top=32, color="FFFFFF"),
        ]
    ]

def key(key_name, text_content, width=30):
    div, text = actions.user.ui_elements(["div", "text"])

    return div(key_style, id=key_name, width=width, background_color="333333")[
        text(text_content)
    ]

def blank_key():
    div, text = actions.user.ui_elements(["div", "text"])

    return div(key_style)[text(" ")]

def ui_keys():
    screen, div = actions.user.ui_elements(["screen", "div"])

    return screen(justify_content="flex_end", highlight_color="FFFFFF55")[
        div(flex_direction="row", margin_bottom=20, margin_left=20, opacity=0.5)[
            div(flex_direction="column")[
                div(flex_direction="row")[
                    blank_key(), key("up", "↑", 60), blank_key()
                ],
                div(flex_direction="row")[
                    key("left", "←", 60), key("down", "↓", 60), key("right", "→", 60)
                ]
            ],
            div()[
                div(flex_direction="row")[
                    key("c", "jump", 60),
                    key("p", "jump 2", 60),
                    key("foot_left", "foot1: grab", 60),
                ],
                div(flex_direction="row")[
                    key("x", "dash", 60),
                    key("t", "demo", 60),
                    key("foot_center", "foot2: move", 60)
                ]
            ],
        ],
    ]

def show_big_text_ui():
    actions.user.ui_elements_show(ui_noise_command)
    actions.user.ui_elements_show(ui_keys)
    actions.user.game_ui_register_live_keys()
    actions.user.parrot_config_event_register(on_noise)

def hide_big_text_ui():
    actions.user.game_ui_unregister_live_keys()
    actions.user.parrot_config_event_unregister(on_noise)
    actions.user.ui_elements_hide_all()

def refresh_big_text_ui():
    hide_big_text_ui()
    show_big_text_ui()