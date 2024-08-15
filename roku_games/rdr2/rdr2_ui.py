from talon import actions

accent_color = "87ceeb"

def show_hud():
    global ui_hud
    (div, text, screen) = actions.user.ui_elements(["div", "text", "screen"])

    ui_hud = screen(align_items="center", justify_content="flex_end")[
        div(background_color="00000066", border_radius=16, margin=16, margin_bottom=300, padding=16)[
            div(flex_direction="row", gap=16, height=20, align_items="center", justify_content="center", margin_bottom=12)[
                text("<dir> mode:"),
                text("cam", font_weight="bold", margin_bottom=3),
            ],
            div(background_color="FFFFFF66", width=400, height=2),
            div(flex_direction="row", gap=16, margin_top=12)[
                div(gap=8, width=200)[
                    text("pop"),
                    text("", id="pop_1", font_size=20, font_weight="bold")
                ],
                div(gap=8, width=200)[
                    text("hiss (wish)"),
                    text("", id="hiss_1", font_size=20, font_weight="bold")
                ]
            ]
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

def show_commands():
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
    actions.user.ui_elements_set_text("pop_1", new_action_name)

def update_hiss(new_action_name):
    actions.user.ui_elements_set_text("hiss_1", new_action_name)

def show_ui():
    show_hud()
    show_commands()

def hide_ui():
    actions.user.ui_elements_hide_all()
