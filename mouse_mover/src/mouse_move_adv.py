"""
Mouse Mover
user.mouse_move_delta(dx: int, dy: int, duration_ms: int = 200, callback_tick: Callable[[MouseMoveCallbackEvent], None] = None, easing_type: CurveTypes = "ease_in_out", mouse_api_type: Literal["talon", "windows"] = "talon")
user.mouse_move_from(x: int, y: int, duration_ms: int = 200, callback_tick: Callable[[MouseMoveCallbackEvent], None] = None, easing_type: CurveTypes = "ease_in_out", mouse_api_type: Literal["talon", "windows"] = "talon")
user.mouse_move_from_to(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 200, callback_tick: Callable[[MouseMoveCallbackEvent], None] = None, easing_type: CurveTypes = "ease_in_out", mouse_api_type: Literal["talon", "windows"] = "talon")
user.mouse_move_to(x: int, y: int, duration_ms: int = 200, callback_tick: Callable[[MouseMoveCallbackEvent], None] = None, easing_type: CurveTypes = "ease_in_out", mouse_api_type: Literal["talon", "windows"] = "talon")
"""
from talon import Module, actions, ctrl, cron, settings
from typing import Callable, Literal, Union
from dataclasses import dataclass
import platform
import math
import time

mod = Module()

_mouse_job = None
_last_mouse_job_type = None
_mouse_movement_queue = []
_mouse_continuous_start_ts = None
_mouse_continuous_stop_ts = None
_mouse_continuous_dir = None
_mouse_continuous_speed = 1

@dataclass
class MouseMoveCallbackEvent:
    dx: float
    dy: float
    type: Literal["start", "tick", "stop"]

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
    mouse_move_talon(dx, dy)

if platform.system() == "Windows":
    import win32api, win32con
    def mouse_move_windows(dx: int, dy: int):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy)
    # def mouse_move(dx: int, dy: int):
    #     mouse_move_windows(dx, dy)

def mouse_move_queue(fn: callable):
    """Add to movement _mouse_movement_queue, executed after next mouse_stop."""
    global _mouse_movement_queue
    _mouse_movement_queue.append(fn)

CurveTypes = Literal["linear", "ease_in_out", "ease_in", "ease_out"]

class RealDeltaPath:
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

