from talon import actions, cron

accent_color = "87ceeb"
live_text_keys_state = ""
pressed_keys = []
clear_pressed_keys_job = None
KEY_SIZE = 25

def noises_ui():
    (div, text) = actions.user.ui_elements(["div", "text"])

    return div(flex_direction="column", gap=8)[
        div(id="pop", flex_direction="row", width=150, padding=8, border_width=1, border_color="FFFFFF33", border_radius=4)[
            text("pop"),
            text("", id="pop_value", color=accent_color)
        ],
        div(id="hiss", flex_direction="row", width=150, padding=8, border_width=1, border_color="FFFFFF33", border_radius=4)[
            text("hiss"),
            text("", id="hiss_value", color=accent_color)
        ]
    ]

def cam_mode_ui():
    (div, text) = actions.user.ui_elements(["div", "text"])

    return div(flex_direction="row", gap=16, height=20, align_items="center", justify_content="center", margin_bottom=12)[
        text("<dir> mode:"),
        text("cam", font_weight="bold", margin_bottom=3),
    ]

def live_text_keys_ui():
    (div, text) = actions.user.ui_elements(["div", "text"])

    return div()[
        text("", id="live_text_keys", font_size=20, font_weight="bold")
    ]

def line_separator_ui():
    (div) = actions.user.ui_elements(["div", "text"])
    return div(background_color="FFFFFF66", width=120, height=2)

def show_hud_ui():
    (div, screen, text) = actions.user.ui_elements(["div", "screen", "text"])

    ui_hud = screen(align_items="center", justify_content="flex_end")[
        div(background_color="00000066", border_radius=16, margin=16, margin_bottom=300, padding=16, border_width=1, border_color="FF0000aa")[
            div(flex_direction="row", gap=16)[
                actions.user.game_ui_element_xbox_dpad("pad"),
                actions.user.game_ui_element_xbox_left_stick("go"),
                actions.user.game_ui_element_xbox_right_stick("cam"),
                actions.user.game_ui_element_xbox_primary_buttons("buttons"),
                div()[
                    text("triggers / bumpers", margin_bottom=16),
                    div(flex_direction="column", gap=8)[
                        div(flex_direction="row", gap=8)[
                            actions.user.game_ui_element_xbox_left_trigger("LT"),
                            actions.user.game_ui_element_xbox_right_trigger("RT"),
                        ],
                        div(flex_direction="row", gap=8)[
                            actions.user.game_ui_element_xbox_left_bumper("LB"),
                            actions.user.game_ui_element_xbox_right_bumper("RB"),
                        ]
                    ]
                ],
                div()[
                    text("noises", margin_bottom=16),
                    noises_ui()
                ],
            ],
            live_text_keys_ui()
        ],
    ]

    ui_hud.show()

commands = [
    "<key>",
    "hold <key>",
    "free <key>",
    "long <key>",
    "go",
    "go <dir>",
    "<dir>",
    "back",
    "cam <dir>",
    "cam mid",
    "look <dir>",
    "round",
    "gear <num>",
    "click",
    "trick",
    "run",
    "halt",
    "stop",
    "game exit"
]

def show_commands_ui():
    global ui_commands
    (div, text, screen) = actions.user.ui_elements(["div", "text", "screen"])

    ui_commands = screen(align_items="flex_end", justify_content="center")[
        div(background_color="00000066", margin=16, margin_right=32, padding=16)[
            div(flex_direction="row", gap=16)[
                div(gap=8)[
                    text("commands", font_weight="bold"),
                    *(text(command) for command in commands),
                ],
            ]
        ],
    ]

    ui_commands.show()

def update_pop(new_action_name):
    actions.user.ui_elements_set_text("pop", new_action_name)

def update_hiss(new_action_name):
    actions.user.ui_elements_set_text("hiss", new_action_name)

def on_event(event):
    if event.type == "change":
        if event.name == "pop":
            actions.user.ui_elements_set_text("pop_value", event.action_name)
        elif event.name == "hiss" or event.name == "wish":
            actions.user.ui_elements_set_text("hiss_value", event.action_name)
    elif event.type == "action":
        if event.name == "pop":
            actions.user.ui_elements_highlight_briefly("pop")
        elif event.name == "hiss" or event.name == "wish":
            actions.user.ui_elements_highlight("hiss")
    elif event.type == "action_stop" and event.name == "hiss":
        actions.user.ui_elements_unhighlight("hiss")

# def on_xbox_event(event):
#     print(f"on_xbox_event: {event}")
#     if event.subject == "right_stick" or event.subject == "left_stick":
#         on_stick(event)
#     elif event.subject == "left_trigger" or event.subject == "right_trigger":
#         on_trigger(event)
#     else:
#         if event.type == "hold":
#             actions.user.ui_elements_highlight(f"gamepad_{event.subject}")
#         elif event.type == "release":
#             actions.user.ui_elements_unhighlight(f"gamepad_{event.subject}")

def show_ui():
    show_hud_ui()
    show_commands_ui()
    # actions.user.game_event_register_on_xbox_event(on_xbox_event)
    actions.user.dynamic_actions_event_register(on_event)

def hide_ui():
    actions.user.ui_elements_hide_all()
    # actions.user.game_event_unregister_all()
    actions.user.dynamic_actions_event_unregister_all()
