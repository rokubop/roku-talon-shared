from talon import actions

commands = None
keys = None
accent_color = "87ceeb"

def show_commands(parrot_config):
    global commands

    (screen, div, text) = actions.user.ui_elements(["screen", "div", "text"])
    (cmds, acts) = actions.user.parrot_config_format_display(parrot_config)

    commands = screen(align_items="flex_start", justify_content="flex_start")[
        div(margin_top=48, flex_direction="row", padding=16, gap=16)[
            div(gap=8)[
                text("sound", font_weight="bold"),
                *(text(cmd) for cmd in cmds)
            ],
            div(gap=8)[
                text("action", font_weight="bold", color=accent_color),
                *(text(act, color=accent_color) for act in acts)
            ]
        ]
    ]

    commands.show()

def hide_commands():
    global commands
    commands.hide()

def on_key(key, state):
    if keys:
        if state == "press":
            keys.highlight_briefly(key)
        elif state == "hold":
            keys.highlight(key)
        elif state == "release":
            keys.unhighlight(key)

def show_keys():
    global keys
    (screen, div, text) = actions.user.ui_elements(["screen", "div", "text"])

    key_css = {
        "padding": 8,
        "background_color": "333333dd",
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
        "margin": 1,
        "width": 30,
        "height": 30,
    }

    def key(id, key_name=None, width=30):
        return div(key_css, id=id.lower(), width=width)[text(key_name or id)]

    def blank_key():
        return div(key_css, background_color="33333355")[text(" ")]

    keys = screen(justify_content="flex_start", align_items="flex_start", highlight_color=f"{accent_color}88")[
        div(flex_direction="row", gap=0, margin_top=325, margin_left=16)[
            div(flex_direction="column")[
                div(flex_direction="row")[
                    blank_key(),
                    key("up", "W"),
                    blank_key()
                ],
                div(flex_direction="row")[
                    key("left", "A"),
                    key("down", "S"),
                    key("right", "D")
                ]
            ],
            div(flex_direction="column")[
                div(flex_direction="row")[
                    key("shift", "SH", 60),
                    key("E")
                ],
                div(flex_direction="row")[
                    key("ctrl", "CT", 45),
                    key("space", "SP", 45)
                ]
            ],
        ]
    ]

    keys.show()
    actions.user.game_event_register_on_key(on_key)

def hide_keys():
    actions.user.game_event_unregister_on_key(on_key)
    keys.hide()

def show_ui(parrot_config):
    show_commands(parrot_config)
    show_keys()

def hide_ui():
    hide_commands()
    hide_keys()