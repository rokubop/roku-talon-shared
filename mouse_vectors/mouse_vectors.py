"""
Mouse Vectors System
A physics-based mouse motion system using force vectors that combine additively.
Each vector represents velocity or acceleration that sums together for realistic motion.
"""

import math
import platform
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union, Callable, Literal, Any

from talon import Module, actions, ctrl, cron, settings, ui, app
from talon.screen import Screen

mod = Module()

# Settings
mod.setting("mouse_vectors_tick_rate", default=90, type=int,
           desc="Physics update rate in Hz (60-120 recommended)")
mod.setting("mouse_vectors_enabled", default=True, type=bool,
           desc="Enable/disable the mouse vectors system")
mod.setting("mouse_vectors_dpi_scaling", default=True, type=bool,
           desc="Enable DPI-aware scaling for consistent movement across different displays")

# Global screen tracking for DPI scaling
_current_screen: Screen = None
_last_mouse_pos = (0, 0)
_cached_dpi_scale = 1.0

def get_current_screen(x: float = None, y: float = None) -> Screen:
    """Get the screen containing the current mouse position or specified coordinates"""
    global _current_screen, _last_mouse_pos, _cached_dpi_scale

    if x is None or y is None:
        x, y = ctrl.mouse_pos()

    # Only update screen if mouse moved significantly or we don't have a screen yet
    pos_changed = abs(x - _last_mouse_pos[0]) > 100 or abs(y - _last_mouse_pos[1]) > 100

    if _current_screen is None or pos_changed or not _current_screen.contains(x, y):
        _current_screen = ui.screen_containing(x, y)
        _last_mouse_pos = (x, y)
        _cached_dpi_scale = _current_screen.dpi / 96.0

    return _current_screen

def get_cached_dpi_scale() -> float:
    """Get the cached DPI scale to avoid repeated calculations"""
    global _cached_dpi_scale
    if _cached_dpi_scale == 1.0 and _current_screen is None:
        # Initialize on first use
        get_current_screen()
    return _cached_dpi_scale

def mouse_move_talon(dx: int, dy: int):
    (x, y) = ctrl.mouse_pos()
    ctrl.mouse_move(x + dx, y + dy)

def mouse_move_windows(dx: int, dy: int):
    pass

def mouse_move(dx: int, dy: int):
    """Move mouse with optional DPI scaling"""
    # Apply DPI scaling if enabled
    if settings.get("user.mouse_vectors_dpi_scaling"):
        # Use cached DPI scale to avoid repeated screen lookups
        dpi_scale = get_cached_dpi_scale()
        dx = int(dx * dpi_scale)
        dy = int(dy * dpi_scale)

    if settings.get("user.mouse_move_api") == "windows":
        mouse_move_windows(dx, dy)
    else:
        mouse_move_talon(dx, dy)

if platform.system() == "Windows":
    import win32api, win32con
    def mouse_move_windows(dx: int, dy: int):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy)

# Type definitions
Vector2D = Tuple[float, float]
InterpolationType = Literal["linear", "bezier", "cubic", "ease_in", "ease_out", "ease_in_out", "constant"]

