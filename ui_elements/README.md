# ui_elements

This is an experimental repository for making any generic UI in HTML-like syntax. Currently supports `div`, `screen`, `text`, `button`. In the future I would like to add inputs as well. WIP.

## Usage

first we tell ui_elements what we want to use:
```py
(div, text, screen, button) = actions.user.ui_elements(["div", "text", "screen", "button"])
```

the outermost layer must be the screen component
```py
my_ui = screen()[
    div()[
        ...
    ]
]
```

To define css, we put it inside of the parentheses. This uses standard css naming. To define children, we put it inside the square brackets. let's give it 1 div, positioned to the right center:
```py
my_ui = screen(align_items="flex_end", justify_content="center")[
    div()[
        text("Hello world")
    ]
]
```

By default everything operates under the assumption of `display: flex`.

`background_color` accepts two extra characters at the end, which are the opacity

here's a full example:


```py
global my_ui

# def show
global my_ui
(div, text, screen, button) = actions.user.ui_elements(["div", "text", "screen", "button"])
my_ui = screen(align_items="flex_end", justify_content="center")[
    div(id="box", padding=16, background_color="FF000088")[
        text("Hello world", color="FFFFFF"),
        text("Test", id="test", font_size=24),
    ]
]
my_ui.show()

# trigger update text
actions.user.ui_elements_set_text("test", "Updated")

# trigger highlight
actions.user.ui_elements_highlight("box")
actions.user.ui_elements_highlight_briefly("box")
actions.user.ui_elements_unhighlight("box")

# def hide
global my_ui
my_ui.hide()
```

If you use a button, the canvas will block the mouse instead of being pass through.
```py
# button
button("Click me", on_click=lambda: print("clicked")),
button("Click me", on_click=actions.user.hide_my_custom_ui),
```

If we have a list of commands, we can populate it into a div like this:
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

## CSS Options

| CSS Property | Type |
| -- | -- |
| align_items | `'flex_start'`, `'flex_end'`, `'center'` |
| background_color | `str` - 6 digits with 2 optional ending digits for opacity e.g. `'FF0000'` or `FF000088` for opacity of `88` from `00` to `FF` |
| bold | `bool` |
| border_color | `str` |
| border_radius | `int` |
| border_width | `int` |
| bottom | `int` |
| color | `str` - 6 digits with 2 optional ending digits for opacity e.g. `'FF0000'` or `FF000088` for opacity of `88` from `00` to `FF` |
| flex_direction | `'row'`, `'column'` |
| font_size | `int` - for text |
| font_weight | `str` |
| gap | `int` |
| height | `int` |
| highlight_color | `str` - 6 digits with 2 optional ending digits for opacity e.g. `'FF0000'` or `FF000088` for opacity of `88` from `00` to `FF` |
| id | `str` - Required on builder, and for 'highlight' feature to work on a div |
| justify | `str` |
| justify_content | 'flex_start', 'flex_end', 'center' |
| left | `int` |
| margin | `int` - Margin in every direction |
| margin_bottom | `int` |
| margin_left | `int` |
| margin_right | `int` |
| margin_top | `int` |
| on_click | `function` - Function to call when clicked |
| padding | `int` - Padding in every direction |
| padding_bottom | `int` |
| padding_left | `int` |
| padding_right | `int` |
| padding_top | `int` |
| right | `int` |
| top | `int` |
| width | `int` |