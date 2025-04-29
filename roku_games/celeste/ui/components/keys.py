from talon import actions

key_style = {
    "padding": 8,
    "background_color": "11111188",
    "flex_direction": "row",
    "justify_content": "center",
    "align_items": "center",
    "margin": 1,
    "min_width": 60,
    "height": 60,
    # "opacity": 0.5,
}

def key(key_name, text_content):
    div, text = actions.user.ui_elements(["div", "text"])

    if isinstance(text_content, list):
        return div(key_style, flex_direction="column", id=key_name, gap=8, highlight_color="33333333")[
            text(text_content[0]),
            # text(text_content[0], font_family="roboto"),
            text(text_content[1], font_size=12)
        ]

    return div(key_style, id=key_name, highlight_color="33333333")[
        text(text_content)
    ]
    # return div(key_style, id=key_name)[
    #     text(text_content, font_family="roboto")
    # ]

def key_svg(key_name, icon_name):
    div, icon = actions.user.ui_elements(["div", "icon"])

    return div(key_style, id=key_name, highlight_color="33333333")[
        icon(icon_name, stroke_width=3, size=30, stroke_linecap="butt")
    ]


def blank_key():
    div = actions.user.ui_elements(["div"])

    return div(key_style, opacity=0.5)

def on_mount():
    actions.user.game_ui_register_live_keys()

def on_unmount():
    actions.user.game_ui_unregister_live_keys()

def keys(**props):
    div, effect = actions.user.ui_elements(["div", "effect"])

    effect(on_mount, on_unmount, [])

    return div(flex_direction="row", **props)[
        # div(flex_direction="column", gap=1)[
        #     div(flex_direction="row")[
        #         blank_key(), key("up", "↑"), blank_key()
        #     ],
        #     div(flex_direction="row")[
        #         key("left", "←"), key("down", "↓"), key("right", "→")
        #     ]
        # ],
        div(flex_direction="column")[
            div(flex_direction="row")[
                blank_key(), key_svg("up", "arrow_up"), blank_key()
            ],
            div(flex_direction="row")[
                key_svg("left", "arrow_left"), key_svg("down", "arrow_down"), key_svg("right", "arrow_right")
            ]
        ],
        div(gap=1)[
            div(flex_direction="row")[
                key("c", "jump"),
                key("p", "jump 2"),
                key("x", "dash"),
                key("t", "demo"),
            ],
            div(flex_direction="row", justify_content="space_evenly", border_width=1, border_color="FFFFFF")[
                key("foot_left", ["grab", "foot 1"]),
                key("foot_center", ["side B noises", "foot 2"]),
                key("foot_right", ["jump 3", "foot 3"]),
            ]
        ],
    ]

# def show_keys():
#     actions.user.ui_elements_show(keys)
#     actions.user.game_ui_register_live_keys()

# def hide_keys():
#     actions.user.game_ui_unregister_live_keys()
#     actions.user.ui_elements_hide(keys)