@dataclass
class Vector:
    """Represents a single motion vector with velocity, acceleration, displacement, and animation"""
    name: str
    v: Vector2D = (0.0, 0.0)  # Velocity in pixels/second
    a: Vector2D = (0.0, 0.0)  # Acceleration in pixels/second²
    d: Vector2D = (0.0, 0.0)  # Displacement in pixels (target-based movement)
    enabled: bool = True
    duration: Optional[float] = None  # Duration in milliseconds
    time_remaining: Optional[float] = None
    created_at: float = field(default_factory=time.perf_counter)

    # Animation properties
    a_keyframes: Optional[List[float]] = None
    a_interpolation: InterpolationType = "linear"
    v_keyframes: Optional[List[float]] = None
    v_interpolation: InterpolationType = "linear"
    d_keyframes: Optional[List[float]] = None
    d_interpolation: InterpolationType = "linear"

    # Internal state
    _base_v: Vector2D = field(init=False)
    _base_a: Vector2D = field(init=False)
    _base_d: Vector2D = field(init=False)
    _d_progress: float = field(init=False, default=0.0)  # Track displacement progress
    _d_start_pos: Optional[Vector2D] = field(init=False, default=None)  # Starting position for displacement

    def __post_init__(self):
        """Initialize internal state after creation"""
        self._base_v = self.v
        self._base_a = self.a
        self._base_d = self.d
        if self.duration is not None:
            self.time_remaining = self.duration
        self._validate_arguments()

    def _validate_arguments(self):
        """Validate that vector arguments don't conflict with each other"""
        # Check if we have any meaningful displacement
        has_displacement = self.d != (0.0, 0.0) or self.d_keyframes is not None

        # Check if we have meaningful velocity or acceleration
        has_velocity = self.v != (0.0, 0.0) or self.v_keyframes is not None
        has_acceleration = self.a != (0.0, 0.0) or self.a_keyframes is not None

        # Check for conflicting combinations
        conflicts = []

        # Displacement should generally not be combined with velocity/acceleration
        # unless the displacement is meant to be a cumulative target
        if has_displacement and (has_velocity or has_acceleration):
            # This is allowed but we should warn about potential confusion
            pass  # For now, allow this combination as it might be useful

        # Duration makes sense with displacement but less so with continuous velocity
        if self.duration is not None:
            if has_velocity and not has_displacement and not has_acceleration:
                # Continuous velocity with duration might be intended as time-limited motion
                pass  # Allow this - velocity for a specific duration

        # Check for keyframe mismatches
        if self.v_keyframes is not None and not has_velocity:
            conflicts.append("v_keyframes specified but v is zero")

        if self.a_keyframes is not None and not has_acceleration:
            conflicts.append("a_keyframes specified but a is zero")

        if self.d_keyframes is not None and not has_displacement:
            conflicts.append("d_keyframes specified but d is zero")

        # Report conflicts
        if conflicts:
            conflict_str = "; ".join(conflicts)
            raise ValueError(f"Vector '{self.name}' has conflicting arguments: {conflict_str}")

class InterpolationEngine:
    """Handles keyframe interpolation for vector animation"""

    @staticmethod
    def interpolate(keyframes: List[float], progress: float,
                   interpolation_type: InterpolationType) -> float:
        """Interpolate between keyframes based on progress (0.0 to 1.0)"""
        if not keyframes or len(keyframes) == 0:
            return 1.0

        if len(keyframes) == 1:
            return keyframes[0]

        # Clamp progress
        progress = max(0.0, min(1.0, progress))

        # Find keyframe segment
        segment_size = 1.0 / (len(keyframes) - 1)
        segment_index = min(int(progress / segment_size), len(keyframes) - 2)
        local_progress = (progress - segment_index * segment_size) / segment_size

        # Get values
        v1 = keyframes[segment_index]
        v2 = keyframes[segment_index + 1]

        # Apply interpolation
        if interpolation_type == "linear":
            return InterpolationEngine._linear(v1, v2, local_progress)
        elif interpolation_type == "ease_in":
            return InterpolationEngine._ease_in(v1, v2, local_progress)
        elif interpolation_type == "ease_out":
            return InterpolationEngine._ease_out(v1, v2, local_progress)
        elif interpolation_type == "ease_in_out":
            return InterpolationEngine._ease_in_out(v1, v2, local_progress)
        elif interpolation_type == "bezier":
            return InterpolationEngine._bezier(v1, v2, local_progress)
        elif interpolation_type == "cubic":
            return InterpolationEngine._cubic(v1, v2, local_progress)
        elif interpolation_type == "constant":
            return v1 if local_progress < 1.0 else v2
        else:
            return InterpolationEngine._linear(v1, v2, local_progress)

    @staticmethod
    def _linear(v1: float, v2: float, t: float) -> float:
        return v1 + (v2 - v1) * t

    @staticmethod
    def _ease_in(v1: float, v2: float, t: float) -> float:
        eased_t = 1 - math.cos(t * math.pi / 2)
        return v1 + (v2 - v1) * eased_t

    @staticmethod
    def _ease_out(v1: float, v2: float, t: float) -> float:
        eased_t = math.sin(t * math.pi / 2)
        return v1 + (v2 - v1) * eased_t

    @staticmethod
    def _ease_in_out(v1: float, v2: float, t: float) -> float:
        eased_t = 0.5 * (1 - math.cos(t * math.pi))
        return v1 + (v2 - v1) * eased_t

    @staticmethod
    def _bezier(v1: float, v2: float, t: float) -> float:
        # Simple cubic bezier with automatic control points
        p0, p3 = v1, v2
        p1 = v1 + (v2 - v1) * 0.33
        p2 = v1 + (v2 - v1) * 0.67

        return (1-t)**3 * p0 + 3*(1-t)**2*t * p1 + 3*(1-t)*t**2 * p2 + t**3 * p3

    @staticmethod
    def _cubic(v1: float, v2: float, t: float) -> float:
        # Smooth cubic interpolation
        t2 = t * t
        t3 = t2 * t
        return v1 + (v2 - v1) * (3*t2 - 2*t3)

