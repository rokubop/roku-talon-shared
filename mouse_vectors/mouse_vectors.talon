# Basic movement commands
mouse move right: user.mouse_vectors("move", "v=(50, 0)")
mouse move left: user.mouse_vectors("move", "v=(-50, 0)")
mouse move up: user.mouse_vectors("move", "v=(0, -50)")
mouse move down: user.mouse_vectors("move", "v=(0, 50)")

# Stop movement
mouse stop: user.mouse_vectors_stop()
mouse pause: user.mouse_vectors_disable()

# Acceleration-based movement
mouse thrust right: user.mouse_vectors("thrust", "a=(100, 0); duration=1000")
mouse thrust left: user.mouse_vectors("thrust", "a=(-100, 0); duration=1000")
mouse thrust up: user.mouse_vectors("thrust", "a=(0, -100); duration=1000")
mouse thrust down: user.mouse_vectors("thrust", "a=(0, 100); duration=1000")

# Boost commands (temporary acceleration)
mouse boost right: user.mouse_vectors("boost", "a=(200, 0); duration=500")
mouse boost left: user.mouse_vectors("boost", "a=(-200, 0); duration=500")
mouse boost up: user.mouse_vectors("boost", "a=(0, -200); duration=500")
mouse boost down: user.mouse_vectors("boost", "a=(0, 200); duration=500")

# Brake/slow down
mouse brake: user.mouse_vectors("brake", "a=(-50, 0); duration=800")

# Wobble effect
mouse wobble:
    user.mouse_vectors("wobble", "a=(0, 30); a_keyframes=[1.0, -1.0, 1.0, -1.0]; duration=1000; a_interpolation=linear; duration=2000")

# Pulse effect
mouse pulse:
    user.mouse_vectors("pulse", "a=(80, 0); a_keyframes=[0.0, 1.0, 0.0, 1.0, 0.0]; a_interpolation=ease_in_out; duration=1500")

# Orbit effect (circular motion)
mouse orbit:
    user.mouse_vectors("orbit_x", "v=(100, 0)")
    user.mouse_vectors("orbit_y", "v=(0, 100); v_keyframes=[0.0, 1.0, 0.0, -1.0, 0.0]; v_interpolation=linear; duration=4000")

# Remove specific vectors
mouse remove <user.text>: user.mouse_vectors_remove(text)

# Get system state
# mouse state:
#     state = user.mouse_vectors_get_state()
#     print(f"Mouse vectors state: {state}")

# List all active vectors
# mouse list:
#     vectors = user.mouse_vectors_list()
#     print(f"Active vectors: {vectors}")

# Smooth movement (using direction + speed interface)
mouse smooth right: user.mouse_vectors("smooth", "direction=(1, 0); speed=30")
mouse smooth left: user.mouse_vectors("smooth", "direction=(-1, 0); speed=30")
mouse smooth up: user.mouse_vectors("smooth", "direction=(0, -1); speed=30")
mouse smooth down: user.mouse_vectors("smooth", "direction=(0, 1); speed=30")

# Diagonal movement
mouse diagonal up right: user.mouse_vectors("diag", "direction=(1, -1); speed=50")
mouse diagonal up left: user.mouse_vectors("diag", "direction=(-1, -1); speed=50")
mouse diagonal down right: user.mouse_vectors("diag", "direction=(1, 1); speed=50")
mouse diagonal down left: user.mouse_vectors("diag", "direction=(-1, 1); speed=50")

# Gaming-style controls
mouse strafe right: user.mouse_vectors("strafe", "a=(80, 0)")
mouse strafe left: user.mouse_vectors("strafe", "a=(-80, 0)")
mouse strafe stop: user.mouse_vectors("strafe", "a=(0, 0)")

# Projectile motion
mouse launch:
    user.mouse_vectors("launch", "v=(120, -60)")
    user.mouse_vectors("gravity", "a=(0, 40)")

# Complex multi-vector example
mouse dance:
    user.mouse_vectors("base", "v=(20, 0)")
    user.mouse_vectors("wobble1", "a=(0, 40); a_keyframes=[1.0, -1.0, 1.0, -1.0]; duration=1000")
    user.mouse_vectors("wobble2", "a=(30, 0); a_keyframes=[0.0, 1.0, 0.0, -1.0, 0.0]; duration=1500")

# Enable/disable specific vectors
mouse enable <user.text>: user.mouse_vectors(text, "enabled=True")
mouse disable <user.text>: user.mouse_vectors(text, "enabled=False")
