# Mouse Vectors System

A physics-based mouse motion system using the intuitive concept of **force vectors**. Like arrows in Blender's transform gizmo, each vector represents a velocity or acceleration that combines additively to create realistic mouse movement.

## Features

- **Physics-Based Motion**: True velocity and acceleration vectors with realistic physics integration
- **Named Vectors**: Create, update, and manage multiple named motion vectors
- **Additive Combination**: All active vectors sum together each frame for complex motion
- **Target-Based Movement**: Displacement vectors for precise positioning
- **Keyframe Animation**: Animate vector properties over time with multiple interpolation types
- **Subpixel Accuracy**: Maintains fractional pixel positions for smooth motion
- **Voice Control**: Full Talon voice command integration

## Vector Types

The system supports three fundamental vector types, each with different physics behaviors:

### Velocity Vectors (`v`)
Continuous motion at a constant rate. Multiple velocity vectors sum together additively.
- **Use case**: Constant movement, base motion, steady drift
- **Physics**: Additive combination
- **Example**: `mouse_vector("drift", v=(30, 0))` # Move right at 30 px/s

### Acceleration Vectors (`a`)
Apply forces that change velocity over time. Multiple acceleration vectors sum together.
- **Use case**: Thrust, braking, forces, dynamic motion
- **Physics**: Integrated into velocity, then into position
- **Example**: `mouse_vector("thrust", a=(100, 0), duration=1000)` # Accelerate right

### Displacement Vectors (`d`)
Target-based movement that aims for a specific relative position.
- **Use case**: Precise positioning, "move to target" behavior
- **Physics**: Independent targeting (non-additive)
- **Example**: `mouse_vector("target", d=(100, 50), duration=2000)` # Move to offset position

> **Note**: Displacement vectors override their own velocity to reach their target, making them fundamentally different from velocity/acceleration vectors which combine additively.

## Quick Start

```python
from mouse_vector import mouse_vector

# Basic movement - move right at 50 pixels/second
mouse_vector("move", v=(50, 0))

# Physics acceleration - accelerate right for 1 second
mouse_vector("thrust", a=(100, 0), duration=1000)

# Stop all movement
mouse_vector_stop()
```

## API Reference

### Core Function

```python
def mouse_vector(name: str = None, **properties) -> dict:
    """Create, update, or query motion vectors"""
```

### Vector Properties

- **`v`**: `(x, y)` - Velocity vector in pixels/second
- **`a`**: `(x, y)` - Acceleration vector in pixels/second²
- **`d`**: `(x, y)` - Displacement vector in pixels (target-based movement)
- **`duration`**: `float` - How long vector exists in milliseconds
- **`enabled`**: `bool` - Whether vector affects movement
- **`direction`**: `(x, y)` - Unit vector for direction-based movement
- **`speed`**: `float` - Magnitude for direction-based movement
- **`acceleration`**: `float` - Magnitude for direction-based acceleration
- **`max_speed`**: `float` - Maximum speed limit in pixels/second (caps velocity + acceleration)

### Animation Properties

- **`a_keyframes`**: `list` - Acceleration multipliers over time
- **`a_interpolation`**: `str` - Interpolation type for acceleration
- **`v_keyframes`**: `list` - Velocity multipliers over time
- **`v_interpolation`**: `str` - Interpolation type for velocity
- **`d_keyframes`**: `list` - Displacement multipliers over time
- **`d_interpolation`**: `str` - Interpolation type for displacement
- **`a_interpolation`**: `str` - Interpolation type ("linear", "ease_in_out", etc.)
- **`v_keyframes`**: `list` - Velocity multipliers over time
- **`v_interpolation`**: `str` - Velocity interpolation type

## Usage Examples

### Basic Movement

```python
# Create/update named vectors
mouse_vector("movement", v=(50, 0))                    # Move right at 50 px/s
mouse_vector("movement", v=(0, 50))                    # Update to move down
mouse_vector("movement", enabled=False)                # Stop movement

# Query existing vectors
current = mouse_vector("movement")                     # Get current state
```

### Physics-Based Control

```python
# Apply acceleration forces
mouse_vector("thrust", a=(100, 0), duration=1000)     # Accelerate right for 1s
mouse_vector("turn", a=(0, 50), duration=500)         # Add downward force
mouse_vector("brake", a=(-30, 0))                     # Apply opposing force
```

### Direction + Speed Interface

```python
# Alternative syntax for intuitive control
mouse_vector("move", direction=(1, 0), speed=50)      # Move right at 50 px/s
mouse_vector("boost", direction=(0, 1), acceleration=100, duration=500)  # Boost down
```

### Target-Based Movement (Displacement)

```python
# Move to a specific target position relative to current location
mouse_vector("target", d=(100, 50), duration=2000)    # Move 100px right, 50px down over 2s
mouse_vector("quick_move", d=(200, 0))                 # Move 200px right at default speed

# Animated displacement with keyframes
mouse_vector("growing_target", d=(150, 100),
              d_keyframes=[0.0, 0.5, 1.0],             # Start slow, accelerate, then reach target
              d_interpolation="ease_in_out",
              duration=3000)

# Displacement with variable target size
mouse_vector("shrinking_target", d=(300, 0),
              d_keyframes=[1.2, 1.0, 0.8, 1.0],        # Overshoot then settle
              d_interpolation="bezier",
              duration=2500)
```

