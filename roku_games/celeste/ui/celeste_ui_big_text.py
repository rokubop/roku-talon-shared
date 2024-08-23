from talon import actions, cron

ui_big_text = None
accent_color = "87ceeb"

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

def show_big_text_ui():
    global ui_big_text
    (screen, div, text) = actions.user.ui_elements(["screen", "div", "text"])
    ui_big_text = screen(align_items="center", justify_content="flex_start")[
        div(width=1920, background_color="00000066", justify_content="center", align_items="center")[
            div(justify_content="center", align_items="center", padding=40, margin_right=200)[
                text("", id="noise", font_size=100, font_weight="bold", color="FFFFFF"),
                text("", id="command", font_size=30, margin_top=32, color="FFFFFF")
            ]
        ]
    ]
    ui_big_text.show()
    actions.user.parrot_config_event_register(on_noise)

def hide_big_text_ui():
    global ui_big_text
    if ui_big_text:
        ui_big_text.hide()
        actions.user.parrot_config_event_unregister(on_noise)

def refresh_big_text_ui():
    hide_big_text_ui()
    show_big_text_ui()