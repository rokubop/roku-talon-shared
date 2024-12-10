from talon import actions

container_css = {
    "background_color": "222222",
    "padding": 16,
    "flex_direction": "column",
    "justify_content": "center",
    "align_items": "center",
    "border_width": 1,
    "border_color": "666666",
    "border_radius": 4,
}

screen_align_css = {
    "left": {
        "flex_direction": "row",
        "justify_content": "flex_start",
        "padding_left": 32,
        "align_items": "center",
    },
    "right": {
        "flex_direction": "row",
        "justify_content": "flex_end",
        "padding_right": 32,
        "align_items": "center",
    },
    "up": {
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "flex_start",
    },
    "down": {
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "flex_end",
    },
}

def drag_mode_menu_ui():
    screen, div, text, state = actions.user.ui_elements(["screen", "div", "text", "state"])

    position = state.get("position", "right")

    return screen(screen_align_css[position])[
        div(container_css)[
            div(flex_direction="column", gap=12)[
                text("Mode:", color="87CEEB", font_weight="bold"),
                text("drag mode - LMB"),
                text("roll mode - RMB"),
                text("pan mode - MMB"),
                text("Dir verbs", color="87CEEB", font_weight="bold", margin_top=12),
                text("<dir>, go <dir>"),
                text("fly <dir>"),
                text("swipe, tick"),
                text("<T> verbs", color="87CEEB", font_weight="bold", margin_top=12),
                text("<T>, to <T>"),
                text("bring, bring this to"),
                text("go, hover, fly, fly to"),
                text("center, swipe, past"),
                text("drag, pan, roll"),
                text("Noises:", color="87CEEB", font_weight="bold", margin_top=12),
                text("hiss: stop"),
                text("Layout:", color="87CEEB", font_weight="bold", margin_top=12),
                text("more squares"),
                text("less squares"),
                text("clear <T> past <T>"),
                text("clear line <T>"),
                text("take <T> past <T>"),
                text("grid reset"),
                text("commands <dir>"),
                text("commands hide"),
                text("grid hide", color="F33A6A", font_weight="bold", margin_top=12),
            ]
        ]
    ]