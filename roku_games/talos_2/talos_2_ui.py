from talon import actions

accent_color = "87ceeb"

def show_ui(parrot_config, background_color="22266688"):
    (div, screen, text) = actions.user.ui_elements(['div', 'screen', 'text'])
    (cmds, acts) = actions.user.parrot_config_format_display(parrot_config)

    commands = screen(align_items="flex_end", justify_content="center")[
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

    commands.show()

def hide_ui():
    actions.user.ui_elements_hide_all()

def refresh_ui(parrot_config):
    hide_ui()
    show_ui(parrot_config)