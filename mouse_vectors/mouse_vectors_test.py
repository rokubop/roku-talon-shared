# """
# Mouse Vectors Test and Example Usage
# This file demonstrates the mouse vectors system with various examples.
# """

# from .mouse_vectors import mouse_vectors

# def test_basic_movement():
#     """Test basic velocity-based movement"""
#     # Move right at 50 pixels per second
#     mouse_vectors("move_right", v=(50, 0))

#     # Move diagonally
#     mouse_vectors("diagonal", v=(30, 30))

#     # Stop movement
#     mouse_vectors("move_right", enabled=False)

# def test_acceleration():
#     """Test acceleration-based physics"""
#     # Apply rightward acceleration for 1 second
#     mouse_vectors("thrust", a=(100, 0), duration=1000)

#     # Add perpendicular force
#     mouse_vectors("turn", a=(0, 50), duration=500)

#     # Apply braking force
#     mouse_vectors("brake", a=(-30, 0))

# def test_direction_speed_interface():
#     """Test direction + speed interface"""
#     # Move right at 50 px/s using direction interface
#     mouse_vectors("move", direction=(1, 0), speed=50)

#     # Boost down using acceleration
#     mouse_vectors("boost", direction=(0, 1), acceleration=100, duration=500)

# def test_keyframe_animation():
#     """Test keyframe-based animation"""
#     # Variable acceleration over time (ease in/out)
#     mouse_vectors("gas", a=(150, 0),
#                   a_keyframes=[0.0, 1.0, 0.3],
#                   a_interpolation="ease_in_out",
#                   duration=2000)

#     # Pulsing motion
#     mouse_vectors("pulse", a=(80, 0),
#                   a_keyframes=[0.0, 1.0, 0.0, 1.0, 0.0],
#                   a_interpolation="linear",
#                   duration=1000)

# def test_complex_composition():
#     """Test multiple vectors working together"""
#     # Base rightward movement
#     mouse_vectors("base", v=(30, 0))

#     # Temporary acceleration boost
#     mouse_vectors("boost", a=(100, 0), duration=500)

#     # Perpendicular drift
#     mouse_vectors("drift", v=(0, 10))

#     # Oscillating wobble effect
#     mouse_vectors("wobble", a=(0, 20),
#                   a_keyframes=[1.0, -1.0, 1.0, -1.0],
#                   duration=2000)

# def test_gaming_controls():
#     """Test gaming-style physics controls"""
#     # WASD-style movement with physics
#     mouse_vectors("forward", a=(100, 0))      # W key pressed
#     mouse_vectors("forward", a=(0, 0))        # W key released (coast)
#     mouse_vectors("strafe", a=(0, 50))        # A key pressed

#     # Mouse look with momentum and smoothing (example values)
#     # mouse_vectors("look", v=(mouse_delta_x, mouse_delta_y))  # Direct mouse input
#     # mouse_vectors("smoothing", a=(-velocity_x * 0.1, -velocity_y * 0.1))  # Friction

# def test_projectile_motion():
#     """Test realistic projectile physics"""
#     # Launch with initial velocity
#     mouse_vectors("launch", v=(100, -50))

#     # Apply gravity
#     mouse_vectors("gravity", a=(0, 30))

# def test_query_and_state():
#     """Test querying vector state"""
#     # Create a vector
#     mouse_vectors("test", v=(50, 0), duration=1000)

#     # Query specific vector
#     vector_state = mouse_vectors("test")
#     print(f"Vector state: {vector_state}")

#     # Get complete system state
#     from .mouse_vectors import mouse_vectors_get_state
#     system_state = mouse_vectors_get_state()
#     print(f"System state: {system_state}")

#     # List all vectors
#     from .mouse_vectors import mouse_vectors_list
#     all_vectors = mouse_vectors_list()
#     print(f"All vectors: {all_vectors}")

# # Example usage scenarios
# if __name__ == "__main__":
#     # This would be called from Talon voice commands or other triggers

#     # Simple movement
#     test_basic_movement()

#     # Physics-based gaming controls
#     test_gaming_controls()

#     # Advanced animation
#     test_keyframe_animation()
