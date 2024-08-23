from talon import actions

def noises_wheel():
    actions.user.dynamic_action_set_phrase("hiss", "grid hide lob")
    actions.user.dynamic_action_set_phrase("pop", "grid hide lob")
    noises_default()

def noises_default():
    actions.user.dynamic_action_set("hiss", "stop", actions.user.game_stopper)
    actions.user.dynamic_action_set("pop", "A", lambda: actions.user.game_xbox_button_press('a'))

def noises_fighter():
    actions.user.dynamic_action_set("hiss", "stop", actions.user.game_stopper)
    actions.user.dynamic_action_set("pop", "RT", lambda: actions.user.game_xbox_button_press('rt'))