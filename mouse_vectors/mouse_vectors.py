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
mod.setting("mouse_vector_tick_rate", default=80, type=int,
           desc="Physics update rate in Hz (60-120 recommended)")
mod.setting("mouse_vector_enabled", default=True, type=bool,
           desc="Enable/disable the mouse vectors system")
mod.setting("mouse_vector_dpi_scaling", default=True, type=bool,
           desc="Enable DPI-aware scaling for consistent movement across different displays")

# Global screen tracking for DPI scaling
_current_screen: Screen = None
_last_mouse_pos = (0, 0)
_cached_dpi_scale = 1.0

# Global debug logging state
_debug_logging_enabled = False
_last_throttled_log_time = {}

def debug_log(message: str, throttle_key: str = None, throttle_ms: int = None):
    """
    Print debug message if debug logging is enabled

    Args:
        message: The debug message to print
        throttle_key: Unique key for throttling (if None, no throttling)
        throttle_ms: Minimum milliseconds between messages for this throttle_key
    """
    if not _debug_logging_enabled:
        return

    # Handle throttling for high-frequency messages
    if throttle_key and throttle_ms:
        current_time = time.perf_counter() * 1000  # Convert to milliseconds
        last_time = _last_throttled_log_time.get(throttle_key, 0)

        if current_time - last_time < throttle_ms:
            return  # Skip this message due to throttling

        _last_throttled_log_time[throttle_key] = current_time

    print(message)

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
    if settings.get("user.mouse_vector_dpi_scaling"):
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

    # Centripetal turn parameters
    _turn_target: Optional[Vector2D] = field(init=False, default=None)
    _turn_radius: Optional[float] = field(init=False, default=None)
    _turn_type: Optional[str] = field(init=False, default=None)

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
        self.tick_interval_ms = 1000 // settings.get("user.mouse_vector_tick_rate")

    def add_or_update_vector(self, name: Optional[str] = None, **properties) -> str:
        """Add a new vector or update existing one"""
        if name is None:
            if properties.get('duration') is not None:
                name = f"temp_{uuid.uuid4().hex[:8]}"
            else:
                name = "main"  # Default vector name - user's primary movement

        # Handle alternative property names before creating vector
        direction = properties.pop('direction', None)
        speed = properties.pop('speed', None)
        default_speed = properties.pop('default_speed', None)
        acceleration_magnitude = properties.pop('acceleration', None)

        # Convert direction+speed to velocity
        if direction is not None and speed is not None:
            direction_normalized = self._normalize_vector(direction)
            properties['v'] = (direction_normalized[0] * speed, direction_normalized[1] * speed)
        # Handle direction-only changes: preserve existing speed while changing direction
        elif direction is not None and name in self.vectors:
            existing_vector = self.vectors[name]
            current_speed = math.sqrt(existing_vector.v[0]**2 + existing_vector.v[1]**2)
            if current_speed > 0:  # Only change direction if there's existing velocity
                direction_normalized = self._normalize_vector(direction)
                properties['v'] = (direction_normalized[0] * current_speed, direction_normalized[1] * current_speed)
            elif default_speed is not None:  # Use default speed if no current velocity
                direction_normalized = self._normalize_vector(direction)
                properties['v'] = (direction_normalized[0] * default_speed, direction_normalized[1] * default_speed)
        # Handle direction with default_speed for new vectors
        elif direction is not None and default_speed is not None:
            direction_normalized = self._normalize_vector(direction)
            properties['v'] = (direction_normalized[0] * default_speed, direction_normalized[1] * default_speed)

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
                **{k: v for k, v in properties.items() if not k.startswith('_')}
            }
            vector = Vector(**vector_props)
            vector._base_v = vector.v
            vector._base_a = vector.a
            vector._base_d = vector.d

            # Handle special turn parameters
            if '_turn_target' in properties:
                vector._turn_target = properties['_turn_target']
            if '_turn_radius' in properties:
                vector._turn_radius = properties['_turn_radius']
            if '_turn_type' in properties:
                vector._turn_type = properties['_turn_type']

            self.vectors[name] = vector

        # Auto-remove vectors that are set to zero velocity/acceleration with no duration
        # BUT don't remove turn vectors - they start with zero velocity but will be calculated dynamically
        is_turn_vector = hasattr(vector, '_turn_type') and vector._turn_type == 'centripetal'
        if (not is_turn_vector and
            vector.v == (0.0, 0.0) and vector.a == (0.0, 0.0) and vector.d == (0.0, 0.0) and
            vector.duration is None and vector.v_keyframes is None and vector.a_keyframes is None and vector.d_keyframes is None):
            del self.vectors[name]
            if not self.vectors:
                self._stop_physics()
            return name

        # Reset accumulated velocity when vectors change to prevent acceleration accumulation
        # This fixes the issue where acceleration from previous commands continues to affect new movements
        # Only reset if we're adding/updating vectors with explicit velocity (not pure acceleration)
        has_explicit_velocity = 'v' in properties or 'speed' in properties or 'direction' in properties
        if has_explicit_velocity:
            self.current_velocity = (0.0, 0.0)

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
            # Reset accumulated velocity when vectors are removed to prevent acceleration accumulation
            self.current_velocity = (0.0, 0.0)
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
        if self.physics_job is None and settings.get("user.mouse_vector_enabled"):
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
        if not settings.get("user.mouse_vector_enabled"):
            return

        current_time = time.perf_counter()
        if self.last_update_time is None:
            self.last_update_time = current_time
            return

        dt = current_time - self.last_update_time
        self.last_update_time = current_time

        # Log active vectors at start of physics update (throttled to once per 500ms)
        active_vectors = [f"{name}(v={vec.v}, type={getattr(vec, '_turn_type', 'normal')})" for name, vec in self.vectors.items() if vec.enabled]
        if active_vectors:
            debug_log(f"[PHYSICS] Active vectors: {active_vectors}", "physics_active_vectors", 500)

        # Update vector lifetimes and animations
        vectors_to_remove = []
        # Create a copy of items to avoid "dictionary changed during iteration" error
        for name, vector in list(self.vectors.items()):
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

            # Handle centripetal turning vectors
            if vector._turn_type == 'centripetal' and vector._turn_target is not None and vector._turn_radius is not None:
                debug_log(f"[PHYSICS] Processing centripetal turn vector '{name}'")

                # Calculate total velocity INCLUDING this turn vector to get the actual current direction
                total_v = (0.0, 0.0)
                for vector_name, other_vector in self.vectors.items():
                    if other_vector.enabled:
                        total_v = (total_v[0] + other_vector.v[0], total_v[1] + other_vector.v[1])

                debug_log(f"[PHYSICS] Total velocity (including turn progress): {total_v}", "physics_turn_velocity", 200)

                current_speed = math.sqrt(total_v[0]**2 + total_v[1]**2)
                debug_log(f"[PHYSICS] Current speed: {current_speed}", "physics_turn_speed", 200)

                if current_speed > 0.1:  # Only apply if we have meaningful velocity to turn
                    # Calculate current direction
                    current_dir = (total_v[0] / current_speed, total_v[1] / current_speed)
                    debug_log(f"[PHYSICS] Current direction: {current_dir}", "physics_turn_direction", 200)

                    # Calculate angle between current direction and target direction
                    target_dir = vector._turn_target
                    debug_log(f"[PHYSICS] Target direction: {target_dir}", "physics_turn_target", 200)

                    dot_product = current_dir[0] * target_dir[0] + current_dir[1] * target_dir[1]
                    dot_product = max(-1.0, min(1.0, dot_product))  # Clamp to prevent math domain error
                    angle_to_target = math.acos(dot_product)
                    debug_log(f"[PHYSICS] Angle to target: {angle_to_target} radians ({math.degrees(angle_to_target)} degrees)", "physics_turn_angle", 200)

                    # Physics-based turning using actual turn radius
                    # Formula: angular_velocity = speed / radius
                    # Smaller radius = tighter/faster turns, larger radius = wider/slower turns
                    turn_radius = vector._turn_radius
                    base_angular_velocity = current_speed / turn_radius

                    debug_log(f"[PHYSICS] Turn radius: {turn_radius} px", "physics_turn_calc", 300)
                    debug_log(f"[PHYSICS] Physics-based angular velocity: {base_angular_velocity} rad/s ({math.degrees(base_angular_velocity)} deg/s)", "physics_turn_calc", 300)

                    # Optional: Add small multipliers for responsiveness (keeping physics realistic)
                    responsiveness_multiplier = 1.0  # Can be adjusted for feel
                    if angle_to_target > math.pi / 2:  # 90+ degrees
                        responsiveness_multiplier = 1.2  # 20% faster for sharp turns

                    # Final angular velocity
                    angular_velocity = base_angular_velocity * responsiveness_multiplier
                    debug_log(f"[PHYSICS] Responsiveness multiplier: {responsiveness_multiplier} (based on angle {math.degrees(angle_to_target)}°)", "physics_turn_calc", 300)
                    debug_log(f"[PHYSICS] Final angular velocity: {angular_velocity} rad/s ({math.degrees(angular_velocity)} deg/s)", "physics_turn_calc", 300)

                    # Convert to radians for THIS frame based on actual time elapsed (dt)
                    # This makes turn speed independent of tick rate
                    angular_velocity_this_frame = angular_velocity * dt
                    debug_log(f"[PHYSICS] dt: {dt:.6f}s, Angular velocity this frame: {angular_velocity_this_frame:.6f} rad", "physics_turn_frame", 300)

                    if angle_to_target > 0.02:  # Only turn if we're not already aligned (about 1 degree)
                        debug_log(f"[PHYSICS] Need to turn, angle > 0.02 rad")

                        # Calculate how much to rotate this frame
                        # Cap rotation to prevent overshoot and ensure smooth motion
                        # Maximum rotation is either our target angular velocity or the remaining angle
                        # Also cap at a reasonable maximum per frame to prevent visual artifacts
                        max_rotation_per_frame = min(math.pi / 2, angular_velocity * dt * 2)  # Cap at 90 degrees or 2x target
                        rotation_this_frame = min(angular_velocity_this_frame, angle_to_target, max_rotation_per_frame)

                        debug_log(f"[PHYSICS] Max rotation per frame: {max_rotation_per_frame:.6f} rad", "physics_turn_rotation", 300)
                        debug_log(f"[PHYSICS] Calculated rotation this frame: {rotation_this_frame:.6f} rad", "physics_turn_rotation", 300)

                        # Determine turn direction using cross product
                        cross = current_dir[0] * target_dir[1] - current_dir[1] * target_dir[0]
                        if cross < 0:  # Turn clockwise
                            rotation_this_frame = -rotation_this_frame

                        debug_log(f"[PHYSICS] Rotation this frame: {rotation_this_frame} rad, cross product: {cross}", "physics_turn_rotation", 300)

                        # Rotate the current velocity by the calculated amount
                        cos_rot = math.cos(rotation_this_frame)
                        sin_rot = math.sin(rotation_this_frame)

                        rotated_x = current_dir[0] * cos_rot - current_dir[1] * sin_rot
                        rotated_y = current_dir[0] * sin_rot + current_dir[1] * cos_rot

                        debug_log(f"[PHYSICS] Rotated direction: ({rotated_x}, {rotated_y})", "physics_turn_rotation", 300)

                        # Calculate what the new total velocity should be
                        target_total_v = (rotated_x * current_speed, rotated_y * current_speed)

                        # Calculate what this turn vector needs to contribute
                        # Get velocity from all OTHER vectors (excluding this turn vector)
                        other_total_v = (0.0, 0.0)
                        for other_name, other_vector in self.vectors.items():
                            if other_name != name and other_vector.enabled:
                                other_total_v = (other_total_v[0] + other_vector.v[0], other_total_v[1] + other_vector.v[1])

                        # Set this vector's velocity to make the total equal the target
                        vector.v = (target_total_v[0] - other_total_v[0], target_total_v[1] - other_total_v[1])

                        debug_log(f"[PHYSICS] Setting turn vector velocity to: {vector.v}", "physics_turn_velocity_set", 300)

                        # No additional acceleration needed - we're directly setting velocity
                        vector.a = (0.0, 0.0)

                    else:
                        debug_log(f"[PHYSICS] Target direction reached! Finalizing turn...")

                        # Calculate what velocity we SHOULD have (original speed, new direction)
                        # Get the original speed from other vectors (excluding turn vector)
                        other_total_v = (0.0, 0.0)
                        for other_name, other_vector in self.vectors.items():
                            if other_name != name and other_vector.enabled:
                                other_total_v = (other_total_v[0] + other_vector.v[0], other_total_v[1] + other_vector.v[1])

                        original_speed = math.sqrt(other_total_v[0]**2 + other_total_v[1]**2)
                        final_velocity = (target_dir[0] * original_speed, target_dir[1] * original_speed)
                        debug_log(f"[PHYSICS] Original speed: {original_speed}, Final velocity: {final_velocity}")

                        # Replace all movement vectors with one final vector at original speed
                        movement_vectors_to_remove = []
                        for other_name, other_vector in list(self.vectors.items()):
                            if other_name != name and other_vector.enabled and (other_vector.v != (0.0, 0.0) or other_vector.a != (0.0, 0.0)):
                                movement_vectors_to_remove.append(other_name)

                        debug_log(f"[PHYSICS] Removing movement vectors: {movement_vectors_to_remove}")

                        # Remove old movement vectors
                        for remove_name in movement_vectors_to_remove:
                            if remove_name in self.vectors:
                                del self.vectors[remove_name]

                        # Replace with main movement vector - no auxiliary vectors needed
                        self.vectors["main"] = Vector(
                            name="main",
                            v=final_velocity,
                            a=(0.0, 0.0),
                            enabled=True,
                            duration=None  # Persistent movement
                        )
                        debug_log(f"[PHYSICS] Created main movement vector with velocity {final_velocity}")

                        # Remove this turn vector
                        vectors_to_remove.append(name)
                        debug_log(f"[PHYSICS] Marking turn vector '{name}' for removal")
                        continue
                else:
                    debug_log(f"[PHYSICS] No meaningful velocity to turn (speed={current_speed}), removing turn vector")
                    # No meaningful velocity to turn, just remove this vector
                    vectors_to_remove.append(name)
                    continue

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
            debug_log(f"[PHYSICS] Removing vector: {name}")
            self.remove_vector(name)

        # Calculate physics
        total_v, total_a = self._calculate_totals()
        debug_log(f"[PHYSICS] Total velocity: {total_v}, Total acceleration: {total_a}", "physics_totals", 500)

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
        debug_log(f"[PHYSICS] Final velocity after integration: {final_velocity}", "physics_final_velocity", 500)

        # Calculate displacement
        dx = final_velocity[0] * dt
        dy = final_velocity[1] * dt
        debug_log(f"[PHYSICS] Displacement this frame: dx={dx}, dy={dy}", "physics_displacement", 500)

        # Apply movement with subpixel accuracy
        if abs(dx) > 0.01 or abs(dy) > 0.01:  # Only move if significant
            int_dx, int_dy = self.subpixel_tracker.update(dx, dy)
            if int_dx != 0 or int_dy != 0:
                debug_log(f"[PHYSICS] Moving mouse by: ({int_dx}, {int_dy})", "physics_mouse_move", 1000)
                mouse_move(int_dx, int_dy)
        else:
            debug_log(f"[PHYSICS] Movement too small, not moving mouse", "physics_no_move", 2000)

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
_mouse_vector_system = None

