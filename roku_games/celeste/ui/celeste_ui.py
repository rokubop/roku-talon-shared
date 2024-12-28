from .components.keys import show_keys, hide_keys
from .components.current_noise import show_current_noise, hide_current_noise
from .components.commands import show_commands, hide_commands

def show_ui():
    # show_commands()
    show_keys()
    show_current_noise()

def hide_ui():
    # hide_commands()
    hide_keys()
    hide_current_noise()

def refresh_ui():
    hide_ui()
    show_ui()