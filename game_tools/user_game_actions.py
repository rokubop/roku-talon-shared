from talon import Module, actions
from typing import Any, Union
from .src.game_core import (
    camera_continuous_dynamic,
    camera_snap_dynamic,
    game_gear_set,
    game_key,
    game_key_down,
    game_key_hold,
    game_key_toggle,
    game_key_up,
    game_move_dir_hold_down_horizontal,
    game_move_dir_hold_last_horizontal,
    game_move_dir_hold_up_horizontal,
    game_state_switch_horizontal,
    mouse_calibrate_90_y,
    mouse_calibrate_x_360,
    mouse_click,
    mouse_hold,
    mouse_move_continuous,
    mouse_move_continuous_stop,
    mouse_move_deg,
    mouse_release,
    mouse_release_all,
    mouse_reset_center_y,
    mouse_toggle,
    move_dir,
    move_dir_curve,
    move_dir_toggle,
    move_dir_toggle_last_horizontal,
    step_dir,
    stopper,
)
from .src.game_xbox import (
    xbox_left_analog_hold_dir,
    xbox_right_analog_hold_dir,
    xbox_dpad_hold_dir,
    xbox_set_gear,
    xbox_button_release,
    xbox_button_press,
    xbox_button_hold,
    xbox_button_toggle,
    xbox_trigger_hold,
    xbox_trigger_release,
    xbox_left_stick,
    xbox_right_stick,
    xbox_stopper,
)

mod = Module()

action_duration_ms = 200

