from talon import Module, Context, actions

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

def face_tester_ui():
    version = actions.user.ui_elements_version()
    if version < "0.6.0":
        print("Face Tester requires talon-ui-elements version 0.6.0 or higher.")

    screen, div, text, icon, button = actions.user.ui_elements(["screen", "div", "text", "icon", "button"])

    def item(key):
        return div(id=key, padding=8)[text(key)]

    def title(title):
        return text(title, font_weight="bold", color="87ceeb")

    def subtitle(title):
        return text(title, font_weight="bold", margin_top=16)

    return screen(align_items="center", justify_content="center")[
        div(draggable=True, background_color="333333", border_radius=4, border_width=1, border_color="555555")[
            div(flex_direction="row", justify_content="space_between", align_items="center")[
                div(flex_direction="row", padding=16, gap=16, align_items="flex_end")[
                    text("Face Tester", font_size=24, font_weight="bold"),
                    text("Say 'face tester' to stop / toggle", color="BBBBBB"),
                ],
                button(on_click=face_tester_disable, margin=0)[
                    icon("close", padding=6),
                ]
            ],
            div(flex_direction="row", padding=16, gap=16)[
                div(flex_direction="column", gap=8, border_width=1, border_color="555555", padding=16)[
                    title("Eyes"),
                    subtitle("Blink"),
                    *(item(key) for key in blink),
                    subtitle("Squint / Widen"),
                    *(item(key) for key in squint),
                    *(item(key) for key in widen),
                    subtitle("Brow"),
                    *(item(key) for key in brow),
                ],
                div(flex_direction="column", gap=8, border_width=1, border_color="555555", padding=16)[
                    title("Mouth"),
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
    ]

def face_tester_enable():
    ctx.tags = ["user.face_tester"]
    actions.user.ui_elements_show(face_tester_ui)

def face_tester_disable():
    ctx.tags = []
    actions.user.ui_elements_hide_all()

@mod.action_class
class Actions:
    def face_tester_toggle():
        """Toggle face tester"""
        if "user.face_tester" in ctx.tags:
            face_tester_disable()
        else:
            face_tester_enable()
