"""
Talon noise override tag

UPDATE THIS BASED ON YOUR OWN REPO:
Skip actions that are normally enabled in your repo
"""

from talon import Module, Context, actions

mod = Module()
mod.tag("dynamic_actions_talon_noise_override", desc="Tag for enabling dynamic noises")
ctx_dynamic_actions_talon_noises = Context()
ctx_dynamic_actions_talon_noises.matches = "tag: user.dynamic_actions_talon_noise_override"

@ctx_dynamic_actions_talon_noises.action_class("user")
class Actions:
    # Skip talon noise actions that are normally enabled in your repo

    # remove this def if you don't have an on_pop in your repo
    def on_pop():
        actions.skip()

    def noise_trigger_pop():
        actions.skip()

    def noise_trigger_hiss(active: bool):
        actions.skip()