class SubpixelTracker:
    """Tracks fractional pixel movement for accuracy"""

    def __init__(self):
        self.accumulated_x = 0.0
        self.accumulated_y = 0.0

    def update(self, dx: float, dy: float) -> Tuple[int, int]:
        """Add fractional movement and return integer pixels to move"""
        self.accumulated_x += dx
        self.accumulated_y += dy

        # Extract integer pixels
        int_dx = int(self.accumulated_x)
        int_dy = int(self.accumulated_y)

        # Keep fractional remainder
        self.accumulated_x -= int_dx
        self.accumulated_y -= int_dy

        return int_dx, int_dy

class MouseVectorsSystem:
    """Core physics-based mouse vectors system"""

    def __init__(self):
        self.vectors: Dict[str, Vector] = {}
        self.current_velocity = (0.0, 0.0)
        self.subpixel_tracker = SubpixelTracker()
        self.physics_job = None
        self.last_update_time = None
        self.tick_interval_ms = 1000 // settings.get("user.mouse_vectors_tick_rate")

    def add_or_update_vector(self, name: Optional[str] = None, **properties) -> str:
        """Add a new vector or update existing one"""
        if name is None:
            name = f"unnamed_{uuid.uuid4().hex[:8]}"

        # Handle alternative property names before creating vector
        direction = properties.pop('direction', None)
        speed = properties.pop('speed', None)
        acceleration_magnitude = properties.pop('acceleration', None)

        # Convert direction+speed to velocity
        if direction is not None and speed is not None:
            direction_normalized = self._normalize_vector(direction)
            properties['v'] = (direction_normalized[0] * speed, direction_normalized[1] * speed)

        # Convert direction+acceleration to acceleration vector
        if direction is not None and acceleration_magnitude is not None:
            direction_normalized = self._normalize_vector(direction)
            properties['a'] = (direction_normalized[0] * acceleration_magnitude, direction_normalized[1] * acceleration_magnitude)

        # Get existing vector or create new one
        if name in self.vectors:
            vector = self.vectors[name]
            # Update properties
            for key, value in properties.items():
                if hasattr(vector, key):
                    old_value = getattr(vector, key)
                    setattr(vector, key, value)
            # Update base values for keyframe calculations
            if 'v' in properties:
                vector._base_v = properties['v']
            if 'a' in properties:
                vector._base_a = properties['a']
            if 'd' in properties:
                vector._base_d = properties['d']
                # Reset displacement tracking when displacement changes
                vector._d_start_pos = None
                vector._d_progress = 0.0
        else:
            # Create new vector
            vector_props = {
                'name': name,
                'v': (0.0, 0.0),
                'a': (0.0, 0.0),
                'd': (0.0, 0.0),
                'enabled': True,
                **properties
            }
            vector = Vector(**vector_props)
            vector._base_v = vector.v
            vector._base_a = vector.a
            vector._base_d = vector.d
            self.vectors[name] = vector

        # Auto-remove vectors that are set to zero velocity/acceleration with no duration
        if (vector.v == (0.0, 0.0) and vector.a == (0.0, 0.0) and vector.d == (0.0, 0.0) and
            vector.duration is None and vector.v_keyframes is None and vector.a_keyframes is None and vector.d_keyframes is None):
            del self.vectors[name]
            if not self.vectors:
                self._stop_physics()
            return name

        # Start physics if not running
        self._ensure_physics_running()

        return name

    def get_vector(self, name: str) -> Optional[Dict]:
        """Get vector state as dictionary"""
        if name not in self.vectors:
            return None

        vector = self.vectors[name]
        return {
            'name': vector.name,
            'v': vector.v,
            'a': vector.a,
            'enabled': vector.enabled,
            'duration': vector.duration,
            'time_remaining': vector.time_remaining,
            'a_keyframes': vector.a_keyframes,
            'a_interpolation': vector.a_interpolation,
            'v_keyframes': vector.v_keyframes,
            'v_interpolation': vector.v_interpolation
        }

    def remove_vector(self, name: str) -> bool:
        """Remove a specific vector"""
        if name in self.vectors:
            del self.vectors[name]
            if not self.vectors:
                self._stop_physics()
            return True
        return False

    def stop_all(self):
        """Remove all vectors and stop physics"""
        self.vectors.clear()
        self.current_velocity = (0.0, 0.0)
        self._stop_physics()

    def disable_all(self):
        """Disable all vectors without removing them"""
        for vector in self.vectors.values():
            vector.enabled = False

    def list_vectors(self) -> List[str]:
        """Get list of all vector names"""
        return list(self.vectors.keys())

    def get_state(self) -> Dict:
        """Get complete system state"""
        total_v, total_a = self._calculate_totals()
        speed = math.sqrt(total_v[0]**2 + total_v[1]**2)
        direction = math.degrees(math.atan2(total_v[1], total_v[0])) if speed > 0 else 0

        return {
            'total_velocity': {'x': total_v[0], 'y': total_v[1]},
            'total_acceleration': {'x': total_a[0], 'y': total_a[1]},
            'speed': speed,
            'direction': direction,
            'vectors': {name: self.get_vector(name) for name in self.vectors}
        }

    def _ensure_physics_running(self):
        """Start physics updates if not already running"""
        if self.physics_job is None and settings.get("user.mouse_vectors_enabled"):
            self.last_update_time = time.perf_counter()
            self.physics_job = cron.interval(f"{self.tick_interval_ms}ms", self._physics_update)

    def _stop_physics(self):
        """Stop physics updates"""
        if self.physics_job is not None:
            cron.cancel(self.physics_job)
            self.physics_job = None
            self.last_update_time = None

    def _physics_update(self):
        """Main physics update loop"""
        if not settings.get("user.mouse_vectors_enabled"):
            return

        current_time = time.perf_counter()
        if self.last_update_time is None:
            self.last_update_time = current_time
            return

        dt = current_time - self.last_update_time
        self.last_update_time = current_time

        # Update vector lifetimes and animations
        vectors_to_remove = []
        for name, vector in self.vectors.items():
            if vector.duration is not None and vector.time_remaining is not None:
                vector.time_remaining -= dt * 1000  # Convert to milliseconds

                if vector.v_keyframes is not None:
                    progress = 1.0 - (vector.time_remaining / vector.duration)

                if vector.time_remaining <= 0:
                    vectors_to_remove.append(name)
                    continue

                # Update animated properties
                progress = 1.0 - (vector.time_remaining / vector.duration)

                # Update acceleration with keyframes
                if vector.a_keyframes:
                    multiplier = InterpolationEngine.interpolate(
                        vector.a_keyframes, progress, vector.a_interpolation)
                    vector.a = (vector._base_a[0] * multiplier, vector._base_a[1] * multiplier)

                # Update velocity with keyframes
                if vector.v_keyframes:
                    multiplier = InterpolationEngine.interpolate(
                        vector.v_keyframes, progress, vector.v_interpolation)
                    vector.v = (vector._base_v[0] * multiplier, vector._base_v[1] * multiplier)

                # Update displacement with keyframes
                if vector.d_keyframes:
                    multiplier = InterpolationEngine.interpolate(
                        vector.d_keyframes, progress, vector.d_interpolation)
                    vector.d = (vector._base_d[0] * multiplier, vector._base_d[1] * multiplier)

            # Handle displacement vectors
            if vector.d != (0.0, 0.0):
                # Initialize starting position for displacement if not set
                if vector._d_start_pos is None:
                    current_pos = ctrl.mouse_pos()
                    vector._d_start_pos = (float(current_pos[0]), float(current_pos[1]))

                # Calculate target position
                target_pos = (
                    vector._d_start_pos[0] + vector.d[0],
                    vector._d_start_pos[1] + vector.d[1]
                )

                # Get current position
                current_pos = ctrl.mouse_pos()
                current_pos_f = (float(current_pos[0]), float(current_pos[1]))

                # Calculate remaining displacement
                remaining_d = (
                    target_pos[0] - current_pos_f[0],
                    target_pos[1] - current_pos_f[1]
                )

                # Check if we've reached the target (within 1 pixel tolerance)
                distance_to_target = math.sqrt(remaining_d[0]**2 + remaining_d[1]**2)
                if distance_to_target < 1.0:
                    # We've reached the target, remove this vector
                    vectors_to_remove.append(name)
                    continue

                # Calculate velocity needed to reach target
                # For displacement vectors, we override velocity to move toward target
                if vector.duration is not None and vector.time_remaining is not None:
                    # Use time-based movement
                    time_remaining_sec = vector.time_remaining / 1000.0
                    if time_remaining_sec > 0.01:  # Avoid division by near-zero
                        vector.v = (
                            remaining_d[0] / time_remaining_sec,
                            remaining_d[1] / time_remaining_sec
                        )
                    else:
                        # Very little time left, move directly
                        vector.v = (remaining_d[0] / dt, remaining_d[1] / dt)
                else:
                    # Use default displacement speed
                    displacement_speed = 1000.0  # pixels per second
                    if distance_to_target > 0:
                        normalized_d = (
                            remaining_d[0] / distance_to_target,
                            remaining_d[1] / distance_to_target
                        )
                        vector.v = (
                            normalized_d[0] * displacement_speed,
                            normalized_d[1] * displacement_speed
                        )

        # Remove expired vectors
        for name in vectors_to_remove:
            self.remove_vector(name)

        # Calculate physics
        total_v, total_a = self._calculate_totals()

        # Integrate acceleration into velocity
        self.current_velocity = (
            self.current_velocity[0] + total_a[0] * dt,
            self.current_velocity[1] + total_a[1] * dt
        )

        # Add direct velocity vectors
        final_velocity = (
            self.current_velocity[0] + total_v[0],
            self.current_velocity[1] + total_v[1]
        )

        # Calculate displacement
        dx = final_velocity[0] * dt
        dy = final_velocity[1] * dt

        # Apply movement with subpixel accuracy
        if abs(dx) > 0.01 or abs(dy) > 0.01:  # Only move if significant
            int_dx, int_dy = self.subpixel_tracker.update(dx, dy)
            if int_dx != 0 or int_dy != 0:
                mouse_move(int_dx, int_dy)

        # Stop physics if no vectors remain
        if not self.vectors:
            self._stop_physics()

    def _calculate_totals(self) -> Tuple[Vector2D, Vector2D]:
        """Calculate total velocity and acceleration from all enabled vectors"""
        total_v = (0.0, 0.0)
        total_a = (0.0, 0.0)

        for vector in self.vectors.values():
            if vector.enabled:
                total_v = (total_v[0] + vector.v[0], total_v[1] + vector.v[1])
                total_a = (total_a[0] + vector.a[0], total_a[1] + vector.a[1])

        return total_v, total_a

    def _normalize_vector(self, vector: Vector2D) -> Vector2D:
        """Normalize a vector to unit length"""
        magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
        if magnitude == 0:
            return (0.0, 0.0)
        return (vector[0] / magnitude, vector[1] / magnitude)

