from talon import actions
import time

def row(item, color):
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="row", gap=16)[
        text(f"{item['time_display']}", width=50),
        div(flex_direction="row", gap=8, width=100)[
            text(item["noise"]),
        ],
        text(item["power_display"]),
    ]

def log():
    div, text, state = actions.user.ui_elements(["div", "text", "state"])

    log = state.get("log")
    noises = state.get("noises")

    return div(id="log", flex_direction="column", height=500, overflow_y="scroll", border_width=1, background_color="161616")[
        *[row(item, noises[item["noise"]]["color"]) for item in log],
    ]

def log_to_vertical_lines(log, noises):
    max_power = 40
    duration = 10.0
    lines = []
    for item in log:
        if item["power"]:
            lines.append({
                "time_fraction": (item["time"] % duration) / duration,
                "power_fraction": (min(item["power"] / max_power, max_power) * 0.8) + 0.2,
                "color": noises[item["noise"]]["color"],
            })
    return lines

def filter_last_x_seconds(log, seconds):
    now = time.perf_counter() - start_time
    filtered_log = []
    for item in log:
        if item["time"] >= now - seconds:
            filtered_log.append(item)
    return filtered_log

def graph(props):
    div, screen, state = actions.user.ui_elements(["div", "screen", "state"])
    rect = props["rect"]
    time_fraction = state.get("time_fraction", 0)
    log = state.get("log")
    filtered_log = filter_last_x_seconds(log, 10)
    noises = state.get("noises")
    lines = log_to_vertical_lines(filtered_log, noises)

    return screen()[
        div(position="absolute", left=rect.x, top=rect.y, width=rect.width, height=rect.height)[
            div(position="absolute", z_index=2, bottom=0, height=2, width=f"{time_fraction * 100}%", background_color="00FF00", border_radius=2),
            *[
                div(
                    position="absolute",
                    left=f"{line['time_fraction'] * 100}%",
                    bottom=0,
                    height=f"{line['power_fraction'] * 100}%",
                    width=2,
                    background_color=line["color"],
                    border_radius=2) for line in lines
            ],
        ]
    ]

def init_graph():
    timeline_node = actions.user.ui_elements_get_node("timeline")
    rect = timeline_node.box_model.padding_rect
    actions.user.ui_elements_show(graph, props={
        "rect": rect,
    })

def timeline():
    div, state, effect = actions.user.ui_elements(["div", "state", "effect"])

    effect(init_graph, [])

    return div(id="timeline", position="relative", width="100%", min_width=900, height=150, background_color="161616", border_width=1)[
     *[div(position="absolute", width=1, height="100%", background_color="333333", left=f"{i * 10}%") for i in range(11)],
    ]

def play_button():
    div, text, icon, button, state = actions.user.ui_elements(["div", "text", "icon", "button", "state"])
    play, set_play = state.use("play", False)
    play_bg_color = "161616"

    def toggle_play(e):
        global start_time
        is_live = not play
        set_play(is_live)

    if play:
        return button(on_click=toggle_play, align_items="center", gap=16, padding=12, padding_left=24, padding_right=28, flex_direction="row", border_width=1, margin_right=16, border_color="333333", border_radius=16)[
            icon("stop", color="FF0000"),
            text("Stop listening"),
        ]
    else:
        return button(on_click=toggle_play, autofocus=True, align_items="center", gap=16, padding=12, padding_left=24, padding_right=28, flex_direction="row", border_width=1, margin_right=16, border_color="333333", border_radius=16)[
            icon("play", fill=play_bg_color),
            text("Start listening"),
        ]

def controls():
    div, text, icon, button, state = actions.user.ui_elements(["div", "text", "icon", "button", "state"])

    # play_bg_color = "00FF00"
    return div(flex_direction='row', gap=16, align_items="center")[
        play_button(),
        button()[icon("chevron_left")],
        text("Page 1"),
        button()[icon("chevron_right")],
        button("New page"),
        button("Clear page"),
        button("Clear all"),
        button("Import"),
        button("Export"),
    ]

def noise_item(noise):
    div, text, icon, button = actions.user.ui_elements(["div", "text", "icon", "button"])

    return button(flex_direction="row", padding=8, border_width=1, gap=8, border_color="333333", align_items="center")[
        icon("chevron_right", size=20),
        icon("check", size=20),
        div(min_width=100, flex_direction="row", justify_content="space_between")[
            text(noise),
            text("20"),
        ]
    ]

def filters():
    div, button = actions.user.ui_elements(["div", "button"])
    return div(flex_direction="row", gap=12)[
        button("View: Log"),
        button("Noises"),
        button("Columns"),
        button("Scope: Single page"),
        button("Mode: One-shot"),
    ]

def header():
    div, text, icon, button = actions.user.ui_elements(["div", "text", "icon", "button"])
    return div(flex_direction='row', justify_content="space_between")[
        text("App", font_size=24, margin=18),
        button()[
            icon("close")
        ]
    ]

def sidebar():
    div, text, state = actions.user.ui_elements(["div", "text", "state"])

    noises = state.get("noises")

    return div(flex_direction='column', padding=16, border_right=1, border_color="555555")[
        text("Parrot Tester", font_size=24, margin_bottom=24),
        *[noise_item(noise) for noise in noises]
    ]

def app():
    div, screen, window = actions.user.ui_elements(["div", "text", "screen", "window"])

    return screen(justify_content="center", align_items="center")[
        window(title="Parrot Tester")[
            header(),
            div(flex_direction='row')[
                sidebar(),
                div(flex_direction='column', width="100%", gap=16, padding=16)[
                    controls(),
                    filters(),
                    log(),
                    timeline(),
                    controls(),
                ]
            ],

        ]
    ]