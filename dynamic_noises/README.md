# Dynamic Noises

This is an experimental repository. WIP.

Dynamic noises allow you to update noises "pop" and "hiss" on the fly, individually, or as a group.

## Try it
Say "dynamic noises" to try it out. A UI will show you your current phrase binding.

## Manual setup
```python
# enable
actions.user.dynamic_noises_enable()

# disable
actions.user.dynamic_noises_disable()
```

While enabled:
- Default talon pop and hiss replaced with ctx dynamic versions
- Speech recognition will listen for "pop" and "hiss" at the beginning of a phrase and bind whatever comes after it.
- We can also update individual noises using actions `actions.user.dynamic_noises_set_pop` and `actions.user.dynamic_noises_set_hiss`

This looks like:
```python
actions.user.dynamic_noises_set_pop("repeater", actions.core.repeat_phrase)
```

## Modes
We can also set up modes conveniently

```python
dynamic_noises = {
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
    def dynamic_noises():
        return dynamic_noises

# Enable
actions.user.dynamic_noises_enable()

# Disable
actions.user.dynamic_noises_disable()
```

This sets us up with two modes, "default" and "repeater". If we speak the words "default" or "repeater", we get the corresponding mode.

## ctx for modes
| ctx | Description |
| --- | --- |
| `dynamic_noises` | User defined dictionary of modes and their corresponding actions. |

## Actions
| Action | Description |
| --- | --- |
| `dynamic_noises_enable` | Enable dynamic noises. Replaces talon noises with dynamic noises. `dynamic_noises_set` will now work, and phrases such as "pop go down" or "hiss again" will bind it. |
| `dynamic_noises_disable` | Disable dynamic noises. Restores talon noises if applicable.  Stops listening to phrase binding. |
| `dynamic_noises_use_mode` | Use mode (group of bindings) as set up by the user in `dynamic_actions`
| `dynamic_noises_set` | Primary action for assigning a dynamic action. The words "pop" and "hiss" will automatically use talon noises unless specified otherwise in `dynamic_noises_enable`. |
| `dynamic_noises_set_hiss` | Convenience wrapper around `dynamic_noises_set`. Set a dynamic action to "hiss". |
| `dynamic_noises_set_pop` | Convenience wrapper around `dynamic_noises_set`. Set a dynamic action to "pop". |
| `dynamic_noises_trigger` | Trigger a dynamic action manually. For example if you're using parrot instead of talon noises. |
| `dynamic_noises_event_register` | If you want to listen to state changes, you can register a listener for dynamic action changes. |
| `dynamic_noises_event_unregister` | Unregister an event for a dynamic action. |
| `dynamic_noises_event_unregister_all` | Unregister all events for a dynamic action. |
| `dynamic_noises_ui_element` | A UI built from `ui_elements` showing pop and hiss you can place inside of other `ui_elements` to show the current dynamic action. |