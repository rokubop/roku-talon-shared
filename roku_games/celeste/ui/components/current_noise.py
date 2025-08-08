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

def on_mount():
    actions.user.parrot_config_event_register(on_noise)

def on_unmount():
    actions.user.parrot_config_event_unregister(on_noise)

def current_noise(scale=1, **props):
    div, text, effect = actions.user.ui_elements(["div", "text", "effect"])

    effect(on_mount, on_unmount, [])

    return div(gap=int(10 * scale), padding_left=12, **props, justify_content="center")[
        # text("Noise - command", font_size=12),
        text("", id="noise", font_size=int(40 * scale), font_family="renogare"),
        text("", id="command", font_size=int(24 * scale), font_family="roboto"),
    ]

    # return div(padding=40, **props)[
    #     text("", id="noise", font_size=100, font_weight="bold", color="FFFFFF"),
    #     text("", id="command", font_size=50, margin_top=30, color="FFFFFF"),
    # ]

    # return active_window()[
    #     # div(padding=40, margin_top=120, margin_left=25)[
    #     div(padding=40, margin_top=120, margin_left=40)[
    #         text("", id="noise", font_size=80, color="FFFFFF", font_family="renogare"),
    #         text("", id="command", font_size=35, margin_top=16, color="FFFFFF", font_family="renogare"),
    #     ]
    # ]

# def show_current_noise():
#     actions.user.ui_elements_show(current_noise)
#     actions.user.parrot_config_event_register(on_noise)

# def hide_current_noise():
#     actions.user.parrot_config_event_unregister(on_noise)
#     actions.user.ui_elements_hide_all()