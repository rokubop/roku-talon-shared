#!/usr/bin/env python3
"""
Test script to verify direction-only changes preserve existing speed
"""

import sys
import os
import math

# Add the current directory to the path so we can import mouse_vectors
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the mouse vectors system
from mouse_vectors import MouseVectorsSystem

def test_direction_change_preserves_speed():
    """Test that changing direction only preserves the existing speed"""
    print("Testing direction change while preserving speed...")

    system = MouseVectorsSystem()

    # Step 1: Create initial movement (equivalent to "mouse move start left")
    print("\n1. Creating initial leftward movement with speed 50...")
    system.add_or_update_vector("move", v=(-50, 0))

    vector = system.get_vector("move")
    initial_speed = math.sqrt(vector['v'][0]**2 + vector['v'][1]**2)
    print(f"   Initial velocity: {vector['v']}")
    print(f"   Initial speed: {initial_speed}")

    # Step 2: Change direction to down (equivalent to "mouse move down")
    print("\n2. Changing direction to down...")
    system.add_or_update_vector("move", direction=(0, 1))

    vector = system.get_vector("move")
    final_speed = math.sqrt(vector['v'][0]**2 + vector['v'][1]**2)
    print(f"   Final velocity: {vector['v']}")
    print(f"   Final speed: {final_speed}")

    # Step 3: Verify speed is preserved
    speed_diff = abs(final_speed - initial_speed)
    print(f"\n3. Speed difference: {speed_diff}")

    if speed_diff < 0.01:  # Allow for small floating point differences
        print("✅ SUCCESS: Speed was preserved when changing direction!")
        return True
    else:
        print("❌ FAILED: Speed was not preserved")
        return False

def test_direction_change_with_no_existing_movement():
    """Test that direction-only changes on non-existent vectors don't create movement"""
    print("\n\nTesting direction change with no existing movement...")

    system = MouseVectorsSystem()

    # Try to change direction of non-existent vector
    print("1. Attempting to change direction of non-existent 'test' vector...")
    system.add_or_update_vector("test", direction=(1, 0))

    vector = system.get_vector("test")
    if vector is None:
        print("✅ SUCCESS: No vector created when trying to change direction of non-existent vector")
        return True
    else:
        speed = math.sqrt(vector['v'][0]**2 + vector['v'][1]**2)
        print(f"   Created vector with velocity: {vector['v']}, speed: {speed}")
        if speed == 0:
            print("✅ SUCCESS: Vector created but with zero velocity (no movement)")
            return True
        else:
            print("❌ FAILED: Vector created with non-zero velocity")
            return False

if __name__ == "__main__":
    print("Testing mouse vectors direction change functionality")
    print("=" * 60)

    test1_passed = test_direction_change_preserves_speed()
    test2_passed = test_direction_change_with_no_existing_movement()

    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Test 1 (Direction change preserves speed): {'PASSED' if test1_passed else 'FAILED'}")
    print(f"Test 2 (No creation without existing movement): {'PASSED' if test2_passed else 'FAILED'}")

    if test1_passed and test2_passed:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)
