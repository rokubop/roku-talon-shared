from talon import Module, actions
from typing import Union
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
    xbox_mode_enable,
    xbox_mode_disable
)

mod = Module()

@mod.action_class
class Actions:
    def game_xbox_gamepad_enable(): """Enable xbox gamepad actions. Enables vgamepad. Windows and Linux only."""; xbox_mode_enable()
    def game_xbox_gamepad_disable(): """Disable xbox gamepad actions. Disables vgamepad."""; xbox_mode_disable()
    def game_xbox_button_press(button: str, hold: int = None):
        """
        Press an xbox button

        **buttons**:  a, b, x, y, left_shoulder, right_shoulder, left_thumb, right_thumb, start, back, guide, dpad_up, dpad_down, dpad_left, dpad_right, view, guide, menu

        **button aliases**: lb, rb, lt, rt, l1, r1, l2, r2, l3, r3, xbox
        """
        xbox_button_press(button, hold)
    def game_xbox_button_release(button: str): """Release an xbox button"""; xbox_button_release(button)
    def game_xbox_button_hold(button: str, hold_ms: int = None):
        """Hold an xbox button indefinitely or for a fixed duration.

        **buttons**:  a, b, x, y, left_shoulder, right_shoulder, left_thumb, right_thumb, start, back, guide, dpad_up, dpad_down, dpad_left, dpad_right, view, guide, menu

        **button aliases**: lb, rb, lt, rt, l1, r1, l2, r2, l3, r3, xbox
        """
        xbox_button_hold(button, hold_ms)
    def game_xbox_button_toggle(button: str):
        """
        Toggle holding an xbox button

        **buttons**:  a, b, x, y, left_shoulder, right_shoulder, left_thumb, right_thumb, start, back, guide, dpad_up, dpad_down, dpad_left, dpad_right, view, guide, menu

        **button aliases**: lb, rb, lt, rt, l1, r1, l2, r2, l3, r3, xbox
        """
        xbox_button_toggle(button)
    def game_xbox_stick_hold_dir(stick_side: str, dir: str, power: float = None):
        """
        Hold a stick_side direction

        **sticks**:  left, right

        **directions**:  up, down, left, right
        """
        if stick_side == "left": xbox_left_analog_hold_dir(dir, power)
        elif stick_side == "right": xbox_right_analog_hold_dir(dir, power)
    def game_xbox_stick_set_gear(stick_side: str, gear: Union[int, str]):
        """
        Set stick_side gear from 1 to 5

        **sticks**:  left, right
        """
        xbox_set_gear(f"{stick_side}_stick", gear)
    def game_xbox_stick_stop(stick_side: str):
        """
        Stop holding a stick_side

        **sticks**:  left, right
        """
        if stick_side == "left": xbox_left_stick(0, 0)
        elif stick_side == "right": xbox_right_stick(0, 0)
    def game_xbox_left_stick_hold_dir(dir: str | tuple, power: float = None): """Hold left stick dir up down left right"""; xbox_left_analog_hold_dir(dir, power)
    def game_xbox_left_stick_set_gear(gear: Union[int, str]): """Set left stick gear from 1 to 5"""; xbox_set_gear("left_stick", gear)
    def game_xbox_left_stick_stop(): """Stop holding left stick"""; xbox_left_stick(0, 0)
    def game_xbox_right_stick_hold_dir(dir: str | tuple, power: float = None): """Hold right stick dir up down left right"""; xbox_right_analog_hold_dir(dir, power)
    def game_xbox_right_stick_set_gear(gear: Union[int, str]): """Set right stick gear from 1 to 5"""; xbox_set_gear("right_stick", gear)
    def game_xbox_right_stick_stop(): """Stop holding right stick"""; xbox_right_stick(0, 0)
    def game_xbox_dpad_press_dir(dir: str): """up, down, left, right"""; xbox_button_press(f"dpad_{dir}")
    def game_xbox_dpad_hold_only_dir(dir: str): """Hold dpad dir up, down, left, right"""; xbox_dpad_hold_dir(dir)
    def game_xbox_trigger(trigger: str, power: float = None): """Press a trigger (left or right)"""; xbox_button_press(f"{trigger}_trigger")
    def game_xbox_trigger_hold(trigger: str, power: float = None): """Hold a trigger (left or right)"""; xbox_trigger_hold(f"{trigger}_trigger", power)
    def game_xbox_trigger_release(trigger: str): """Release a trigger (left or right)"""; xbox_trigger_release(f"{trigger}_trigger")
    def game_xbox_trigger_set_gear(trigger: str, gear: Union[int, str]): """Set trigger gear from 1 to 5"""; xbox_set_gear(f"{trigger}_trigger", gear)
    def game_xbox_left_trigger(power: float = None): """Press the left trigger (LT)"""; xbox_button_press("left_trigger")
    def game_xbox_left_trigger_hold(power: float = None): """Hold the left trigger (LT)"""; xbox_trigger_hold("left_trigger", power)
    def game_xbox_left_trigger_release(): """Release the left trigger (LT)"""; xbox_trigger_release("left_trigger")
    def game_xbox_left_trigger_set_gear(gear: Union[int, str]): """Set left trigger gear from 1 to 5"""; xbox_set_gear("left_trigger", gear)
    def game_xbox_right_trigger(power: float = None): """Press the right trigger (LT)"""; xbox_button_press("right_trigger")
    def game_xbox_right_trigger_hold(power: float = None): """Hold the right trigger (LT)"""; xbox_trigger_hold("right_trigger", power)
    def game_xbox_right_trigger_release(): """Release the right trigger (LT)"""; xbox_trigger_release("right_trigger")
    def game_xbox_right_trigger_set_gear(gear: Union[int, str]): """Set right trigger gear from 1 to 5"""; xbox_set_gear("right_trigger", gear)
    def game_xbox_stopper(): """General stopper based on priority for xbox actions"""; xbox_stopper()