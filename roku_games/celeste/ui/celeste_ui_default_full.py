from talon import actions

accent_color = "87ceeb"

screen_style = {
    "id": "keys",
    "justify_content": "flex_start",
    "align_items": "flex_end",
    "highlight_color": f"{accent_color}88"
}

gamepad_style = {
    "flex_direction": "column",
    "gap": 0,
    "margin_top": 605,
    "margin_right": 16
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

def commands_ui():
    div, text, screen, state = actions.user.ui_elements(["div", "text", "screen", "state"])
    parrot_config = state.get("parrot_config")
    background_color = state.get("background_color", "000000")
    commands, acts = actions.user.parrot_config_format_display(parrot_config)

    return screen(align_items="flex_end", justify_content="flex_start")[
        div(background_color=f"{background_color}66", margin=16, margin_right=32, padding=16)[
            div(flex_direction="row", gap=16)[
                div(gap=8)[
                    text("sound", font_weight="bold"),
                    *(text(command) for command in commands),
                ],
                div(gap=8)[
                    text("actions", font_weight="bold", color=accent_color),
                    *(text(action, color=accent_color) for action in acts),
                ]
            ],
        ],
    ]

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
                    row()[key("x", "dash"), key("t", "demo")]
                ]
            ],
            row()[
                key("foot_left", "foot1: grab"),
                key("foot_center", "foot2: move mode")
            ]
        ]
    ]

def on_key(key, state):
    if state == "press":
        actions.user.ui_elements_highlight_briefly(key)
    elif state == "hold":
        actions.user.ui_elements_highlight(key)
    elif state == "release":
        actions.user.ui_elements_unhighlight(key)

def show_full_ui(parrot_config):
    actions.user.ui_elements_show(commands_ui, initial_state={
        "parrot_config": parrot_config
    })
    actions.user.ui_elements_show(keys_ui)
    actions.user.game_event_register_on_key(on_key)

def hide_full_ui():
    actions.user.game_event_unregister_on_key(on_key)
    actions.user.ui_elements_hide_all()