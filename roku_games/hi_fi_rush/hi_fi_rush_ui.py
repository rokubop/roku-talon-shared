from talon import actions

accent_color = "87ceeb"

def ui():
    div, screen, text, state = actions.user.ui_elements(['div', 'screen', 'text', 'state'])
    parrot_config = state.get("parrot_config")
    background_color = state.get("background_color")
    cmds, acts = actions.user.parrot_config_format_display(parrot_config)

    return screen(flex_direction="row", align_items="center", justify_content="flex_end")[
        div(flex_direction="row", background_color=background_color, padding=16, gap=16)[
            div(gap=8)[
                text("sound", font_weight="bold"),
                *(text(command) for command in cmds)
            ],
            div(gap=8)[
                text("action", font_weight="bold"),
                *(text(action, color=accent_color) for action in acts)
            ]
        ]
    ]