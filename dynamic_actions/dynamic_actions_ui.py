from talon import Module, actions
import time

accent_color = "87ceeb"

mod = Module()

is_listening_to_ui_elements_events = False
is_dyanmic_actions_registered = False

NOISE_UI_ID = "noises"

def update_pop(new_action_name):
    actions.user.ui_elements_set_text("pop", new_action_name)

def update_hiss(new_action_name):
    actions.user.ui_elements_set_text("hiss", new_action_name)

def on_event(event):
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

def on_ui_lifecycle(event):
    global is_dyanmic_actions_registered, is_listening_to_ui_elements_events

    if NOISE_UI_ID not in event.children_ids:
        return

    if event.type == "mount":
        actions.user.dynamic_actions_event_register(on_event)
    elif event.type == "unmount":
        actions.user.dynamic_actions_event_unregister(on_event)
        actions.user.ui_elements_unregister_on_lifecycle(on_ui_lifecycle)

def events_init():
    global is_listening_to_ui_elements_events, is_dyanmic_actions_registered
    actions.user.ui_elements_register_on_lifecycle(on_ui_lifecycle)

def dynamic_actions_ui_element():
    (div, text) = actions.user.ui_elements(["div", "text"])
    events_init()

    noise_css = {
        "flex_direction": "row",
        "width": 150,
        "padding": 8,
        "border_width": 1,
        "border_color": "FFFFFF33",
        "border_radius": 4
    }

    return div(id=NOISE_UI_ID, flex_direction="column", gap=8)[
        div(noise_css, id="pop")[
            text("pop"),
            text("", id="pop_value", color=accent_color)
        ],
        div(noise_css, id="hiss")[
            text("hiss"),
            text("", id="hiss_value", color=accent_color)
        ]
    ]

def show_tester_ui():
    (screen, div, text) = actions.user.ui_elements(["screen", "div", "text"])

    container_css = {
        "background_color": "222222",
        "opacity": 0.8,
        "margin_right": 32,
        "padding": 16,
        "flex_direction": "column",
        "border_width": 1,
        "border_color": "666666",
        "border_radius": 4,
    }

    ui = screen(id="dynamic_actions_tester", justify_content="center", align_items="flex_end")[
        div(container_css)[
            text("Dynamic actions", margin_bottom=16),
            dynamic_actions_ui_element(),
            text("Commands", color="87CEEB", font_weight="bold", margin_top=16),
            text("pop <phrase>"),
            text("hiss <phrase>"),
            div(flex_direction="row", margin_top=16)[
                text("dynamic actions"),
                text("exit", color="F33A6A")
            ]
        ]
    ]
    ui.show()

def hide_tester_ui():
    actions.user.ui_elements_hide("dynamic_actions_tester")