# Public API functions
def mouse_vector(name: Optional[str] = None, **properties) -> Optional[Dict]:
    """
    Create, update, or query motion vectors

    Examples:
        mouse_vector("move", v=(50, 0))                    # Move right at 50 px/s
        mouse_vector("thrust", a=(100, 0), duration=1000)  # Accelerate right for 1s
        mouse_vector("wobble", a=(0, 20),                  # Oscillating force
                     a_keyframes=[1.0, -1.0, 1.0, -1.0],
                     duration=2000)

        # Query existing vector
        state = mouse_vector("move")
    """
    if name is not None and not properties:
        # Query mode
        return _mouse_vector_system.get_vector(name)
    else:
        # Create/update mode
        vector_name = _mouse_vector_system.add_or_update_vector(name, **properties)
        return {'name': vector_name}

def mouse_vector_get_state() -> Dict:
    """Get complete system state including all vectors and resulting motion"""
    return _mouse_vector_system.get_state()

def mouse_vector_stop():
    """Remove all vectors (instant stop)"""
    _mouse_vector_system.stop_all()

def mouse_vector_disable():
    """Disable all vectors without removing them"""
    _mouse_vector_system.disable_all()

def mouse_vector_remove(name: str) -> bool:
    """Remove specific named vector"""
    return _mouse_vector_system.remove_vector(name)

