from .components.keys import show_keys, hide_keys
from .components.current_noise import show_current_noise, hide_current_noise
from .components.commands import show_commands, hide_commands
from .components.history_rollover import show_history_rollover, hide_history_rollover

def show_ui():
    # show_commands()
    show_keys()
    show_history_rollover()
    # show_current_noise()

def hide_ui():
    # hide_commands()
    hide_keys()
    hide_history_rollover()
    # hide_current_noise()

def refresh_ui():
    hide_ui()
    show_ui()