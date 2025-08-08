"""
Mouse Move Adv
Continous = Move the mouse continuously until manually stopped
Smooth = Move the mouse smoothly over a duration
Tick = Move the mouse a short distance in a direction
"""
from talon import Module, actions, ctrl, cron, settings, ui
from typing import Callable, Literal, Union
from dataclasses import dataclass
import platform
import math
import time
from talon.screen import Screen

mod = Module()
mod.setting("mouse_move_api", default="talon", type=str, desc="Mouse API to use for mouse movement - talon or windows")
mod.setting("mouse_move_continuous_speed_default", default=2, type=int, desc="Default speed for continuous mouse movement")
mod.setting("mouse_move_tick_distance", default=50, type=int, desc="Distance for mouse_move_tick_last_direction")
mod.setting("mouse_move_smooth_duration", default=200, type=int, desc="Speed for mouse_move_smooth_delta")

_mouse_job = None
_last_mouse_job_type = None
_mouse_movement_queue = []
_mouse_continuous_start_ts = None
_mouse_continuous_stop_ts = None
_mouse_continuous_dir = None
_mouse_continuous_speed_default = 2
_mouse_continuous_speed = _mouse_continuous_speed_default
dir_change_event_subscribers = []
mouse_move_event_subscribers = []

@dataclass
class UnitVector:
    x: float
    y: float

_last_unit_vector = UnitVector(0, 0)

@dataclass
class MouseMoveCallbackEvent:
    x: float
    y: float
    dx: float
    dy: float
    type: Literal["start", "tick", "stop"]

class MouseInfo:
    def __init__(self):
        self.last_unit_vector = _last_unit_vector
        self.last_cardinal_dir = unit_vector_to_cardinal_dir()
        self.continuous_active = _mouse_continuous_start_ts
        self.is_moving = bool(_mouse_job)

    def __getitem__(self, key):
        return getattr(self, key)

easing_types = {
    "linear": lambda x: x,
    "ease_in_out": lambda x: math.sin(x * math.pi / 2),
    "ease_in": lambda x: 1 - math.cos(x * math.pi / 2),
    "ease_out": lambda x: math.sin(x * math.pi / 2),
    "instant": lambda x: 1 if x >= 1 else 0,
}

def mouse_move_talon(dx: int, dy: int):
    (x, y) = ctrl.mouse_pos()
    ctrl.mouse_move(x + dx, y + dy)

def mouse_move_windows(dx: int, dy: int):
    pass

def mouse_move(dx: int, dy: int):
    if settings.get("user.mouse_move_api") == "windows":
        mouse_move_windows(dx, dy)
    else:
        mouse_move_talon(dx, dy)

if platform.system() == "Windows":
    import win32api, win32con
    def mouse_move_windows(dx: int, dy: int):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy)

def mouse_move_smooth_queue(fn: callable):
    """Add to movement _mouse_movement_queue, executed after next mouse_stop."""
    global _mouse_movement_queue
    _mouse_movement_queue.append(fn)

def unit_vector_to_cardinal_dir():
    if not _last_unit_vector:
        return None
    x = _last_unit_vector.x
    y = _last_unit_vector.y
    if x == 0 and y == 0:
        return None
    if abs(x) > abs(y):
        return "right" if x > 0 else "left"
    return "down" if y > 0 else "up"

CurveTypes = Literal["linear", "ease_in_out", "ease_in", "ease_out"]

class SubpixelAdjuster:
    """
    Some apis require ints, but that will throw off our calculations
    over time. This class helps us keep track of the fractional part
    of the delta so we can keep track of the accumulated error and
    adjust the int part accordingly.
    """
    def __init__(self):
        self.dx_frac = 0.0
        self.dy_frac = 0.0

    def update_pos(self, dx: Union[int, float], dy: Union[int, float]):
        dx_int = int(dx)
        dy_int = int(dy)

        self.dx_frac += dx - dx_int
        self.dy_frac += dy - dy_int

        if abs(self.dx_frac) >= 0.5:
            dx_int += int(math.copysign(1, self.dx_frac))
            self.dx_frac -= int(math.copysign(1, self.dx_frac))

        if abs(self.dy_frac) >= 0.5:
            dy_int += int(math.copysign(1, self.dy_frac))
            self.dy_frac -= int(math.copysign(1, self.dy_frac))

        return dx_int, dy_int

def convert_to_unit_vector(dx: int, dy: int):
    """Convert a delta to a unit vector (length of 1) """
    magnitude = math.sqrt(dx ** 2 + dy ** 2)
    return UnitVector(dx / magnitude, dy / magnitude)

