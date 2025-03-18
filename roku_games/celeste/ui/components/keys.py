from talon import actions

key_style = {
    "padding": 8,
    "background_color": "333333",
    "flex_direction": "row",
    "justify_content": "center",
    "align_items": "center",
    "margin": 1,
    "min_width": 60,
    "height": 60,
    "opacity": 0.7,
}

def key(key_name, text_content):
    div, text = actions.user.ui_elements(["div", "text"])

    if isinstance(text_content, list):
        return div(key_style, flex_direction="column", id=key_name, gap=8)[
            text(text_content[0]),
            text(text_content[1], font_size=12)
        ]

    return div(key_style, id=key_name)[
        text(text_content)
    ]

def blank_key():
    div = actions.user.ui_elements(["div"])

    return div(key_style, opacity=0.5)

def keys():
    active_window, div = actions.user.ui_elements(["active_window", "div"])

    return active_window(align_items="flex_end", justify_content="flex_start", highlight_color="FFFFFF55")[
        div(flex_direction="row", margin_top=50, margin_right=300)[
            div(flex_direction="column")[
                div(flex_direction="row")[
                    blank_key(), key("up", "↑"), blank_key()
                ],
                div(flex_direction="row")[
                    key("left", "←"), key("down", "↓"), key("right", "→")
                ]
            ],
            div()[
                div(flex_direction="row")[
                    key("c", "jump"),
                    key("p", "jump 2"),
                    key("x", "dash"),
                    key("t", "demo"),
                ],
                div(flex_direction="row", justify_content="space_evenly")[
                    key("foot_left", ["grab", "pedal 1"]),
                    key("foot_center", ["move", "pedal 2"]),
                    key("foot_right", ["jump 3", "pedal 3"])
                ]
            ],
        ],
    ]

def show_keys():
    actions.user.ui_elements_show(keys)
    actions.user.game_ui_register_live_keys()

def hide_keys():
    actions.user.game_ui_unregister_live_keys()
    actions.user.ui_elements_hide(keys)