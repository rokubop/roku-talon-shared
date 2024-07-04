from talon import Module, actions, ctrl
from .src.game_core import (
    move_dir,
    step_dir,
    move_dir_toggle,
    stopper,
    mouse_calibrate_90_y,
    mouse_calibrate_x_360,
    game_move_dir_hold_last_horizontal,
    move_dir_toggle_last_horizontal,
    mouse_reset_center_y,
    game_key,
    game_key_down,
    game_key_up,
    game_key_hold,
    game_key_toggle,
    game_move_dir_hold_up_horizontal,
    game_move_dir_hold_down_horizontal,
    game_state_switch_horizontal,
)

mod = Module()

action_duration_ms = 200

def mouse_move_deg(deg_x: int, deg_y: int):
    actions.user.mouse_move_delta_degrees(deg_x, deg_y, action_duration_ms, mouse_api_type="windows")

@mod.action_class
class Actions:
    def game_key(key: str): """Press a key"""; game_key(key)
    def game_key_down(key: str): """Start holding a key"""; game_key_down(key)
    def game_key_up(key: str): """Release a key"""; game_key_up(key)
    def game_key_hold(key: str, hold: int = None): """Hold a key"""; game_key_hold(key, hold)
    def game_key_toggle(key: str): """Toggle holding a key"""; game_key_toggle(key)
    def game_mouse_click(button: int = 0, hold: int = 16000): """Click"""; ctrl.mouse_click(button=button, hold=hold)
    def game_mouse_click_left(hold: int = 16000): """Left click"""; ctrl.mouse_click(button=0, hold=hold)
    def game_mouse_click_right(hold: int = 16000): """Right click"""; ctrl.mouse_click(button=1, hold=hold)
    def game_mouse_click_middle(hold: int = 16000): """Middle click"""; ctrl.mouse_click(button=2, hold=hold)
    def game_mouse_hold_left(duration_ms: int = None): """Hold left click"""; ctrl.mouse_click(button=0, hold=duration_ms*1000) if duration_ms else ctrl.mouse_click(button=0, down=True)
    def game_mouse_hold_right(duration_ms: int = None): """Hold right click"""; ctrl.mouse_click(button=1, hold=duration_ms*1000) if duration_ms else ctrl.mouse_click(button=1, down=True)
    def game_mouse_hold_middle(duration_ms: int = None): """Hold middle click"""; ctrl.mouse_click(button=2, hold=duration_ms*1000) if duration_ms else ctrl.mouse_click(button=2, down=True)
    def game_move_dir_hold_a(): """Start holding direction 'a'"""; move_dir('a')
    def game_move_dir_hold_d(): """Start holding direction 'd'"""; move_dir('d')
    def game_move_dir_hold_w(): """Start holding direction 'w'"""; move_dir('w')
    def game_move_dir_hold_s(): """Start holding direction 's'"""; move_dir('s')
    def game_move_dir_hold_w_a(): """Start holding direction 'w' and 'a'"""; move_dir(('w', 'a'))
    def game_move_dir_hold_w_d(): """Start holding direction 'w' and 'd'"""; move_dir(('w', 'd'))
    def game_move_dir_hold_s_a(): """Start holding direction 's' and 'a'"""; move_dir(('s', 'a'))
    def game_move_dir_hold_s_d(): """Start holding direction 's' and 'd'"""; move_dir(('s', 'd'))
    def game_move_dir_hold_left(): """Start holding direction 'left'"""; move_dir('left')
    def game_move_dir_hold_right(): """Start holding direction 'right'"""; move_dir('right')
    def game_move_dir_hold_up(): """Start holding direction 'up'"""; move_dir('up')
    def game_move_dir_hold_down(): """Start holding direction 'down'"""; move_dir('down')
    def game_move_dir_hold_up_left(): """Start holding direction 'up' and 'left'"""; move_dir(('up', 'left'))
    def game_move_dir_hold_up_right(): """Start holding direction 'up' and 'right'"""; move_dir(('up', 'right'))
    def game_move_dir_hold_up_horizontal(): """Start holding direction 'up' and last 'left' or 'right'"""; game_move_dir_hold_up_horizontal()
    def game_move_dir_hold_down_left(): """Start holding direction 'down' and 'left'"""; move_dir(('down', 'left'))
    def game_move_dir_hold_down_right(): """Start holding direction 'down' and 'right'"""; move_dir(('down', 'right'))
    def game_move_dir_hold_down_horizontal(): """Start holding direction 'down' and last 'left' or 'right'"""; game_move_dir_hold_down_horizontal()
    def game_move_dir_hold_last_horizontal(): """Start holding the last left or right direction"""; game_move_dir_hold_last_horizontal()
    def game_move_dir_toggle_last_horizontal(): """Toggle between stop and holding the last left or right direction"""; move_dir_toggle_last_horizontal()
    def game_move_dir_toggle_a(): """Toggle between stop and holding direction 'a'"""; move_dir_toggle('a')
    def game_move_dir_toggle_d(): """Toggle between stop and holding direction 'd'"""; move_dir_toggle('d')
    def game_move_dir_toggle_w(): """Toggle between stop and holding direction 'w'"""; move_dir_toggle('w')
    def game_move_dir_toggle_s(): """Toggle between stop and holding direction 's'"""; move_dir_toggle('s')
    def game_move_dir_step_a(): """Briefly hold direction 'a'"""; step_dir('a', '200ms')
    def game_move_dir_step_d(): """Briefly hold direction 'd'"""; step_dir('d', '200ms')
    def game_move_dir_step_w(): """Briefly hold direction 'w'"""; step_dir('w', '200ms')
    def game_move_dir_step_s(): """Briefly hold direction 's'"""; step_dir('s', '200ms')
    def game_stopper(): """All purpose stopper for movement and mouse"""; stopper()
    def game_stop_all(): """Stop all movement and mouse actions"""; stopper()
    def game_turn_left_15(): """Turn left 15 degrees"""; mouse_move_deg(-15, 0)
    def game_turn_left_30(): """Turn left 30 degrees"""; mouse_move_deg(-30, 0)
    def game_turn_left_45(): """Turn left 45 degrees"""; mouse_move_deg(-45, 0)
    def game_turn_left_60(): """Turn left 60 degrees"""; mouse_move_deg(-60, 0)
    def game_turn_left_75(): """Turn left 75 degrees"""; mouse_move_deg(-75, 0)
    def game_turn_left_90(): """Turn left 90 degrees"""; mouse_move_deg(-90, 0)
    def game_turn_left(deg: int): """Turn left x degrees"""; mouse_move_deg(-deg, 0 )
    def game_turn_right_15(): """Turn right 15 degrees"""; mouse_move_deg(15, 0)
    def game_turn_right_30(): """Turn right 30 degrees"""; mouse_move_deg(30, 0)
    def game_turn_right_45(): """Turn right 45 degrees"""; mouse_move_deg(45, 0)
    def game_turn_right_60(): """Turn right 60 degrees"""; mouse_move_deg(60, 0)
    def game_turn_right_75(): """Turn right 75 degrees"""; mouse_move_deg(75, 0)
    def game_turn_right_90(): """Turn right 90 degrees"""; mouse_move_deg(90, 0)
    def game_turn_right(deg: int): """Turn right x degrees"""; mouse_move_deg(deg, 0 )
    def game_turn_right_continuous(speed: int): """Turn right continuously at speed x"""; actions.user.mouse_move_continuous(1, 0, speed)
    def game_turn_right_continuous_5(): """Turn right continuously speed 5"""; actions.user.mouse_move_continuous(1, 0, 5)
    def game_turn_right_continuous_10(): """Turn right continuously speed 10"""; actions.user.mouse_move_continuous(1, 0, 10)
    def game_turn_right_continuous_20(): """Turn right continuously speed 20"""; actions.user.mouse_move_continuous(1, 0, 20)
    def game_turn_right_continuous_30(): """Turn right continuously speed 30"""; actions.user.mouse_move_continuous(1, 0, 30)
    def game_turn_right_continuous_50(): """Turn right continuously speed 50"""; actions.user.mouse_move_continuous(1, 0, 50)
    def game_turn_right_continuous_100(): """Turn right continuously speed 100"""; actions.user.mouse_move_continuous(1, 0, 100)
    def game_turn_left_continuous(speed: int): """Turn left continuously at speed x"""; actions.user.mouse_move_continuous(-1, 0, speed)
    def game_turn_left_continuous_5(): """Turn left continuously speed 5"""; actions.user.mouse_move_continuous(-1, 0, 5)
    def game_turn_left_continuous_10(): """Turn left continuously speed 10"""; actions.user.mouse_move_continuous(-1, 0, 10)
    def game_turn_left_continuous_20(): """Turn left continuously speed 20"""; actions.user.mouse_move_continuous(-1, 0, 20)
    def game_turn_left_continuous_30(): """Turn left continuously speed 30"""; actions.user.mouse_move_continuous(-1, 0, 30)
    def game_turn_left_continuous_50(): """Turn left continuously speed 50"""; actions.user.mouse_move_continuous(-1, 0, 50)
    def game_turn_left_continuous_100(): """Turn left continuously speed 100"""; actions.user.mouse_move_continuous(-1, 0, 100)
    def game_look_up_continuous(speed: int): """Look up continuously at speed x"""; actions.user.mouse_move_continuous(0, -1, speed)
    def game_look_up_continuous_5(): """Look up continuously speed 5"""; actions.user.mouse_move_continuous(0, -1, 5)
    def game_look_up_continuous_10(): """Look up continuously speed 10"""; actions.user.mouse_move_continuous(0, -1, 10)
    def game_look_up_continuous_20(): """Look up continuously speed 20"""; actions.user.mouse_move_continuous(0, -1, 20)
    def game_look_up_continuous_30(): """Look up continuously speed 30"""; actions.user.mouse_move_continuous(0, -1, 30)
    def game_look_up_continuous_50(): """Look up continuously speed 50"""; actions.user.mouse_move_continuous(0, -1, 50)
    def game_look_up_continuous_100(): """Look up continuously speed 100"""; actions.user.mouse_move_continuous(0, -1, 100)
    def game_look_down_continuous(speed: int): """Look down continuously at speed x"""; actions.user.mouse_move_continuous(0, 1, speed)
    def game_look_down_continuous_5(): """Look down continuously speed 5"""; actions.user.mouse_move_continuous(0, 1, 5)
    def game_look_down_continuous_10(): """Look down continuously speed 10"""; actions.user.mouse_move_continuous(0, 1, 10)
    def game_look_down_continuous_20(): """Look down continuously speed 20"""; actions.user.mouse_move_continuous(0, 1, 20)
    def game_look_down_continuous_30(): """Look down continuously speed 30"""; actions.user.mouse_move_continuous(0, 1, 30)
    def game_look_down_continuous_50(): """Look down continuously speed 50"""; actions.user.mouse_move_continuous(0, 1, 50)
    def game_look_down_continuous_100(): """Look down continuously speed 100"""; actions.user.mouse_move_continuous(0, 1, 100)
    def game_turn_continuous_stop(): """Stop turning left continuously"""; actions.user.mouse_move_continuous_stop(150)
    def game_turn_180(): """Turn 180"""; mouse_move_deg(180, 0)
    def game_turn_360(): """Turn 360"""; mouse_move_deg(360, 0, 1500)
    def game_look_up_15(): """Look up 15 degrees"""; mouse_move_deg(0, -15)
    def game_look_up_30(): """Look up 30 degrees"""; mouse_move_deg(0, -30)
    def game_look_up_45(): """Look up 45 degrees"""; mouse_move_deg(0, -45)
    def game_look_up_60(): """Look up 60 degrees"""; mouse_move_deg(0, -60)
    def game_look_up_75(): """Look up 75 degrees"""; mouse_move_deg(0, -75)
    def game_look_up_90(): """Look up 90 degrees"""; mouse_move_deg(0, -90)
    def game_look_up(deg: int): """Look up y degrees"""; mouse_move_deg(0, -deg)
    def game_look_down_15(): """Look down 15 degrees"""; mouse_move_deg(0, 15)
    def game_look_down_30(): """Look down 30 degrees"""; mouse_move_deg(0, 30)
    def game_look_down_45(): """Look down 45 degrees"""; mouse_move_deg(0, 45)
    def game_look_down_60(): """Look down 60 degrees"""; mouse_move_deg(0, 60)
    def game_look_down_75(): """Look down 75 degrees"""; mouse_move_deg(0, 75)
    def game_look_down_90(): """Look down 90 degrees"""; mouse_move_deg(0, 90)
    def game_look_down(deg: int): """Look down y degrees"""; mouse_move_deg(0, deg)
    def game_reset_center_y(): """Reset the mouse to the center of the screen"""; mouse_reset_center_y()
    def game_state_switch_horizontal(): """Switch state value of horizontal"""; game_state_switch_horizontal()
    def game_calibrate_x_360(num: int): """Calibrate the mouse for x movement in degrees"""; mouse_calibrate_x_360(num)
    def game_calibrate_y_90(num: int): """Calibrate the mouse for y movement in degrees"""; mouse_calibrate_90_y(num)