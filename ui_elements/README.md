# ui_elements

This is an experimental repository for making any generic UI in HTML-like syntax. Currently supports `div`, `screen`, `text`. In the future I would like to add buttons and inputs. WIP.

## Usage

first we tell ui_elements what we want to use:
```py
(css, div, text, screen) = actions.user.ui_elements(["css", "div", "text", "screen"])
```

the outermost layer must be the screen component
```py
my_ui = screen()[
    div()[
        ...
    ]
]
```

To define css, we put it inside of the parentheses, and to define children, we put it inside the square brackets. let's give it 1 div, positioned to the right center:
```py
my_ui = screen(align_items="flex_end", justify_content="center")[
    div()[
        text("Hello world")
    ]
]
```

by default everything operates under the assumption of `display: flex`, and all properties are the same wording as regular css syntax, including `padding`, `margin`, etc...

`background_color` accepts two extra characters at the end, which are the opacity

here's a full example:


```py
global my_ui

# def show
global my_ui
(css, div, text, screen) = actions.user.ui_elements(["css", "div", "text", "screen"])
my_ui = screen(align_items="flex_end", justify_content="center")[
    div(id="box", padding=16, background_color="FF000088")[
        text("Hello world", color="FFFFFF"),
        text("Test", id="test", font_size=24)
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
| padding | `int` - Padding in every direction |
| padding_bottom | `int` |
| padding_left | `int` |
| padding_right | `int` |
| padding_top | `int` |
| right | `int` |
| top | `int` |
| width | `int` |