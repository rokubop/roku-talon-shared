from talon import actions

def get_labels(game_state, noise):
    return game_state.get(noise, {}).get('labels', [])

def is_active(game_state, noise, index):
    return game_state.get(noise, {}).get('value', None) == index

def actions_table():
    div, text, state, table, tr, td, style = actions.user.ui_elements(['div', 'text', 'state', 'table', 'tr', 'td', 'style'])
    game_state = state.get('game_state', {})

    return div()[
        text("Actions"),
        table()[
            *[
                tr()[
                    td()[text(noise, id=noise)],
                    *[td()[text(
                        label,
                        class_name="active" if is_active(game_state, noise, index) else ""
                    )] for index, label in enumerate(get_labels(game_state, noise))],
                ]
                for noise in ["nn", "pop", "palate", "t", "er"]
            ]
        ]
    ]

def movement_table():
    div, text, state, table, tr, td, style = actions.user.ui_elements(['div', 'text', 'state', 'table', 'tr', 'td', 'style'])
    game_state = state.get('game_state', {})

    return div()[
        text("Movement"),
        table()[
            *[
                tr()[
                    td()[text(noise, id=noise)],
                    *[td()[text(
                        label,
                        class_name="active" if is_active(game_state, noise, index) else ""
                    )] for index, label in enumerate(get_labels(game_state, noise))],
                ]
                for noise in ["ah", "oh", "ee", "guh", "eh", "hiss", "shush"]
            ]
        ]
    ]

def special_table():
    div, text, state, table, tr, td, style = actions.user.ui_elements(['div', 'text', 'state', 'table', 'tr', 'td', 'style'])
    game_state = state.get('game_state', {})

    return div()[
        text("Special"),
        table()[
            *[
                tr()[
                    td()[text(noise, id=noise)],
                    *[td()[text(
                        label,
                        class_name="active" if is_active(game_state, noise, index) else ""
                    )] for index, label in enumerate(get_labels(game_state, noise))],
                ]
                for noise in ["cluck <any>", "cluck", "tut", "tut <any>", "tut tut"]
            ]
        ]
    ]

def talos_2_ui():
    div, screen, text, state, style = actions.user.ui_elements(['div', 'screen', 'text', 'state', 'style'])

    style({
        "text": {
            "font_family": "roboto",
            "padding": 6,
            "border_radius": 4,
        },
        "td": {
            "padding": 2
        },
        ".active": {
            "background_color": "#0d7cbd66",
        },
    })

    return screen(align_items="flex_end", justify_content="center")[
        div(background_color="11111177", padding=16, gap=16)[
            actions_table(),
            movement_table(),
            special_table(),
        ]
    ]