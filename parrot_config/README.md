# Parrot Config

This is an alternate way to define your parrot commands in a way that supports
- combos
- throttling
- debounce
- screen positions (WIP)
- switching out configs easily without needing to create new modes.

When you define a combo, then if you try to do the first one by itself without combing, it will have a timeout of `300ms`

## Example

```talon
parrot(pop):                 user.use_parrot_config("pop")
parrot(hiss):                user.use_parrot_config("hiss")
parrot(hiss:stop):           user.use_parrot_config("hiss_stop")
parrot(shush):               user.use_parrot_config("shush")
parrot(shush:stop):          user.use_parrot_config("shush_stop")
parrot(cluck):               user.use_parrot_config("cluck")
```

```py
parrot_config = {
    "pop":         ("attack", lambda: actions.mouse_click(0)),
    "pop pop":     ("hard attack", lambda: actions.mouse_click(1)),
    "hiss:db_100": ("jump", lambda: actions.key("space")),
    "hiss:stop":   ("", lambda: None),
    "shush:th_100":("crouch", lambda: actions.key("c")),
    "cluck@left":  ("left", lambda: actions.key("a")), # WIP
    "cluck@right": ("right", lambda: actions.key("d")), # WIP
}

@ctx.action_class("user")
class Actions:
    def parrot_config():
        return parrot_config
```

If you want to swap out the parrot config, you can simply override the variable.

## Options:
| Definition | Description |
|------------|-------------|
| `"pop pop"` | Triggers when you combo two pops in a row within `300ms`. If you define this combo, then a regular `"pop"` will be delayed, in order to determine to use the single pop or wait for the combo pop. |
| `"pop cluck"` | Triggers when you combo pop then cluck within `300ms`. If you use this combo, then a regular `"pop"` will be delayed, in order to determine to use the single pop or wait for the pop+cluck. |
| `"pop cluck pop"` | Triggers when you combo pop then cluck then pop within `300ms` between each. If you use this combo, then a regular `"pop"` and `"pop cluck"` will be delayed, in order to determine to use the partial command or wait for the full potential combo. |
| `"pop:th_100"` | Throttles the pop command to only trigger once every 100ms. |
| `"pop:th"` | Default throttle for the pop command. |
| `"hiss:db_100"` | Debounces the hiss command to only trigger after 100ms of continuous popping. |
| `"hiss:db"` | Default debounce for the hiss command. |

## WIP:
| Definition | Description |
|------------|-------------|
| `"pop@left"` | Triggers when you pop on the left side of the screen. |
| `"pop@right"` | Triggers when you pop on the right side of the screen. |
| `"pop@up"` | Triggers when you pop on the top side of the screen. |
| `"pop@down"` | Triggers when you pop on the bottom side of the screen. |
| `"hiss:db@left"` | Debounces the hiss command to only trigger after 100ms of continuous popping on the left side of the screen. |