from talon import actions

accent_color = "87ceeb"

def commands():
    div, text, screen, state = actions.user.ui_elements(["div", "text", "screen", "state"])
    parrot_config = state.get("parrot_config")
    background_color = state.get("background_color", "000000")
    cmds, acts = actions.user.parrot_config_format_display(parrot_config)

    return screen(align_items="flex_end", justify_content="flex_start")[
        div(background_color=f"{background_color}66", margin=16, margin_right=32, padding=16)[
            div(flex_direction="row", gap=16)[
                div(gap=8)[
                    text("sound", font_weight="bold"),
                    *(text(command) for command in cmds),
                ],
                div(gap=8)[
                    text("actions", font_weight="bold", color=accent_color),
                    *(text(action, color=accent_color) for action in acts),
                ]
            ],
        ],
    ]

def show_commands():
    actions.user.ui_elements_show(commands)

def hide_commands():
    actions.user.ui_elements_hide(commands)