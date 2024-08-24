from talon import Module, actions

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
    print("hello event", event)
    if event.type == "change":
        if event.name == "pop":
            print(f"change pop {event.action_name}")
            actions.user.ui_elements_set_text("pop_value", event.action_name)
        elif event.name == "hiss":
            print(f"change hiss {event.action_name}")
            actions.user.ui_elements_set_text("hiss_value", event.action_name)
    elif event.type == "action":
        if event.name == "pop":
            print(f"action pop")
            actions.user.ui_elements_highlight_briefly("pop")
        elif event.name == "hiss":
            print(f"action hiss")
            actions.user.ui_elements_highlight("hiss")
    elif event.type == "action_stop" and event.name == "hiss":
        actions.user.ui_elements_unhighlight("hiss")

def on_ui_lifecycle(event):
    global is_dyanmic_actions_registered, is_listening_to_ui_elements_events

    if NOISE_UI_ID not in event.children_ids:
        return

    if event.type == "mount":
        if not is_dyanmic_actions_registered:
            is_dyanmic_actions_registered = True
            actions.user.dynamic_actions_event_register(on_event)
    elif event.type == "unmount":
        if is_dyanmic_actions_registered:
            is_dyanmic_actions_registered = False
            actions.user.dynamic_actions_event_unregister(on_event)
        if is_listening_to_ui_elements_events:
            is_listening_to_ui_elements_events = False
            actions.user.ui_elements_unregister_on_lifecycle(on_ui_lifecycle)

def events_init():
    global is_listening_to_ui_elements_events
    if not is_listening_to_ui_elements_events:
        is_listening_to_ui_elements_events = True
        actions.user.ui_elements_register_on_lifecycle(on_ui_lifecycle)

def dynamic_actions_ui_element():
    (div, text) = actions.user.ui_elements(["div", "text"])
    events_init()

    return div(id=NOISE_UI_ID)[
        text("noises", margin_bottom=16),
        div(flex_direction="column", gap=8)[
            div(id="pop", flex_direction="row", width=150, padding=8, border_width=1, border_color="FFFFFF33", border_radius=4)[
                text("pop"),
                text("", id="pop_value", color=accent_color)
            ],
            div(id="hiss", flex_direction="row", width=150, padding=8, border_width=1, border_color="FFFFFF33", border_radius=4)[
                text("hiss"),
                text("", id="hiss_value", color=accent_color)
            ]
        ]
    ]

def show_tester_ui():
    screen = actions.user.ui_elements_screen()

    ui = screen(id="dynamic_actions_tester", justify_content="center", align_items="flex_end")[
        dynamic_actions_ui_element(),
    ]
    ui.show()

def hide_tester_ui():
    actions.user.ui_elements_hide("dynamic_actions_tester")
