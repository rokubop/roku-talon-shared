# ui_elements

This is an experimental repository for making any generic UI in HTML-like syntax.

## Elements
- `screen`
- `div`
- `text`
- `button`
- `input_text`

## Usage
First we pick the elements we want to use:
```py
(screen, div, text) = actions.user.ui_elements(["screen", "div", "text"])
```

The outermost layer must be the screen component
```py
my_ui = screen()[
    div()[
        ...
    ]
]
```

To define css, we put it inside of the parentheses. This uses standard CSS property naming. To define children, we put it inside the square brackets. let's give it 1 div, positioned to the right center:
```py
my_ui = screen(align_items="flex_end", justify_content="center")[
    div()[
        text("Hello world")
    ]
]
```

Now we just need to show it:
```py
global my_ui

def show_ui():
    global my_ui
    my_ui = screen()[
        div()[
            text("Hello world")
        ]
    ]
    my_ui.show()

def hide_ui():
    global my_ui
    my_ui.hide()
```

## Full example
```py
global my_ui

def show_ui():
    global my_ui
    (div, text, screen, button) = actions.user.ui_elements(["div", "text", "screen", "button"])
    my_ui = screen(align_items="flex_end", justify_content="center")[
        div(id="box", padding=16, background_color="FF000088")[
            text("Hello world", color="FFFFFF"),
            text("Test", id="test", font_size=24),
        ]
    ]
    my_ui.show()

def hide_ui():
    global my_ui
    my_ui.hide()
```

## Alignment
You can look up CSS flexbox guide for learning more about alignment. Here are some examples:

```py
# children of screen will be bottom right
screen(align_items="flex_end", justify_content="flex_end")[]

# children of screen will be center
screen(align_items="center", justify_content="center")[]

# children of screen will be top left
screen(align_items="flex_start", justify_content="flex_start")[]

# children of screen will be top right
screen(align_items="flex_start", justify_content="flex_end")[]

# Use margin to offset
div(margin_top=16)[
    text("Hello world")
]
```

## Updating text
We must give a unique id to the thing we want to update.
```py
text("Hello world", id="test"),
```

Then we can use this action to update the text:
```py
actions.user.ui_elements_update_text("test", "New text")
```



## Highlighting elements
We must give a unique id to the thing we want to highlight.
```py
div(id="box")[
    text("Hello world"),
]
```

We can then use these actions to trigger a highlight or unhighlight:
```py
actions.user.ui_elements_highlight("box")
actions.user.ui_elements_highlight_briefly("box")
actions.user.ui_elements_unhighlight("box")
```

We can customize the highlight color with custom css prop:
```py
div(id="box", highlight_color="FF0000")[
    text("Hello world"),
]
```

## Buttons
If you use a button, the UI will block the mouse instead of being pass through.
```py
# button
button("Click me", on_click=lambda: print("clicked")),
button("Click me", on_click=actions.user.hide_my_custom_ui),
```

## Text inputs
```py
div()[
    input_text(id="your_name"),
],

# later
actions.user.ui_elements_get_value("your_name")
```

## Unpacking a list into elements
```py
commands = [
    "left",
    "right",
    "up",
    "down"
]
div(gap=8)[
    text("Commands", font_weight="bold"),
    *(text(command) for command in commands)
],
```

## Opacity
```py
# 50% opacity
div(background_color="FF0000", opacity=0.5)[
    text("Hello world")
]

# or we can use the last 2 digits of the color
div(background_color="FF000088")[
    text("Hello world")
]
```

## Alternate screen
```py
# screen 1
screen(1, align_items="flex_end", justify_content="center")[
    div()[
        text("Hello world")
    ]
]
# or
screen(screen=2, align_items="flex_end", justify_content="center")[
    div()[
        text("Hello world")
    ]
]
```

## CSS Options

| CSS Property | Type |
| -- | -- |
| align_items | `'flex_start'`, `'flex_end'`, `'center'` |
| background_color | `str` - 6-digit hexadecimal with 2 optional digits for opacity e.g. `'FF0000'` or `FF000088` for opacity of `88` from `00` to `FF` |
| border_color | `str` |
| border_radius | `int` |
| border_width | `int` |
| bottom | `int` |
| color | `str` - 6-digit hexadecimal with 2 optional digits for opacity e.g. `'FF0000'` or `FF000088` for opacity of `88` from `00` to `FF` |
| flex_direction | `'row'`, `'column'` |
| font_size | `int` - for text |
| font_weight | `str` - e.g. `'bold'` |
| gap | `int` - gap between children |
| height | `int` |
| highlight_color | `str` - 6-digit hexadecimal with 2 optional digits for opacity e.g. `'FF0000'` or `FF000088` for opacity of `88` from `00` to `FF` |
| id | `str` - Required on builder, and for 'highlight' feature to work on a div |
| justify | `str` |
| justify_content | `'flex_start'`, `'flex_end'`, `'center'` |
| left | `int` |
| margin | `int` - Margin in every direction |
| margin_bottom | `int` |
| margin_left | `int` |
| margin_right | `int` |
| margin_top | `int` |
| on_click | `Callable[[], None]` - Callback function to call when button is clicked. Takes 0 arguments. |
| on_change | `Callable[[str], None]` - Callback function to call when value of input changes. Takes 1 argument for the current value. |
| opacity | `float` - 0.0 to 1.0. Or you can use the last 2 digits of the color instead of opacity |
| padding | `int` - Padding in every direction |
| padding_bottom | `int` |
| padding_left | `int` |
| padding_right | `int` |
| padding_top | `int` |
| right | `int` |
| screen | `int` - Screen number (only applicable to screen element). Defaults to main screen if omitted. |
| top | `int` |
| value | `str` - For input |
| width | `int` |