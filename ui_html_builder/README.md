# ui_html_builder

Build a UI using a object oriented html style. Supports common css properties such as:

- [ui\_html\_builder](#ui_html_builder)
  - [Actions](#actions)
  - [CSS Options](#css-options)
  - [Example command list with 2 columns](#example-command-list-with-2-columns)
  - [Example dpad display with highlighting](#example-dpad-display-with-highlighting)

## Actions

| Method | Description |
| -- | -- |
| `builder = actions.user.ui_html_builder_screen(**options)` | Create a new html builder from the screens dimensions |
| `div = builder.add_div(**options)` | Add div to the builder |
| `child_div = div.add_div(**options)` | Add div to a div |
| `builder.add_text("text", **options)` | Add a text element |
| `div.add_text("text", **options)` | Add a text element |
| `builder.show()` | Show the UI |
| `builder.hide()` | Hide the UI |
| `builder.highlight('id_name')` | Highlight a div by id |
| `builder.unhighlight('id_name')` | Unhighlight a div by id |
| `builder.highlight_briefly('id_name')` | Highlight a div by id briefly |

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
| size | `int` - for text |
| top | `int` |
| width | `int` |

## Example command list with 2 columns

**Example**: Show a "Command | Action" list of commands on the right side of screen in the center
```py
builder = actions.user.ui_html_builder_screen(
    id="commands",
    justify_content="flex_end",
    align_items="center",
)

box = builder.add_div(
    flex_direction="row",
    padding=16,
    gap=16,
    background_color="00000088" # color: 000000, opacity: 88
)

commands_column = box.add_div(gap=8)
commands_column.add_text("Command", font_weight="bold")
commands_column.add_text("hello")
commands_column.add_text("peanut")
commands_column.add_text("french")

actions_column = box.add_div(gap=8)
actions_column.add_text("Action", font_weight="bold")
actions_column.add_text("world")
actions_column.add_text("butter")
actions_column.add_text("fries")

builder.show()

# later
builder.hide()
```

---

## Example dpad display with highlighting

**Example**: Make a dpad that highlights when the key is active at the top left of your screen
```py
builder = actions.user.ui_html_css_builder_screen(
    id="keys",
    justify_content="flex_start",
    align_items="flex_start",
    highlight_color="87ceeb88",
)

dpad = gamepad.add_div(
    flex_direction="column",
)

key_css = {
    "padding": 8,
    "background_color": "333333dd",
    "flex_direction": "row",
    "justify_content": "center",
    "align_items": "center",
    "margin": 1,
    "width": 30,
    "height": 30,
}

first_row = dpad.add_div(flex_direction="row")
first_row.add_div(**key_css).add_text(' ')
first_row.add_div(**{**key_css, 'id': 'W'}).add_text('W')
first_row.add_div(**key_css).add_text(' ')

second_row = dpad.add_div(flex_direction="row")
second_row.add_div(**key_css).add_text('A').add_text('A')
second_row.add_div(**{**key_css, 'id': 'S'}).add_text('S')
second_row.add_div(**key_css).add_text('D').add_text('D')

builder.show()

# highlighting the keys
builder.highlight('A') # targeting the 'id'
builder.unhighlight('S')

builder.highlight_briefly('D')

# later
builder.hide()
```