def mouse_move_delta(
    dx: int,
    dy: int,
    duration_ms: int = 200,
    callback_tick: Callable[[MouseMoveCallbackEvent], None] = None,
    easing_type: Literal["linear", "ease_in_out", "ease_in", "ease_out"] = "ease_in_out",
    mouse_api_type: Literal["talon", "windows"] = "talon"):
    """
    Move the mouse in a natural way over a duration.
    Examples:
    ```
    mouse_move_delta(300, 0, 200) # 300 right over 200ms
    mouse_move_delta(0, -1000, 2000) # 1000 up over 2s

    Callback example:
    def callback_tick(ev):
        # ev.dx
        # ev.dy
        # ev.type # "start", "tick", "stop"
    mouse_move_delta(100, 0, 100, callback_tick)
    ```
    """
    global _mouse_job, _last_mouse_job_type
    mouse_stop()

    _last_mouse_job_type = "natural"
    update_interval_ms = 16
    steps = max(1, duration_ms // update_interval_ms)
    step_count = 0
    last_x, last_y = 0, 0
    convert_linear_to_curve = easing_types[easing_type]
    delta_path = RealDeltaPath()

    mouse_move_fn = mouse_move

    if mouse_api_type == "windows":
        mouse_move_fn = mouse_move_windows
    elif mouse_api_type == "talon":
        mouse_move_fn = mouse_move_talon

    def update_position():
        nonlocal step_count, last_x, last_y, mouse_move_fn

        step_count += 1
        if step_count > steps:
            mouse_stop()
            if callback_tick:
                callback_tick(MouseMoveCallbackEvent(dx, dy, "stop"))
            return
        progress = step_count / steps
        curve_progress = convert_linear_to_curve(progress)

        current_x = dx * curve_progress
        current_y = dy * curve_progress

        dx_step = current_x - last_x
        dy_step = current_y - last_y

        (int_dx_step, int_dy_step) = delta_path.update_pos(dx_step, dy_step)

        mouse_move_fn(int_dx_step, int_dy_step)

        last_x, last_y = current_x, current_y
        if callback_tick:
            callback_tick(MouseMoveCallbackEvent(current_x, current_y, "tick"))

    update_position()
    _mouse_job = cron.interval("16ms", update_position)
    if callback_tick:
        callback_tick(MouseMoveCallbackEvent(0, 0, "start"))

def mouse_stop():
    """Stop current mouse movement, and start next in the _mouse_movement_queue if it exists."""
    global _mouse_job, _mouse_movement_queue, _last_mouse_job_type, _mouse_continuous_dir, _mouse_continuous_start_ts, _mouse_continuous_stop_ts
    if _mouse_job:
        cron.cancel(_mouse_job)
        _mouse_job = None
        _last_mouse_job_type = None
        _mouse_continuous_dir = None
        _mouse_continuous_start_ts = None
        _mouse_continuous_stop_ts = None
    if len(_mouse_movement_queue) > 0:
        fn = _mouse_movement_queue.pop(0)
        fn()

def mouse_move_degrees(dx_degrees: int, dy_degrees: int, duration_ms: int = 200, callback_tick: Callable[[MouseMoveCallbackEvent], None] = None):
    """
    Move the mouse by a number of degrees over a duration.
    Based on the calibration settings.
    """
    dx_360 = settings.get("user.game_calibrate_x_360")
    dy_90 = settings.get("user.game_calibrate_y_90")
    dx_total = dx_360 / 360 * dx_degrees
    dy_total = dy_90 / 90 * dy_degrees
    mouse_move_delta(dx_total, dy_total, duration_ms, callback_tick)

def mouse_move_continuous(x: Literal[1, 0, -1], y: Literal[1, 0, -1], speed: int = 1):
    """
    Move the mouse continuously.
    Examples:
    ```
    mouse_move_continuous(1, 0) # right at default speed
    mouse_move_continuous(-1, 0) # left at default speed
    mouse_move_continuous(0, 1, 5) # down at speed 5
    mouse_move_continuous(1, -1, 10) # right and up at speed 10
    ```
    """
    global _mouse_job, _mouse_continuous_dir, _mouse_continuous_start_ts, _mouse_continuous_stop_ts, _last_mouse_job_type, _mouse_continuous_speed
    _mouse_continuous_stop_ts = None
    _mouse_continuous_speed = speed
    last_mouse_job_type = _last_mouse_job_type
    _last_mouse_job_type = "continuous"
    if _mouse_job:
        if last_mouse_job_type == 'natural':
            mouse_stop()
        if _mouse_continuous_dir != (x, y):
            _mouse_continuous_dir = (x, y)
            _mouse_continuous_start_ts = time.perf_counter()
        # already going in this direction
        return

    _mouse_continuous_dir = (x, y)
    _mouse_continuous_start_ts = time.perf_counter()

    def update_position():
        global _mouse_continuous_stop_ts, _mouse_continuous_speed, _mouse_continuous_dir
        ts = time.perf_counter()

        if _mouse_continuous_stop_ts and ts - _mouse_continuous_stop_ts > 0:
            mouse_stop()
            return

        (x, y) = _mouse_continuous_dir
        mouse_move(x * _mouse_continuous_speed, y * _mouse_continuous_speed)

    update_position()
    _mouse_job = cron.interval("16ms", update_position)

def get_normalized_delta(pos_1_x, pos_1_y, pos_2_x, pos_2_y):
    dx = pos_2_x - pos_1_x
    dy = pos_2_y - pos_1_y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    return dx / distance, dy / distance

def mouse_move_continuous_towards(target_x: int, target_y: int, speed: int = 1):
    """
    Move the mouse continuously towards xy coordinate.
    Examples:
    ```
    mouse_move_continuous_towards(ctrl.mouse_pos()[0] + 100, ctrl.mouse_pos()[1] + 100) # move mouse towards 100,100
    ```
    """
    global _mouse_job, _mouse_continuous_dir, _mouse_continuous_start_ts, _mouse_continuous_stop_ts, _last_mouse_job_type, _mouse_continuous_speed
    _mouse_continuous_stop_ts = None
    _mouse_continuous_speed = speed
    last_mouse_job_type = _last_mouse_job_type
    _last_mouse_job_type = "continuous"
    current_pos = ctrl.mouse_pos()
    dx, dy = get_normalized_delta(current_pos[0], current_pos[1], target_x, target_y)

    if _mouse_job:
        if last_mouse_job_type == 'natural':
            mouse_stop()
        if _mouse_continuous_dir != (dx, dy):
            _mouse_continuous_dir = (dx, dy)
            _mouse_continuous_start_ts = time.perf_counter()
        # already going in this direction
        return

    _mouse_continuous_dir = (dx, dy)
    _mouse_continuous_start_ts = time.perf_counter()
    delta_path = RealDeltaPath()

    def update_position():
        global _mouse_continuous_stop_ts, _mouse_continuous_speed, _mouse_continuous_dir
        ts = time.perf_counter()

        if _mouse_continuous_stop_ts and ts - _mouse_continuous_stop_ts > 0:
            mouse_stop()
            return

        (dx, dy) = _mouse_continuous_dir
        dx_int, dy_int = delta_path.update_pos(dx * _mouse_continuous_speed, dy * _mouse_continuous_speed)
        mouse_move(dx_int, dy_int)

    update_position()
    _mouse_job = cron.interval("16ms", update_position)

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

def mouse_move_from_to(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 200, callback_tick: Callable[[MouseMoveCallbackEvent], None] = None):
    """
    Move the mouse from one point to another over a duration.
    Examples:
    ```
    mouse_move_from_to(100, 100, 200, 200, 500) # move from 100,100 to 200,200 over 500ms
    ```
    """
    dx = x2 - x1
    dy = y2 - y1
    actions.mouse_move(x1, y1)
    mouse_move_delta(dx, dy, duration_ms, callback_tick, mouse_api_type="talon")

# def mouse_move_to(x: int, y: int, duration_ms: int = 200, callback_tick: Callable[[MouseMoveCallbackEvent], None] = None):
#     """
#     Move the mouse to a point over a duration.
#     Examples:
#     ```
#     mouse_move_to(480, 1000) # move to 480,1000 over default ms
#     mouse_move_to(480, 1000, 500) # move to 480,1000 over 500ms
#     ```
#     """
#     (cur_x, cur_y) = ctrl.mouse_pos()
#     dx = x - cur_x
#     dy = y - cur_y
#     mouse_move_delta(dx, dy, duration_ms, callback_tick, mouse_api_type="talon")



@mod.action_class
class Actions:
    def mouse_move_delta(
        dx: int,
        dy: int,
        duration_ms: int = 200,
        callback_tick: Callable[[MouseMoveCallbackEvent], None] = None,
        easing_type: Literal["linear", "ease_in_out", "ease_in", "ease_out"] = "ease_in_out",
        mouse_api_type: Literal["talon", "windows"] = "talon"):
        """Move the mouse over a delta with control over the curve type, duration, mouse api type, and callback."""
        mouse_move_delta(dx, dy, duration_ms, callback_tick, easing_type, mouse_api_type)

    def mouse_move_from_to(
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        duration_ms: int = 200,
        callback_tick: Callable[[MouseMoveCallbackEvent], None] = None,
        easing_type: CurveTypes = "ease_in_out",
        mouse_api_type: Literal["talon", "windows"] = "talon"):
        """Move the mouse from one point to another over a duration."""
        dx = x2 - x1
        dy = y2 - y1
        # probably queue a move_to
        actions.mouse_move(x1, y1)
        mouse_move_delta(dx, dy, duration_ms, callback_tick, easing_type, mouse_api_type)

    def mouse_move_to(
        x: int,
        y: int,
        duration_ms: int = 200,
        callback_tick: Callable[[MouseMoveCallbackEvent], None] = None,
        easing_type: CurveTypes = "ease_in_out",
        mouse_api_type: Literal["talon", "windows"] = "talon"):
        """Move the mouse to a point over a duration."""
        (cur_x, cur_y) = ctrl.mouse_pos()
        dx = x - cur_x
        dy = y - cur_y
        mouse_move_delta(dx, dy, duration_ms, callback_tick, easing_type, mouse_api_type)

    def mouse_move_from(
        x: int,
        y: int,
        duration_ms: int = 200,
        callback_tick: Callable[[MouseMoveCallbackEvent], None] = None,
        easing_type: CurveTypes = "ease_in_out",
        mouse_api_type: Literal["talon", "windows"] = "talon"):
        """Move the mouse from a point over a duration."""
        (cur_x, cur_y) = ctrl.mouse_pos()
        dx = cur_x - x
        dy = cur_y - y
        actions.user.mouse_move_from_to(dx, dy, duration_ms, callback_tick, easing_type, mouse_api_type)

    def mouse_move_delta_degrees(
        dx_degrees: int,
        dy_degrees: int,
        duration_ms: int = 200,
        callback_tick: Callable[[MouseMoveCallbackEvent], None] = None,
        easing_type: CurveTypes = "ease_in_out"):
        """Move the mouse by a number of degrees over a duration."""
        mouse_move_degrees(dx_degrees, dy_degrees, duration_ms, callback_tick)

    def mouse_move_delta_queue(fn: callable):
        """Add to movement queue, executed after next mouse_stop."""
        mouse_move_queue(fn)

    def mouse_move_continuous(x: int, y: int, speed: int = 1):
        """Move the mouse continuously."""
        mouse_move_continuous(x, y, speed)

    def mouse_move_continuous_towards(x: int, y: int, speed: int = 1):
        """Move the mouse continuously."""
        mouse_move_continuous_towards(x, y, speed)

    def mouse_move_continuous_stop(debounce_ms: int = 0):
        """Stop continuous mouse movement with optional debounce."""
        mouse_move_continuous_stop(debounce_ms)