@mod.action_class
class Actions:
    def game_key(key: str): """Press a key"""; game_key(key)
    def game_key_down(key: str): """Start holding a key"""; game_key_down(key)
    def game_key_up(key: str): """Release a key"""; game_key_up(key)
    def game_key_hold(key: str, hold_ms: int = None): """Hold a key indefinitely or for a fixed duration e.g. game_key_hold(\"space\", 500)"""; game_key_hold(key, hold_ms)
    def game_key_toggle(key: str): """Toggle holding a key"""; game_key_toggle(key)
    def game_mouse_click(button: int = 0, duration_ms: int = None): """Mouse click; 0=left, 1=right, 2=middle"""; mouse_click(button, duration_ms)
    def game_mouse_click_left(duration_ms: int = None): """Left click"""; mouse_click(0, duration_ms)
    def game_mouse_click_right(duration_ms: int = None): """Right click"""; mouse_click(1, duration_ms)
    def game_mouse_click_middle(duration_ms: int = None): """Middle click"""; mouse_click(2, duration_ms)
    def game_mouse_hold(button: int = 0, duration_ms: int = None): """Mouse hold button indefinitely (None) or specified duration e.g. 500 for half a second; 0=left, 1=right, 2=middle"""; mouse_hold(button, duration_ms)
    def game_mouse_hold_left(duration_ms: int = None): """Hold left click indefinitely (None) or specified duration e.g. 500 for half a second"""; mouse_hold(0, duration_ms)
    def game_mouse_hold_right(duration_ms: int = None): """Hold right click indefinitely (None) or specified duration e.g. 500 for half a second"""; mouse_hold(1, duration_ms)
    def game_mouse_hold_middle(duration_ms: int = None): """Hold middle click indefinitely (None) or specified duration e.g. 500 for half a second"""; mouse_hold(2, duration_ms)
    def game_mouse_down(button: int = 0): """Mouse hold button down; 0=left, 1=right, 2=middle"""; mouse_hold(button)
    def game_mouse_down_left(): """Hold down left click"""; mouse_hold(0)
    def game_mouse_down_right(): """Hold down right click"""; mouse_hold(1)
    def game_mouse_down_middle(): """Hold down middle click"""; mouse_hold(2)
    def game_mouse_up(button: int = 0): """Release mouse button; 0=left, 1=right, 2=middle"""; mouse_release(button)
    def game_mouse_up_left(): """Release left click"""; mouse_release(0)
    def game_mouse_up_right(): """Release right click"""; mouse_release(1)
    def game_mouse_up_middle(): """Release middle click"""; mouse_release(2)
    def game_mouse_up_all(): """Release all mouse buttons"""; mouse_release_all()
    def game_mouse_toggle(button: int = 0): """Toggle holding mouse click; 0=left, 1=right, 2=middle"""; mouse_toggle(button)
    def game_mouse_toggle_left(): """Toggle holding left click"""; mouse_toggle(0)
    def game_mouse_toggle_right(): """Toggle holding right click"""; mouse_toggle(1)
    def game_mouse_toggle_middle(): """Toggle holding middle click"""; mouse_toggle(2)
    def game_move_dir_hold(key: str): """Start holding a custom direction. Mutually exclusive."""; move_dir(key)
    def game_move_dir_hold_a(): """Start holding direction 'a'. Mutually exclusive."""; move_dir('a')
    def game_move_dir_hold_d(): """Start holding direction 'd'. Mutually exclusive."""; move_dir('d')
    def game_move_dir_hold_w(): """Start holding direction 'w'. Mutually exclusive."""; move_dir('w')
    def game_move_dir_hold_s(): """Start holding direction 's'. Mutually exclusive."""; move_dir('s')
    def game_move_dir_hold_a_curved(initial_curve_speed: int = 5): """Start holding direction 'a' with an adjustable curve. Mutually exclusive."""; move_dir_curve('a', initial_curve_speed)
    def game_move_dir_hold_d_curved(initial_curve_speed: int = 5): """Start holding direction 'd' with an adjustable curve. Mutually exclusive."""; move_dir_curve('d', initial_curve_speed)
    def game_move_dir_hold_w_a(): """Start holding direction 'w' and 'a'"""; move_dir(('w', 'a'))
    def game_move_dir_hold_w_d(): """Start holding direction 'w' and 'd'"""; move_dir(('w', 'd'))
    def game_move_dir_hold_s_a(): """Start holding direction 's' and 'a'"""; move_dir(('s', 'a'))
    def game_move_dir_hold_s_d(): """Start holding direction 's' and 'd'"""; move_dir(('s', 'd'))
    def game_move_dir_hold_left(): """Start holding direction 'left'. Mutually exclusive."""; move_dir('left')
    def game_move_dir_hold_right(): """Start holding direction 'right'. Mutually exclusive."""; move_dir('right')
    def game_move_dir_hold_up(): """Start holding direction 'up'. Mutually exclusive."""; move_dir('up')
    def game_move_dir_hold_down(): """Start holding direction 'down'. Mutually exclusive."""; move_dir('down')
    def game_move_dir_hold_up_left(): """Start holding direction 'up' and 'left'"""; move_dir(('up', 'left'))
    def game_move_dir_hold_up_right(): """Start holding direction 'up' and 'right'"""; move_dir(('up', 'right'))
    def game_move_dir_hold_up_horizontal(): """Start holding direction 'up' and last 'left' or 'right'"""; game_move_dir_hold_up_horizontal()
    def game_move_dir_hold_down_left(): """Start holding direction 'down' and 'left'"""; move_dir(('down', 'left'))
    def game_move_dir_hold_down_right(): """Start holding direction 'down' and 'right'"""; move_dir(('down', 'right'))
    def game_move_dir_hold_down_horizontal(): """Start holding direction 'down' and last 'left' or 'right'"""; game_move_dir_hold_down_horizontal()
    def game_move_dir_hold_last_horizontal(): """Start holding the last left or right direction. Mutually exclusive."""; game_move_dir_hold_last_horizontal()
    def game_move_dir_toggle_last_horizontal(): """Toggle between stop and holding the last left or right direction"""; move_dir_toggle_last_horizontal()
    def game_move_dir_toggle(key: str): """Toggle between stop and holding direction"""; move_dir_toggle(key)
    def game_move_dir_toggle_a(): """Toggle between stop and holding direction 'a'"""; move_dir_toggle('a')
    def game_move_dir_toggle_d(): """Toggle between stop and holding direction 'd'"""; move_dir_toggle('d')
    def game_move_dir_toggle_w(): """Toggle between stop and holding direction 'w'"""; move_dir_toggle('w')
    def game_move_dir_toggle_s(): """Toggle between stop and holding direction 's'"""; move_dir_toggle('s')
    def game_move_dir_step_a(duration_ms: int = 200): """Briefly hold direction 'a'"""; step_dir('a', duration_ms)
    def game_move_dir_step_d(duration_ms: int = 200): """Briefly hold direction 'd'"""; step_dir('d', duration_ms)
    def game_move_dir_step_w(duration_ms: int = 200): """Briefly hold direction 'w'"""; step_dir('w', duration_ms)
    def game_move_dir_step_s(duration_ms: int = 200): """Briefly hold direction 's'"""; step_dir('s', duration_ms)
    def game_stopper(): """All purpose stopper for movement and mouse"""; stopper()
    def game_stop_all(): """Stop all movement and mouse actions"""; stopper()
    def game_camera_snap_dynamic(dir: str): """Dynamic action based on current gear/setting. Snap the camera in a direction"""; camera_snap_dynamic(dir)
    # def game_camera_snap_dynamic_set_angle(num: int): """Set angle for game_camera_snap"""; mouse_snap_dynamic(dir)
    def game_camera_continuous_dynamic(dir: str): """Dynamic action based on current gear/setting. Move the camera continuously"""; camera_continuous_dynamic(dir)
    # def game_camera_continuous_dynamic_set_speed(num: int): """Set speed for game_camera_continuous"""; mouse_move_continuous_dy
    def game_turn_left_15(mouse_button: int = None): """Turn left 15 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(-15, 0, mouse_button)
    def game_turn_left_30(mouse_button: int = None): """Turn left 30 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(-30, 0, mouse_button)
    def game_turn_left_45(mouse_button: int = None): """Turn left 45 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(-45, 0, mouse_button)
    def game_turn_left_60(mouse_button: int = None): """Turn left 60 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(-60, 0, mouse_button)
    def game_turn_left_75(mouse_button: int = None): """Turn left 75 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(-75, 0, mouse_button)
    def game_turn_left_90(mouse_button: int = None): """Turn left 90 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(-90, 0, mouse_button)
    def game_turn_left(deg: int = 90, mouse_button: int = None): """Turn left x degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(-deg, 0, mouse_button)
    def game_turn_right_15(mouse_button: int = None): """Turn right 15 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(15, 0, mouse_button)
    def game_turn_right_30(mouse_button: int = None): """Turn right 30 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(30, 0, mouse_button)
    def game_turn_right_45(mouse_button: int = None): """Turn right 45 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(45, 0, mouse_button)
    def game_turn_right_60(mouse_button: int = None): """Turn right 60 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(60, 0, mouse_button)
    def game_turn_right_75(mouse_button: int = None): """Turn right 75 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(75, 0, mouse_button)
    def game_turn_right_90(mouse_button: int = None): """Turn right 90 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(90, 0, mouse_button)
    def game_turn_right(deg: int = 90, mouse_button: int = None): """Turn right x degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(deg, 0, mouse_button)
    def game_turn_right_continuous(speed: int = 20, mouse_button: int = None): """Turn right continuously at speed x; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(1, 0, speed, mouse_button)
    def game_turn_right_continuous_5(mouse_button: int = None): """Turn right continuously speed 5; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(1, 0, 5, mouse_button)
    def game_turn_right_continuous_10(mouse_button: int = None): """Turn right continuously speed 10; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(1, 0, 10, mouse_button)
    def game_turn_right_continuous_20(mouse_button: int = None): """Turn right continuously speed 20; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(1, 0, 20, mouse_button)
    def game_turn_right_continuous_30(mouse_button: int = None): """Turn right continuously speed 30; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(1, 0, 30, mouse_button)
    def game_turn_right_continuous_50(mouse_button: int = None): """Turn right continuously speed 50; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(1, 0, 50, mouse_button)
    def game_turn_right_continuous_100(mouse_button: int = None): """Turn right continuously speed 100; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(1, 0, 100, mouse_button)
    def game_turn_left_continuous(speed: int = 20, mouse_button: int = None): """Turn left continuously at speed x; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(-1, 0, speed, mouse_button)
    def game_turn_left_continuous_5(mouse_button: int = None): """Turn left continuously speed 5; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(-1, 0, 5, mouse_button)
    def game_turn_left_continuous_10(mouse_button: int = None): """Turn left continuously speed 10; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(-1, 0, 10, mouse_button)
    def game_turn_left_continuous_20(mouse_button: int = None): """Turn left continuously speed 20; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(-1, 0, 20, mouse_button)
    def game_turn_left_continuous_30(mouse_button: int = None): """Turn left continuously speed 30; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(-1, 0, 30, mouse_button)
    def game_turn_left_continuous_50(mouse_button: int = None): """Turn left continuously speed 50; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(-1, 0, 50, mouse_button)
    def game_turn_left_continuous_100(mouse_button: int = None): """Turn left continuously speed 100; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(-1, 0, 100, mouse_button)
    def game_turn_continuous_stop(): """Stop turning continuously"""; mouse_move_continuous_stop(150)
    def game_turn_180(mouse_button: int = None): """Turn 180; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(180, 0, mouse_button)
    def game_turn_360(mouse_button: int = None): """Turn 360; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(360, 0, 1500)
    def game_look_up_continuous(speed: int = 10, mouse_button: int = None): """Look up continuously at speed x"""; mouse_move_continuous(0, -1, speed, mouse_button)
    def game_look_up_continuous_5(mouse_button: int = None): """Look up continuously speed 5"""; mouse_move_continuous(0, -1, 5, mouse_button)
    def game_look_up_continuous_10(mouse_button: int = None): """Look up continuously speed 10"""; mouse_move_continuous(0, -1, 10, mouse_button)
    def game_look_up_continuous_20(mouse_button: int = None): """Look up continuously speed 20"""; mouse_move_continuous(0, -1, 20, mouse_button)
    def game_look_up_continuous_30(mouse_button: int = None): """Look up continuously speed 30"""; mouse_move_continuous(0, -1, 30, mouse_button)
    def game_look_up_continuous_50(mouse_button: int = None): """Look up continuously speed 50"""; mouse_move_continuous(0, -1, 50, mouse_button)
    def game_look_up_continuous_100(mouse_button: int = None): """Look up continuously speed 100"""; mouse_move_continuous(0, -1, 100, mouse_button)
    def game_look_down_continuous(speed: int = 10, mouse_button: int = None): """Look down continuously at speed x"""; mouse_move_continuous(0, 1, speed, mouse_button)
    def game_look_down_continuous_5(mouse_button: int = None): """Look down continuously speed 5"""; mouse_move_continuous(0, 1, 5, mouse_button)
    def game_look_down_continuous_10(mouse_button: int = None): """Look down continuously speed 10"""; mouse_move_continuous(0, 1, 10, mouse_button)
    def game_look_down_continuous_20(mouse_button: int = None): """Look down continuously speed 20"""; mouse_move_continuous(0, 1, 20, mouse_button)
    def game_look_down_continuous_30(mouse_button: int = None): """Look down continuously speed 30"""; mouse_move_continuous(0, 1, 30, mouse_button)
    def game_look_down_continuous_50(mouse_button: int = None): """Look down continuously speed 50"""; mouse_move_continuous(0, 1, 50, mouse_button)
    def game_look_down_continuous_100(mouse_button: int = None): """Look down continuously speed 100"""; mouse_move_continuous(0, 1, 100, mouse_button)
    def game_look_continuous_stop(): """Stop looking continuously"""; mouse_move_continuous_stop(150)
    def game_look_up_15(mouse_button: int = None): """Look up 15 degrees"""; mouse_move_deg(0, -15)
    def game_look_up_30(mouse_button: int = None): """Look up 30 degrees"""; mouse_move_deg(0, -30)
    def game_look_up_45(mouse_button: int = None): """Look up 45 degrees"""; mouse_move_deg(0, -45)
    def game_look_up_60(mouse_button: int = None): """Look up 60 degrees"""; mouse_move_deg(0, -60)
    def game_look_up_75(mouse_button: int = None): """Look up 75 degrees"""; mouse_move_deg(0, -75)
    def game_look_up_90(mouse_button: int = None): """Look up 90 degrees"""; mouse_move_deg(0, -90)
    def game_look_up(deg: int = 20, mouse_button: int = None): """Look up y degrees"""; mouse_move_deg(0, -deg)
    def game_look_down_15(mouse_button: int = None): """Look down 15 degrees"""; mouse_move_deg(0, 15)
    def game_look_down_30(mouse_button: int = None): """Look down 30 degrees"""; mouse_move_deg(0, 30)
    def game_look_down_45(mouse_button: int = None): """Look down 45 degrees"""; mouse_move_deg(0, 45)
    def game_look_down_60(mouse_button: int = None): """Look down 60 degrees"""; mouse_move_deg(0, 60)
    def game_look_down_75(mouse_button: int = None): """Look down 75 degrees"""; mouse_move_deg(0, 75)
    def game_look_down_90(mouse_button: int = None): """Look down 90 degrees"""; mouse_move_deg(0, 90)
    def game_look_down(deg: int = 20, mouse_button: int = None): """Look down y degrees"""; mouse_move_deg(0, deg, mouse_button)
    def game_gear_set(gear_num: int): """Set gear for current/last action. For dynamic actions."""; game_gear_set(gear_num)
    def game_reset_center_y(mouse_button: int = None): """Reset the mouse to the center of the screen"""; mouse_reset_center_y()
    def game_state_switch_horizontal(): """Switch state value of horizontal"""; game_state_switch_horizontal()
    def game_calibrate_x_360(num: int, mouse_button: int = None): """Calibrate x by testing a 360"""; mouse_calibrate_x_360(num)
    def game_calibrate_y_90(num: int, mouse_button: int = None): """Calibrate y by testing ground to center"""; mouse_calibrate_90_y(num)
    # xbox gamepad actions
    def game_xbox_gamepad_enable(): """Enable xbox gamepad actions. Enables vgamepad. Windows and Linux only."""; actions.user.vgamepad_enable()
    def game_xbox_gamepad_disable(): """Disable xbox gamepad actions. Disables vgamepad."""; actions.user.vgamepad_disable()
    def game_xbox_button_press(button: str, hold: int = None):
        """
        Press an xbox button

        **buttons**:  a, b, x, y, left_shoulder, right_shoulder, left_thumb, right_thumb, start, back, guide, dpad_up, dpad_down, dpad_left, dpad_right

        **button aliases**: lb, rb, lt, rt, l1, r1, l2, r2, l3, r3
        """
        xbox_button_press(button, hold)
    def game_xbox_button_release(button: str): """Release an xbox button"""; xbox_button_release(button)
    def game_xbox_button_hold(button: str, hold_ms: int = None):
        """Hold an xbox button indefinitely or for a fixed duration.

        **buttons**:  a, b, x, y, left_shoulder, right_shoulder, left_thumb, right_thumb, start, back, guide, dpad_up, dpad_down, dpad_left, dpad_right

        **button aliases**: lb, rb, lt, rt, l1, r1, l2, r2, l3, r3
        """
        xbox_button_hold(button, hold_ms)
    def game_xbox_button_toggle(button: str):
        """
        Toggle holding an xbox button

        **buttons**:  a, b, x, y, left_shoulder, right_shoulder, left_thumb, right_thumb, start, back, guide, dpad_up, dpad_down, dpad_left, dpad_right

        **button aliases**: lb, rb, lt, rt, l1, r1, l2, r2, l3, r3
        """
        xbox_button_toggle(button)
    def game_xbox_left_stick_hold_dir(dir: str, power: float = None): """Hold left stick dir up down left right"""; xbox_left_analog_hold_dir(dir, power)
    def game_xbox_left_stick_set_gear(gear: Union[int, str]): """Set left stick gear from 1 to 5"""; xbox_set_gear("left_stick", gear)
    def game_xbox_left_stick_stop(): """Stop holding left stick"""; xbox_left_stick(0, 0)
    def game_xbox_right_stick_hold_dir(dir: str, power: float = None): """Hold right stick dir up down left right"""; xbox_right_analog_hold_dir(dir, power)
    def game_xbox_right_stick_set_gear(gear: Union[int, str]): """Set right stick gear from 1 to 5"""; xbox_set_gear("right_stick", gear)
    def game_xbox_right_stick_stop(): """Stop holding right stick"""; xbox_right_stick(0, 0)
    def game_xbox_dpad_press_dir(dir: str): """up, down, left, right"""; xbox_button_press(f"dpad_{dir}")
    def game_xbox_dpad_hold_only_dir(dir: str): """Hold dpad dir up, down, left, right"""; xbox_dpad_hold_dir(dir)
    def game_xbox_left_trigger(power: float = None): """Press the left trigger (LT)"""; xbox_button_press("left_trigger")
    def game_xbox_left_trigger_hold(power: float = None): """Hold the left trigger (LT)"""; xbox_trigger_hold("left_trigger", power)
    def game_xbox_left_trigger_release(): """Release the left trigger (LT)"""; xbox_trigger_release("left_trigger")
    def game_xbox_right_trigger_set_gear(gear: Union[int, str]): """Set right trigger gear from 1 to 5"""; xbox_set_gear("right_trigger", gear)
    def game_xbox_right_trigger(power: float = None): """Press the right trigger (LT)"""; xbox_button_press("right_trigger")
    def game_xbox_right_trigger_hold(power: float = None): """Hold the right trigger (LT)"""; xbox_trigger_hold("right_trigger", power)
    def game_xbox_right_trigger_release(): """Release the right trigger (LT)"""; xbox_trigger_release("right_trigger")
    def game_xbox_left_trigger_set_gear(gear: Union[int, str]): """Set left trigger gear from 1 to 5"""; xbox_set_gear("left_trigger", gear)
    def game_xbox_stopper(): """General stopper based on priority for xbox actions"""; xbox_stopper()