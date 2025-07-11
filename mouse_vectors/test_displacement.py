# """
# Test script to demonstrate displacement vector functionality.
# Run this in Talon's REPL to test the new displacement features.
# """

# # Test basic displacement
# actions.user.mouse_vectors("move_to_target", d=(100, 50), duration=2000)

# # Test displacement with keyframes (growing target)
# actions.user.mouse_vectors("growing_target",
#                           d=(200, 0),
#                           d_keyframes=[0.0, 0.5, 1.0],
#                           d_interpolation="bezier",
#                           duration=3000)

# # Test displacement combined with acceleration (should work, but displacement will dominate)
# actions.user.mouse_vectors("complex_motion",
#                           d=(150, 100),
#                           a=(10, 10),
#                           duration=2500)

# # Test string parsing for displacement
# actions.user.mouse_vectors("string_test", "d=(300, -100);duration=1500;d_keyframes=[0.0, 1.2, 1.0];d_interpolation=linear")

# # Check system state
# print("System state:", actions.user.mouse_vectors_get_state())

# # Stop all vectors
# # actions.user.mouse_vectors_stop()
