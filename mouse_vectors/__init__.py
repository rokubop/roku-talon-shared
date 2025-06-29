"""
Mouse Vectors System Package
A physics-based mouse motion system using force vectors.
"""

from .mouse_vectors import (
    mouse_vectors,
    mouse_vectors_get_state,
    mouse_vectors_stop,
    mouse_vectors_disable,
    mouse_vectors_remove,
    mouse_vectors_list
)

__version__ = "1.0.0"
__author__ = "Roku"
__description__ = "Physics-based mouse motion system using force vectors"

__all__ = [
    "mouse_vectors",
    "mouse_vectors_get_state",
    "mouse_vectors_stop",
    "mouse_vectors_disable",
    "mouse_vectors_remove",
    "mouse_vectors_list"
]
