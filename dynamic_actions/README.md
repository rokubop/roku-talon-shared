# Dynamic Actions

This is an experimental repository. WIP.

Dynamic actions allow you to update noises like "pop" or "hiss" on the fly, programatically or to any spoken phrase e.g. saying "pop scroll down" to bind "scroll down" to noise "pop". Keeps a history of recent actions and allows you to swap between them. Can be used with commands, noises, or parrot.

## Actions
| Action | Description |
| --- | --- |
| dynamic_actions_enable | Enable dynamic actions. Replaces talon noises with dynamic actions. Starts listening to speech for setting actions on the fly. |
| dynamic_actions_disable | Disable dynamic actions. Restores talon noises if applicable. |
| dynamic_actions_set | Set a named action like "pop" or "hiss" or "shush" to any function. "pop" and "hiss" will automatically use talon noises. |
| dynamic_actions_set_hiss | Set a dynamic action to "hiss". |
| dynamic_actions_set_pop | Set a dynamic action to "pop". |
| dynamic_actions_trigger | Trigger a dynamic action manually. For example if you're using parrot instead of talon noises. |
| dynamic_actions_event_register | If you want to listen to state changes, you can register a listener for dynamic action changes. |
| dynamic_actions_event_unregister | Unregister an event for a dynamic action. |
| dynamic_actions_event_unregister_all | Unregister all events for a dynamic action. |

## Usage
```python
actions.user.dynamic_actions_enable()
actions.user.dynamic_action_set_pop("repeater", actions.core.repeat_phrase)

# disable - restores original talon noise
actions.user.dynamic_actions_disable()
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
actions.user.dynamic_actions_set("pop", phrase="go down")
```

## Monitor changes
```python
def on_change(event):
    print(event)

actions.user.dynamic_actions_event_register(on_change)
```