def _parse_tuple_string(value: str) -> Tuple[float, float]:
    """Safely parse a tuple string like '(50, 0)' into a tuple of floats"""
    # Remove parentheses and whitespace
    value = value.strip().strip('()').strip()
    # Split by comma and convert to floats
    parts = [part.strip() for part in value.split(',')]
    if len(parts) != 2:
        raise ValueError(f"Expected tuple with 2 values, got {len(parts)}")
    return (float(parts[0]), float(parts[1]))

def _parse_list_string(value: str) -> List[float]:
    """Safely parse a list string like '[1.0, -1.0, 1.0]' into a list of floats"""
    # Remove brackets and whitespace
    value = value.strip().strip('[]').strip()
    if not value:
        return []
    # Split by comma and convert to floats
    parts = [part.strip() for part in value.split(',')]
    return [float(part) for part in parts]

# Global system instance
_mouse_vectors_system = None

# Public API functions
def mouse_vectors(name: Optional[str] = None, **properties) -> Optional[Dict]:
    """
    Create, update, or query motion vectors

    Examples:
        mouse_vectors("move", v=(50, 0))                    # Move right at 50 px/s
        mouse_vectors("thrust", a=(100, 0), duration=1000)  # Accelerate right for 1s
        mouse_vectors("wobble", a=(0, 20),                  # Oscillating force
                     a_keyframes=[1.0, -1.0, 1.0, -1.0],
                     duration=2000)

        # Query existing vector
        state = mouse_vectors("move")
    """
    if name is not None and not properties:
        # Query mode
        return _mouse_vectors_system.get_vector(name)
    else:
        # Create/update mode
        vector_name = _mouse_vectors_system.add_or_update_vector(name, **properties)
        return {'name': vector_name}

