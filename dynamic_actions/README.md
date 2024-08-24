# Dynamic Actions

This is an experimental repository. WIP.

Dynamic actions allow you to update noises like "pop" or "hiss" on the fly, programatically or to any spoken phrase e.g. saying "pop scroll down" to bind "scroll down" to noise "pop". Keeps a history of recent actions and allows you to swap between them. Can be used with commands, noises, or parrot.

## Try it out
- Say "dynamic actions" to try it out with default talon noises.
- Say "pop again" to bind "again" to "pop". Now you have a repeater for "pop"
- Say "touch pop" to both execute touch and bind it at the same time.

### hiss noise
The word "hiss" will inadvertently trigger the "hiss" noise, so we use the alias "wish".
- Say "wish scroll up" to bind "scroll up" to "hiss" (wish).

## Programmatic setup
```python
# .enable
actions.user.dynamic_actions_talon_noise_replace_enable()
actions.user.dynamic_actions_phrase_assignment_enable()
# actions.user.dynamic_actions_enable({
#     replace_talon_noises: true,
#     register_phrase_assignment: true,
# })
actions.user.dynamic_action_set_default([{
    name: "pop",
    action: lambda: print("pop"),
    action_name: "click",
}, {
    name: "hiss",
    action: lambda: print("hiss"),
    action_name: "scroll down", # optional
    throttle: int, # optional
    debounce: int, # optional
    once: bool # optional
}, {
    name: "hiss_stop",
    action: lambda: print("hiss_stop"),
}])

# disable
actions.user.dynamic_actions_talon_noise_replace_disable()
actions.user.dynamic_actions_phrase_assignment_disable()
```


## Update with spoken phrase
- Saying "pop" at the beginning of any phrase will assign that phrase to the "pop" noise, and will not be executed
- Saying "pop" at the end of any phrase will execute the action and be assigned to the "pop" noise

| Phrase | Action |
| --- | --- |
| "pop each" | "pop" noise assigned to "each" |
| "pop say hello" | "pop" noise assigned to "say hello" |
| "go down 3 pop" | "go down 3" will execute and be assigned to "pop" noise |
| "jump hiss" | "jump" will execute and be assigned to "hiss" noise |

## Update programatically
```python
# simple
actions.user.dynamic_actions_set("pop", lambda: print("pop"))

# advanced
actions.user.dynamic_actions_set({
    name: "pop",
    action: lambda: print("pop"),
    action_name: "go down", # optional
    throttle: int, # optional
    debounce: int, # optional
    once: bool # optional
})
```

## Monitor changes
```python
@ctx.action_class
class Actions:
    def on_dynamic_action_change(state: dict):
        print(f"Dynamic action {state.name} set to {state.action_name}")
```

## Actions
| Function | Description |
| --- | --- |
| `dynamic_actions_set(name: str, callable: Callable)` | Set a dynamic action to a callable (Simple) |
| `dynamic_actions_set(dict)` | Set a dynamic action to a callable (Advanced) |
| `dynamic_action_set_once(name: str, callable: Callable)` | Set a dynamic action to a callable, but only once |
| `dynamic_actions_set_phrase(name: str, phrase: str)` | Set a dynamic action to a phrase |
| `dynamic_action_reset(name: str)` | Reset a dynamic action to the default |
| `dynamic_action_unset_current(name: str)` | Unset the current dynamic action |
| `dynamic_action_swap_recent(name: str)` | Swap the current dynamic action with the most recent one |

```python
dynamic_actions_set("pop", callable)
dynamic_action_set_once("pop", callable)
dynamic_actions_set_phrase("pop", "go down")
dynamic_action_reset("pop")
dynamic_action_unset_current("pop")
dynamic_action_swap_recent("pop")

# my command: dynamic_actions_trigger("pop")