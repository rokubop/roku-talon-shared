from talon import Module, actions

mod = Module()

game_settings_show = False
accent_color = "ffdb58"
accent_color_button = "A08607"
accent_color_text_button = "FFFFFF"

def body():
    (div, text, button, state) = actions.user.ui_elements(["div", "text", "button", "state"])
    active_tab = state("active_tab")

    def text_setting(label, value):
        """Text setting"""
        return div(flex_direction="row", background_color="333333", align_items="center", gap=8, margin_top=8, margin_bottom=8)[
            text(f"{label}:", margin_right=8),
            text(value, color=accent_color),
        ]

    def choice_setting(label, choices):
        """Choice setting"""
        return div(flex_direction="row", background_color="333333", align_items="center", gap=8, margin_top=8, margin_bottom=8)[
            text(f"{label}:", margin_right=8),
            *(button(
                choice["value"],
                color=accent_color_text_button if choice["active"] else "CCCCCC",
                background_color=accent_color_button if choice["active"] else "444444",
                border_radius=4) for choice in choices
            ),

        ]

    if active_tab == "game_settings":
        return div()[
            text_setting("Game", '"Celeste"'),
            text_setting("speech.timeout", "0.05"),
            text_setting("key_hold", "64.0"),
            text_setting("key_wait", "0.0"),
            text_setting("user.game_key_repeat_wait", "16.0"),
            text_setting("user.mouse_move_api", '"windows"'),
            text_setting("user.mouse_move_continuous_speed_default", "6"),
            choice_setting("Input type", [
                {"value": "KB/M", "active": True},
                {"value": "Xbox gamepad", "active": False},
            ]),
            choice_setting("Something", [
                {"value": "Yes", "active": True},
                {"value": "No", "active": False},
            ]),
        ]

    return div()[text("Test", color="FF0000")]

@mod.action_class
class Actions:
    def game_settings():
        """Game Settings"""
        global game_settings_show

        if game_settings_show:
            actions.user.ui_elements_hide_all()
            game_settings_show = False
            return

        game_settings_show = True

        # def ui():
        #     elements = ["screen", "div", "button", "state", "window", "input"]
        #     (screen, div, button, state, window, input) = actions.user.ui_elements(elements)

        #     active_tab = state("active_tab", "game_settings")

        #     tabs_names = ["Game Settings", "Eye tracking", "Mouse", "Actions", "Noises", "Face actions"]
        #     tabs = [{
        #         "name": button_name,
        #         "active": True if active_tab == button_name.lower().replace(" ", "_") else False,
        #     } for button_name in tabs_names]

        #     def test(name):
        #         print(f'clicked {name}')
        #         actions.user.ui_elements_set_state("active_tab", name)

        #     return screen(justify_content="center", align_items="center")[
        #         window(flex_direction="column", background_color="333333")[
        #             div(background_color="444444", width=800, flex_direction="row", gap=2)[
        #                 *(button(tab["name"],
        #                     color=accent_color_text_button if tab["active"] else "CCCCCC",
        #                     background_color=accent_color_button if tab["active"] else "444444",
        #                     border_color="333333",
        #                     border_width=1,
        #                     on_click=lambda tab_name=tab["name"]: test(tab_name.lower().replace(" ", "_")))
        #                 for tab in tabs),
        #             ],
        #             div(flex_direction="column", width=800, height=250, padding=16, gap=4)[
        #                 body(),
        #                 # input(id="input"),
        #             ],
        #             div(flex_direction="row", gap=8, margin_top=8, background_color="444444", width=800)[
        #                 button("Save", padding=16),
        #                 button("Cancel", padding=16),
        #             ],
        #         ]
        #     ]