def mouse_vectors_get_state() -> Dict:
    """Get complete system state including all vectors and resulting motion"""
    return _mouse_vectors_system.get_state()

def mouse_vectors_stop():
    """Remove all vectors (instant stop)"""
    _mouse_vectors_system.stop_all()

def mouse_vectors_disable():
    """Disable all vectors without removing them"""
    _mouse_vectors_system.disable_all()

def mouse_vectors_remove(name: str) -> bool:
    """Remove specific named vector"""
    return _mouse_vectors_system.remove_vector(name)

def mouse_vectors_list() -> List[str]:
    """Get list of all active vector names"""
    return _mouse_vectors_system.list_vectors()

def mouse_vectors_enable_dpi_scaling():
    """Enable DPI-aware scaling for consistent movement across displays"""
    settings.set("user.mouse_vectors_dpi_scaling", True)

def mouse_vectors_disable_dpi_scaling():
    """Disable DPI scaling for raw pixel movement"""
    settings.set("user.mouse_vectors_dpi_scaling", False)

def mouse_vectors_get_dpi_info() -> dict:
    """Get current DPI information"""
    current_pos = ctrl.mouse_pos()
    screen = get_current_screen(current_pos[0], current_pos[1])
    return {
        'dpi': screen.dpi,
        'scale': screen.dpi / 96.0,
        'screen_rect': {
            'x': screen.rect.x,
            'y': screen.rect.y,
            'width': screen.rect.width,
            'height': screen.rect.height
        }
    }

