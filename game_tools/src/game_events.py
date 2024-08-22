EVENT_ON_KEY = "on_key"
EVENT_KEY_PRESS = "press"
EVENT_KEY_HOLD = "hold"
EVENT_KEY_RELEASE = "release"

EVENT_ON_MOUSE = "on_mouse"
EVENT_MOUSE_CLICK = "click"
EVENT_MOUSE_HOLD = "hold"
EVENT_MOUSE_RELEASE = "release"

EVENT_ON_GAME_MODE = "on_game_mode_changed"
EVENT_GAME_MODE_DISABLED = "disabled"
EVENT_GAME_MODE_ENABLED = "enabled"

default_event_subscribers = {
    EVENT_ON_GAME_MODE: [],
    EVENT_ON_KEY: [],
    EVENT_ON_MOUSE: []
}

event_subscribers = default_event_subscribers

def event_register_on_game_mode(callback):
    global event_subscribers
    event_subscribers[EVENT_ON_GAME_MODE].append(callback)

def event_unregister_on_game_mode(callback):
    global event_subscribers
    event_subscribers[EVENT_ON_GAME_MODE].remove(callback)

def event_trigger_on_game_mode():
    global event_subscribers
    for callback in event_subscribers[EVENT_ON_GAME_MODE]:
        callback()

def event_register_on_key(callback: callable):
    global event_subscribers
    if EVENT_ON_KEY not in event_subscribers:
        event_subscribers[EVENT_ON_KEY] = []
    event_subscribers[EVENT_ON_KEY].append(callback)

def event_unregister_on_key(callback: callable):
    global event_subscribers
    if EVENT_ON_KEY in event_subscribers:
        event_subscribers[EVENT_ON_KEY].remove(callback)
        if not event_subscribers[EVENT_ON_KEY]:
            del event_subscribers[EVENT_ON_KEY]

def event_trigger_on_key(key: str, state: str):
    global event_subscribers
    if EVENT_ON_KEY in event_subscribers:
        for callback in event_subscribers[EVENT_ON_KEY]:
            callback(key, state)

def event_register_on_mouse(callback: callable):
    global event_subscribers
    if EVENT_ON_MOUSE not in event_subscribers:
        event_subscribers[EVENT_ON_MOUSE] = []
    event_subscribers[EVENT_ON_MOUSE].append(callback)

def event_unregister_on_mouse(callback: callable):
    global event_subscribers
    if EVENT_ON_MOUSE in event_subscribers:
        event_subscribers[EVENT_ON_MOUSE].remove(callback)
        if not event_subscribers[EVENT_ON_MOUSE]:
            del event_subscribers[EVENT_ON_MOUSE]

def event_trigger_on_mouse(button: str, state: str):
    global event_subscribers
    if EVENT_ON_MOUSE in event_subscribers:
        for callback in event_subscribers[EVENT_ON_MOUSE]:
            callback(button, state)

def event_unregister_all():
    global event_subscribers
    event_subscribers = default_event_subscribers