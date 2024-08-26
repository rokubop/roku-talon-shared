from talon import actions
from .celeste_ui_default_full import show_full_ui, hide_full_ui, refresh_full_ui
from .celeste_ui_big_text import show_big_text_ui, hide_big_text_ui, refresh_big_text_ui
from .celeste_ui_minimal import show_minimal_ui, hide_minimal_ui
from .celeste_ui_for_obs_second_screen import show_obs_ui, hide_obs_ui

# Choose a UI to use
ui = "full"
# ui = "big_text"
# ui = "minimal"
# ui = "minimal"

def show_ui(parrot_config):
    if ui == "full":
        show_full_ui(parrot_config)
    elif ui == "big_text":
        show_big_text_ui()
    elif ui == "minimal":
        show_minimal_ui()
    elif ui == "obs":
        show_obs_ui(parrot_config)

def hide_ui():
    if ui == "full":
        hide_full_ui()
    elif ui == "big_text":
        hide_big_text_ui()
    elif ui == "minimal":
        hide_minimal_ui()
    elif ui == "obs":
        hide_obs_ui()

def refresh_ui(parrot_config, bg_color: str):
    if ui == "full":
        refresh_full_ui(parrot_config, {"background_color": bg_color})
    elif ui == "big_text":
        refresh_big_text_ui()
    else:
        actions.skip()
