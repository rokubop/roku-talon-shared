# from talon import Module, Context, actions

# mod = Module()
# ctx = Context()

# mod.apps.talos_2 = r"""
# os: windows
# and app.exe: Talos2-Win64-Shipping.exe
# """

# ctx.matches = r"""
# os: windows
# app: talos_2
# """

# mod.mode("game_talos_2_parrot", "Parrot mode for talos 2 game")

# @mod.action_class
# class Actions:
#     def game_v2_talos_2_game_parrot_mode_enable(ev: dict):
#         """Enter game mode"""
#         actions.mode.disable("command")
#         actions.mode.enable("user.game_talos_2_parrot")
#         actions.user.game_v2_canvas_box_color("222666")
#         actions.user.game_v2_canvas_status_enable()
#         actions.user.game_v2_canvas_status_update("mode", "game")

#     def game_v2_talos_2_game_parrot_mode_disable(ev: dict):
#         """Enter game mode"""
#         actions.user.event_mouse_move_stop_hard()
#         actions.user.game_v2_stop_all()
#         actions.mode.disable("user.game_talos_2_parrot")
#         actions.user.game_v2_canvas_status_disable()
#         actions.mode.enable("command")

# @ctx.action_class("user")
# class Actions:
#     def on_parrot_v5_mode_enable(ev: dict):
#         actions.user.game_v2_canvas_box_color("ff0000")
#         actions.user.game_v2_canvas_status_enable()
#         actions.user.game_v2_canvas_status_update("mode", "parrot global")
#         actions.next()

#     def on_parrot_v5_mode_disable(ev: dict):
#         actions.user.game_v2_canvas_status_disable()
#         actions.next()
