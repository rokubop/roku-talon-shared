# Parrot Config

This is an alternate way to define your parrot commands in a way that supports
- combos
- throttling
- debounce
- switching out configs easily without needing to create new modes.
- screen positions (WIP)

Combos have a timeout of `300ms`. If you define a combo, then the first sound will no longer fire immediately, but only after `300ms`.

## Example

```talon
parrot(pop):                 user.parrot_config_noise("pop")
parrot(hiss):                user.parrot_config_noise("hiss")
parrot(hiss:stop):           user.parrot_config_noise("hiss_stop")
parrot(shush):               user.parrot_config_noise("shush")
parrot(shush:stop):          user.parrot_config_noise("shush_stop")
parrot(cluck):               user.parrot_config_noise("cluck")
```

```py
parrot_config = {
    "pop":         ("use", lambda: actions.user.game_key("e")),
    "cluck":       ("attack", lambda: actions.mouse_click(0)),
    "cluck cluck": ("hard attack", lambda: actions.mouse_click(1)),
    "cluck pop":   ("special", lambda: actions.mouse_click(2)),
    "hiss:db_100": ("jump", lambda: actions.user.game_key("space")),
    "hiss:stop":   ("", lambda: None),
    "shush:th_100":("crouch", lambda: actions.user.game_key("c")),
    "tut":         ("alt", lambda: actions.user.game_key("alt")),
    "tut ah":      ("turn left", actions.user.game_mouse_move_deg_left_90),
    "tut oh":      ("turn right", actions.user.game_mouse_move_deg_right_90),
    "tut guh":     ("turn around", actions.user.game_mouse_move_deg_180),
}

@ctx.action_class("user")
class Actions:
    def parrot_config():
        return parrot_config
```

## Define different modes:
```py
default_config = {
    "pop":         ("use", lambda: actions.user.game_key("e")),
    "cluck":       ("attack", lambda: actions.mouse_click(0)),
    "cluck cluck": ("hard attack", lambda: actions.mouse_click(1)),
    "cluck pop":   ("special", lambda: actions.mouse_click(2)),
    "hiss:db_100": ("jump", lambda: actions.user.game_key("space")),
    "hiss:stop":   ("", lambda: None),
    "shush:th_100":("crouch", lambda: actions.user.game_key("c")),
}
move_config = {
    **default_config,
    "pop":         ("left", lambda: actions.user.go_left()),
    "cluck":     ("right", lambda: actions.user.go_right()),
}
combat_config = {
    **default_config,
    "cluck":       ("attack", lambda: actions.mouse_click(0)),
    "cluck cluck": ("hard attack", lambda: actions.mouse_click(1)),
}
parrot_config = {
    "default": default_config,
    "move": move_config,
    "combat": combat_config,
}

@ctx.action_class("user")
class Actions:
    def parrot_config():
        return parrot_config

# Actions
actions.user.parrot_config_set_mode("default")
actions.user.parrot_config_cycle_mode()
actions.user.parrot_config_get_mode()
```

## Throttling
Throttling is useful when you have a continuous parrot noise, but you only want to trigger it once per 100ms for example:
```py
"shush:th_100":("jump", lambda: actions.user.game_key("space")),
```

## Debouncing
Debouncing on the start of a command means that you need to hold it for 100ms until it will trigger. You might want this if you also want to use normal english commands as well and don't want the shush to be triggered immediately.
```py
"shush:db_100":("turn left", actions.user.game_mouse_move_continuous_left),
```

Debouncing at the stop of a command basically just means the stop will be delayed
```py
"shush_stop:db_100":("", actions.user.game_mouse_move_continuous_stop),
```

## Switching config dynamically
If you don't want to use modes, you can also swap out the parrot config on the fly, and it will automatically update.

```py
parrot_config = default_config

def use_other_config():
    global parrot_config
    parrot_config = other_config

@ctx.action_class("user")
class Actions:
    def parrot_config():
        return parrot_config
```

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

## Dependencies
none