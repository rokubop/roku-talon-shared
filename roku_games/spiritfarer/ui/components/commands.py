from talon import actions

accent_color = "87ceeb"

def commands():
    div, text, screen, state = actions.user.ui_elements(["div", "text", "screen", "state"])
    parrot_config = state.get("parrot_config")
    background_color = state.get("background_color", "000000")
    cmds, acts = actions.user.parrot_config_format_display(parrot_config)

    return screen()[
        div(position="absolute", right=32, top=100, background_color=f"{background_color}66", padding=16)[
            div(flex_direction="row", gap=16, z_index=2)[
                div(gap=8)[
                    text("sound", font_weight="bold", color="FFFFFF"),
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