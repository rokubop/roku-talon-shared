"""
Talon noise override tag

UPDATE THIS BASED ON YOUR OWN REPO:
Skip actions that are normally enabled in your repo
"""

from talon import Module, Context, actions
from .dynamic_actions import dynamic_actions_state, dynamic_actions_event_trigger, DynamicActionEvent, EVENT_TYPE_ACTION

mod = Module()
mod.tag("dynamic_actions_talon_noise_override", desc="Tag for enabling dynamic noises")
ctx_dynamic_actions_talon_noises = Context()
ctx_dynamic_actions_talon_noises.matches = "tag: user.dynamic_actions_talon_noise_override"

@ctx_dynamic_actions_talon_noises.action_class("user")
class Actions:
    # When this ctx is active, it will skip talon noise actions
    # that are normally enabled in your repo. Add functions here
    # that are normally active for you. Remove functions here if
    # you don't have them in your repo.
    def on_pop():
        print("on_pop")
        print(f"dynamic_actions_state from ctx: {dynamic_actions_state}")
        if dynamic_actions_state.get("pop"):
            print("pop skip")
            actions.skip()
        else:
            print("pop next")
            dynamic_actions_event_trigger(DynamicActionEvent(EVENT_TYPE_ACTION, "pop", "default"))
            actions.next()

    def noise_trigger_pop():
        print("noise_trigger_pop")
        if dynamic_actions_state.get("pop"):
            actions.skip()
        else:
            dynamic_actions_event_trigger(DynamicActionEvent(EVENT_TYPE_ACTION, "pop", "default"))
            actions.next()

    def noise_trigger_hiss(active: bool):
        if dynamic_actions_state.get("hiss"):
            print("hiss skip")
            actions.skip()
        else:
            print("hiss next")
            dynamic_actions_event_trigger(DynamicActionEvent(EVENT_TYPE_ACTION, "hiss", "default"))
            actions.next(active)