def mouse_move_smooth_delta(
    dx_total: Union[int, float],
    dy_total: Union[int, float],
    duration_ms: int = None,
    callback_tick: Callable[[MouseMoveCallbackEvent], None] = None,
    callback_stop: Callable[[], None] = None,
    easing_type: Literal["linear", "ease_in_out", "ease_in", "ease_out"] = "ease_in_out",
    mouse_api_type: Literal["talon", "windows"] = None):
    """
    Move the mouse in a natural way over a duration.
    Examples:
    ```
    mouse_move_smooth_delta(300, 0, 200) # 300 right over 200ms
    mouse_move_smooth_delta(0, -1000, 2000) # 1000 up over 2s

    Callback example:
    def callback_tick(ev):
        # ev.dx_total
        # ev.dy_total
        # ev.type # "start", "tick", "stop"
    mouse_move_smooth_delta(100, 0, 100, callback_tick)
    ```
    """
    global _mouse_job, _last_mouse_job_type, _last_unit_vector
    duration_ms = duration_ms or settings.get("user.mouse_move_smooth_duration")
    mouse_stop(start_next_queue=False)

    _last_mouse_job_type = "natural"
    update_interval_ms = 16
    steps = max(1, duration_ms // update_interval_ms)
    step_count = 0
    last_x, last_y = 0, 0
    _last_unit_vector = convert_to_unit_vector(dx_total, dy_total)
    mouse_move_dir_change_event_trigger(_last_unit_vector.x, _last_unit_vector.y)
    convert_linear_to_curve = easing_types[easing_type]
    subpixel_adjuster = SubpixelAdjuster()

    mouse_move_fn = mouse_move

    if not mouse_api_type:
        mouse_api_type = settings.get("user.mouse_move_api")

    if mouse_api_type == "windows":
        mouse_move_fn = mouse_move_windows
    elif mouse_api_type == "talon":
        mouse_move_fn = mouse_move_talon

    def update_position():
        nonlocal step_count, last_x, last_y, mouse_move_fn

        step_count += 1
        if step_count > steps:
            mouse_stop()
            (x, y) = ctrl.mouse_pos()
            if mouse_move_event_subscribers:
                mouse_move_event_trigger(MouseMoveCallbackEvent(x, y, dx_total, dy_total, "stop"))
            if callback_tick:
                callback_tick(MouseMoveCallbackEvent(x, y, dx_total, dy_total, "stop"))
            if callback_stop:
                callback_stop()
            return
        progress = step_count / steps
        curve_progress = convert_linear_to_curve(progress)

        current_x = dx_total * curve_progress
        current_y = dy_total * curve_progress

        dx_step = current_x - last_x
        dy_step = current_y - last_y

        (int_dx_step, int_dy_step) = subpixel_adjuster.update_pos(dx_step, dy_step)

        mouse_move_fn(int_dx_step, int_dy_step)

        last_x, last_y = current_x, current_y
        if callback_tick:
            (x, y) = ctrl.mouse_pos()
            callback_tick(MouseMoveCallbackEvent(x, y, current_x, current_y, "tick"))

    update_position()
    _mouse_job = cron.interval("16ms", update_position)
    (x, y) = ctrl.mouse_pos()
    if mouse_move_event_subscribers:
        mouse_move_event_trigger(MouseMoveCallbackEvent(x, y, dx_total, dy_total, "start"))
    if callback_tick:
        callback_tick(MouseMoveCallbackEvent(x, y, 0, 0, "start"))

def mouse_stop(start_next_queue: bool = True):
    """Stop current mouse movement, and start next in the _mouse_movement_queue if it exists."""
    global _mouse_job, _mouse_movement_queue, _last_mouse_job_type, _mouse_continuous_dir, _mouse_continuous_start_ts, _mouse_continuous_stop_ts
    if _mouse_job:
        cron.cancel(_mouse_job)
        _mouse_job = None
        _last_mouse_job_type = None
        _last_unit_vector = None
        _mouse_continuous_dir = None
        _mouse_continuous_start_ts = None
        _mouse_continuous_stop_ts = None
        if mouse_move_event_subscribers:
            mouse_move_event_trigger(MouseMoveCallbackEvent(0, 0, 0, 0, "stop"))
        mouse_move_dir_change_event_trigger(0, 0)
    if start_next_queue and len(_mouse_movement_queue) > 0:
        fn = _mouse_movement_queue.pop(0)
        fn()

def mouse_move_continuous(dx_unit: Union[int, float], dy_unit: Union[int, float], speed_initial: int = None):
    """
    Move the mouse continuously.
    Examples:
    ```
    mouse_move_continuous(1, 0) # right at default speed_initial
    mouse_move_continuous(-1, 0) # left at default speed_initial
    mouse_move_continuous(0, 1, 5) # down at speed_initial 5
    mouse_move_continuous(1, -1, 10) # right and up at speed_initial 10
    ```
    """
    global _mouse_job, _last_unit_vector, _mouse_continuous_start_ts, _mouse_continuous_stop_ts, _last_mouse_job_type, _mouse_continuous_speed
    speed_initial = speed_initial or settings.get("user.mouse_move_continuous_speed_default")
    _mouse_continuous_stop_ts = None
    subpixel_adjuster = None
    unit_vector = convert_to_unit_vector(dx_unit, dy_unit)
    last_mouse_job_type = _last_mouse_job_type
    _last_mouse_job_type = "continuous"

    def init(reset_speed=True):
        nonlocal subpixel_adjuster
        global _mouse_continuous_speed, _last_unit_vector, _mouse_continuous_start_ts
        _mouse_continuous_speed = speed_initial if reset_speed else _mouse_continuous_speed
        _last_unit_vector = unit_vector
        if mouse_move_event_subscribers:
            mouse_move_event_trigger(MouseMoveCallbackEvent(0, 0, dx_unit, dy_unit, "start"))
        mouse_move_dir_change_event_trigger(_last_unit_vector.x, _last_unit_vector.y)
        _mouse_continuous_start_ts = time.perf_counter()
        subpixel_adjuster = SubpixelAdjuster()

    if _mouse_job:
        if last_mouse_job_type == 'natural':
            mouse_stop(start_next_queue=False)
        if _last_unit_vector != unit_vector:
            init(reset_speed=False)
        # else already in progress
        return

    init()

    def update_position():
        global _mouse_continuous_stop_ts, _mouse_continuous_speed, _last_unit_vector
        ts = time.perf_counter()

        if _mouse_continuous_stop_ts and ts - _mouse_continuous_stop_ts > 0:
            mouse_stop()
            return

        dx_int, dy_int = subpixel_adjuster.update_pos(
            _last_unit_vector.x * _mouse_continuous_speed,
            _last_unit_vector.y * _mouse_continuous_speed)
        mouse_move(dx_int, dy_int)

    update_position()
    _mouse_job = cron.interval("16ms", update_position)

def mouse_move_continuous_towards(x: int, y: int, speed_initial: int = None):
    """
    Move the mouse continuously towards xy coordinate.
    Examples:
    ```
    (x, y) = ctrl.mouse_pos()
    mouse_move_continuous_towards(x + 100, y + 100) # move mouse towards 100,100
    ```
    """
    current_pos = ctrl.mouse_pos()
    dx, dy = x - current_pos[0], y - current_pos[1]
    mouse_move_continuous(dx, dy, speed_initial)
    return

def mouse_move_continuous_stop(debounce_ms: int = 150):
    """
    Stop continuous mouse movement with optional debounce.
    e.g. hissing may start and stop continuously so we need to debounce.
    Examples:
    ```
    mouse_move_continuous_stop(0) # stop continuous movement immediately
    mouse_move_continuous_stop(150) # stop continuous movement with 150ms debounce
    ```
    """
    global _mouse_continuous_stop_ts
    debounce = debounce_ms / 1000 if debounce_ms else 0
    _mouse_continuous_stop_ts = time.perf_counter() + debounce

def mouse_move_smooth_from_to(
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        duration_ms: int = None,
        callback_tick: Callable[[MouseMoveCallbackEvent], None] = None,
        callback_stop: Callable[[], None] = None,
        mouse_api_type: Literal["talon", "windows"] = None):
    """
    Move the mouse from one point to another over a duration.
    Examples:
    ```
    mouse_move_smooth_from_to(100, 100, 200, 200, 500) # move from 100,100 to 200,200 over 500ms
    ```
    """
    dx = x2 - x1
    dy = y2 - y1
    actions.mouse_move(x1, y1)
    mouse_move_smooth_delta(dx, dy, duration_ms, callback_tick, callback_stop, mouse_api_type=mouse_api_type)

def mouse_move_event_dir_change_register(on_event: callable):
    dir_change_event_subscribers.append(on_event)

def mouse_move_event_dir_change_unregister(on_event: callable):
    dir_change_event_subscribers.remove(on_event)

def mouse_move_dir_change_event_trigger(x: float, y: float):
    for subscriber in dir_change_event_subscribers:
        subscriber(x, y)

def mouse_move_event_register(on_event: callable):
    mouse_move_event_subscribers.append(on_event)

def mouse_move_event_unregister(on_event: callable):
    mouse_move_event_subscribers.remove(on_event)

def mouse_move_event_trigger(event: MouseMoveCallbackEvent):
    for subscriber in mouse_move_event_subscribers:
        subscriber(event)

@mod.action_class
class Actions:
    def mouse_move_talon(dx: int, dy: int):
        """Move the mouse using talon api"""
        mouse_move_talon(dx, dy)

    def mouse_move_windows(dx: int, dy: int):
        """Move the mouse using windows api"""
        mouse_move_windows(dx, dy)

    def mouse_move_smooth_delta(
        dx: int,
        dy: int,
        duration_ms: int = None,
        callback_tick: Callable[[MouseMoveCallbackEvent], None] = None,
        callback_stop: Callable[[], None] = None,
        easing_type: Literal["linear", "ease_in_out", "ease_in", "ease_out"] = "ease_in_out",
        mouse_api_type: Literal["talon", "windows"] = None):
        """Move the mouse over a delta with control over the curve type, duration, mouse api type, and callback."""
        mouse_move_smooth_delta(dx, dy, duration_ms, callback_tick, callback_stop, easing_type, mouse_api_type=mouse_api_type)

    def mouse_move_smooth_from_to(
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        duration_ms: int = None,
        callback_tick: Callable[[MouseMoveCallbackEvent], None] = None,
        callback_stop: Callable[[], None] = None,
        easing_type: CurveTypes = "ease_in_out",
        mouse_api_type: Literal["talon", "windows"] = "talon"):
        """Move the mouse from one point to another over a duration."""
        dx = x2 - x1
        dy = y2 - y1
        # probably queue a move_to
        actions.mouse_move(x1, y1)
        mouse_move_smooth_delta(dx, dy, duration_ms, callback_tick, callback_stop, easing_type, mouse_api_type=mouse_api_type)

    def mouse_move_smooth_to(
        x: int,
        y: int,
        duration_ms: int = None,
        callback_tick: Callable[[MouseMoveCallbackEvent], None] = None,
        callback_stop: Callable[[], None] = None,
        easing_type: CurveTypes = "ease_in_out",
        mouse_api_type: Literal["talon", "windows"] = None):
        """Move the mouse to a point over a duration."""
        (cur_x, cur_y) = ctrl.mouse_pos()
        dx = x - cur_x
        dy = y - cur_y
        mouse_move_smooth_delta(dx, dy, duration_ms, callback_tick, callback_stop, easing_type, mouse_api_type=mouse_api_type)

    def mouse_move_smooth_from(
        x: int,
        y: int,
        duration_ms: int = None,
        callback_tick: Callable[[MouseMoveCallbackEvent], None] = None,
        callback_stop: Callable[[], None] = None,
        easing_type: CurveTypes = "ease_in_out",
        mouse_api_type: Literal["talon", "windows"] = None):
        """Move the mouse from a point over a duration."""
        (cur_x, cur_y) = ctrl.mouse_pos()
        dx = cur_x - x
        dy = cur_y - y
        actions.user.mouse_move_smooth_from_to(dx, dy, duration_ms, callback_tick, callback_stop, easing_type, mouse_api_type)

    def mouse_move_smooth_queue(fn: callable):
        """Add to movement queue, executed after next mouse_stop."""
        mouse_move_smooth_queue(fn)

    def mouse_move_continuous(dx_unit: Union[int, float], dy_unit: Union[int, float], speed: int = None):
        """
        Move the mouse continuously given a unit vector.
        Examples:
        ```
        mouse_move_continuous(1, 0) # right at default or specified speed
        mouse_move_continuous(-1, 0) # left at default or specified speed
        mouse_move_continuous(0, 1, 5) # down at speed 5
        mouse_move_continuous(1, -1, 10) # right and up at speed 10
        ```
        """
        mouse_move_continuous(dx_unit, dy_unit, speed)

    def mouse_move_continuous_left(speed: int = None):
        """Move the mouse continuously left."""
        mouse_move_continuous(-1, 0, speed)

    def mouse_move_continuous_right(speed: int = None):
        """Move the mouse continuously right."""
        mouse_move_continuous(1, 0, speed)

    def mouse_move_continuous_up(speed: int = None):
        """Move the mouse continuously up."""
        mouse_move_continuous(0, -1, speed)

    def mouse_move_continuous_down(speed: int = None):
        """Move the mouse continuously down."""
        mouse_move_continuous(0, 1, speed)

    def mouse_move_continuous_towards(x: Union[int, float], y: Union[int, float], speed_initial: int = None):
        """Move the mouse continuously towards an xy screen position."""
        mouse_move_continuous_towards(x, y, speed_initial)

    def mouse_move_continuous_stop(debounce_ms: int = 0):
        """Stop continuous mouse movement with optional debounce."""
        mouse_move_continuous_stop(debounce_ms)

    def mouse_move_tick_last_direction(distance: int = None, duration_ms: int = 0):
        """Jump the mouse a short distance in the same direction of the last continuous movement."""
        global _last_unit_vector

        distance = distance or settings.get("user.mouse_move_tick_distance")

        if not _last_unit_vector.x and not _last_unit_vector.y:
            return None
        return mouse_move_smooth_delta(_last_unit_vector.x * distance, _last_unit_vector.y * distance, duration_ms)

    def mouse_move_tick_reverse_last_direction(distance: int = None, duration_ms: int = 0):
        """Jump the mouse a short distance in the opposite direction of the last continuous movement."""
        global _last_unit_vector

        distance = distance or settings.get("user.mouse_move_tick_distance")

        if not _last_unit_vector.x and not _last_unit_vector.y:
            return None
        return mouse_move_smooth_delta(-_last_unit_vector.x * distance, -_last_unit_vector.y * distance, duration_ms)

    def mouse_move_tick(dx: int, dy: int, distance: int = None, duration_ms: int = 0):
        """Jump the mouse a short distance in a specific direction."""
        distance = distance or settings.get("user.mouse_move_tick_distance")
        return mouse_move_smooth_delta(dx * distance, dy * distance, duration_ms)

    def mouse_move_tick_left(distance: int = None, duration_ms: int = 0):
        """Jump the mouse a short distance to the left."""
        return mouse_move_smooth_delta(-1, 0, distance, duration_ms)

    def mouse_move_tick_right(distance: int = None, duration_ms: int = 0):
        """Jump the mouse a short distance to the right."""
        return mouse_move_smooth_delta(1, 0, distance, duration_ms)

    def mouse_move_tick_up(distance: int = None, duration_ms: int = 0):
        """Jump the mouse a short distance up."""
        return mouse_move_smooth_delta(0, -1, distance, duration_ms)

    def mouse_move_tick_down(distance: int = None, duration_ms: int = 0):
        """Jump the mouse a short distance down."""
        return mouse_move_smooth_delta(0, 1, distance, duration_ms)

    def mouse_move_continuous_speed(value: int):
        """Increase the speed of a current continuous movement."""
        global _mouse_continuous_speed
        _mouse_continuous_speed = value

    def mouse_move_continuous_speed_increase(multipler: Union[int, float] = 2):
        """Increase the speed of a current continuous movement."""
        global _mouse_continuous_speed
        _mouse_continuous_speed *= multipler

    def mouse_move_continuous_speed_decrease(multipler: Union[int, float] = 2):
        """Decrease the speed of a current continuous movement."""
        global _mouse_continuous_speed
        _mouse_continuous_speed /= multipler

    def mouse_move_info():
        """Get mouse movement info"""
        return MouseInfo()

    def mouse_move_event_register(on_event: callable):
        """
        Register callback event for mouse movement.
        Will trigger when movement starts or stops.

        ```py
        def on_event(event):
            print(event.type)
        actions.user.mouse_move_event_register(on_event)
        ```
        """
        mouse_move_event_register(on_event)

    def mouse_move_event_unregister(on_event: callable):
        """
        Unregister event set by actions.user.mouse_move_event_register
        """
        mouse_move_event_unregister(on_event)

    def mouse_move_event_dir_change_register(on_event: callable):
        """
        Register callback event for mouse_move_dir_change.
        Will trigger when direction changes.

        ```py
        def on_event(event):
            print(event.type, event.dir)
        actions.user.mouse_move_event_dir_change_register(on_event)
        ```
        """
        mouse_move_event_dir_change_register(on_event)

    def mouse_move_event_dir_change_unregister(on_event: callable):
        """
        Unregister event set by actions.user.mouse_move_event_dir_change_register
        """
        mouse_move_event_dir_change_unregister(on_event)

    def mouse_move_event_unregister_all():
        """
        Unregister all events
        """
        global dir_change_event_subscribers, mouse_move_event_subscribers
        dir_change_event_subscribers = []
        mouse_move_event_subscribers = []
