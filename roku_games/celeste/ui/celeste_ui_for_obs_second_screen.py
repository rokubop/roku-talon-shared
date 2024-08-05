from talon import actions, cron

ui_keys = None
ui_live_text = None
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
        actions.user.ui_elements_set_text("noise", noise[:3])
        actions.user.ui_elements_set_text("command", command_name)
        if live_keys_timeout:
            cron.cancel(live_keys_timeout)
        live_keys_timeout = cron.after("2s", reset_live_keys)

def show_live_text_ui():
    global ui_live_text
    (screen, div, text) = actions.user.ui_elements(["screen", "div", "text"])
    ui_live_text = screen(1, align_items="flex_end", justify_content="flex_start")[
        div(justify_content="center", align_items="center", padding=16, margin_right=400, margin_top=100)[
            text("", id="noise", font_size=180, font_weight="bold", color="FFFFFF"),
            text("", id="command", font_size=50, margin_top=35, color="FFFFFF")
        ]
    ]
    ui_live_text.show()
    actions.user.parrot_config_event_register(on_noise)

def hide_live_text_ui():
    global ui_live_text
    if ui_live_text:
        ui_live_text.hide()
        actions.user.parrot_config_event_unregister(on_noise)

def refresh_live_text_ui():
    hide_live_text_ui()
    show_live_text_ui()

def on_key(key, state):
    if ui_keys and key in ["foot_left", "foot_center", "up", "down", "left", "right"]:
        if state == "press":
            ui_keys.highlight_briefly(key)
        elif state == "hold":
            ui_keys.highlight(key)
        elif state == "release":
            ui_keys.unhighlight(key)

def show_keys():
    global ui_keys
    (css, div, text, screen) = actions.user.ui_elements(["css", "div", "text", "screen"])

    screen_css = css(
        id="keys",
        justify_content="flex_start",
        align_items="flex_end",
        highlight_color=f"{accent_color}88"
    )

    gamepad_css = css(
        flex_direction="col",
        gap=8,
        margin_top=380,
        margin_right=200
    )

    key_css = css(
        padding=10,
        background_color="333333dd",
        flex_direction="row",
        justify_content="center",
        align_items="center",
        margin=2,
        width=60,
        height=60
    )

    def key(key_name, text_content, width=60):
        return div(key_css, id=key_name, width=width)[
            text(text_content, font_size=20, font_weight="bold")
        ]

    def blank_key():
        return div(key_css, background_color="33333355")[text(" ")]

    def col(**kwargs):
        return div(flex_direction="column", **kwargs)

    def row():
        return div(flex_direction="row")

    ui_keys = screen(1, screen_css)[
        div(gamepad_css)[
            col()[
                row()[blank_key(), key("up", "↑"), blank_key()],
                row()[key("left", "←"), key("down", "↓"), key("right", "→")],
                key("foot_left", "foot1: grab (z)", 190),
                key("foot_center", "foot2: move mode", 190)
            ],
        ]
    ]

    ui_keys.show()
    actions.user.game_event_register_on_key(on_key)

def hide_keys():
    actions.user.game_event_unregister_on_key(on_key)
    ui_keys.hide()

def show_obs_ui():
    show_keys()
    show_live_text_ui()

def hide_obs_ui():
    hide_keys()
    hide_live_text_ui()