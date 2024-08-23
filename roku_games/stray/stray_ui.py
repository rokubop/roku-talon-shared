from talon import actions

accent_color = "87ceeb"

def show_ui(parrot_config):
    (commands, acts) = actions.user.parrot_config_format_display(parrot_config)
    (div, text, screen) = actions.user.ui_elements(["div", "text", "screen"])

    ui_commands = screen(align_items="flex_end", justify_content="flex_start")[
        div(background_color="00000066", margin=16, margin_right=32, padding=16)[
            div(flex_direction="row", gap=16)[
                div(gap=8)[
                    text("sound", font_weight="bold"),
                    *(text(command) for command in commands),
                ],
                div(gap=8)[
                    text("actions", font_weight="bold", color=accent_color),
                    *(text(action, color=accent_color) for action in acts),
                ]
            ]
        ],
    ]
    ui_commands.show()

def hide_ui():
    actions.user.ui_elements_hide_all()
