from talon import Module, Context, actions, cron

mod = Module()
mod.tag("face_tester", desc="Tag for enabling face tester")
ctx = Context()

blink = ['blink', 'blink_left', 'blink_right']
squint = ['squint', 'squint_left', 'squint_right']
widen = ['eye_wide_left', 'eye_wide_right']
brow = ['brow_down_left', 'brow_down_right', 'brow_inner_up', 'brow_outer_up_left', 'brow_outer_up_right']
jaw = ['jaw_open', 'jaw_left', 'jaw_right']
frown = ['frown', 'frown_left', 'frown_right']
dimple = ['dimple', 'dimple_left', 'dimple_right']
mouth_shrug = ['mouth_shrug_lower', 'mouth_shrug_upper']
mouth_misc = ['mouth_close', 'mouth_pucker', 'mouth_funnel', 'mouth_lower_down_left', 'mouth_lower_down_right', 'mouth_press_left', 'mouth_press_right', 'mouth_right', 'mouth_left', 'mouth_roll_lower', 'mouth_roll_upper', 'mouth_stretch_left', 'mouth_stretch_right', 'mouth_upper_up_left', 'mouth_upper_up_right']
smile = ['smile', 'smile_left', 'smile_right']
gaze_up = ['gaze_up_left', 'gaze_up_right']
gaze_down = ['gaze_down_left', 'gaze_down_right']
gaze_left = ['gaze_out_left', 'gaze_in_right']
gaze_right = ['gaze_in_left', 'gaze_out_right']

def play_button():
    text, icon, button, state = actions.user.ui_elements(["text", "icon", "button", "state"])
    play, set_play = state.use("play", True)

    def toggle_play(e):
        new_play = not play

        if new_play:
            ctx.tags = ["user.face_tester"]
        else:
            ctx.tags = []

        set_play(new_play)

    return button(
        padding=8,
        padding_left=24,
        padding_right=28,
        flex_direction="row",
        align_items="center",
        gap=16,
        border_width=1,
        border_radius=2,
        on_click=toggle_play,
        border_color="#000000",
        background_color="#3B71D9" if play else "#13A126",
        autofocus=True,
    )[
        icon("pause" if play else "play", fill=True),
        text("PAUSE" if play else "START"),
    ]

def star_icon():
    svg, path = actions.user.ui_elements(["svg", "path"])

    return svg()[
        path(d="M12 2l3.09 6.26L22 9.27l-5 4.87L18.18 22 12 19.27 5.82 22l1.18-7.86-5-4.87 6.91-1L12 2z"),
        path(stroke="#FFD700", stroke_width=2, d="M12 2l3.09 6.26L22 9.27l-5 4.87L18.18 22 12 19.27 5.82 22l1.18-7.86-5-4.87 6.91-1L12 2z"),
    ]

