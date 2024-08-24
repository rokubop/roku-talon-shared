
from talon import Module, actions, ui
from talon.screen import Screen
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia import RoundRect
from talon.types import Rect, Point2d

mod = Module()

builders = {}
colors = {
    'gold': 'FFD700',
    'white': 'ffffff',
    'dark': '222222',
}

def draw_center_text(c: SkiaCanvas, text: str, x: int, y: int):
    text_rect = c.paint.measure_text(text)[1]
    text_rect_default = c.paint.measure_text("ABC")[1]
    c.draw_text(
        text,
        x + text_rect.x - text_rect.width / 2,
        y - text_rect_default.y - text_rect_default.height / 2,
    )

class Cursor:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y

    def move_down(self, amount):
        """Move the cursor down by 'amount'."""
        self.y += amount

    def move_up(self, amount):
        """Move the cursor up by 'amount'."""
        self.y -= amount

    def move_right(self, amount):
        """Move the cursor right by 'amount'."""
        self.x += amount

    def reset_x(self):
        """Reset the cursor's x position (for new lines or alignment)."""
        self.x = self.start_x

    def set(self, x, y):
        """Set the cursor's position."""
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y

class UIFlexboxBuilder:
    def __init__(self, config=None):
        self.config = config if config else {}
        self.components = []
        self.id = self.config.get('id', None)
        self._ids = []
        self.align = self.config.get('align', 'center')
        self.width = self.config.get('width', None)
        self.margin_left = self.config.get('margin_left', 0)
        self.margin_top = self.config.get('margin_top', 0)
        self.margin_right = self.config.get('margin_right', 0)
        self.margin_bottom = self.config.get('margin_bottom', 0)
        self.darken = self.config.get('darken', False)
        self.canvas = None
        self.padding = self.config.get('padding', 24)
        self.gap = 20
        self.cursor = Cursor(start_x=0, start_y=0)
        self.rect = None
        self.clickables = {}
        self.content_edges = Rect(0, 0, 0, 0)
        self.next_gap = 0

    def debug_cursor(self, c: SkiaCanvas):
        cursor = self.cursor
        c.paint.color = "FF0000"
        c.draw_line(cursor.x, cursor.y, cursor.x + 10, cursor.y)
        c.draw_line(cursor.x, cursor.y, cursor.x, cursor.y + 10)

    def add_component(self, component):
        """Add a component to the flexbox layout."""
        self.components.append(component)

    def add_title(self, title):
        self.add_component({'type': 'title', 'text': title})

    def add_header(self, options):
        if isinstance(options, str):
            title = options
            options = {}
        else:
            title = options.get('title', '')
            options = options

        self.add_component({
            'type': 'header',
            'text': title,
            **options
        })

    def add_line(self):
        self.add_component({'type': 'line'})

    def add_text(self, text, size=16, id="", color="ffffff", margin_top=0, margin_bottom=0, margin_left=0, margin_right=0, margin=0):
        component = {
            'id': id,
            'type': 'text',
            'text': text,
            'size': size,
            'color': color,
            'margin_top': margin_top,
            'margin_bottom': margin_bottom,
            'margin_left': margin_left,
            'margin_right': margin_right,
            'margin': margin,
        }
        self.add_component(component)

    def add_link(self, link):
        component = {
            'type': 'link',
            'text': link["text"],
            'action': link["action"],
            'margin_top': link.get('margin_top', 0),
            'margin_bottom': link.get('margin_bottom', 0),
            'margin_left': link.get('margin_left', 0),
            'margin_right': link.get('margin_right', 0),
            'color': link.get('color', 'FFFF00'),
        }
        self.add_component(component)

    def add_link_group(self, links):
        self.add_component({'type': 'link_group', 'links': links})

    def add_key_value(self, key, value):
        self.add_component({'type': 'key_value', 'key': key, 'value': value})

    def add_gap(self, amount=6):
        self.add_component({'type': 'gap', 'amount': amount})

    def add_code_block(self, code):
        self.add_component({'type': 'code_block', 'code': code})

    def add_button_group(self, buttons):
        self.add_component({'type': 'button_group', 'buttons': buttons})

    def add_button(self, button):
        self.add_component({'type': 'button', 'text': button['text'], 'action': button['action'], 'primary': button.get('primary', False)})

    def add_placeholder(self, id, height):
        self.add_component({'type': 'placeholder', 'id': id, 'height': height})

    def on_mouse(self, e):
        if e.event == "mousemove":
            for clickable in self.clickables.values():
                hovering = clickable["rect"].contains(e.gpos)
                if clickable["is_hovering"] != hovering:
                    clickable["is_hovering"] = hovering
                    self.canvas.freeze()
        elif e.event == "mousedown":
            for clickable in self.clickables.values():
                hovering = clickable["rect"].contains(e.gpos)
                if clickable["is_hovering"]:
                    clickable["action"]()

    def accumulate_content_edges(self, rect):
        if self.content_edges.x == 0 or rect.x < self.content_edges.x:
            self.content_edges.x = rect.x
        if self.content_edges.y == 0 or rect.y < self.content_edges.y:
            self.content_edges.y = rect.y
        if rect.x + rect.width > self.content_edges.x + self.content_edges.width:
            self.content_edges.width = rect.x + rect.width - self.content_edges.x
        if rect.y + rect.height > self.content_edges.y + self.content_edges.height:
            self.content_edges.height = rect.y + rect.height - self.content_edges.y

    def draw_line(self, c: SkiaCanvas):
        c.paint.stroke_width = 1
        c.paint.color = f"ffffff99"
        line_width = self.rect.width - self.padding * 2
        c.draw_line(self.cursor.x, self.cursor.y, self.cursor.x + line_width, self.cursor.y)
        bounding_rect = Rect(self.cursor.x, self.cursor.y, line_width, 1)
        self.cursor.move_down(16)
        return bounding_rect

    def draw_title(self, c: SkiaCanvas, title: str):
        self.cursor.move_down(self.next_gap)
        c.paint.textsize = 18
        c.paint.font.embolden = True
        c.paint.color = "ffffff"
        self.cursor.move_down(18)
        c.draw_text(title, self.cursor.x, self.cursor.y)
        bounding_rect = Rect(self.cursor.x, self.cursor.y - 18, c.paint.measure_text(title)[1].width, 18)
        self.next_gap = int(self.gap * 1.75)
        c.paint.font.embolden = False
        return bounding_rect

    def draw_header(self, c: SkiaCanvas, title: str):
        self.debug_cursor(c)
        self.cursor.move_down(self.next_gap)
        c.paint.textsize = 18
        c.paint.font.embolden = True
        c.paint.color = "ffffff"
        self.cursor.move_down(18)
        c.draw_text(title, self.cursor.x, self.cursor.y)
        bounding_rect = Rect(self.cursor.x, self.cursor.y - 18, c.paint.measure_text(title)[1].width, 18)
        self.next_gap = int(self.gap * 1.75)
        c.paint.font.embolden = False
        return bounding_rect

    def draw_placeholder(self, c: SkiaCanvas, id: str, height: int):
        self.cursor.move_down(self.next_gap)
        self.cursor.move_down(height)
        bounding_rect = Rect(self.cursor.x, self.cursor.y - height, 0, height)
        self.next_gap = self.gap
        return bounding_rect

    def draw_text(self, c: SkiaCanvas, text: str, size: int = 16, color: str = "ffffff", margin_top=0, margin_bottom=0, margin_left=0, margin_right=0, margin=0):
        self.cursor.move_down(self.next_gap)
        c.paint.textsize = size
        c.paint.color = color
        c.paint.style = c.paint.Style.FILL
        self.cursor.move_down(size)
        c.draw_text(text, self.cursor.x, self.cursor.y)
        bounding_rect = Rect(self.cursor.x, self.cursor.y - size, c.paint.measure_text(text)[1].width, size)
        if margin_bottom:
            self.cursor.move_down(margin_bottom)
        self.next_gap = self.gap
        return bounding_rect

    def draw_link(self, c: SkiaCanvas, text: str, action: callable):
        self.cursor.move_down(self.next_gap)
        c.paint.textsize = 16
        is_hovering = self.clickables.get(text, {}).get("is_hovering", False)
        if is_hovering:
            c.paint.color = "FFFF99"
        else:
            c.paint.color = colors['gold']
        c.paint.style = c.paint.Style.FILL
        self.cursor.move_down(16)
        c.draw_text(text, self.cursor.x, self.cursor.y)
        text_width = c.paint.measure_text(text)[1].width
        self.cursor.move_down(5)
        c.draw_line(self.cursor.x, self.cursor.y, self.cursor.x + text_width, self.cursor.y)

        bounding_rect = Rect(self.cursor.x, self.cursor.y - 16, text_width, 16 +5)
        if text not in self.clickables or self.clickables[text]["rect"] != bounding_rect:
            self.clickables[text] = {
                "rect": bounding_rect,
                "is_hovering": False,
                "action": action,
            }
        self.next_gap = self.gap
        return bounding_rect

    def draw_key_value(self, c: SkiaCanvas, key: str, value: str):
        self.cursor.move_down(self.next_gap)
        c.paint.textsize = 16
        c.paint.color = colors['white']
        c.paint.style = c.paint.Style.FILL
        width_key = c.paint.measure_text(key)[1].width
        width_value = c.paint.measure_text(value)[1].width
        self.cursor.move_down(16)
        c.draw_text(key, self.cursor.x, self.cursor.y)
        c.paint.color = colors['gold']
        c.draw_text(value, self.cursor.x + width_key + 16, self.cursor.y)
        total_width = width_key + width_value + 16
        total_height = 16
        bounding_rect = Rect(self.cursor.x, self.cursor.y - 16, total_width, total_height)
        self.next_gap = self.gap
        return bounding_rect

    def draw_code_block(self, c: SkiaCanvas, code: str):
        self.cursor.move_down(self.next_gap)
        c.paint.textsize = 14
        lines = code.split('\n')
        height = 0
        max_width = 0
        for line in lines:
            text_rect = c.paint.measure_text(line)[1]
            max_width = max(max_width, text_rect.width)
            height += 24
        height += 16
        max_width += 32
        c.paint.color = "222222"
        rrect = RoundRect.from_rect(Rect(self.cursor.x, self.cursor.y, max_width, height), x=10, y=10)
        bounding_rect = Rect(self.cursor.x, self.cursor.y, max_width, height)
        c.draw_rrect(rrect)
        self.cursor.move_right(16)
        c.paint.color = colors['gold']
        for line in lines:
            self.cursor.move_down(24)
            c.draw_text(line, self.cursor.x, self.cursor.y)
        self.cursor.move_down(16)
        self.cursor.reset_x()
        self.next_gap = self.gap
        return bounding_rect

    def draw_button(self, c: SkiaCanvas, button):
        self.cursor.move_down(self.next_gap)
        text = button["text"]
        text_width = c.paint.measure_text(text)[1].width
        button_rect = Rect(self.cursor.x, self.cursor.y, text_width + 32, 32)
        rrect = RoundRect.from_rect(button_rect, x=10, y=10)
        c.paint.style = c.paint.Style.FILL
        is_hovering = self.clickables.get(text, {}).get("is_hovering", False)
        if button.get("primary", False):
            c.paint.color = "FFD70099" if is_hovering else "FFD70066"
        else:
            c.paint.color = "FFD70033" if is_hovering else "FFD70011"
        c.draw_rrect(rrect)
        c.paint.color = "FFD70066"
        c.paint.style = c.paint.Style.STROKE
        c.draw_rrect(rrect)
        c.paint.color = "ffffff"
        c.paint.style = c.paint.Style.FILL
        draw_center_text(c, text, button_rect.x + button_rect.width / 2, button_rect.y + button_rect.height / 2)
        if text not in self.clickables or self.clickables[text]["rect"] != button_rect:
            self.clickables[text] = {
                "rect": button_rect,
                "is_hovering": False,
                "action": button["action"],
            }
        self.cursor.move_down(48)
        self.next_gap = self.gap
        return button_rect

    def draw_background(self, c: SkiaCanvas):
        screen: Screen = ui.main_screen()
        rect = screen.rect
        if self.darken:
            c.paint.color = "00000055"
            c.draw_rect(rect)
        if self.width:
            self.content_edges.width = self.width
        box_size = self.content_edges
        box_size_padded = Rect(box_size.x - self.padding, box_size.y - self.padding, box_size.width + self.padding * 2, box_size.height + self.padding * 2)
        screen_center = Point2d(rect.width / 2, rect.height / 2)
        modal_top_y = screen_center.y - box_size_padded.height / 2
        modal_left_x = screen_center.x - box_size_padded.width / 2
        if self.align == 'left':
            modal_left_x = 0
        elif self.align == 'right':
            modal_left_x = rect.width - box_size_padded.width
        elif self.align == 'top':
            modal_top_y = 0
        elif self.align == 'bottom':
            modal_top_y = rect.height - box_size_padded.height
        elif self.align == 'top_left':
            modal_left_x = 0
            modal_top_y = 0
        elif self.align == 'top_right':
            modal_left_x = rect.width - box_size_padded.width
            modal_top_y = 0
        elif self.align == 'bottom_left':
            modal_left_x = 0
            modal_top_y = rect.height - box_size_padded.height
        elif self.align == 'bottom_right':
            modal_left_x = rect.width - box_size_padded.width
            modal_top_y = rect.height - box_size_padded.height
        if self.margin_left:
            modal_left_x += self.margin_left
        if self.margin_top:
            modal_top_y += self.margin_top
        if self.margin_right:
            modal_left_x -= self.margin_right
        if self.margin_bottom:
            modal_top_y -= self.margin_bottom
        self.rect = Rect(modal_left_x, modal_top_y, box_size_padded.width, box_size_padded.height)
        rect = self.rect

        c.paint.style = c.paint.Style.FILL
        shadow_rect = Rect(rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4)
        c.paint.color = f"6082B633"
        c.draw_rrect(RoundRect.from_rect(shadow_rect, x=12, y=12))
        c.paint.color = f"00000099"
        shadow_rect = Rect(rect.x - 1, rect.y - 1, rect.width + 2, rect.height + 2)
        c.draw_rrect(RoundRect.from_rect(shadow_rect, x=11, y=11))

        c.paint.stroke_width = 1
        c.paint.color = f"333333"
        c.paint.style = c.paint.Style.FILL
        c.draw_rrect(RoundRect.from_rect(rect, x=10, y=10))

        c.paint.color = f"ffffff66"
        c.paint.style = c.paint.Style.STROKE
        c.draw_rrect(RoundRect.from_rect(rect, x=10, y=10))
        c.paint.style = c.paint.Style.FILL

        self.cursor.set(self.rect.x + self.padding, self.rect.y + self.padding)

    def on_ui_update(self, c: SkiaCanvas):
        redraw = False
        if not self.content_edges.width:
            redraw = True
        self.draw_background(c)
        self.next_gap = 0
        for component in self.components:
            if component['type'] == 'title':
                bounds = self.draw_title(c, component['text'])
                self.accumulate_content_edges(bounds)
            elif component['type'] == 'header':
                bounds = self.draw_header(c, component['text'])
                self.accumulate_content_edges(bounds)
            elif component['type'] == 'line':
                bounds = self.draw_line(c)
                self.accumulate_content_edges(bounds)
            elif component['type'] == 'key_value':
                bounds = self.draw_key_value(c, component['key'], component['value'])
                self.accumulate_content_edges(bounds)
            elif component['type'] == 'gap':
                self.cursor.move_down(component['amount'])
                self.accumulate_content_edges(bounds)
            elif component['type'] == 'text':
                omit = ['type', 'rect', 'id']
                kwargs = {k: v for k, v in component.items() if k not in omit}
                bounds = self.draw_text(c, **kwargs)
                self.accumulate_content_edges(bounds)
            elif component['type'] == 'link':
                bounds = self.draw_link(c, component['text'], component['action'])
                self.accumulate_content_edges(bounds)
            elif component['type'] == 'link_group':
                for i, link in enumerate(component['links']):
                    bounds = self.draw_link(c, link['text'], link['action'])
                    self.cursor.move_right(bounds.width + 16)
                    self.cursor.move_up(16 + 5)
                    self.cursor.move_up(self.next_gap)
                    self.accumulate_content_edges(bounds)
                self.cursor.reset_x()
                self.cursor.move_down(16 + 5 + self.next_gap)
            elif component['type'] == 'code_block':
                bounds = self.draw_code_block(c, component['code'])
                self.accumulate_content_edges(bounds)
            elif component['type'] == 'button':
                bounds = self.draw_button(c, component)
                self.accumulate_content_edges(bounds)
            elif component['type'] == 'button_group':
                for i, button in enumerate(component['buttons']):
                    bounds = self.draw_button(c, button)
                    self.cursor.move_right(bounds.width + 16)
                    self.cursor.move_up(48)
                    self.cursor.move_up(self.next_gap)
                    self.accumulate_content_edges(bounds)
                self.cursor.reset_x()
                self.cursor.move_down(48)
            elif component['type'] == 'placeholder':
                bounds = self.draw_placeholder(c, component['id'], component['height'])
                self.accumulate_content_edges(bounds)
        if redraw:
            self.canvas.freeze()

    def show(self):
        screen: Screen = ui.main_screen()
        rect = screen.rect
        print(rect.width, rect.height)
        self.canvas = Canvas.from_screen(screen)
        self.canvas.register("draw", self.on_ui_update)
        has_clickables = any(['button' in c['type'] or 'link' in c['type'] for c in self.components])
        if has_clickables:
            self.canvas.blocks_mouse = True
            self.canvas.register("mouse", self.on_mouse)
        self.canvas.freeze()

    def redraw(self):
        if self.canvas:
            self.canvas.freeze()

    def hide(self):
        if self.canvas:
            self.canvas.unregister("draw", self.on_ui_update)
            self.canvas.unregister("mouse", self.on_mouse)
            self.canvas.hide()
            self.canvas.close()
            self.canvas = None

    def update_id(self, id: str, config: dict):
        self._ids[id]
        if self.canvas:
            self.canvas.freeze()

    def get_components(self):
        return self.components

@mod.action_class
class Actions:
    def ui_flexbox_builder(config: dict) -> UIFlexboxBuilder:
        """Create a flexbox builder"""
        global builders
        if config.get('id') in builders:
            actions.user.ui_flexbox_hide(config.get('id'))
        builder = UIFlexboxBuilder(config)
        builders[builder.id] = builder
        return builder

    def ui_flexbox_hide(id: str):
        """Hide the element with the given id"""
        global builders
        if id in builders:
            builders[id].hide()

    def ui_flexbox_builder_update(config: dict):
        """Hide the element with the given id"""
        global builders
        builder_id = config.get('id')
        if builder_id in builders:
            for component in config['components']:
                components_with_ids = [c for c in builders[builder_id].components if 'id' in c]
                for existing in components_with_ids:
                    if component.get('id') == existing.get('id'):
                        existing.update(component)
            builders[builder_id].redraw()