### Advanced Animation

```python
# Variable acceleration over time
mouse_vector("gas", a=(150, 0),
              a_keyframes=[0.0, 1.0, 0.3],
              a_interpolation="ease_in_out",
              duration=2000)

# Pulsing motion
mouse_vector("pulse", a=(80, 0),
              a_keyframes=[0.0, 1.0, 0.0, 1.0, 0.0],
              a_interpolation="linear",
              duration=1000)
```

### Multiple Vector Composition

```python
# Base movement + temporary effects
mouse_vector("base", v=(30, 0))                       # Base rightward motion
mouse_vector("boost", a=(100, 0), duration=500)       # Temporary acceleration
mouse_vector("drift", v=(0, 10))                      # Perpendicular drift
mouse_vector("wobble", a=(0, 20),
              a_keyframes=[1.0, -1.0, 1.0, -1.0],
              duration=2000)                           # Oscillating force
```

## Control Functions

```python
# State management
mouse_vector_get_state()    # Get complete system state
mouse_vector_stop()         # Remove all vectors (instant stop)
mouse_vector_disable()      # Disable all vectors without removing them

# Vector management
mouse_vector_remove(name)   # Remove specific named vector
mouse_vector_list()         # Get list of all active vector names
```

## Voice Commands

The system includes comprehensive voice control via Talon:

```
# Velocity-based movement
mouse move right          # Basic velocity movement (continuous)
mouse move left/up/down   # Velocity in other directions

# Acceleration-based movement
mouse thrust right        # Acceleration-based movement (builds up speed)
mouse boost right         # Temporary acceleration burst
mouse brake               # Apply opposing force to slow down

# Target-based movement (displacement)
mouse target right        # Move to target position (precise)
mouse jump right          # Larger displacement movement
mouse slide right         # Animated displacement with easing

# Special effects
mouse wobble             # Oscillating motion effect
mouse pulse              # Pulsing acceleration
mouse orbit              # Circular motion pattern

# Control commands
mouse stop               # Stop all movement
mouse pause              # Disable all vectors without removing
mouse remove <name>      # Remove specific named vector
```

## Interpolation Types

- **`linear`**: Straight lines between keyframes
- **`ease_in`**: Slow start, fast finish
- **`ease_out`**: Fast start, slow finish
- **`ease_in_out`**: Slow start and finish, fast middle
- **`bezier`**: Smooth curves with automatic control points
- **`cubic`**: Cubic spline interpolation
- **`constant`**: Hold value until next keyframe

## Physics Behavior

### Vector Combination
All enabled vectors sum each frame:
```python
final_velocity = sum(all_velocity_vectors)
final_acceleration = sum(all_acceleration_vectors)
```

### Physics Integration
```python
velocity += acceleration * time_delta
position += velocity * time_delta
```

## Settings

- **`user.mouse_vector_tick_rate`**: Physics update rate in Hz (default: 60)
- **`user.mouse_vector_enabled`**: Enable/disable the system (default: True)

## Files

- **`mouse_vector.py`**: Core implementation
- **`mouse_vector.talon`**: Voice commands
- **`mouse_vector_test.py`**: Usage examples and tests
- **`mouse_vector.prd`**: Product requirements document

## Use Cases

- **Gaming Controls**: WASD movement with realistic physics
- **UI Navigation**: Smooth scrolling and magnetic attraction
- **Animation**: Complex motion patterns and effects
- **Accessibility**: Voice-controlled mouse movement with natural physics

## Speed-Capped Acceleration

```python
# Accelerate with speed limits using mouse_vector directly
mouse_vector("capped", v=(0, 0), a=(100, 0), max_speed=200)           # Start at 0, accelerate, cap at 200 px/s
mouse_vector("rocket", direction=(1, 0), acceleration=300, max_speed=500)  # High-acceleration rocket
mouse_vector("gentle", direction=(0, -1), acceleration=60, max_speed=120)  # Gentle acceleration

# Using string syntax for Talon commands
user.mouse_vector("name=accel; direction=(1, 0); speed=0; a=(120, 0); max_speed=200")

# Decelerate to zero using velocity keyframes
mouse_vector("main", v_keyframes=[1.0, 0.0], v_interpolation="ease_out", duration=2000)
mouse_vector("accel", v_keyframes=[1.0, 0.0], v_interpolation="ease_out", duration=1000)
```

The speed capping system ensures that:
- **Velocity vectors** are clamped to `max_speed` each frame
- **Acceleration vectors** are reduced when they would exceed `max_speed`
- **Physics remain realistic** - direction is preserved, only magnitude is limited
- **Multiple vectors** can have different speed limits independently
- **Deceleration** uses velocity keyframes to smoothly reduce speed to zero
