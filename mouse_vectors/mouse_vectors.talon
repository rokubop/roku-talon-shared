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

# Target-based movement (displacement)
mouse target right: user.mouse_vectors("target", "d=(100, 0); duration=1500")
mouse target left: user.mouse_vectors("target", "d=(-100, 0); duration=1500")
mouse target up: user.mouse_vectors("target", "d=(0, -100); duration=1500")
mouse target down: user.mouse_vectors("target", "d=(0, 100); duration=1500")

# Larger displacement movements
mouse jump right: user.mouse_vectors("jump", "d=(200, 0); duration=1000")
mouse jump left: user.mouse_vectors("jump", "d=(-200, 0); duration=1000")
mouse jump up: user.mouse_vectors("jump", "d=(0, -200); duration=1000")
mouse jump down: user.mouse_vectors("jump", "d=(0, 200); duration=1000")

# Animated displacement
mouse slide right: user.mouse_vectors("slide", "d=(150, 0); d_keyframes=[0.0, 0.8, 1.0]; d_interpolation=ease_out; duration=2000")
mouse slide left: user.mouse_vectors("slide", "d=(-150, 0); d_keyframes=[0.0, 0.8, 1.0]; d_interpolation=ease_out; duration=2000")

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
mouse state:
    state = user.mouse_vectors_get_state()
    print(state)

# List all active vectors
mouse list:
    vectors = user.mouse_vectors_list()
    print(vectors)

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

# Physics-based curved motion commands (real centripetal force)
mouse curve down: user.mouse_vectors_curve_turn("turn", 0, 1, 50)
mouse curve up: user.mouse_vectors_curve_turn("turn", 0, -1, 50)
mouse curve right: user.mouse_vectors_curve_turn("turn", 1, 0, 50)
mouse curve left: user.mouse_vectors_curve_turn("turn", -1, 0, 50)

# Diagonal curves
mouse curve down right: user.mouse_vectors_curve_turn("turn", 1, 1, 50)
mouse curve down left: user.mouse_vectors_curve_turn("turn", -1, 1, 50)
mouse curve up right: user.mouse_vectors_curve_turn("turn", 1, -1, 50)
mouse curve up left: user.mouse_vectors_curve_turn("turn", -1, -1, 50)

# Banking turns (tighter radius = sharper turns)
mouse bank down: user.mouse_vectors_curve_turn("turn", 0, 1, 30)
mouse bank up: user.mouse_vectors_curve_turn("turn", 0, -1, 30)
mouse bank right: user.mouse_vectors_curve_turn("turn", 1, 0, 30)
mouse bank left: user.mouse_vectors_curve_turn("turn", -1, 0, 30)

# Wide gentle turns
mouse sweep down: user.mouse_vectors_curve_turn("turn", 0, 1, 100)
mouse sweep up: user.mouse_vectors_curve_turn("turn", 0, -1, 100)
mouse sweep right: user.mouse_vectors_curve_turn("turn", 1, 0, 100)
mouse sweep left: user.mouse_vectors_curve_turn("turn", -1, 0, 100)

# Spiral motion
mouse spiral: user.mouse_vectors_spiral_turn("spiral", 0.5, 100, 3000)
mouse spiral fast: user.mouse_vectors_spiral_turn("spiral", 1.0, 120, 2000)
mouse spiral slow: user.mouse_vectors_spiral_turn("spiral", 0.3, 80, 4000)

# Physics-based turns that respect momentum
mouse turn down:
    # Gradually reduce current horizontal motion while adding downward acceleration
    user.mouse_vectors("fade_horizontal", "v=(-100, 0); v_keyframes=[1.0, 0.5, 0.0]; duration=2000")
    user.mouse_vectors("add_vertical", "a=(0, 80); a_keyframes=[0.0, 0.5, 1.0]; duration=2000")

mouse turn right:
    user.mouse_vectors("fade_vertical", "v=(0, -100); v_keyframes=[1.0, 0.5, 0.0]; duration=2000")
    user.mouse_vectors("add_horizontal", "a=(80, 0); a_keyframes=[0.0, 0.5, 1.0]; duration=2000")

# Smooth S-curve
mouse snake:
    user.mouse_vectors("base", "v=(60, 0)")
    user.mouse_vectors("wave", "a=(0, 50); a_keyframes=[0.0, 1.0, 0.0, -1.0, 0.0, 1.0, 0.0]; a_interpolation=cubic; duration=3000")