# Talon Actions
@mod.action_class
class Actions:
    def mouse_vectors(
        name: str = None,
        v: Union[str | Tuple[float, float]] = None,
        a: Tuple[float, float] = None,
        d: Tuple[float, float] = None,
        enabled: bool = None,
        duration: float = None,
        speed: float = None,
        direction: Tuple[float, float] = None,
        acceleration: float = None,
        a_keyframes: List[float] = None,
        a_interpolation: str = None,
        v_keyframes: List[float] = None,
        v_interpolation: str = None,
        d_keyframes: List[float] = None,
        d_interpolation: str = None
    ) -> dict:
        """
        Create, update, or query motion vectors for physics-based mouse movement.

        Args:
            name: Vector name (None for auto-generated)
            v: Velocity vector (x, y) in pixels/second
            a: Acceleration vector (x, y) in pixels/second²
            d: Displacement vector (x, y) in pixels - target-based movement
            enabled: Whether vector affects movement
            duration: How long vector exists in milliseconds
            speed: Magnitude for direction-based movement
            direction: Unit vector for direction-based movement
            acceleration: Magnitude for direction-based acceleration
            a_keyframes: Acceleration multipliers over time
            a_interpolation: Interpolation type for acceleration
            v_keyframes: Velocity multipliers over time
            v_interpolation: Interpolation type for velocity
            d_keyframes: Displacement multipliers over time
            d_interpolation: Interpolation type for displacement

        Returns:
            Dictionary with vector state or name

        Examples:
            actions.user.mouse_vectors("move", v=(50, 0))
            actions.user.mouse_vectors("boost", a=(100, 0), duration=1000)
            actions.user.mouse_vectors("target", d=(100, 50), duration=2000)
            actions.user.mouse_vectors("pulse", a=(80, 0),
                                     a_keyframes=[0.0, 1.0, 0.0], duration=1000)
        """
        # Build properties dict from non-None arguments
        properties = {}

        if isinstance(v, str):
            # if string, all the options are trying to be passed in a single string.
            # .talon files have to do this because they can't use tuples
            # e.g. mouse move up: user.mouse_vectors("move", "v=(0, -50);a=(0, 0);duration=1000;a_keyframes=[0.0, 1.0, 0.0];v_keyframes=[1.0, 0.5, 1.0];a_interpolation=linear;v_interpolation=bezier")
            try:
                # Reset v to None so it doesn't get added as a string
                original_v_string = v
                v = None

                options = original_v_string.split(";")
                for option in options:
                    if "=" not in option:
                        continue
                    key, value = option.split("=", 1)  # Split only on first =
                    key = key.strip()
                    value = value.strip()

                    if key == "v":
                        v = _parse_tuple_string(value)
                    elif key == "a":
                        a = _parse_tuple_string(value)
                    elif key == "d":
                        d = _parse_tuple_string(value)
                    elif key == "duration":
                        duration = float(value)
                    elif key == "speed":
                        speed = float(value)
                    elif key == "acceleration":
                        acceleration = float(value)
                    elif key == "enabled":
                        enabled = value.lower() in ('true', '1', 'yes', 'on')
                    elif key == "direction":
                        direction = _parse_tuple_string(value)
                    elif key == "a_keyframes":
                        a_keyframes = _parse_list_string(value)
                    elif key == "a_interpolation":
                        a_interpolation = value
                    elif key == "v_keyframes":
                        v_keyframes = _parse_list_string(value)
                    elif key == "v_interpolation":
                        v_interpolation = value
                    elif key == "d_keyframes":
                        d_keyframes = _parse_list_string(value)
                    elif key == "d_interpolation":
                        d_interpolation = value
            except Exception as e:
                raise ValueError(f"Error parsing vector options: {e}")

        if v is not None:
            properties['v'] = v
        if a is not None:
            properties['a'] = a
        if d is not None:
            properties['d'] = d
        if enabled is not None:
            properties['enabled'] = enabled
        if duration is not None:
            properties['duration'] = duration
        if speed is not None:
            properties['speed'] = speed
        if direction is not None:
            properties['direction'] = direction
        if acceleration is not None:
            properties['acceleration'] = acceleration
        if a_keyframes is not None:
            properties['a_keyframes'] = a_keyframes
        if a_interpolation is not None:
            properties['a_interpolation'] = a_interpolation
        if v_keyframes is not None:
            properties['v_keyframes'] = v_keyframes
        if v_interpolation is not None:
            properties['v_interpolation'] = v_interpolation
        if d_keyframes is not None:
            properties['d_keyframes'] = d_keyframes
        if d_interpolation is not None:
            properties['d_interpolation'] = d_interpolation

        return mouse_vectors(name, **properties)

    def mouse_vectors_get_state() -> dict:
        """Get complete system state including all vectors and resulting motion"""
        return mouse_vectors_get_state()

    def mouse_vectors_stop():
        """Remove all vectors (instant stop)"""
        mouse_vectors_stop()

    def mouse_vectors_disable():
        """Disable all vectors without removing them"""
        mouse_vectors_disable()

    def mouse_vectors_remove(name: str) -> bool:
        """Remove specific named vector"""
        return mouse_vectors_remove(name)

    def mouse_vectors_list() -> list:
        """Get list of all active vector names"""
        return mouse_vectors_list()

    def mouse_vectors_enable_dpi_scaling():
        """Enable DPI-aware scaling for consistent movement across displays"""
        mouse_vectors_enable_dpi_scaling()

    def mouse_vectors_disable_dpi_scaling():
        """Disable DPI scaling for raw pixel movement"""
        mouse_vectors_disable_dpi_scaling()

    def mouse_vectors_get_dpi_info() -> dict:
        """Get current DPI information for debugging"""
        return mouse_vectors_get_dpi_info()


def on_ready():
    global _mouse_vectors_system
    _mouse_vectors_system = MouseVectorsSystem()

app.register("ready", on_ready)