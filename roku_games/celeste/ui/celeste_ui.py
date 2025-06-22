from talon import actions
from .colors import BG_PRIMARY
from .components.keys import keys
from .components.current_noise import current_noise
from .components.commands import show_commands, hide_commands
from .components.history_log import show_history_log, hide_history_log
from .components.apm import apm

def layout():
    screen, active_window, div, state, style = actions.user.ui_elements(
        ["screen", "active_window", "div", "state", "style"]
    )

    screen_index = state.get("screen_index", 1)

    style({
        "text": {
            "stroke_color": "000000",
            "stroke_width": 4
        }
    })

    # For OBS second screen
    return screen(screen_index)[
        div(margin_top=100, margin_left=50)[
            div(gap=2)[
                keys(),
                div(flex_direction="row", gap=1, flex=1, justify_content="space_between")[
                    current_noise(
                        flex=1,
                        padding=8,
                        background_color=f"{BG_PRIMARY}67",
                    ),
                    apm(
                        padding=8,
                        background_color=f"{BG_PRIMARY}67",
                    ),
                ],
            ]
        ],
    ]

    # For directly on the game screen
    # return active_window()[
    #     keys(position="absolute", top=50, right=300),
    #     current_noise(position="absolute", top=120, left=25),
    # ]

def show_ui():
    actions.user.ui_elements_show(layout)
    # show_commands()
    # show_keys()
    # show_current_noise()
    # show_history_log()

def hide_ui():
    actions.user.ui_elements_hide_all()
    # hide_commands()
    # hide_keys()
    # hide_current_noise()
    # hide_history_log()

def refresh_ui():
    hide_ui()
    show_ui()