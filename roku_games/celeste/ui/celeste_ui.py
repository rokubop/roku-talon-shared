from talon import actions
from .colors import BG_PRIMARY
from .components.keys import keys, keys_2
from .components.current_noise import current_noise
from .components.apm import apm

COMPACT_LAYOUT = False
OVERLAY_DIRECTLY_ON_GAME_SCREEN = False

def vertical_layout():
    div = actions.user.ui_elements(["div"])

    bg_color = f"{BG_PRIMARY}88"

    return div(gap=2)[
        keys(background_color=bg_color),
        div(flex_direction="row", gap=1, flex=1, justify_content="space_between")[
            current_noise(
                flex=1,
                padding=8,
                background_color=bg_color,
            ),
            apm(
                padding=8,
                background_color=bg_color,
            ),
        ]
    ]

def horizontal_layout():
    div = actions.user.ui_elements(["div"])
    scale = 1.5

    return div(gap=2, flex_direction="row")[
        div(flex_direction="row", align_items="center", gap=1, width=int(400 * scale), justify_content="space_between")[
            current_noise(
                flex=1,
                padding=8,
                background_color=f"{BG_PRIMARY}67",
                scale=scale,
            ),
            apm(
                padding=8,
                background_color=f"{BG_PRIMARY}67",
                scale=scale,
            )
        ],
        keys(),
    ]

def horizontal_layout_2():
    div = actions.user.ui_elements(["div"])

    return div(flex_direction="row", gap=30)[
        div(flex_direction="column", width=210, justify_content="space_between")[
            current_noise(
                flex=1,
                padding=8,
                background_color=f"{BG_PRIMARY}67",
                scale=1.2,
            ),
            apm(
                padding=8,
                background_color=f"{BG_PRIMARY}67",
                scale=0.5,
            )
        ],
        keys(),
    ]

def horizontal_layout_3():
    div = actions.user.ui_elements(["div"])

    return div(flex_direction="row", gap=30)[
        keys_2(),
        div(flex_direction="row", width=600, justify_content="space_between", align_items="center")[
            current_noise(
                flex=1,
                padding=8,
                scale=1.2,
            ),
            apm(
                padding=8,
                scale=1.2,
            )
        ],
    ]


def custom_layout():
    div = actions.user.ui_elements(["div"])

    return div(gap=2, flex_direction="row")[
        div(flex_direction="column",  gap=1, width=400, justify_content="space_between")[
            div(width=170, height=100, justify_content="center")[
                current_noise(
                    flex=1,
                    padding=8,
                    background_color=f"{BG_PRIMARY}67",
                    scale=1,
                ),
            ],
            div(flex_direction="row", align_items="center", gap=60)[
                keys(),
                apm(
                    padding=8,
                    background_color=f"{BG_PRIMARY}67",
                    scale=1,
                )
            ],
        ],

    ]

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

    if not COMPACT_LAYOUT:
        return screen(screen_index)[
            div(margin_top=100, margin_left=50)[
                horizontal_layout_3()
            ],
        ]

    if OVERLAY_DIRECTLY_ON_GAME_SCREEN:
        return active_window()[
            keys(position="absolute", top=50, right=300),
            current_noise(position="absolute", top=120, left=25),
        ]

    return screen(1)[
        div(margin_top=100, margin_left=50)[
            vertical_layout()
        ],
    ]


def show_ui():
    actions.user.ui_elements_show(layout)

def hide_ui():
    actions.user.ui_elements_hide_all()

def refresh_ui():
    hide_ui()
    show_ui()