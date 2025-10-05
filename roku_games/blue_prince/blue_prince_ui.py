from talon import actions

accent_color = "87ceeb"

def ui(props):
    div, text, screen = actions.user.ui_elements(["div", "text", "screen"])
    commands, acts = actions.user.parrot_config_format_display(props["parrot_config"])

    return screen(align_items="flex_end", justify_content="flex_start")[
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