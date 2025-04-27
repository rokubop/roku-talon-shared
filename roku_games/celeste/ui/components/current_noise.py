from talon import actions, cron

live_keys_timeout = None

def reset_live_keys():
    global live_keys_timeout
    actions.user.ui_elements_set_text("noise", "")
    actions.user.ui_elements_set_text("command", "")
    live_keys_timeout = None

def on_noise(noise, command_name):
    global live_keys_timeout

    if command_name:
        actions.user.ui_elements_set_text("noise", noise)
        actions.user.ui_elements_set_text("command", command_name)
        if live_keys_timeout:
            cron.cancel(live_keys_timeout)
        live_keys_timeout = cron.after("2s", reset_live_keys)

def current_noise():
    active_window, div, text = actions.user.ui_elements(["active_window", "div", "text"])

    return active_window()[
        div(padding=40, margin_top=120, margin_left=25)[
            text("", id="noise", font_size=100, font_weight="bold", color="FFFFFF"),
            text("", id="command", font_size=50, margin_top=30, color="FFFFFF"),
        ]
    ]

    # return active_window()[
    #     # div(padding=40, margin_top=120, margin_left=25)[
    #     div(padding=40, margin_top=120, margin_left=40)[
    #         text("", id="noise", font_size=80, color="FFFFFF", font_family="renogare"),
    #         text("", id="command", font_size=35, margin_top=16, color="FFFFFF", font_family="renogare"),
    #     ]
    # ]

def show_current_noise():
    actions.user.ui_elements_show(current_noise)
    actions.user.parrot_config_event_register(on_noise)

def hide_current_noise():
    actions.user.parrot_config_event_unregister(on_noise)
    actions.user.ui_elements_hide_all()