from talon import Context, actions, clip, cron
from pathlib import Path
import pprint
import re
import random
import math
import time
from .utils import parrot_tester_initialize, restore_patterns

pp = pprint.PrettyPrinter()

ctx = Context()
data = {}
start_time = 0
cron_job = None
duration = 10.0

def on_noise(noise, power, f0, f1, f2):
    actions.user.ui_elements_set_state("log", lambda log: log + [{
        "time": time.perf_counter() - start_time,
        "time_display": f"{(time.perf_counter() - start_time):.3f}",
        "noise": noise,
        "power": power,
        "power_display": f"{power:.2f}" if power else '',
        "f0": str(round(f0)) if f0 is not None else '',
        "f1": str(round(f1)) if f1 is not None else '',
        "f2": str(round(f2)) if f2 is not None else '',
    }])

def set_data(noise, power, f0, f1, f2):
    global data

    if noise not in data:
        data[noise] = {
            "triggered_count": 0,
            "power": [],
            "f0": [],
            "f1": [],
            "f2": [],
            "average_power": 0,
            "average_f0": 0,
            "average_f1": 0,
            "average_f2": 0,
            "min_power": 0,
            "min_f0": 0,
            "min_f1": 0,
            "min_f2": 0,
            "max_power": 0,
            "max_f0": 0,
            "max_f1": 0,
            "max_f2": 0,
        }

    if power is not None:
        data[noise]["power"].append(power)

    if f0 is not None:
        data[noise]["f0"].append(f0)

    if f1 is not None:
        data[noise]["f1"].append(f1)

    if f2 is not None:
        data[noise]["f2"].append(f2)

    data[noise]["triggered_count"] += 1

    data[noise]["average_power"] = sum(data[noise]["power"]) / len(data[noise]['power'])
    data[noise]["average_f0"] = sum(data[noise]["f0"]) / len(data[noise]['f0'])
    data[noise]["average_f1"] = sum(data[noise]["f1"]) / len(data[noise]['f1'])
    data[noise]["average_f2"] = sum(data[noise]["f2"]) / len(data[noise]['f2'])
    data[noise]["min_power"] = min(data[noise]["power"])
    data[noise]["min_f0"] = min(data[noise]["f0"])
    data[noise]["min_f1"] = min(data[noise]["f1"])
    data[noise]["min_f2"] = min(data[noise]["f2"])
    data[noise]["max_power"] = max(data[noise]["power"])
    data[noise]["max_f0"] = max(data[noise]["f0"])
    data[noise]["max_f1"] = max(data[noise]["f1"])
    data[noise]["max_f2"] = max(data[noise]["f2"])

    actions.user.ui_elements_set_text(f"{noise}_count", f"({data[noise]['triggered_count']})")
    actions.user.ui_elements_set_text(f"{noise}_power_latest", f"{power:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f0_latest", f"{f0:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f1_latest", f"{f1:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f2_latest", f"{f2:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_power_average", f"{data[noise]['average_power']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f0_average", f"{data[noise]['average_f0']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f1_average", f"{data[noise]['average_f1']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f2_average", f"{data[noise]['average_f2']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_power_min", f"{data[noise]['min_power']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f0_min", f"{data[noise]['min_f0']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f1_min", f"{data[noise]['min_f1']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f2_min", f"{data[noise]['min_f2']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_power_max", f"{data[noise]['max_power']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f0_max", f"{data[noise]['max_f0']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f1_max", f"{data[noise]['max_f1']:.2f}")
    actions.user.ui_elements_set_text(f"{noise}_f2_max", f"{data[noise]['max_f2']:.2f}")

def init_parrot_noises_state():
    noise_definitions_file = Path(__file__).parent.parent / "auto_generated" / "parrot_tester_active.talon"

    with open(noise_definitions_file, "r") as file:
        content = file.readlines()

    noises = [re.search(r'parrot\(([^):]+)', line).group(1) for line in content if line.startswith("parrot(")]

    noises = {
        noise: { "active": True, "color": random_hex_color() } for noise in noises
    }

    return noises

def copy_all_data_to_clipboard():
    clip.set_text(pp.pformat(data))

def copy_data_to_clipboard(noise):
    return lambda e: clip.set_text(pp.pformat(data[noise])) if noise in data else None

