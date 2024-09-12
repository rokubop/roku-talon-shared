"""
Override pop and hiss while ctx is active
"""

from talon import Module, Context, actions, app, registry
from .dynamic_noises import (
    dynamic_noises_state,
    dynamic_noises_event_trigger,
    DynamicActionEvent,
    EVENT_TYPE_ACTION,
    EVENT_TYPE_ACTION_STOP
)

mod = Module()
mod.tag("dynamic_noises_talon_noise_override", desc="Tag for enabling dynamic noises")
ctx_overrides = Context()
ctx_overrides.matches = "tag: user.dynamic_noises_talon_noise_override"

def on_pop():
    pop_state = dynamic_noises_state.get("pop")
    if pop_state:
        print("new pop")
        print(vars(pop_state))
    if pop_state and pop_state.current:
        # Old community version used this 2023
        actions.skip()
    else:
        print("old pop")
        dynamic_noises_event_trigger(DynamicActionEvent(EVENT_TYPE_ACTION, "pop", "default"))
        actions.next()

def noise_trigger_pop():
    pop_state = dynamic_noises_state.get("pop")
    print(pop_state)
    if pop_state and pop_state.current:
        # dynamic_noises is active so it will mange this instead
        actions.skip()
    else:
        # we should defer to the user's original action
        dynamic_noises_event_trigger(DynamicActionEvent(EVENT_TYPE_ACTION, "pop", "default"))
        actions.next()

def noise_trigger_hiss(active: bool):
    hiss_state = dynamic_noises_state.get("hiss")
    print(hiss_state)
    if hiss_state and hiss_state.current:
        actions.skip()
    else:
        if active:
            dynamic_noises_event_trigger(DynamicActionEvent(EVENT_TYPE_ACTION, "hiss", "default"))
        else:
            dynamic_noises_event_trigger(DynamicActionEvent(EVENT_TYPE_ACTION_STOP, "hiss_stop", "default"))
        actions.next(active)

def on_ready():
    if registry.actions.get("user.noise_trigger_pop"):
        ctx_overrides.action("user.noise_trigger_pop")(noise_trigger_pop)

    if registry.actions.get("user.noise_trigger_hiss"):
        ctx_overrides.action("user.noise_trigger_hiss")(noise_trigger_hiss)

    if registry.actions.get("user.on_pop"):
        ctx_overrides.action("user.on_pop")(on_pop)

app.register("ready", on_ready)