def mouse_vector_list() -> List[str]:
    """Get list of all active vector names"""
    return _mouse_vector_system.list_vectors()

def mouse_vector_enable_dpi_scaling():
    """Enable DPI-aware scaling for consistent movement across displays"""
    settings.set("user.mouse_vector_dpi_scaling", True)

def mouse_vector_disable_dpi_scaling():
    """Disable DPI scaling for raw pixel movement"""
    settings.set("user.mouse_vector_dpi_scaling", False)

def mouse_vector_get_dpi_info() -> dict:
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

def mouse_vector_curve_turn(name: str, target_direction: Vector2D, turn_radius: float = 200.0, duration: float = 2000.0, interpolation: str = "cubic") -> str:
    """
    Create a physics-based curved turn using proper centripetal force.

    Args:
        name: Name for the turning vector
        target_direction: Final direction to turn towards (will be normalized)
        turn_radius: Radius of the turning circle in pixels (smaller = tighter turn)
        duration: IGNORED - turn duration is now physics-based (speed-dependent)
        interpolation: IGNORED - turning is now purely physics-based

    Returns:
        Vector name

    Example:
        # Turn from current direction toward down with a 150px radius curve
        mouse_vector_curve_turn("smooth_turn", (0, 1), turn_radius=150)

    Physics:
        - Turn rate is determined by: angular_velocity = current_speed / turn_radius
        - Higher speed = faster turning (like a real object)
        - Smaller radius = tighter/faster turning
        - Speed remains constant throughout the turn
    """
    debug_log(f"[CURVE_TURN] Starting curve turn: name='{name}', target_direction={target_direction}, turn_radius={turn_radius}")

    # Normalize target direction
    magnitude = math.sqrt(target_direction[0]**2 + target_direction[1]**2)
    if magnitude > 0:
        target_direction = (target_direction[0] / magnitude, target_direction[1] / magnitude)
    else:
        target_direction = (0.0, 1.0)  # Default to down

    debug_log(f"[CURVE_TURN] Normalized target direction: {target_direction}")

    # Create a special vector that stores turn parameters
    # The physics system will calculate the proper centripetal force each frame
    # No duration - the turn completes when the velocity aligns with target
    vector_name = _mouse_vector_system.add_or_update_vector(
        name,
        v=(0.0, 0.0),  # No direct velocity - will be calculated
        duration=None,  # Physics-based - completes when aligned
        # Store turn parameters in custom fields
        **{
            '_turn_target': target_direction,
            '_turn_radius': turn_radius,
            '_turn_type': 'centripetal'
        }
    )

    debug_log(f"[CURVE_TURN] Created/updated vector '{vector_name}' with turn parameters")
    return vector_name