def noise_data_ui(noise):
    div, text, icon, button = actions.user.ui_elements(["div", "text", "icon", "button"])

    def cell():
        return div(padding=8, border=1, background_color="212141")

    def cell_alt():
        return div(padding=8, border=1, background_color="313151")

    def stat_category(name):
        return div(width=80, flex_direction="column")[
            div()[
                cell()[text(name)],
                cell_alt()[text(id=f"{noise}_power_{name.lower()}")],
                cell()[text(id=f"{noise}_f0_{name.lower()}")],
                cell_alt()[text(id=f"{noise}_f1_{name.lower()}")],
                cell()[text(id=f"{noise}_f2_{name.lower()}")],
            ],
        ]

    return div(flex_direction="column", padding=16, border_width=1, id=noise)[
        div(flex_direction="row", justify_content="space_between", align_items="center")[
            div(flex_direction="row", align_items="center", gap=8, margin_bottom=16)[
                text(noise, font_size=20, font_weight="bold"),
                text(id=f"{noise}_count"),
            ],
            button(border_radius=4, on_click=copy_data_to_clipboard(noise), align_items="center", flex_direction="row", gap=8)[
                text("Copy", font_size=14),
                icon("copy")
            ]
        ],
        div(flex_direction="row")[
            div(flex_direction="column")[
                cell()[text(" ")],
                cell_alt()[text("Power")],
                cell()[text("F0")],
                cell_alt()[text("F1")],
                cell()[text("F2")],
            ],
            stat_category("Latest"),
            stat_category("Average"),
            stat_category("Min"),
            stat_category("Max"),
        ],
    ]

def column(noises):
    div = actions.user.ui_elements("div")

    return div(flex_direction="column")[
        *[noise_data_ui(noise) for noise in noises]
    ]

def parrot_tester_ui(props):
    div, text, screen, icon, button = actions.user.ui_elements(["div", "text", "screen", "icon", "button"])

    return screen(justify_content="center", align_items="center")[
        div(draggable=True, background_color="1D2126", border_radius=8, border_width=1)[
            div(flex_direction='row', justify_content="space_between", border_bottom=1, border_color="555555")[
                text("Parrot Tester", font_size=24, padding=16),
                div(flex_direction="row", gap=16)[
                    button(border_radius=4, on_click=copy_all_data_to_clipboard, align_items="center", flex_direction="row", gap=8)[
                        text("Copy all"),
                        icon("copy")
                    ],
                    button(on_click=parrot_tester_disable)[
                        icon("close", size=20, padding=6)
                    ]
                ]
            ],
            div(flex_direction="row", padding=16)[
                *[column(noises) for noises in props["noise_columns"]]
            ]
        ]
    ]

# noises = ["ah", "oh", "ee", "guh", "eh", "er", "t", "mm", "palate", "pop", "tut", "sh", "ss", "cluck"]

def rect_color(color, size=20, **props):
    div = actions.user.ui_elements("div")
    svg, rect = actions.user.ui_elements_svg(["svg", "rect"])

    return div(**props)[
        svg(size=size)[
            rect(x=0, y=0, width=24, height=24, fill=color)
        ]
    ]

def stop_icon(**props):
    div = actions.user.ui_elements("div")
    svg, rect = actions.user.ui_elements_svg(["svg", "rect"])

    return div(justify_content="center", **props)[
        svg()[
            rect(x=4, y=4, width=16, height=16, fill="FFFFFF"),
        ]
    ]

def delta_icon(**props):
    div = actions.user.ui_elements("div")
    svg, path = actions.user.ui_elements_svg(["svg", "path"])

    return div(justify_content="center", **props)[
        svg(size=16)[
            path(d="M5 20h14L12 4z"),
        ]
    ]

def random_hex_color():
    r = random.randint(50, 255)
    g = random.randint(50, 255)
    b = random.randint(50, 255)
    return f"#{r:02X}{g:02X}{b:02X}"

def noise_item(noise):
    div, text, icon, button = actions.user.ui_elements(["div", "text", "icon", "button"])
    svg, rect = actions.user.ui_elements_svg(["svg", "rect"])

    return button(flex_direction="row", padding=8, border_width=1, gap=8, border_color="333333", align_items="center")[
        icon("chevron_right", size=20),
        icon("check", size=20),
        # random color 6 digit hex
        rect_color(random_hex_color()),
        div(min_width=100, flex_direction="row", justify_content="space_between")[
            text(noise),
            text("20"),
        ]
    ]

def cell(children):
    div = actions.user.ui_elements("div")

    return div(padding_left=8, padding_right=8, border_top=1, height=32, justify_content="center", border_color="383838")[
        children
    ]

def color_col():
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="column")[
        cell(text("")),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
        cell(rect_color(random_hex_color())),
    ]

