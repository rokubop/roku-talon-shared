game_talon = '''\
app: {app_name}
-
settings():
    speech.timeout = 0.10
    key_hold = 64.0
    key_wait = 16.0
    user.game_mouse_calibrate_x_360 = 2139
    user.game_mouse_calibrate_y_90 = 542
'''

game_menu_talon = '''\
app: {app_name}
mode: user.game_menu
-
left:  key("a")
right: key("d")
up:    key("w")
down:  key("s")
play:                       user.game_play_mode_enable()
exit:                       user.game_mode_disable()
'''

game_play_talon = '''\
app: {app_name}
mode: user.game_play
-
exit:                       user.game_mode_disable()

go:                         user.game_wasd_hold_w()
go left:                    user.game_wasd_hold_a()
go right:                   user.game_wasd_hold_d()
[go] back:                  user.game_wasd_hold_s()
step:                       user.game_move_dir_step_w()
step left:                  user.game_move_dir_step_a()
step right:                 user.game_move_dir_step_d()
step back:                  user.game_move_dir_step_s()
jump:                       key("space")
^stop$:                     user.game_stopper()
stop:                       user.game_stopper()
stop all:                   user.game_stop_all()
crouch:                     user.game_key_hold_toggle("ctrl")
run:                        user.game_key_hold_toggle("shift")
hop:                        user.game_jump_forward()
round:                      user.game_mouse_move_deg_180()
^left$:                     user.game_mouse_move_deg_left_90()
^right$:                    user.game_mouse_move_deg_right_90()
left:                       user.game_mouse_move_deg_left_90()
right:                      user.game_mouse_move_deg_right_90()
right one:                  user.game_mouse_move_deg_right_15()
right two:                  user.game_mouse_move_deg_right_30()
right three:                user.game_mouse_move_deg_right_45()
right four:                 user.game_mouse_move_deg_right_60()
right five:                 user.game_mouse_move_deg_right_75()
right six:                  user.game_mouse_move_deg_right_90()
left one:                   user.game_mouse_move_deg_left_15()
left two:                   user.game_mouse_move_deg_left_30()
left three:                 user.game_mouse_move_deg_left_45()
lap four:                   user.game_mouse_move_deg_left_60()
left five:                  user.game_mouse_move_deg_left_75()
left six:                   user.game_mouse_move_deg_left_90()
look up:                    user.game_mouse_move_deg_up_45()
look down:                  user.game_mouse_move_deg_down_45()
look up one:                user.game_mouse_move_deg_up_15()
look up two:                user.game_mouse_move_deg_up_30()
look up three:              user.game_mouse_move_deg_up_45()
look up four:               user.game_mouse_move_deg_up_60()
look up five:               user.game_mouse_move_deg_up_75()
look up six:                user.game_mouse_move_deg_up_90()
look down one:              user.game_mouse_move_deg_down_15()
look down two:              user.game_mouse_move_deg_down_30()
look down three:            user.game_mouse_move_deg_down_45()
look down four:             user.game_mouse_move_deg_down_60()
look down five:             user.game_mouse_move_deg_down_75()
look down six:              user.game_mouse_move_deg_down_90()
set | reset:                user.game_mouse_move_reset_center_y()
calibrate x:                user.game_mode_calibrate_x_enable()
calibrate y:                user.game_mode_calibrate_y_enable()
'''


game_py = '''\
from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.apps.{app_name} = r"""
os: {os}
and {app_context}
"""

ctx.matches = r"""
os: {os}
app: {app_name}
"""

# @mod.action_class
# class Actions:
'''

game_parrot_py = '''\
from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.apps.{app_name} = r"""
os: {os}
and {app_context}
"""

ctx.matches = r"""
os: {os}
app: {app_name}
"""

ctx_game = Context()
ctx_game.matches = r"""
os: windows
app: islandsof_insight
mode: user.game_play
"""

dir = "right"
turn_dir = actions.user.game_mouse_move_continuous_right_30
pop = "go stop"

def toggle_left_right():
    global dir, turn_dir
    if dir == "right":
        dir = "left"
        print("turning left")
        turn_dir = actions.user.game_mouse_move_continuous_left_20
    else:
        dir = "right"
        print("turning right")
        turn_dir = actions.user.game_mouse_move_continuous_right_20

def toggle_x_y():
    global dir, turn_dir
    if dir == "up":
        dir = "down"
        turn_dir = actions.user.game_mouse_move_continuous_down_10
    else:
        dir = "up"
        turn_dir = actions.user.game_mouse_move_continuous_up_10

def toggle_go_or_turn():
    global pop
    if pop == "go":
        pop = "turn"
    else:
        pop = "go"

def pop_action():
    if pop == "go":
        actions.user.game_wasd_toggle_w()
    else:
        toggle_left_right()

parrot_commands = {
    "pop":       ("go stop", actions.user.game_wasd_toggle_w),
    "pop pop":   ("toggle dir", toggle_left_right),
    "pop pop pop": ("toggle dir", toggle_x_y),
    "hiss":      ("turn", lambda: turn_dir()),
    "hiss:stop": ("turn", actions.user.game_mouse_move_continuous_stop),
}

game_config = {
    "mode": "play",
    "color": "222666",
    "commands" : parrot_commands
}

@ctx_game.action_class("user")
class Actions:
    def parrot_config():
        return game_config
'''