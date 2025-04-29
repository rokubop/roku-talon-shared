from talon import Context, actions

ctx = Context()

# Constants
HEADER_TEXT = "Parrot Tester"
DOCS_BUTTON_TEXT = "Docs"
PATTERNS_BUTTON_TEXT = "Patterns"
TABS = ["Activity", "Log", "Timeline", "Stats", "Patterns"]
SIDEBAR_ITEMS = [f"Item {i}" for i in range(1, 9)]
CHART_DATA = [10, 20, 30, 40, 50, 40, 30, 20]
DETAILS_TEXT = [f"pop {i*10}, gu4 {i*5}" for i in range(1, 9)]


def parrot_tester_new_ui():
    """Envisioned UI for Parrot Tester based on the provided sketch."""
    div, text, screen, button, icon, tab, chart = actions.user.ui_elements([
        "div", "text", "screen", "button", "icon", "tab", "chart"
    ])

    return screen(justify_content="center", align_items="center")[
        div(flex_direction="column", width="90%", height="90%", padding=16, background_color="1D2126", border_radius=8, border_width=1, border_color="555555")[
            # Header Section
            div(flex_direction="row", justify_content="space_between", align_items="center", padding=16, border_bottom=1, border_color="333333")[
                text(HEADER_TEXT, font_size=24, font_weight="bold"),
                button(on_click=lambda e: print("Docs clicked"), border_radius=4, padding=8)[
                    text(DOCS_BUTTON_TEXT, font_size=16, color="FFFFFF")
                ],
                button(on_click=lambda e: print("Patterns clicked"), border_radius=4, padding=8)[
                    text(PATTERNS_BUTTON_TEXT, font_size=16, color="FFFFFF")
                ]
            ],
            # Tabs Section
            div(flex_direction="row", justify_content="space_between", padding=16, border_bottom=1, border_color="333333")[
                *[tab(label=label, on_click=lambda e, l=label: print(f"{l} tab clicked")) for label in TABS]
            ],
            # Main Content Section
            div(flex_direction="row", flex=1, padding=16, gap=16)[
                # Sidebar
                div(flex_direction="column", width="20%", background_color="161616", border_radius=4, padding=8, gap=8)[
                    *[button(text=item, on_click=lambda e: print(f"{item} clicked")) for item in SIDEBAR_ITEMS]
                ],
                # Graph and Details
                div(flex_direction="column", flex=1, gap=16)[
                    # Graph Section
                    div(flex_direction="column", height="50%", background_color="161616", border_radius=4, padding=8)[
                        text("pop, gu4", font_size=16, color="FFFFFF", margin_bottom=8),
                        text("Graph", font_size=16, color="FFFFFF"),
                        # chart(type="bar", data=[
                        #     {"label": str(i), "value": value} for i, value in enumerate(CHART_DATA, start=1)
                        # ])
                    ],
                    # Details Section
                    div(flex_direction="row", flex=1, gap=8)[
                        div(flex_direction="column", width="30%", background_color="161616", border_radius=4, padding=8, gap=4)[
                            *[text(f"{i}", font_size=16, color="FFFFFF") for i in range(1, 9)]
                        ],
                        div(flex_direction="column", flex=1, background_color="161616", border_radius=4, padding=8, gap=4)[
                            *[text(detail, font_size=16, color="FFFFFF") for detail in DETAILS_TEXT]
                        ]
                    ]
                ]
            ]
        ]
    ]