def noise_col():
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="column")[
        cell(text("Noise")),
        cell(text("pop")),
        cell(text("pop")),
        cell(text("palate")),
        cell(text("pop")),
        cell(text("pop")),
        cell(text("palate")),
        cell(text("pop")),
        cell(text("pop")),
        cell(text("palate")),
        cell(text("pop")),
        cell(text("pop")),
        cell(text("palate")),
        cell(text("pop")),
        cell(text("pop")),
        cell(text("palate")),
    ]

def power_col():
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="column")[
        cell(text("Power")),
        cell(text("20")),
        cell(text("14")),
        cell(text("12")),
        cell(text("20")),
        cell(text("14")),
        cell(text("12")),
        cell(text("20")),
        cell(text("14")),
        cell(text("12")),
        cell(text("20")),
        cell(text("14")),
        cell(text("12")),
        cell(text("20")),
        cell(text("14")),
        cell(text("12")),
    ]

def delta_power_col():
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="column")[
        cell(text("Power")),
        cell(text("20")),
        cell(text("14")),
        cell(text("12")),
        cell(text("20")),
        cell(text("14")),
        cell(text("12")),
        cell(text("20")),
        cell(text("14")),
        cell(text("12")),
        cell(text("20")),
        cell(text("14")),
        cell(text("12")),
        cell(text("20")),
        cell(text("14")),
        cell(text("12")),
    ]

def time_col():
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="column")[
        cell(text("Time")),
        cell(text("0.234")),
        cell(div(flex_direction="row")[text("1.494"),text(" +1.260", color="00FF00")]),
        cell(text("2.234")),
        cell(text("3.236")),
        cell(text("3.494")),
        cell(text("4.234")),
        cell(text("5.234")),
        cell(text("6.294")),
        cell(text("6.434")),
        cell(text("7.234")),
        cell(text("7.494")),
        cell(text("8.234")),
        cell(text("9.234")),
        cell(text("9.494")),
        cell(text("9.923")),
    ]

def time_delta_col():
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="column")[
        cell(text("Time")),
        cell(text("0.000")),
        cell(text("1.260")),
        cell(text("0.740")),
        cell(text("0.000")),
        cell(text("1.260")),
        cell(text("0.740")),
        cell(text("0.000")),
        cell(text("1.260")),
        cell(text("0.740")),
        cell(text("0.000")),
        cell(text("1.260")),
        cell(text("0.740")),
        cell(text("0.000")),
        cell(text("1.260")),
        cell(text("0.740")),
    ]

def count_col():
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="column")[
        cell(text("Count")),
        cell(text("1")),
        cell(text("1")),
        cell(text("2")),
        cell(text("1")),
        cell(text("3")),
        cell(text("4")),
        cell(text("5")),
        cell(text("6")),
        cell(text("7")),
        cell(text("2")),
        cell(text("8")),
        cell(text("9")),
        cell(text("10")),
        cell(text("11")),
        cell(text("12")),
    ]

def f0_col():
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="column")[
        cell(text("F0")),
        cell(text("3333")),
        cell(text("3453")),
        cell(text("5444")),
        cell(text("3333")),
        cell(text("3453")),
        cell(text("5444")),
        cell(text("3333")),
        cell(text("3453")),
        cell(text("5444")),
        cell(text("3333")),
        cell(text("3453")),
        cell(text("5444")),
        cell(text("3333")),
        cell(text("3453")),
        cell(text("5444")),
    ]

def f1_col():
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="column")[
        cell(text("F1")),
        cell(text("6663")),
        cell(text("6432")),
        cell(text("8494")),
        cell(text("6663")),
        cell(text("6432")),
        cell(text("8494")),
        cell(text("6663")),
        cell(text("6432")),
        cell(text("8494")),
        cell(text("6663")),
        cell(text("6432")),
        cell(text("8494")),
        cell(text("6663")),
        cell(text("6432")),
        cell(text("8494")),
    ]

def f2_col():
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="column")[
        cell(text("F2")),
        cell(text("9388")),
        cell(text("8499")),
        cell(text("9003")),
        cell(text("9388")),
        cell(text("8499")),
        cell(text("9003")),
        cell(text("9388")),
        cell(text("8499")),
        cell(text("9003")),
        cell(text("9388")),
        cell(text("8499")),
        cell(text("9003")),
        cell(text("9388")),
        cell(text("8499")),
        cell(text("9003")),
    ]

