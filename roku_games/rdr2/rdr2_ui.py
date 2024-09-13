from talon import actions

accent_color = "87ceeb"
live_text_keys_state = ""
pressed_keys = []
clear_pressed_keys_job = None
KEY_SIZE = 25

def show_left_hud_ui():
    (div, screen, text) = actions.user.ui_elements(["div", "screen", "text"])

    css = {
        "background_color": "00000066",
        "border_radius": 16,
        "padding": 16,
        "border_width": 1,
        "border_color": "FF0000aa",
        "margin_bottom": 250,
        "margin_left": 250
    }

    ui_hud = screen(align_items="flex_start", justify_content="flex_end")[
        div(css)[
            div(flex_direction="row", gap=16)[
                actions.user.game_ui_element_xbox_dpad(),
                actions.user.game_ui_element_xbox_left_stick(),
                actions.user.game_ui_element_xbox_right_stick(),
            ]
        ]
    ]

    ui_hud.show()

def show_right_hud_ui():
    (div, screen, text) = actions.user.ui_elements(["div", "screen", "text"])

    css = {
        "background_color": "00000066",
        "border_radius": 16,
        "margin": 16,
        "padding": 16,
        "border_width": 1,
        "border_color": "FF0000aa",
        "margin_bottom": 250,
        "margin_right": 250
    }

    ui_hud = screen(align_items="flex_end", justify_content="flex_end")[
        div(css)[
            div(flex_direction="row", gap=16)[
                actions.user.game_ui_element_xbox_primary_buttons(size=30),
                div()[
                    text("triggers / bumpers", margin_bottom=16),
                    div(flex_direction="column", gap=8)[
                        div(flex_direction="row", gap=8)[
                            actions.user.game_ui_element_xbox_left_trigger(),
                            actions.user.game_ui_element_xbox_right_trigger(),
                        ],
                        div(flex_direction="row", gap=8)[
                            actions.user.game_ui_element_xbox_left_bumper(),
                            actions.user.game_ui_element_xbox_right_bumper(),
                        ],
                        div(justify_content="center", align_items="center", margin_top=4, margin_left=16)[
                            actions.user.game_ui_element_xbox_center_buttons()
                        ]
                    ],
                ],
                div()[
                    text("noises", margin_bottom=16),
                    actions.user.dynamic_noises_ui_element()
                ],
            ],
        ]
    ]

    ui_hud.show()

def noise_modes_list():
    return actions.user.dynamic_noises().keys()

def show_commands_ui():
    global ui_commands
    (div, text, screen) = actions.user.ui_elements(["div", "text", "screen"])

    ui_commands = screen(align_items="flex_end", justify_content="flex_start")[
        div(background_color="00000066", margin=16, margin_right=32, margin_top=32, padding=16)[
            div(flex_direction="row", gap=16)[
                div(gap=8)[
                    text("camera", font_weight="bold", color=accent_color),
                    text("<dir>"),
                    text("cam <dir>"),
                    text("cam <dir> <dir>"),
                    text("cam mid"),
                    text("look <dir>"),
                    text("cam 1-5"),
                    text("round"),
                    text("movement", font_weight="bold", color=accent_color, margin_top=16),
                    text("go"),
                    text("go <dir>"),
                    text("go <dir> <dir>"),
                    text("go 1-5"),
                    text("back"),
                    text("hiss noise"),
                    text("Noise modes", font_weight="bold", color=accent_color, margin_top=16),
                    *(text(mode) for mode in noise_modes_list()),
                    text("pop <phrase>"),
                    text("hiss <phrase>"),
                ],
                div(gap=8)[
                    text("commands", font_weight="bold", color=accent_color),
                    text("<button>"),
                    text("<button> ee/er"),
                    text("pad <dir>"),
                    text("hold <button>"),
                    text("free <button>"),
                    text("long <button>"),
                    text("weapon | gun"),
                    text("run"),
                    text("jump | greet"),
                    text("halt | stop"),
                    text("shoot"),
                    text("sell | satchel"),
                    text("reload"),
                    text("scope"),
                    text("kill"),
                    text("aim | target | talk"),
                    text("hide"),
                    text("call"),
                    text("wheel"),
                    text("crouch"),
                    text("look back"),
                    text("dead eye"),
                    text("Game", font_weight="bold", color=accent_color, margin_top=16),
                    text("game exit")
                ]
            ]
        ]
    ]

    ui_commands.show()

def show_ui():
    show_commands_ui()
    show_right_hud_ui()
    show_left_hud_ui()

def hide_ui():
    actions.user.ui_elements_hide_all()