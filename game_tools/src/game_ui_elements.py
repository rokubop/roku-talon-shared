# def game_ui_elements_arrows_dpad():
#     (css, div, text, screen) = actions.user.ui_elements(["css", "div", "text", "screen"])

#     screen_css = css(
#         id="keys",
#         justify_content="flex_end",
#         align_items="flex_start",
#         highlight_color=f"{accent_color}88"
#     )

#     gamepad_css = css(
#         flex_direction="row",
#         gap=8,
#         margin_bottom=16,
#         margin_left=16
#     )

#     key_css = css(
#         padding=8,
#         background_color="333333dd",
#         flex_direction="row",
#         justify_content="center",
#         align_items="center",
#         margin=1,
#         width=30,
#         height=30
#     )

#     def key(key_name, text_content, width=30):
#         return div(key_css, id=key_name, width=width)[
#             text(text_content)
#         ]

#     def blank_key():
#         return div(key_css, background_color="33333355")[text(" ")]

#     def row():
#         return div(flex_direction="row")

#     return div(flex_direction="column")[
#         row()[blank_key(), key("up", "↑"), blank_key()],
#         row()[key("left", "←"), key("down", "↓"), key("right", "→")]
#     ]