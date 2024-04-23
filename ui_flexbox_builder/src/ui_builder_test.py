import unittest
from unittest.mock import Mock
from ui_builder import UIBuilder, UIContainer, UITextOptions, BoxModelLayout, Rect, UIOptions, Padding, Margin

class TestUIBuilder(unittest.TestCase):
    def setup(self):
        self.default_margin = Margin(10, 10, 10, 10)
        self.default_padding = Padding(5, 5, 5, 5)
        self.options = UIOptions(margin=self.default_margin, padding=self.default_padding)

    def test_create_ui(self):
        container = UIContainer(self.options)
        cursor_mock = Mock(x=0, y=0, virtual_x=0, virtual_y=0)
        canvas_mock = Mock()

        container.virtual_render(canvas_mock, cursor_mock)

        expected_x = self.options.margin.left + self.options.padding.left
        expected_y = self.options.margin.top + self.options.padding.top
        self.assertEqual(cursor_mock.virtual_x, expected_x)
        self.assertEqual(cursor_mock.virtual_y, expected_y)

if __name__ == '__main__':
    unittest.main()