def mouth_icon():
    svg, path = actions.user.ui_elements(["svg", "path"])

    return svg()[
        # path(d="M24,0 L24,24 L0,24 L0,0 L24,0 Z M12.5934901,23.257841 L12.5819402,23.2595131 L12.5108777,23.2950439 L12.4918791,23.2987469 L12.4918791,23.2987469 L12.4767152,23.2950439 L12.4056548,23.2595131 C12.3958229,23.2563662 12.3870493,23.2590235 12.3821421,23.2649074 L12.3780323,23.275831 L12.360941,23.7031097 L12.3658947,23.7234994 L12.3769048,23.7357139 L12.4804777,23.8096931 L12.4953491,23.8136134 L12.4953491,23.8136134 L12.5071152,23.8096931 L12.6106902,23.7357139 L12.6232938,23.7196733 L12.6232938,23.7196733 L12.6266527,23.7031097 L12.609561,23.275831 C12.6075724,23.2657013 12.6010112,23.2592993 12.5934901,23.257841 L12.5934901,23.257841 Z M12.8583906,23.1452862 L12.8445485,23.1473072 L12.6598443,23.2396597 L12.6498822,23.2499052 L12.6498822,23.2499052 L12.6471943,23.2611114 L12.6650943,23.6906389 L12.6699349,23.7034178 L12.6699349,23.7034178 L12.678386,23.7104931 L12.8793402,23.8032389 C12.8914285,23.8068999 12.9022333,23.8029875 12.9078286,23.7952264 L12.9118235,23.7811639 L12.8776777,23.1665331 C12.8752882,23.1545897 12.8674102,23.1470016 12.8583906,23.1452862 L12.8583906,23.1452862 Z M12.1430473,23.1473072 C12.1332178,23.1423925 12.1221763,23.1452606 12.1156365,23.1525954 L12.1099173,23.1665331 L12.0757714,23.7811639 C12.0751323,23.7926639 12.0828099,23.8018602 12.0926481,23.8045676 L12.108256,23.8032389 L12.3092106,23.7104931 L12.3186497,23.7024347 L12.3186497,23.7024347 L12.3225043,23.6906389 L12.340401,23.2611114 L12.337245,23.2485176 L12.337245,23.2485176 L12.3277531,23.2396597 L12.1430473,23.1473072 Z"),
        path(stroke_width=1, fill="FFFFFF", d="M20.3143,8.03775 C18.9074,7.07308 16.9416,6.0781 14.9267,6.00193 C14.1207,5.97146 13.4445,6.30726 12.7598,6.64733 C12.5678,6.74269 12.3752,6.83838 12.1788,6.92644 C12.0236,6.99598 11.9764,6.99598 11.8212,6.92644 C11.6248,6.83839 11.4322,6.7427 11.2402,6.64735 C10.5555,6.30728 9.87934,5.97148 9.07333,6.00196 C7.05843,6.07815 5.09261,7.07311 3.68571,8.03777 C2.76327,8.67025 1,9.6837 1,11.0007 C1,12.4522 2.9368,14.1171 3.91411,14.9494 C5.72969,16.4957 8.45115,18.000002 12,18.000002 C15.5489,18.000002 18.2703,16.4957 20.0859,14.9494 C21.1019,14.0841 23,12.513 23,11.0007 C23,9.72309 21.206,8.64915 20.3143,8.03775 Z M12.9969,8.75151 C12.7546,8.86017 12.3952,9.00115 12,9.00115 C11.6049,9.00115 11.2455,8.86017 11.0031,8.75151 C10.4188,8.48958 9.81105,7.97557 9.14892,8.0006 C7.23673,8.07291 5.40709,9.14268 3.95508,10.333 C5.81813,11.0831 8.84528,11.5 12,11.5 C15.1548,11.5 18.1819,11.0831 20.045,10.333 C18.593,9.14266 16.7633,8.07286 14.8511,8.00057 C14.2021,7.97604 13.5691,8.49501 12.9969,8.75151 Z M4.30096,12.5648 C6.46268,13.2051 9.27679,13.5 12,13.5 C14.7233,13.5 17.5374,13.2051 19.6991,12.5648 C17.6986,14.6733 14.9328,16 12,16 C9.06722,16 6.30142,14.6733 4.30096,12.5648 Z"),
    ]