def mouse_vector_spiral_turn(name: str, turn_rate: float = 0.5, turn_strength: float = 100.0, duration: float = 3000.0) -> str:
    """
    Create a spiral/circular turn using physics.

    Args:
        name: Name for the spiral vector
        turn_rate: How fast to rotate (radians per second)
        turn_strength: Magnitude of the centripetal force
        duration: How long to maintain the spiral

    Returns:
        Vector name
    """
    # This would need to be implemented with dynamic acceleration updates
    # For now, create a strong perpendicular force
    return _mouse_vector_system.add_or_update_vector(
        name,
        a=(0, turn_strength),  # Initial perpendicular force
        a_keyframes=[0.0, 1.0, 1.0, 0.5],  # Maintain then reduce
        a_interpolation="ease_in_out",
        duration=duration
    )

def mouse_vector_stop_turn() -> bool:
    """
    Stop any active turn and continue moving in the current direction.

    This captures the current total velocity (movement + turn) and replaces
    all vectors with a single movement vector in that direction.

    Returns:
        True if a turn was stopped, False if no turn was active
    """
    if not _mouse_vector_system:
        return False

    # Check if there's an active turn vector
    turn_vector = None
    for name, vector in _mouse_vector_system.vectors.items():
        if hasattr(vector, '_turn_type') and vector._turn_type == 'centripetal':
            turn_vector = vector
            break

    if not turn_vector:
        return False  # No active turn

    debug_log("[STOP_TURN] Stopping turn and preserving current direction")

    # Calculate current total velocity
    total_v, _ = _mouse_vector_system._calculate_totals()
    current_speed = math.sqrt(total_v[0]**2 + total_v[1]**2)

    debug_log(f"[STOP_TURN] Current total velocity: {total_v}, speed: {current_speed}")

    if current_speed > 0.1:
        # Clear all vectors
        _mouse_vector_system.vectors.clear()
        _mouse_vector_system.current_velocity = (0.0, 0.0)  # Reset accumulated velocity

        # Create main movement vector in current direction
        _mouse_vector_system.vectors["main"] = Vector(
            name="main",
            v=total_v,
            a=(0.0, 0.0),
            enabled=True,
            duration=None
        )

        debug_log(f"[STOP_TURN] Created main movement vector with velocity: {total_v}")
    else:
        # No meaningful velocity, just stop everything
        _mouse_vector_system.stop_all()
        debug_log("[STOP_TURN] No meaningful velocity, stopping all movement")

    return True

