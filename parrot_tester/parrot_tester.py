
from talon import Context, Module
from .src.parrot_tester_ui import (
    parrot_tester_discrete,
    parrot_tester_continuous_start,
    parrot_tester_continuous_stop,
    parrot_tester_toggle,
)

mod = Module()
ctx = Context()
mod.tag("parrot_tester", "mode for testing parrot")

@mod.action_class
class Actions:
    def parrot_tester_discrete(noise: str, power: float = None, f0: float = None, f1: float = None, f2: float = None):
        """Trigger parrot tester discrete"""
        parrot_tester_discrete(noise, power, f0, f1, f2)

    def parrot_tester_continuous_start(noise: str, power: float = None, f0: float = None, f1: float = None, f2: float = None):
        """Trigger parrot tester continuous"""
        parrot_tester_continuous_start(noise, power, f0, f1, f2)

    def parrot_tester_continuous_stop(noise: str):
        """Stop parrot tester continuous"""
        parrot_tester_continuous_stop(noise)

    def parrot_tester_toggle():
        """Toggle parrot tester"""
        parrot_tester_toggle()