def row(item, color):
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="row", gap=16)[
        text(f"{item['time_display']}", width=50),
        div(flex_direction="row", gap=8, width=100)[
            rect_color(color),
            text(item["noise"]),
        ],
        # text(item["noise"]),
        text(item["power_display"]),
        # text(f"{float(item["f0"]):.2f}" if item else '', width=100),
        # text(f"{float(item["f1"]):.2f}" if item else '', width=100),
        # text(f"{float(item["f2"]):.2f}" if item else '', width=100),
    ]

def log():
    div, text, state = actions.user.ui_elements(["div", "text", "state"])

    log = state.get("log")
    noises = state.get("noises")

    return div(id="log", flex_direction="column", height=500, overflow_y="scroll", border_width=1, background_color="161616")[
        # text('hello'),
        *[row(item, noises[item["noise"]]["color"]) for item in log],
        # time_col(),
        # # time_delta_col(),
        # color_col(),
        # noise_col(),
        # power_col(),
        # # delta_power_col(),
        # # count_col(),
        # f0_col(),
        # f1_col(),
        # f2_col(),
    ]

# def toggle_play(e):
#     actions.user.ui_elements_set_state("play", lambda p: not p)



def timeline():
    div, state, effect = actions.user.ui_elements(["div", "state", "effect"])

    effect(init_graph, [])

    return div(id="timeline", position="relative", width="100%", min_width=900, height=150, background_color="161616", border_width=1)[
     *[div(position="absolute", width=1, height="100%", background_color="333333", left=f"{i * 10}%") for i in range(11)],
    ]

def cron_timer_enable():
    global cron_job, start_time

    def update():
        elapsed = time.perf_counter() - start_time
        fraction = (elapsed % duration) / duration
        actions.user.ui_elements_set_state("time_fraction", fraction)

    cron_job = cron.interval("32ms", update)

def cron_timer_disable():
    global cron_job
    if cron_job:
        cron.cancel(cron_job)
        cron_job = None

def play_button():
    div, text, icon, button, state = actions.user.ui_elements(["div", "text", "icon", "button", "state"])
    play, set_play = state.use("play", False)
    play_bg_color = "161616"

    def toggle_play(e):
        global start_time
        is_live = not play
        set_play(is_live)

        if is_live:
            start_time = time.perf_counter()
            ctx.tags = ["user.parrot_tester"]
            cron_timer_enable()
        else:
            ctx.tags = []
            cron_timer_disable()

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

def clear_all(e):
    global start_time
    start_time = 0
    actions.user.ui_elements_set_state({
        "log": [],
        "play": False,
        "time_fraction": 0,
    })
    ctx.tags = []
    cron_timer_disable()

def controls():
    div, text, icon, button, state = actions.user.ui_elements(["div", "text", "icon", "button", "state"])

    # play_bg_color = "00FF00"
    return div(flex_direction='row', gap=16, align_items="center")[
        play_button(),
        button()[icon("chevron_left")],
        text("Page 1"),
        button()[icon("chevron_right")],
        styled_button("New page"),
        styled_button("Clear page"),
        styled_button("Clear all", on_click=clear_all),
        # button("Prev page"),
        # button("Page 1"),
        # button("Next page"),
        # div(flex_direction="row", gap=8, margin_right=16, align_items="center")[
        #     text("Time", font_size=14),
        #     input_text(value="10", id="graph_time", width=50, border_radius=4),
        # ],
        # div(flex_direction="row", gap=8, align_items="center")[
        #     text("Power", font_size=14),
        #     input_text(value="20", id="graph_power", width=50, border_radius=4),
        # ],
        styled_button("Import"),
        styled_button("Export"),
    ]

def sidebar():
    div, text, state, button = actions.user.ui_elements(["div", "text", "state", "button"])

    noises = state.get("noises")

    return div(flex_direction='column', padding=16, border_right=1, border_color="555555")[
        text("Parrot Tester", font_size=24, margin_bottom=24),
        *[noise_item(noise) for noise in noises]
    ]

def filter_dropdown_button(title: str):
    text, icon, button = actions.user.ui_elements(["text", "icon", "button"])
    return button(flex_direction="row", align_items="center", gap=8, border_radius=4, border_color="333333", border_width=1, padding=8, padding_left=16, padding_right=16)[
        text(title),
        icon("chevron_down", size=16),
    ]

def styled_button(title: str, on_click=lambda e: None):
    button = actions.user.ui_elements(["button"])
    return button(text=title, on_click=on_click, border_radius=4, border_color="333333", border_width=1, padding=12, padding_left=16, padding_right=16)

