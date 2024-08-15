from talon import actions

ui_commands = None
accent_color = "87ceeb"

def show_ui():
    global ui_commands
    (div, text, screen) = actions.user.ui_elements(["div", "text", "screen"])

    ui_commands = screen(align_items="flex_end", justify_content="flex_start")[
        div(background_color="00000066", margin=16, margin_right=32, padding=16)[
            div(flex_direction="row", gap=16)[
                div(gap=8)[
                    text("sound", font_weight="bold"),
                ],
                div(gap=8)[
                    text("actions", font_weight="bold", color=accent_color),
                ]
            ]
        ],
    ]
    ui_commands.show()

def hide_ui():
    global ui_commands
    ui_commands.hide()