def eye_icon():
    svg, path, circle = actions.user.ui_elements(["svg", "path", "circle"])

    return svg()[
        path(d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"),
        circle(cx=12, cy=12, r=3)
    ]


def item(key):
    div, checkbox, text, state = actions.user.ui_elements(["div", "checkbox", "text", "state"])

    return div(flex_direction="row", align_items="center", gap=8)[
        checkbox(
            id=f"checkbox_{key}",
            background_color="222222",
            border_color="111111",
            border_width=1,
            on_change=lambda e, k=key: state.set("favorites", lambda f: (
                f | {k} if e.checked else f - {k}
            )),
        ),
        text(key, id=key, padding=8, for_id=f"checkbox_{key}"),
    ]

def title(title, svg_icon=None):
    div, text = actions.user.ui_elements(["div", "text"])

    return div(flex_direction="row", align_items="center", gap=8)[
        svg_icon() if svg_icon else None,
        text(title, font_weight="bold", color="87ceeb"),
    ]

def subtitle(title):
    text = actions.user.ui_elements(["text"])

    return text(title, font_weight="bold", margin_top=16)

def header():
    div, text = actions.user.ui_elements(["div", "text"])

    div(flex_direction="row", align_items="center", justify_content="space_between", padding=16)[
        text("Say 'face tester' to stop / toggle"),
        play_button(),
    ],

def favorites():
    div, state = actions.user.ui_elements(["div", "state"])

    div(background_color="222222", border_right=1, width=200)[
        title("Favorites", star_icon),
        div(flex_direction="column", gap=8)[
            *[item(key) for key in state.get("favorites")],
        ]
    ]

def face_tester_ui():
    version = actions.user.ui_elements_version()
    if version < "0.6.0":
        print("Face Tester requires talon-ui-elements version 0.6.0 or higher.")

    screen, window, div = actions.user.ui_elements(["screen", "window", "div"])
    text = actions.user.ui_elements(["text"])

    return screen(align_items="center", justify_content="center")[
        window(title="Face Tester", background_color="333333")[
            header(),
            div(flex_direction="row")[
                favorites(),
                div(flex_direction="row", padding=16, gap=16)[
                    div(flex_direction="column", gap=8, border_width=1, border_color="555555", padding=16, width=200)[
                        title("General"),
                        subtitle("Presence"),
                        item("presence"),
                        subtitle("Gaze XY"),
                        div(padding=8)[
                            text(id="gaze_x", width=50),
                            text(id="gaze_y", width=50),
                        ],
                        subtitle("dimple_value"),
                        div(padding=8)[
                            text(id="dimple_left_value", width=50),
                            text(id="dimple_right_value", width=50),
                        ],
                    ],
                    div(flex_direction="column", gap=8, border_width=1, border_color="555555", padding=16)[
                        title("Eyes", eye_icon),
                        subtitle("Blink"),
                        *(item(key) for key in blink),
                        subtitle("Squint / Widen"),
                        *(item(key) for key in squint),
                        *(item(key) for key in widen),
                        subtitle("Brow"),
                        *(item(key) for key in brow),
                    ],
                    div(flex_direction="column", gap=8, border_width=1, border_color="555555", padding=16)[
                        title("Mouth", mouth_icon),
                        div(flex_direction="row", gap=16)[
                            div(flex_direction="column", gap=8)[
                                subtitle("Jaw"),
                                *(item(key) for key in jaw),
                                subtitle("Frown"),
                                *(item(key) for key in frown),
                                subtitle("Dimple"),
                                *(item(key) for key in dimple),
                            ],
                            div(flex_direction="column", gap=8)[
                                subtitle("Smile"),
                                *(item(key) for key in smile),
                                subtitle("Mouth Shrug"),
                                *(item(key) for key in mouth_shrug),
                            ],
                            div(flex_direction="column", gap=8)[
                                subtitle("Mouth Misc"),
                                *(item(key) for key in mouth_misc),
                            ],
                        ],
                    ],
                    div(flex_direction="column", gap=8, border_width=1, border_color="555555", padding=16)[
                        title("Gaze"),
                        subtitle("Gaze up"),
                        *(item(key) for key in gaze_up),
                        subtitle("Gaze down"),
                        *(item(key) for key in gaze_down),
                        subtitle("Gaze left"),
                        *(item(key) for key in gaze_left),
                        subtitle("Gaze right"),
                        *(item(key) for key in gaze_right),
                    ],
                ],
            ]
        ],
    ]

def on_mount():
    ctx.tags = ["user.face_tester"]

def on_unmount():
    ctx.tags = []

@mod.action_class
class Actions:
    def face_tester_toggle():
        """Toggle face tester"""
        actions.user.ui_elements_toggle(
            face_tester_ui,
            initial_state={
                "favorites": set(),
            },
            on_mount=on_mount,
            on_unmount=on_unmount,
        )