# AUTO-GENERATED
try:
    from talon import Module
    from ....roku_parrot_model.parrot_integration import parrot_delegate
    from ..src.utils import (
        parrot_tester_wrap_parrot_integration,
        parrot_tester_restore_parrot_integration
    )

    mod = Module()

    @mod.action_class
    class Actions:
        def parrot_tester_wrap_parrot_integration(file: str):
            """Wrap parrot_integration file"""
            parrot_tester_wrap_parrot_integration(parrot_delegate, file)

        def parrot_tester_restore_parrot_integration(original_file: str):
            """Restore parrot_integration file"""
            parrot_tester_restore_parrot_integration(parrot_delegate, original_file)
except ImportError:
    pass
