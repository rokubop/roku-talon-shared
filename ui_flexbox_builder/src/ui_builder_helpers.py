from talon.types import Rect

def grow_rect(orig_rect: Rect, new_rect: Rect):
    if new_rect.x < orig_rect.x:
        orig_rect.width += orig_rect.x - new_rect.x
        orig_rect.x = new_rect.x
    if new_rect.y < orig_rect.y:
        orig_rect.height += orig_rect.y - new_rect.y
        orig_rect.y = new_rect.y
    if new_rect.x + new_rect.width > orig_rect.x + orig_rect.width:
        orig_rect.width = new_rect.x + new_rect.width - orig_rect.x
    if new_rect.y + new_rect.height > orig_rect.y + orig_rect.height:
        orig_rect.height = new_rect.y + new_rect.height - orig_rect.y