def mouse_vector_multiply_speed(multiplier: float = 2.0) -> bool:
    """
    Multiply the current movement speed by a factor.

    This function preserves all existing vectors and their names,
    simply scaling their velocities by the multiplier.

    Args:
        multiplier: Factor to multiply speed by (2.0 = double speed)

    Returns:
        True if speed was changed, False if no movement
    """
    if not _mouse_vector_system:
        return False

    # Check if there are any enabled vectors
    enabled_vectors = [v for v in _mouse_vector_system.vectors.values() if v.enabled]
    if not enabled_vectors:
        debug_log(f"[SPEED_MULTIPLY] No enabled vectors to multiply")
        return False

    # Calculate current total velocity for logging
    total_v, _ = _mouse_vector_system._calculate_totals()
    current_speed = math.sqrt(total_v[0]**2 + total_v[1]**2)

    if current_speed < 0.1:
        debug_log(f"[SPEED_MULTIPLY] No meaningful movement to multiply")
        return False

    debug_log(f"[SPEED_MULTIPLY] Current velocity: {total_v}, speed: {current_speed}")
    debug_log(f"[SPEED_MULTIPLY] Multiplying speed by {multiplier}x for {len(enabled_vectors)} vectors")

    # Multiply velocity of all enabled vectors
    for vector in enabled_vectors:
        old_velocity = vector.v
        vector.v = (vector.v[0] * multiplier, vector.v[1] * multiplier)
        debug_log(f"[SPEED_MULTIPLY] Vector '{vector.name}': {old_velocity} -> {vector.v}")

    return True

def mouse_vector_change_direction(direction: Vector2D) -> bool:
    """
    Change movement direction while preserving current speed.

    This function preserves all existing vectors and their names,
    changing their direction while maintaining their relative speeds.

    Args:
        direction: New direction vector (will be normalized)

    Returns:
        True if direction was changed, False if no movement
    """
    if not _mouse_vector_system:
        return False

    # Check if there are any enabled vectors
    enabled_vectors = [v for v in _mouse_vector_system.vectors.values() if v.enabled]
    if not enabled_vectors:
        debug_log(f"[CHANGE_DIR] No enabled vectors to redirect")
        return False

    # Calculate current total velocity and speed
    total_v, _ = _mouse_vector_system._calculate_totals()
    current_speed = math.sqrt(total_v[0]**2 + total_v[1]**2)

    if current_speed < 0.1:
        debug_log(f"[CHANGE_DIR] No meaningful movement to redirect")
        return False

    # Normalize the new direction
    direction_magnitude = math.sqrt(direction[0]**2 + direction[1]**2)
    if direction_magnitude == 0:
        debug_log(f"[CHANGE_DIR] Invalid direction vector")
        return False

    normalized_direction = (direction[0] / direction_magnitude, direction[1] / direction_magnitude)

    debug_log(f"[CHANGE_DIR] Current velocity: {total_v}, speed: {current_speed}")
    debug_log(f"[CHANGE_DIR] New direction: {normalized_direction}")
    debug_log(f"[CHANGE_DIR] Redirecting {len(enabled_vectors)} vectors")

    # Change direction of all enabled vectors while preserving their individual speeds
    for vector in enabled_vectors:
        # Calculate this vector's current speed
        vector_speed = math.sqrt(vector.v[0]**2 + vector.v[1]**2)
        if vector_speed > 0.1:  # Only redirect vectors with meaningful speed
            old_velocity = vector.v
            # Apply the new direction with this vector's speed
            vector.v = (normalized_direction[0] * vector_speed, normalized_direction[1] * vector_speed)
            debug_log(f"[CHANGE_DIR] Vector '{vector.name}': {old_velocity} -> {vector.v}")

    return True

