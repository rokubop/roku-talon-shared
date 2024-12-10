from talon import Module, actions

mod = Module()

accent_color = "87ceeb"
NOISE_UI_ID = "noises"

def update_pop(new_action_name):
    actions.user.ui_elements_set_text("pop", new_action_name)

def update_hiss(new_action_name):
    actions.user.ui_elements_set_text("hiss", new_action_name)

def on_noise_event(event):
    if event.type == "change":
        actions.user.ui_elements_set_text(f"{event.name}_value", event.action_name)
    elif event.type == "action":
        if event.name == "pop":
            color = "F33A6A99" if event.error else None
            actions.user.ui_elements_highlight_briefly("pop", color)
        elif event.name == "hiss":
            color = "F33A6A99" if event.error else None
            actions.user.ui_elements_highlight("hiss", color)
    elif event.type == "action_stop" and event.name == "hiss":
        actions.user.ui_elements_unhighlight("hiss")

noise_style = {
    "flex_direction": "row",
    "width": 150,
    "padding": 8,
    "border_width": 1,
    "border_color": "FFFFFF33",
    "border_radius": 4
}

def on_mount():
    actions.user.dynamic_noises_event_register(on_noise_event)

def on_unmount():
    actions.user.dynamic_noises_event_unregister(on_noise_event)


def dynamic_noises_ui():
    div, text, effect = actions.user.ui_elements(["div", "text", "effect"])

    effect(on_mount, on_unmount, [])

    return div(id=NOISE_UI_ID, flex_direction="column", gap=8)[
        div(noise_style, id="pop", gap=16)[
            text("pop"),
            text("", id="pop_value", color=accent_color)
        ],
        div(noise_style, id="hiss", gap=16)[
            text("hiss"),
            text("", id="hiss_value", color=accent_color)
        ]
    ]

screen_align_style = {
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

container_style = {
    "background_color": "222222",
    "opacity": 0.8,
    "margin_right": 32,
    "padding": 16,
    "flex_direction": "column",
    "border_width": 1,
    "border_color": "666666",
    "border_radius": 4,
}

def dynamic_noise_tester_ui():
    screen, div, text, state = actions.user.ui_elements(["screen", "div", "text", "state"])

    position = state.get("position", "right")

    return screen(screen_align_style[position])[
        div(container_style, gap=16)[
            text("Dynamic noises", margin_bottom=16),
            dynamic_noises_ui(),
            text("Commands", font_weight="bold"),
            text("<noise> <phrase>", color=accent_color),
            div(flex_direction="ropw")[
                text("<noise>", color=accent_color), text(" clear")
            ],
             div(flex_direction="row")[
                text("<noise>", color=accent_color), text(" revert")
            ],
            text("dynamic clear"),
            text("view (hide | show)", margin_top=16),
            text("view (left | right)"),
            div(flex_direction="row", margin_top=16)[
                text("dynamic (stop | quit)")
            ]
        ]
    ]

def show_tester_ui():
    actions.user.ui_elements_show(dynamic_noise_tester_ui)

def hide_tester_ui():
    actions.user.ui_elements_hide(dynamic_noise_tester_ui)
