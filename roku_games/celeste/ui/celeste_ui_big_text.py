from talon import actions, cron

ui_big_text = None
accent_color = "87ceeb"

live_keys_timeout = None

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

def show_big_text_ui():
    global ui_big_text
    (screen, div, text) = actions.user.ui_elements(["screen", "div", "text"])

    key = actions.user.game_ui_element_key
    opts = { "opacity": 0.5 }

    ui_big_text = screen()[
        div(padding=40, margin_top=130, margin_left=50)[
            text("", id="noise", font_size=140, font_weight="bold", color="FFFFFF"),
            text("", id="command", font_size=60, margin_top=32, color="FFFFFF"),
        ]
    ]
    ui_lower = screen(justify_content="flex_end", highlight_color="FFFFFF55")[
        div(flex_direction="row", margin_bottom=20, margin_left=20, opacity=0.5)[
            actions.user.game_ui_element_arrows(60, opts),
            div()[
                div(flex_direction="row")[
                    key("c", "jump", 60, opts),
                    key("p", "jump 2", 60, opts),
                    key("foot_left", "foot1: grab", 60, opts),
                ],
                div(flex_direction="row")[
                    key("x", "dash", 60, opts),
                    key("t", "demo", 60, opts),
                    key("foot_center", "foot2: move", 60, opts)
                ]
            ],
        ],
    ]

    ui_big_text.show()
    ui_lower.show()
    actions.user.parrot_config_event_register(on_noise)

def hide_big_text_ui():
    actions.user.ui_elements_hide_all()
    actions.user.parrot_config_event_unregister(on_noise)

def refresh_big_text_ui():
    hide_big_text_ui()
    show_big_text_ui()