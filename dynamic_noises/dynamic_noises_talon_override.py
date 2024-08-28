"""
Talon noise override tag

UPDATE THIS BASED ON YOUR OWN REPO:
Skip actions that are normally enabled in your repo
"""

from talon import Module, Context, actions
from .dynamic_noises import (
    dynamic_noises_state,
    dynamic_noises_event_trigger,
    DynamicActionEvent,
    EVENT_TYPE_ACTION,
    EVENT_TYPE_ACTION_STOP
)

mod = Module()
mod.tag("dynamic_noises_talon_noise_override", desc="Tag for enabling dynamic noises")
ctx_dynamic_noises_talon_noises = Context()
ctx_dynamic_noises_talon_noises.matches = "tag: user.dynamic_noises_talon_noise_override"

@ctx_dynamic_noises_talon_noises.action_class("user")
class Actions:
    # When this ctx is active, it will skip talon noise actions
    # that are normally enabled in your repo. Add functions here
    # that are normally active for you. Remove functions here if
    # you don't have them in your repo.
    def on_pop():
        if dynamic_noises_state.get("pop"):
            # Old community version used this 2023
            actions.skip()
        else:
            dynamic_noises_event_trigger(DynamicActionEvent(EVENT_TYPE_ACTION, "pop", "default"))
            actions.next()

    def noise_trigger_pop():
        if dynamic_noises_state.get("pop"):
            actions.skip()
        else:
            dynamic_noises_event_trigger(DynamicActionEvent(EVENT_TYPE_ACTION, "pop", "default"))
            actions.next()

    def noise_trigger_hiss(active: bool):
        if dynamic_noises_state.get("hiss"):
            actions.skip()
        else:
            if active:
                dynamic_noises_event_trigger(DynamicActionEvent(EVENT_TYPE_ACTION, "hiss", "default"))
            else:
                dynamic_noises_event_trigger(DynamicActionEvent(EVENT_TYPE_ACTION_STOP, "hiss_stop", "default"))
            actions.next(active)