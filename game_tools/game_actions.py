from talon import Module
from .src.game_core import (
    camera_continuous_dynamic,
    camera_snap_dynamic,
    game_key,
    game_key_hold,
    game_key_hold,
    game_key_toggle,
    game_key_release,
    game_key_sequence,
    game_arrows_hold_down_horizontal,
    game_dir_hold_last_horizontal,
    game_arrows_hold_up_horizontal,
    game_state_switch_horizontal,
    game_calibrate_90_y,
    game_mouse_calibrate_x_360,
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
    stopper,
)

mod = Module()

@mod.action_class
class Actions:
    def game_key(key: str): """Press a key"""; game_key(key)
    def game_key_hold(key: str, hold_ms: int = None): """Hold a key indefinitely or for a fixed duration e.g. game_key_hold(\"space\", 500)"""; game_key_hold(key, hold_ms)
    def game_key_release(key: str): """Release a key"""; game_key_release(key)
    def game_key_toggle(key: str): """Toggle holding a key"""; game_key_toggle(key)
    def game_key_sequence(keys: str, delay_ms: int = None): """Press a sequence of keys with a delay between each"""; game_key_sequence(keys, delay_ms)
    def game_mouse_click(button: int = 0): """Mouse click; 0=left, 1=right, 2=middle"""; mouse_click(button)
    def game_mouse_click_left(): """Left click"""; mouse_click(0)
    def game_mouse_click_right(): """Right click"""; mouse_click(1)
    def game_mouse_click_middle(): """Middle click"""; mouse_click(2)
    def game_mouse_hold(button: int = 0, hold_ms: int = None): """Mouse hold button indefinitely (None) or specified duration e.g. 500 for half a second; 0=left, 1=right, 2=middle"""; mouse_hold(button, hold_ms)
    def game_mouse_hold_left(hold_ms: int = None): """Hold left click indefinitely (None) or specified duration e.g. 500 for half a second"""; mouse_hold(0, hold_ms)
    def game_mouse_hold_right(hold_ms: int = None): """Hold right click indefinitely (None) or specified duration e.g. 500 for half a second"""; mouse_hold(1, hold_ms)
    def game_mouse_hold_middle(hold_ms: int = None): """Hold middle click indefinitely (None) or specified duration e.g. 500 for half a second"""; mouse_hold(2, hold_ms)
    def game_mouse_release(button: int = 0): """Release mouse button; 0=left, 1=right, 2=middle"""; mouse_release(button)
    def game_mouse_release_left(): """Release left click"""; mouse_release(0)
    def game_mouse_release_right(): """Release right click"""; mouse_release(1)
    def game_mouse_release_middle(): """Release middle click"""; mouse_release(2)
    def game_mouse_release_all(): """Release all mouse buttons"""; mouse_release_all()
    def game_mouse_toggle(button: int = 0): """Toggle holding mouse click; 0=left, 1=right, 2=middle"""; mouse_toggle(button)
    def game_mouse_toggle_left(): """Toggle holding left click"""; mouse_toggle(0)
    def game_mouse_toggle_right(): """Toggle holding right click"""; mouse_toggle(1)
    def game_mouse_toggle_middle(): """Toggle holding middle click"""; mouse_toggle(2)
    def game_wasd_hold(key: str): """Start holding a wasd key. Mutually exclusive."""; move_dir(key)
    def game_wasd_hold_a(): """Start holding direction 'a'. Mutually exclusive."""; move_dir('a')
    def game_wasd_hold_d(): """Start holding direction 'd'. Mutually exclusive."""; move_dir('d')
    def game_wasd_hold_w(): """Start holding direction 'w'. Mutually exclusive."""; move_dir('w')
    def game_wasd_hold_s(): """Start holding direction 's'. Mutually exclusive."""; move_dir('s')
    def game_wasd_hold_a_curved(speed_curve: int = None): """Start holding direction 'a' with a mouse curve. Mutually exclusive."""; move_dir_curve('a', speed_curve)
    def game_wasd_hold_d_curved(speed_curve: int = None): """Start holding direction 'd' with a mouse curve. Mutually exclusive."""; move_dir_curve('d', speed_curve)
    def game_wasd_hold_w_a(): """Start holding direction 'w' and 'a'"""; move_dir(('w', 'a'))
    def game_wasd_hold_w_d(): """Start holding direction 'w' and 'd'"""; move_dir(('w', 'd'))
    def game_wasd_hold_s_a(): """Start holding direction 's' and 'a'"""; move_dir(('s', 'a'))
    def game_wasd_hold_s_d(): """Start holding direction 's' and 'd'"""; move_dir(('s', 'd'))
    def game_wasd_toggle(key: str): """Toggle between stop and holding direction"""; move_dir_toggle(key)
    def game_wasd_toggle_a(): """Toggle between stop and holding direction 'a'"""; move_dir_toggle('a')
    def game_wasd_toggle_d(): """Toggle between stop and holding direction 'd'"""; move_dir_toggle('d')
    def game_wasd_toggle_w(): """Toggle between stop and holding direction 'w'"""; move_dir_toggle('w')
    def game_wasd_toggle_s(): """Toggle between stop and holding direction 's'"""; move_dir_toggle('s')
    def game_arrows_hold(key: str): """Start holding left up right or down. Mutually exclusive."""; move_dir(key)
    def game_arrows_hold_left(): """Start holding direction 'left'. Mutually exclusive."""; move_dir('left')
    def game_arrows_hold_right(): """Start holding direction 'right'. Mutually exclusive."""; move_dir('right')
    def game_arrows_hold_up(): """Start holding direction 'up'. Mutually exclusive."""; move_dir('up')
    def game_arrows_hold_down(): """Start holding direction 'down'. Mutually exclusive."""; move_dir('down')
    def game_arrows_hold_up_left(): """Start holding direction 'up' and 'left'"""; move_dir(('up', 'left'))
    def game_arrows_hold_up_right(): """Start holding direction 'up' and 'right'"""; move_dir(('up', 'right'))
    def game_arrows_hold_up_horizontal(): """Start holding direction 'up' and last 'left' or 'right'"""; game_arrows_hold_up_horizontal()
    def game_arrows_hold_down_left(): """Start holding direction 'down' and 'left'"""; move_dir(('down', 'left'))
    def game_arrows_hold_down_right(): """Start holding direction 'down' and 'right'"""; move_dir(('down', 'right'))
    def game_arrows_hold_down_horizontal(): """Start holding direction 'down' and last 'left' or 'right'"""; game_arrows_hold_down_horizontal()
    def game_dir_hold_last_horizontal(): """Start holding the last left or right direction. Mutually exclusive."""; game_dir_hold_last_horizontal()
    def game_dir_toggle_last_horizontal(): """Toggle between stop and holding the last left or right direction"""; move_dir_toggle_last_horizontal()
    def game_stopper(): """All purpose stopper for movement and mouse"""; stopper()
    def game_stop_all(): """Stop all movement and mouse actions"""; stopper()
    def game_mouse_move_deg_dynamic(dir: str): """Dynamic action based on current gear/setting. Snap the camera in a direction"""; camera_snap_dynamic(dir)
    def game_mouse_move_continuous_dynamic(dir: str): """Dynamic action based on current gear/setting. Move the camera continuously"""; camera_continuous_dynamic(dir)
    def game_mouse_move_deg_left_15(mouse_button: int = None): """Turn left 15 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(-15, 0, mouse_button)
    def game_mouse_move_deg_left_30(mouse_button: int = None): """Turn left 30 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(-30, 0, mouse_button)
    def game_mouse_move_deg_left_45(mouse_button: int = None): """Turn left 45 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(-45, 0, mouse_button)
    def game_mouse_move_deg_left_90(mouse_button: int = None): """Turn left 90 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(-90, 0, mouse_button)
    def game_mouse_move_deg_left(deg: int = 90, mouse_button: int = None): """Turn left x degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(-deg, 0, mouse_button)
    def game_mouse_move_deg_right_15(mouse_button: int = None): """Turn right 15 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(15, 0, mouse_button)
    def game_mouse_move_deg_right_30(mouse_button: int = None): """Turn right 30 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(30, 0, mouse_button)
    def game_mouse_move_deg_right_45(mouse_button: int = None): """Turn right 45 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(45, 0, mouse_button)
    def game_mouse_move_deg_right_90(mouse_button: int = None): """Turn right 90 degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(90, 0, mouse_button)
    def game_mouse_move_deg_right(deg: int = 90, mouse_button: int = None): """Turn right x degrees; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(deg, 0, mouse_button)
    def game_mouse_move_deg_180(mouse_button: int = None): """Turn 180; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(180, 0, mouse_button)
    def game_mouse_move_deg_360(mouse_button: int = None): """Turn 360; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_deg(360, 0, 1500)
    def game_mouse_move_deg_up_15(mouse_button: int = None): """Look up 15 degrees"""; mouse_move_deg(0, -15)
    def game_mouse_move_deg_up_30(mouse_button: int = None): """Look up 30 degrees"""; mouse_move_deg(0, -30)
    def game_mouse_move_deg_up_45(mouse_button: int = None): """Look up 45 degrees"""; mouse_move_deg(0, -45)
    def game_mouse_move_deg_up_90(mouse_button: int = None): """Look up 90 degrees"""; mouse_move_deg(0, -90)
    def game_mouse_move_deg_up(deg: int = 20, mouse_button: int = None): """Look up y degrees"""; mouse_move_deg(0, -deg)
    def game_mouse_move_deg_down_15(mouse_button: int = None): """Look down 15 degrees"""; mouse_move_deg(0, 15)
    def game_mouse_move_deg_down_30(mouse_button: int = None): """Look down 30 degrees"""; mouse_move_deg(0, 30)
    def game_mouse_move_deg_down_45(mouse_button: int = None): """Look down 45 degrees"""; mouse_move_deg(0, 45)
    def game_mouse_move_deg_down_90(mouse_button: int = None): """Look down 90 degrees"""; mouse_move_deg(0, 90)
    def game_mouse_move_deg_down(deg: int = 20, mouse_button: int = None): """Look down y degrees"""; mouse_move_deg(0, deg, mouse_button)
    def game_mouse_move_continuous_right(speed: int = 20, mouse_button: int = None): """Turn right continuously at speed x; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(1, 0, speed, mouse_button)
    def game_mouse_move_continuous_right_5(mouse_button: int = None): """Turn right continuously speed 5; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(1, 0, 5, mouse_button)
    def game_mouse_move_continuous_right_10(mouse_button: int = None): """Turn right continuously speed 10; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(1, 0, 10, mouse_button)
    def game_mouse_move_continuous_right_20(mouse_button: int = None): """Turn right continuously speed 20; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(1, 0, 20, mouse_button)
    def game_mouse_move_continuous_right_30(mouse_button: int = None): """Turn right continuously speed 30; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(1, 0, 30, mouse_button)
    def game_mouse_move_continuous_left(speed: int = 20, mouse_button: int = None): """Turn left continuously at speed x; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(-1, 0, speed, mouse_button)
    def game_mouse_move_continuous_left_5(mouse_button: int = None): """Turn left continuously speed 5; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(-1, 0, 5, mouse_button)
    def game_mouse_move_continuous_left_10(mouse_button: int = None): """Turn left continuously speed 10; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(-1, 0, 10, mouse_button)
    def game_mouse_move_continuous_left_20(mouse_button: int = None): """Turn left continuously speed 20; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(-1, 0, 20, mouse_button)
    def game_mouse_move_continuous_left_30(mouse_button: int = None): """Turn left continuously speed 30; Optionally specify mouse button 0=left, 1=right, 2=middle to hold"""; mouse_move_continuous(-1, 0, 30, mouse_button)
    def game_mouse_move_continuous_up(speed: int = 10, mouse_button: int = None): """Look up continuously at speed x"""; mouse_move_continuous(0, -1, speed, mouse_button)
    def game_mouse_move_continuous_up_5(mouse_button: int = None): """Look up continuously speed 5"""; mouse_move_continuous(0, -1, 5, mouse_button)
    def game_mouse_move_continuous_up_10(mouse_button: int = None): """Look up continuously speed 10"""; mouse_move_continuous(0, -1, 10, mouse_button)
    def game_mouse_move_continuous_up_20(mouse_button: int = None): """Look up continuously speed 20"""; mouse_move_continuous(0, -1, 20, mouse_button)
    def game_mouse_move_continuous_up_30(mouse_button: int = None): """Look up continuously speed 30"""; mouse_move_continuous(0, -1, 30, mouse_button)
    def game_mouse_move_continuous_down(speed: int = 10, mouse_button: int = None): """Look down continuously at speed x"""; mouse_move_continuous(0, 1, speed, mouse_button)
    def game_mouse_move_continuous_down_5(mouse_button: int = None): """Look down continuously speed 5"""; mouse_move_continuous(0, 1, 5, mouse_button)
    def game_mouse_move_continuous_down_10(mouse_button: int = None): """Look down continuously speed 10"""; mouse_move_continuous(0, 1, 10, mouse_button)
    def game_mouse_move_continuous_down_20(mouse_button: int = None): """Look down continuously speed 20"""; mouse_move_continuous(0, 1, 20, mouse_button)
    def game_mouse_move_continuous_down_30(mouse_button: int = None): """Look down continuously speed 30"""; mouse_move_continuous(0, 1, 30, mouse_button)
    def game_mouse_move_continuous_stop(): """Stop looking continuously"""; mouse_move_continuous_stop(150)
    def game_mouse_move_reset_center_y(mouse_button: int = None): """Reset the mouse to the center of the screen"""; mouse_reset_center_y()
    def game_mouse_calibrate_x_360(num: int, mouse_button: int = None): """Calibrate x by testing a 360"""; game_mouse_calibrate_x_360(num)
    def game_mouse_calibrate_y_90(num: int, mouse_button: int = None): """Calibrate y by testing ground to center"""; game_calibrate_90_y(num)
    def game_state_switch_horizontal(): """Switch state value of horizontal"""; game_state_switch_horizontal()