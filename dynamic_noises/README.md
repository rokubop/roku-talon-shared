# Dynamic Noises

This is an experimental repository. WIP.

Dynamic noises allow you to update noises like "pop" or "hiss" on the fly, programatically or to any spoken phrase e.g. saying "pop scroll down" to bind "scroll down" to noise "pop", as well as a convenient way to setup a dictionary of modes.

## Try it
Say "dynamic noises" to try it out. A UI will show you your current phrase binding.

## Usage modes
```python
noise_modes = {
    "default": {
        "pop": lambda: print("pop"),
        "hiss": lambda: print("hiss"),
    },
    "repeater": {
        "pop": actions.core.repeat_phrase,
        "hiss": lambda: print("hiss"),
    },
}

@ctx.action_class("user")
class Actions:
    def dynamic_noise_modes():
        return noise_modes

# Enable
actions.user.dynamic_noises_enable()

# Disable
actions.user.dynamic_noises_disable()
```

## Usage individual
```python
actions.user.dynamic_noises_enable()
actions.user.dynamic_noises_set_pop("repeater", actions.core.repeat_phrase)

# disable - restores original talon noise
actions.user.dynamic_noises_disable()
```


## Update with spoken phrase (WIP)
- Saying "pop" at the beginning of any phrase will assign that phrase to the "pop" noise, and will not be executed
- Saying "pop" at the end of any phrase will execute the action and be assigned to the "pop" noise

| Phrase | Action |
| --- | --- |
| "pop each" | "pop" noise assigned to "each" |
| "pop say hello" | "pop" noise assigned to "say hello" |
| "go down 3 pop" | "go down 3" will execute and be assigned to "pop" noise |
| "jump hiss" | "jump" will execute and be assigned to "hiss" noise |

## Set to phrase programmatically (WIP)
```python
actions.user.dynamic_noises_set("pop", phrase="go down")
```

## Monitor changes
```python
def on_change(event):
    print(event)

actions.user.dynamic_noises_event_register(on_change)
```

## Actions
| Action | Description |
| --- | --- |
| `dynamic_noises_enable` | Enable dynamic noises. Replaces talon noises with dynamic noises. `dynamic_noises_set` will now work, and phrases such as "pop go down" or "hiss again" will bind it. |
| `dynamic_noises_disable` | Disable dynamic noises. Restores talon noises if applicable.  Stops listening to phrase binding. |
| `dynamic_noises_set` | Primary action for assigning a dynamic action. The words "pop" and "hiss" will automatically use talon noises unless specified otherwise in `dynamic_noises_enable`. |
| `dynamic_noises_set_hiss` | Convenience wrapper around `dynamic_noises_set`. Set a dynamic action to "hiss". |
| `dynamic_noises_set_pop` | Convenience wrapper around `dynamic_noises_set`. Set a dynamic action to "pop". |
| `dynamic_noises_trigger` | Trigger a dynamic action manually. For example if you're using parrot instead of talon noises. |
| `dynamic_noises_event_register` | If you want to listen to state changes, you can register a listener for dynamic action changes. |
| `dynamic_noises_event_unregister` | Unregister an event for a dynamic action. |
| `dynamic_noises_event_unregister_all` | Unregister all events for a dynamic action. |
| `dynamic_noises_ui_element` | A UI built from `ui_elements` showing pop and hiss you can place inside of other `ui_elements` to show the current dynamic action. |