def mouse_vector_scale(multiplier: float = 2.0, duration: float = None, interpolation: str = "linear") -> bool:
    """
    Scale current movement speed by a multiplier.

    Args:
        multiplier: Factor to multiply speed by (2.0 = double speed)
        duration: Time in milliseconds to complete the scaling (None = instant)
        interpolation: How to animate the scaling ("linear", "ease_in", "ease_out", "ease_in_out")

    Returns:
        True if speed was changed, False if no movement
    """
    if not _mouse_vector_system:
        return False

    # Calculate current total velocity
    total_v, _ = _mouse_vector_system._calculate_totals()
    current_speed = math.sqrt(total_v[0]**2 + total_v[1]**2)

    if current_speed < 0.1:
        debug_log(f"[SCALE] No meaningful movement to scale")
        return False

    if duration is None:
        # Instant scaling (same as multiply_speed)
        return mouse_vector_multiply_speed(multiplier)
    else:
        # Animated scaling using keyframes
        debug_log(f"[SCALE] Animating scale from 1.0 to {multiplier} over {duration}ms")

        # Clear all vectors and create animated scaling vector
        _mouse_vector_system.vectors.clear()
        _mouse_vector_system.current_velocity = (0.0, 0.0)

        # Create scaling vector with keyframes from current speed to target speed
        target_velocity = (total_v[0] * multiplier, total_v[1] * multiplier)
        _mouse_vector_system.vectors["main"] = Vector(
            name="main",
            v=target_velocity,
            v_keyframes=[1.0/multiplier, 1.0],  # Start at reduced scale, end at full scale
            v_interpolation=interpolation,
            duration=duration,
            enabled=True
        )
        return True

def mouse_vector_scale_to(target_speed: float, duration: float = None, interpolation: str = "linear") -> bool:
    """
    Set movement speed to an exact value while preserving direction.

    Args:
        target_speed: Target speed in pixels/second
        duration: Time in milliseconds to reach target speed (None = instant)
        interpolation: How to animate the change ("linear", "ease_in", "ease_out", "ease_in_out")

    Returns:
        True if speed was changed, False if no movement
    """
    if not _mouse_vector_system:
        return False

    # Calculate current total velocity
    total_v, _ = _mouse_vector_system._calculate_totals()
    current_speed = math.sqrt(total_v[0]**2 + total_v[1]**2)

    if current_speed < 0.1:
        debug_log(f"[SCALE_TO] No meaningful movement to scale")
        return False

    # Calculate current direction
    current_dir = (total_v[0] / current_speed, total_v[1] / current_speed)
    target_velocity = (current_dir[0] * target_speed, current_dir[1] * target_speed)

    debug_log(f"[SCALE_TO] Current speed: {current_speed}, target speed: {target_speed}")
    debug_log(f"[SCALE_TO] Current velocity: {total_v}, target velocity: {target_velocity}")

    if duration is None:
        # Instant change
        _mouse_vector_system.vectors.clear()
        _mouse_vector_system.current_velocity = (0.0, 0.0)
        _mouse_vector_system.vectors["main"] = Vector(
            name="main",
            v=target_velocity,
            a=(0.0, 0.0),
            enabled=True,
            duration=None
        )
    else:
        # Animated change using keyframes
        scale_factor = target_speed / current_speed
        debug_log(f"[SCALE_TO] Animating scale factor: {scale_factor} over {duration}ms")

        _mouse_vector_system.vectors.clear()
        _mouse_vector_system.current_velocity = (0.0, 0.0)
        _mouse_vector_system.vectors["main"] = Vector(
            name="main",
            v=target_velocity,
            v_keyframes=[1.0/scale_factor, 1.0],  # Start at current scale, end at target scale
            v_interpolation=interpolation,
            duration=duration,
            enabled=True
        )

    return True

def mouse_vector_rotate(angle_degrees: float, duration: float = None, interpolation: str = "linear") -> bool:
    """
    Rotate current movement direction by a relative angle.

    Args:
        angle_degrees: Angle to rotate by in degrees (positive = clockwise)
        duration: Time in milliseconds to complete rotation (None = instant)
        interpolation: How to animate the rotation ("linear", "ease_in", "ease_out", "ease_in_out")

    Returns:
        True if direction was changed, False if no movement
    """
    if not _mouse_vector_system:
        return False

    # Calculate current total velocity
    total_v, _ = _mouse_vector_system._calculate_totals()
    current_speed = math.sqrt(total_v[0]**2 + total_v[1]**2)

    if current_speed < 0.1:
        debug_log(f"[ROTATE] No meaningful movement to rotate")
        return False

    # Calculate current direction
    current_dir = (total_v[0] / current_speed, total_v[1] / current_speed)

    # Calculate target direction
    angle_radians = math.radians(angle_degrees)
    cos_angle = math.cos(angle_radians)
    sin_angle = math.sin(angle_radians)

    target_dir = (
        current_dir[0] * cos_angle - current_dir[1] * sin_angle,
        current_dir[0] * sin_angle + current_dir[1] * cos_angle
    )
    target_velocity = (target_dir[0] * current_speed, target_dir[1] * current_speed)

    debug_log(f"[ROTATE] Rotating by {angle_degrees}° from {current_dir} to {target_dir}")

    if duration is None:
        # Instant rotation
        _mouse_vector_system.vectors.clear()
        _mouse_vector_system.current_velocity = (0.0, 0.0)
        _mouse_vector_system.vectors["main"] = Vector(
            name="main",
            v=target_velocity,
            a=(0.0, 0.0),
            enabled=True,
            duration=None
        )
    else:
        # Animated rotation using curve turn - use "turn" as the only auxiliary vector name
        debug_log(f"[ROTATE] Using curve turn for animated rotation over {duration}ms")
        return mouse_vector_curve_turn("turn", target_dir, turn_radius=200.0) is not None

    return True

