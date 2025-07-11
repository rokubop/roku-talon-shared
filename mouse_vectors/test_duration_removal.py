# """Test script to verify that vectors with duration are removed properly"""

# import time
# from mouse_vectors import mouse_vectors

# def test_acceleration_duration_removal():
#     """Test that acceleration vectors with duration are removed when expired"""
#     print("Testing acceleration vector with duration removal...")

#     # Create an acceleration vector with short duration
#     result = mouse_vectors("test_accel", a=(100, 0), duration=500)  # 500ms duration
#     print(f"Created vector: {result}")

#     # Check that vector exists
#     vector_info = mouse_vectors("test_accel")
#     print(f"Vector info immediately after creation: {vector_info}")

#     # Wait for duration to expire (600ms to be safe)
#     print("Waiting 600ms for vector to expire...")
#     time.sleep(0.6)

#     # Check if vector still exists (should be gone)
#     vector_info = mouse_vectors("test_accel")
#     print(f"Vector info after duration expired: {vector_info}")

#     if vector_info is None:
#         print("✓ SUCCESS: Acceleration vector was properly removed after duration expired")
#     else:
#         print("✗ FAILED: Acceleration vector still exists after duration expired")
#         print(f"  Time remaining: {vector_info.get('time_remaining', 'N/A')}")

# def test_velocity_duration_removal():
#     """Test that velocity vectors with duration are removed when expired"""
#     print("\nTesting velocity vector with duration removal...")

#     # Create a velocity vector with short duration
#     result = mouse_vectors("test_vel", v=(50, 0), duration=500)  # 500ms duration
#     print(f"Created vector: {result}")

#     # Check that vector exists
#     vector_info = mouse_vectors("test_vel")
#     print(f"Vector info immediately after creation: {vector_info}")

#     # Wait for duration to expire
#     print("Waiting 600ms for vector to expire...")
#     time.sleep(0.6)

#     # Check if vector still exists (should be gone)
#     vector_info = mouse_vectors("test_vel")
#     print(f"Vector info after duration expired: {vector_info}")

#     if vector_info is None:
#         print("✓ SUCCESS: Velocity vector was properly removed after duration expired")
#     else:
#         print("✗ FAILED: Velocity vector still exists after duration expired")
#         print(f"  Time remaining: {vector_info.get('time_remaining', 'N/A')}")

# if __name__ == "__main__":
#     # Ensure the system is enabled
#     from talon import settings
#     settings.set("user.mouse_vectors_enabled", True)

#     test_acceleration_duration_removal()
#     test_velocity_duration_removal()

#     # Clean up any remaining vectors
#     mouse_vectors(stop_all=True)
#     print("\nTest completed.")
