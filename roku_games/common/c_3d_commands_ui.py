from talon import actions

ui_commands = None
ui_current_noises = None
ui_noise_modes = None
ui_nav_modes = None
accent_color = "45f248"

def show_commands(commands: list[str]):
    global ui_commands
    (div, text, screen) = actions.user.ui_elements(["div", "text", "screen"])

    ui_commands = screen(align_items="flex_end", justify_content="flex_start")[
        div(background_color="00000066", border_color="993333", border_width=1, width=150, margin=16, margin_right=32, padding=16)[
            div(flex_direction="row", gap=16)[
                div(gap=8)[
                    text("commands", font_weight="bold"),
                    *(text(command) for command in commands),
                ]
            ]
        ],
    ]
    ui_commands.show()

def show_noises(noise_mode: str, noises: dict[str, str]):
    global ui_current_noises
    (div, text, screen) = actions.user.ui_elements(["div", "text", "screen"])
    accent = noises["color"]
    print("accent", accent)

    ui_current_noises = screen(align_items="flex_end", justify_content="flex_start")[
        div(background_color="00000066", border_color=accent, border_width=1, width=150, margin=16, margin_top=450, margin_right=32, padding=16)[
            div(flex_direction="row", gap=16)[
                div(gap=8)[
                    div(gap=8, flex_direction="row")[
                        text("Noise mode:", font_weight="bold", font_size=20),
                        text(noise_mode, color=accent, font_size=20),
                    ],
                    div(gap=8, flex_direction="row")[
                        text("pop", color=accent), text(noises["pop"]),
                    ],
                    div(gap=8, flex_direction="row")[
                        text("hiss", color=accent), text(noises["hiss"]),
                    ],
                ]
            ]
        ],
    ]
    ui_current_noises.show()

def show_noise_modes(noise_modes: list[str]):
    global ui_noise_modes
    (div, text, screen) = actions.user.ui_elements(["div", "text", "screen"])

    ui_noise_modes = screen(align_items="flex_end", justify_content="flex_start")[
        div(background_color="00000066", border_color="333399", margin_top=550, border_width=1, width=150, margin=16, margin_right=32, padding=16)[
            div(flex_direction="row", gap=16)[
                div(gap=8)[
                    text("noise modes", font_weight="bold"),
                    *(text(command) for command in noise_modes),
                ]
            ]
        ],
    ]
    ui_noise_modes.show()

def show_nav_modes(nav_modes, state):
    global ui_nav_modes
    (div, text, screen) = actions.user.ui_elements(["div", "text", "screen"])

    print("nav_modes", nav_modes)
    print("state", state)

    cam_bg = "FF000099" if state["nav_mode"] == "cam" else "33333366"
    turn_bg = "FF000099" if state["nav_mode"] == "turn" else "33333366"
    look_bg = "FF000099" if state["nav_mode"] == "look" else "33333366"
    go_bg = "FF000099" if state["nav_mode"] == "go" else "33333366"

    cam_angles = []
    for angle in nav_modes["cam"]["angles"]:
        if state["cam_angle"] == angle:
            cam_angles.append(text(str(angle), background_color="FF000099", padding=4, border_radius=4, margin_top=-4))
        else:
            cam_angles.append(text(str(angle)))

    turn_durations = []
    for duration in nav_modes["turn"]["durations"]:
        if state["turn_duration"] == duration:
            turn_durations.append(text(str(duration), background_color="FF000099", padding=4, border_radius=4, margin_top=-4))
        else:
            turn_durations.append(text(str(duration)))

    look_speeds = []
    for speed in nav_modes["look"]["speeds"]:
        if state["look_speed"] == speed:
            look_speeds.append(text(str(speed), background_color="FF000099", padding=4, border_radius=4, margin_top=-4))
        else:
            look_speeds.append(text(str(speed)))

    go_durations = []
    for duration in nav_modes["go"]["durations"]:
        if state["go_duration"] == duration:
            go_durations.append(text(str(duration), background_color="FF000099", padding=4, border_radius=4, margin_top=-4))
        else:
            go_durations.append(text(str(duration)))

    ui_nav_modes = screen(align_items="center", justify_content="flex_end")[
        div(background_color="00000066", align_items="center", justify_content="center", margin_bottom=180, padding=16)[
            div(gap=24, flex_direction="row")[
                text("left", font_weight="bold"),
                text("right", font_weight="bold")
            ],
            div(flex_direction="column", gap=16, margin_top=16)[
                div(gap=8, flex_direction="row", justify_content="center", align_items="center")[
                    div(width=100)[
                        text("angles", font_size=10, margin_bottom=5),
                        div(flex_direction="row", gap=8)[
                            *cam_angles
                        ]
                    ],
                    div(width=60, align_items="flex_end")[
                        text("cam", background_color=cam_bg, padding=8, border_radius=8)
                    ],
                    div(width=60, align_items="flex_start")[
                        text("turn", background_color=turn_bg, padding=8, border_radius=8)
                    ],
                    div(width=100)[
                        text("duration", font_size=10, margin_bottom=5),
                        div(flex_direction="row", gap=8)[
                            *turn_durations
                        ]
                    ],
                ],
                div(gap=8, flex_direction="row", justify_content="center", align_items="center")[
                    div(width=100)[
                        text("speed", font_size=10, margin_bottom=5),
                        div(flex_direction="row", gap=8)[
                            *look_speeds
                        ]
                    ],
                    div(width=60, align_items="flex_end")[
                        text("look", background_color=look_bg, padding=8, border_radius=8)
                    ],
                    div(width=60, align_items="flex_start")[
                        text("go", background_color=go_bg, padding=8, border_radius=8)
                    ],
                    div(width=100)[
                        text("duration", font_size=10, margin_bottom=5),
                        div(flex_direction="row", gap=8)[
                            *go_durations
                        ]
                    ],
                ],
            ]
        ],
    ]
    ui_nav_modes.show()

def show_ui(commands, state, noises, noise_modes, nav_modes):
    show_commands(commands)
    show_noises(state["noise_mode"], noises)
    show_noise_modes(noise_modes)
    show_nav_modes(nav_modes, state)

def update_current_noises_ui(current_noise_mode, current_noises):
    if ui_current_noises:
        ui_current_noises.hide()
    show_noises(current_noise_mode, current_noises)

def hide_ui():
    if ui_commands:
        ui_commands.hide()
    if ui_current_noises:
        ui_current_noises.hide()
    if ui_noise_modes:
        ui_noise_modes.hide()
    if ui_nav_modes:
        ui_nav_modes.hide()