def mouse_vector_rotate_to(angle_degrees: float, duration: float = None, interpolation: str = "linear") -> bool:
    """
    Set movement direction to an absolute angle while preserving speed.

    Args:
        angle_degrees: Target angle in degrees (0° = right, 90° = down, 180° = left, 270° = up)
        duration: Time in milliseconds to reach target angle (None = instant)
        interpolation: How to animate the rotation ("linear", "ease_in", "ease_out", "ease_in_out")

    Returns:
        True if direction was changed, False if no movement
    """
    if not _mouse_vector_system:
        return False

    # Calculate current total velocity
    total_v, _ = _mouse_vector_system._calculate_totals()
    current_speed = math.sqrt(total_v[0]**2 + total_v[1]**2)

    if current_speed < 0.1:
        debug_log(f"[ROTATE_TO] No meaningful movement to rotate")
        return False

    # Calculate target direction from angle
    angle_radians = math.radians(angle_degrees)
    target_dir = (math.cos(angle_radians), math.sin(angle_radians))
    target_velocity = (target_dir[0] * current_speed, target_dir[1] * current_speed)

    debug_log(f"[ROTATE_TO] Setting direction to {angle_degrees}° ({target_dir}), speed: {current_speed}")

    if duration is None:
        # Instant rotation
        _mouse_vector_system.vectors.clear()
        _mouse_vector_system.current_velocity = (0.0, 0.0)
        _mouse_vector_system.vectors["main"] = Vector(
            name="main",
            v=target_velocity,
            a=(0.0, 0.0),
            enabled=True,
            duration=None
        )
    else:
        # Animated rotation using curve turn - use "turn" as the only auxiliary vector name
        debug_log(f"[ROTATE_TO] Using curve turn for animated rotation to {angle_degrees}° over {duration}ms")
        return mouse_vector_curve_turn("turn", target_dir, turn_radius=200.0) is not None

    return True