def filters():
    div, text = actions.user.ui_elements(["div", "text"])
    return div(flex_direction="row", gap=12)[
        filter_dropdown_button("View: Log"),
        filter_dropdown_button("Noises"),
        filter_dropdown_button("Columns"),
        filter_dropdown_button("Scope: Single page"),
        filter_dropdown_button("Mode: One-shot"),
    ]

def noise(name, color, active, toggle_active):
    div, text = actions.user.ui_elements(["div", "text"])
    opacity = 1 if active else 0.5
    color = color if active else "999999"

    return div(
        opacity=opacity,
        # on_click=toggle_active,
        flex_direction="row",
        gap=4,
        align_items="center",
        border_width=1,
        border_radius=4,
        padding=6,
        id=name,
    )[
        rect_color(color, size=15),
        text(name),
    ]

def noises_ui():
    div, state = actions.user.ui_elements(["div", "state"])

    noises, set_noises = state.use("noises")

    def toggle_active(name):
        def toggle(e):
            set_noises({
                **noises,
                name: {
                    **noises[name],
                    "active": not noises[name]["active"]
                }
            })

        return toggle

    return div(flex_direction="row", gap=12)[
        *[noise(
            name=name,
            color=data["color"],
            active=data["active"],
            toggle_active=toggle_active(name)
        ) for name, data in noises.items()]
    ]
        # noise("ah", random_hex_color()),
        # noise("oh", random_hex_color()),
        # noise("ee", random_hex_color()),
        # noise("guh", random_hex_color()),
        # noise("eh", random_hex_color()),
        # noise("er", random_hex_color()),
        # noise("t", random_hex_color()),
        # noise("mm", random_hex_color()),
        # noise("palate", random_hex_color()),
        # noise("pop", random_hex_color()),
        # noise("tut", random_hex_color()),
        # noise("sh", random_hex_color()),
        # noise("ss", random_hex_color()),
        # noise("cluck", random_hex_color()),
    # ]

# def nav():
#     div, text, icon, button = actions.user.ui_elements(["div", "text", "icon", "button"])
#     return div(flex_direction="row", gap=16, width="100%", justify_content="center", align_items="center")[
#         button()[icon("chevron_left")],
#         text("Page 1"),
#         button()[icon("chevron_right")],
#     ]
def header():
    div, text, icon, button = actions.user.ui_elements(["div", "text", "icon", "button"])
    return div(flex_direction='row', justify_content="space_between")[
        text("Parrot Tester", font_size=24, margin=18),
        button(on_click=parrot_tester_disable, padding=18)[
            icon("close")
        ]
    ]

def parrot_tester_ui_2(props):
    div, text, screen, icon, button, input_text = actions.user.ui_elements(["div", "text", "screen", "icon", "button", "input_text"])

    return screen(justify_content="center", align_items="center")[
        div(draggable=True, background_color="222222", border_radius=8, border_width=1)[
            # div(flex_direction='row')[
                # sidebar(),
            header(),
            div(flex_direction='column', width="100%", gap=16, padding=16)[
                # controls(),
                filters(),
                noises_ui(),
                # log(),
                timeline(),
                # nav(),
                controls(),
            ]
        ]
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

def listen():
    ctx.tags = ["user.parrot_tester"]

def stop_listen():
    ctx.tags = []

def parrot_tester_discrete(noise: str, power: float = None, f0: float = None, f1: float = None, f2: float = None):
    """Trigger parrot tester discrete"""
    actions.user.ui_elements_highlight_briefly(noise)
    on_noise(noise, power, f0, f1, f2)

def parrot_tester_continuous_start(noise: str, power: float = None, f0: float = None, f1: float = None, f2: float = None):
    """Trigger parrot tester continuous"""
    actions.user.ui_elements_highlight(noise)
    on_noise(noise, power, f0, f1, f2)
    # set_data(noise, power, f0, f1, f2)

def parrot_tester_continuous_stop(noise: str):
    """Stop parrot tester continuous"""
    on_noise(noise, None, None, None, None)
    actions.user.ui_elements_unhighlight(noise)

def parrot_tester_disable():
    global start_time
    print("Disabling parrot tester")
    restore_patterns()
    start_time = 0
    ctx.tags = []
    data.clear()
    actions.user.ui_elements_hide_all()
    data.clear()
    cron_timer_disable()

def parrot_tester_toggle():
    """Toggle parrot tester"""
    global start_time

    if actions.user.ui_elements_is_active(parrot_tester_ui_2):
        parrot_tester_disable()
    else:
        parrot_tester_initialize()
        actions.user.ui_elements_show(parrot_tester_ui_2, initial_state={
            "noises": init_parrot_noises_state(),
            "log": [],
        })