from talon import Module, Context, actions, clip
from pathlib import Path
import pprint
import re
pp = pprint.PrettyPrinter()

mod = Module()
ctx = Context()
mod.tag("parrot_tester", "mode for testing parrot")

data = {}

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

def parrot_tester_disable():
    global data
    actions.user.ui_elements_hide_all()
    ctx.tags = []
    data = {}

def get_parrot_noises():
    noise_definitions_file = Path(__file__).parent / "parrot_tester_active.talon"

    with open(noise_definitions_file, "r") as file:
        content = file.readlines()

    noises = [re.search(r'parrot\(([^):]+)', line).group(1) for line in content if line.startswith("parrot(")]

    noises = list(set(noises))

    noise_columns = []
    current_column = []
    for noise in noises:
        if current_column and len(current_column) == 4:
            noise_columns.append(current_column)
            current_column = []

        current_column.append(noise)

    if current_column:
        noise_columns.append(current_column)

    return noise_columns

@mod.action_class
class Actions:
    def parrot_tester_discrete(noise: str, power: float = None, f0: float = None, f1: float = None, f2: float = None):
        """Trigger parrot tester discrete"""
        actions.user.ui_elements_highlight_briefly(noise)
        set_data(noise, power, f0, f1, f2)

    def parrot_tester_continuous_start(noise: str, power: float = None, f0: float = None, f1: float = None, f2: float = None):
        """Trigger parrot tester continuous"""
        actions.user.ui_elements_highlight(noise)
        set_data(noise, power, f0, f1, f2)

    def parrot_tester_continuous_stop(noise: str):
        """Stop parrot tester continuous"""
        actions.user.ui_elements_unhighlight(noise)

    def parrot_tester_toggle():
        """Toggle parrot tester"""
        noise_columns = get_parrot_noises()
        global data
        if not data:
            ctx.tags = ["user.parrot_tester"]
            actions.user.ui_elements_show(parrot_tester_ui, props={
                "noise_columns": noise_columns
            })
        else:
            parrot_tester_disable()

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
                button(on_click=parrot_tester_disable)[
                    icon("close", size=20, padding=6)
                ]
            ],
            div(flex_direction="row", padding=16)[
                *[column(noises) for noises in props["noise_columns"]]
            ]
        ]
    ]