# Talon Actions
@mod.action_class
class Actions:
    def mouse_vector(
        name_or_options: str = None,
        v: Tuple[float, float] = None,
        a: Tuple[float, float] = None,
        d: Tuple[float, float] = None,
        enabled: bool = None,
        duration: float = None,
        speed: float = None,
        default_speed: float = None,
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
            name_or_options: Vector name (for query mode) or string of options
                           (for Talon usage, e.g., "direction=(-1, 0); speed=50")
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
            # Regular Python usage:
            actions.user.mouse_vector("move", v=(50, 0))
            actions.user.mouse_vector("boost", a=(100, 0), duration=1000)

            # Talon string usage:
            actions.user.mouse_vector("direction=(-1, 0); speed=50")
            actions.user.mouse_vector("name=boost; a=(100,0); duration=500")

            # Query mode:
            actions.user.mouse_vector("move")  # Returns state of "move" vector
        """
        # Initialize name and handle string options parsing
        name = None

        # Check if first parameter contains options (for Talon usage)
        if name_or_options and "=" in name_or_options:
            # Parse as options string for Talon
            try:
                options = name_or_options.split(";")
                for option in options:
                    if "=" not in option:
                        continue
                    key, value = option.split("=", 1)  # Split only on first =
                    key = key.strip()
                    value = value.strip()

                    if key == "name":
                        name = value
                    elif key == "v":
                        v = _parse_tuple_string(value)
                    elif key == "a":
                        a = _parse_tuple_string(value)
                    elif key == "d":
                        d = _parse_tuple_string(value)
                    elif key == "duration":
                        duration = float(value)
                    elif key == "speed":
                        speed = float(value)
                    elif key == "default_speed":
                        default_speed = float(value)
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
        else:
            # Treat as name (for query mode or regular Python usage)
            name = name_or_options

        # Build properties dict from non-None arguments
        properties = {}

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
        if default_speed is not None:
            properties['default_speed'] = default_speed
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

        return mouse_vector(name, **properties)

    def mouse_vector_get_state() -> dict:
        """Get complete system state including all vectors and resulting motion"""
        return mouse_vector_get_state()

    def mouse_vector_stop():
        """Remove all vectors (instant stop)"""
        mouse_vector_stop()

    def mouse_vector_disable():
        """Disable all vectors without removing them"""
        mouse_vector_disable()

    def mouse_vector_remove(name: str) -> bool:
        """Remove specific named vector"""
        return mouse_vector_remove(name)

    def mouse_vector_list() -> list:
        """Get list of all active vector names"""
        return mouse_vector_list()

    def mouse_vector_enable_dpi_scaling():
        """Enable DPI-aware scaling for consistent movement across displays"""
        mouse_vector_enable_dpi_scaling()

    def mouse_vector_disable_dpi_scaling():
        """Disable DPI scaling for raw pixel movement"""
        mouse_vector_disable_dpi_scaling()

    def mouse_vector_get_dpi_info() -> dict:
        """Get current DPI information for debugging"""
        return mouse_vector_get_dpi_info()

    def mouse_vector_curve_turn(name: str, target_direction_x: float, target_direction_y: float, turn_radius: float = 200.0, duration: float = None, interpolation: str = "cubic") -> dict:
        """
        Create a physics-based curved turn using proper centripetal force.

        Args:
            name: Name for the turning vector
            target_direction_x: X component of direction to turn towards
            target_direction_y: Y component of direction to turn towards
            turn_radius: Radius of the turning circle in pixels (smaller = tighter turn)
            duration: IGNORED - turn duration is now physics-based (speed-dependent)
            interpolation: IGNORED - turning is now purely physics-based

        Returns:
            Dictionary with vector name

        Physics:
            - Turn rate is determined by: angular_velocity = current_speed / turn_radius
            - Higher speed = faster turning (like a real object)
            - Smaller radius = tighter/faster turning
            - Speed remains constant throughout the turn
        """
        debug_log(f"[TALON_ACTION] mouse_vector_curve_turn called: name='{name}', target_direction=({target_direction_x}, {target_direction_y}), turn_radius={turn_radius}")
        # Duration is ignored - turns are now physics-based
        vector_name = mouse_vector_curve_turn(name, (target_direction_x, target_direction_y), turn_radius)
        debug_log(f"[TALON_ACTION] mouse_vector_curve_turn returning: {{'name': '{vector_name}'}}")
        return {'name': vector_name}

    def mouse_vector_spiral_turn(name: str, turn_rate: float = 0.5, turn_strength: float = 100.0, duration: float = 3000.0) -> dict:
        """
        Create a spiral/circular turn using physics.

        Args:
            name: Name for the spiral vector
            turn_rate: How fast to rotate (radians per second)
            turn_strength: Magnitude of the centripetal force
            duration: How long to maintain the spiral

        Returns:
            Dictionary with vector name
        """
        vector_name = mouse_vector_spiral_turn(name, turn_rate, turn_strength, duration)
        return {'name': vector_name}

    def mouse_vector_multiply_speed(multiplier: float = 2.0) -> bool:
        """
        Multiply the current movement speed by a factor.

        Args:
            multiplier: Factor to multiply speed by (2.0 = double speed)

        Returns:
            True if speed was changed, False if no movement
        """
        return mouse_vector_multiply_speed(multiplier)

    def mouse_vector_stop_turn() -> bool:
        """
        Stop any active turn and continue moving in the current direction.

        This captures the current total velocity (movement + turn) and replaces
        all vectors with a single movement vector in that direction.

        Returns:
            True if a turn was stopped, False if no turn was active
        """
        return mouse_vector_stop_turn()

    def mouse_vector_enable_debug_logging():
        """Enable debug logging for physics updates and turn calculations"""
        global _debug_logging_enabled
        _debug_logging_enabled = True
        print("[DEBUG] Mouse vectors debug logging enabled")

    def mouse_vector_disable_debug_logging():
        """Disable debug logging for physics updates and turn calculations"""
        global _debug_logging_enabled
        _debug_logging_enabled = False
        print("[DEBUG] Mouse vectors debug logging disabled")

    def mouse_vector_scale(multiplier: float = 2.0, duration: float = None, interpolation: str = "linear") -> bool:
        """
        Scale current movement speed by a multiplier.

        Args:
            multiplier: Factor to multiply speed by (2.0 = double speed)
            duration: Time in milliseconds to complete the scaling (None = instant)
            interpolation: How to animate the scaling ("linear", "ease_in", "ease_out", "ease_in_out")

        Returns:
            True if speed was changed, False if no movement
        """
        return mouse_vector_scale(multiplier, duration, interpolation)

    def mouse_vector_scale_to(target_speed: float, duration: float = None, interpolation: str = "linear") -> bool:
        """
        Set movement speed to an exact value while preserving direction.

        Args:
            target_speed: Target speed in pixels/second
            duration: Time in milliseconds to reach target speed (None = instant)
            interpolation: How to animate the change ("linear", "ease_in", "ease_out", "ease_in_out")

        Returns:
            True if speed was changed, False if no movement
        """
        return mouse_vector_scale_to(target_speed, duration, interpolation)

    def mouse_vector_rotate(angle_degrees: float, duration: float = None, interpolation: str = "linear") -> bool:
        """
        Rotate current movement direction by a relative angle.

        Args:
            angle_degrees: Angle to rotate by in degrees (positive = clockwise)
            duration: Time in milliseconds to complete rotation (None = instant)
            interpolation: How to animate the rotation ("linear", "ease_in", "ease_out", "ease_in_out")

        Returns:
            True if direction was changed, False if no movement
        """
        return mouse_vector_rotate(angle_degrees, duration, interpolation)

    def mouse_vector_rotate_to(angle_degrees: float, duration: float = None, interpolation: str = "linear") -> bool:
        """
        Set movement direction to an absolute angle while preserving speed.

        Args:
            angle_degrees: Target angle in degrees (0° = right, 90° = down, 180° = left, 270° = up)
            duration: Time in milliseconds to reach target angle (None = instant)
            interpolation: How to animate the rotation ("linear", "ease_in", "ease_out", "ease_in_out")

        Returns:
            True if direction was changed, False if no movement
        """
        return mouse_vector_rotate_to(angle_degrees, duration, interpolation)

def on_ready():
    global _mouse_vector_system
    _mouse_vector_system = MouseVectorsSystem()

app.register("ready", on_ready)