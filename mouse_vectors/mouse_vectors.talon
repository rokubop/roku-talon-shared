# Basic movement commands
mouse move start right: user.mouse_vector("v=(50, 0)")
mouse move start left: user.mouse_vector("v=(-50, 0)")
mouse move start up: user.mouse_vector("v=(0, -50)")
mouse move start down: user.mouse_vector("v=(0, 50)")

mouse move right: user.mouse_vector("direction=(1, 0); default_speed=50")
mouse move left: user.mouse_vector("direction=(-1, 0); default_speed=50")
mouse move up: user.mouse_vector("direction=(0, -1); default_speed=50")
mouse move down: user.mouse_vector("direction=(0, 1); default_speed=50")

# Simple movement commands using default "main" vector
mouse right: user.mouse_vector(v="direction=(1, 0); default_speed=50")
mouse left: user.mouse_vector(v="direction=(-1, 0); default_speed=50")
mouse up: user.mouse_vector(v="direction=(0, -1); default_speed=50")
mouse down: user.mouse_vector(v="direction=(0, 1); default_speed=50")

#* Stop movement
mouse stop: user.mouse_vector_stop()
mouse pause: user.mouse_vector_disable()

mouse test: user.mouse_vector("v=(100, 0); duration=400;")

# Acceleration-based movement
mouse thrust right: user.mouse_vector("thrust", "a=(100, 0); duration=1000")
mouse thrust left: user.mouse_vector("thrust", "a=(-100, 0); duration=1000")
mouse thrust up: user.mouse_vector("thrust", "a=(0, -100); duration=1000")
mouse thrust down: user.mouse_vector("thrust", "a=(0, 100); duration=1000")

# Boost commands (temporary acceleration)
mouse boost right: user.mouse_vector("boost", "a=(200, 0); duration=500")
mouse boost left: user.mouse_vector("boost", "a=(-200, 0); duration=500")
mouse boost up: user.mouse_vector("boost", "a=(0, -200); duration=500")
mouse boost down: user.mouse_vector("boost", "a=(0, 200); duration=500")

# Brake/slow down
mouse brake: user.mouse_vector("brake", "a=(-50, 0); duration=800")

# Target-based movement (displacement)
mouse target right: user.mouse_vector("target", "d=(100, 0); duration=1500")
mouse target left: user.mouse_vector("target", "d=(-100, 0); duration=1500")
mouse target up: user.mouse_vector("target", "d=(0, -100); duration=1500")
mouse target down: user.mouse_vector("target", "d=(0, 100); duration=1500")

# Larger displacement movements
mouse jump right: user.mouse_vector("jump", "d=(200, 0); duration=1000")
mouse jump left: user.mouse_vector("jump", "d=(-200, 0); duration=1000")
mouse jump up: user.mouse_vector("jump", "d=(0, -200); duration=1000")
mouse jump down: user.mouse_vector("jump", "d=(0, 200); duration=1000")

# Animated displacement
mouse slide right: user.mouse_vector("slide", "d=(150, 0); d_keyframes=[0.0, 0.8, 1.0]; d_interpolation=ease_out; duration=2000")
mouse slide left: user.mouse_vector("slide", "d=(-150, 0); d_keyframes=[0.0, 0.8, 1.0]; d_interpolation=ease_out; duration=2000")

# Wobble effect
mouse wobble:
    user.mouse_vector("wobble", "a=(0, 30); a_keyframes=[1.0, -1.0, 1.0, -1.0]; duration=1000; a_interpolation=linear; duration=2000")

# Pulse effect
mouse pulse:
    user.mouse_vector("pulse", "a=(80, 0); a_keyframes=[0.0, 1.0, 0.0, 1.0, 0.0]; a_interpolation=ease_in_out; duration=1500")

# Orbit effect (circular motion)
mouse orbit:
    user.mouse_vector("orbit_x", "v=(100, 0)")
    user.mouse_vector("orbit_y", "v=(0, 100); v_keyframes=[0.0, 1.0, 0.0, -1.0, 0.0]; v_interpolation=linear; duration=4000")

# Remove specific vectors
mouse remove <user.text>: user.mouse_vector_remove(text)

# Smooth movement (using direction + speed interface)
mouse smooth right: user.mouse_vector("smooth", "direction=(1, 0); speed=30")
mouse smooth left: user.mouse_vector("smooth", "direction=(-1, 0); speed=30")
mouse smooth up: user.mouse_vector("smooth", "direction=(0, -1); speed=30")
mouse smooth down: user.mouse_vector("smooth", "direction=(0, 1); speed=30")

# Diagonal movement
mouse diagonal up right: user.mouse_vector("diag", "direction=(1, -1); speed=50")
mouse diagonal up left: user.mouse_vector("diag", "direction=(-1, -1); speed=50")
mouse diagonal down right: user.mouse_vector("diag", "direction=(1, 1); speed=50")
mouse diagonal down left: user.mouse_vector("diag", "direction=(-1, 1); speed=50")

# Gaming-style controls
mouse strafe right: user.mouse_vector("strafe", "a=(80, 0)")
mouse strafe left: user.mouse_vector("strafe", "a=(-80, 0)")
mouse strafe stop: user.mouse_vector("strafe", "a=(0, 0)")

# Projectile motion
mouse launch:
    user.mouse_vector("launch", "v=(200, -200)")
    user.mouse_vector("gravity", "a=(0, 200)")

# Complex multi-vector example
mouse dance:
    user.mouse_vector("base", "v=(20, 0)")
    user.mouse_vector("wobble1", "a=(0, 40); a_keyframes=[1.0, -1.0, 1.0, -1.0]; duration=1000")
    user.mouse_vector("wobble2", "a=(30, 0); a_keyframes=[0.0, 1.0, 0.0, -1.0, 0.0]; duration=1500")

# Enable/disable specific vectors
mouse enable <user.text>: user.mouse_vector(text, "enabled=True")
mouse disable <user.text>: user.mouse_vector(text, "enabled=False")

# Debug commands
mouse list:
    print("Active vectors:")
    user.mouse_vector_list()

mouse state:
    print("System state:")
    user.mouse_vector_get_state()

# Debug logging control
mouse debug on: user.mouse_vector_enable_debug_logging()
mouse debug off: user.mouse_vector_disable_debug_logging()

# Physics-based curved motion commands (real centripetal force)
mouse curve down: user.mouse_vector_curve_turn("turn", 0, 1, 50)
mouse curve up: user.mouse_vector_curve_turn("turn", 0, -1, 50)
mouse curve right: user.mouse_vector_curve_turn("turn", 1, 0, 50)
mouse curve left: user.mouse_vector_curve_turn("turn", -1, 0, 50)

# Diagonal curves
mouse curve down right: user.mouse_vector_curve_turn("turn", 1, 1, 50)
mouse curve down left: user.mouse_vector_curve_turn("turn", -1, 1, 50)
mouse curve up right: user.mouse_vector_curve_turn("turn", 1, -1, 50)
mouse curve up left: user.mouse_vector_curve_turn("turn", -1, -1, 50)

# Banking turns (tighter radius = sharper turns)
mouse bank down: user.mouse_vector_curve_turn("turn", 0, 1, 10)
mouse bank up: user.mouse_vector_curve_turn("turn", 0, -1, 10)
mouse bank right: user.mouse_vector_curve_turn("turn", 1, 0, 10)
mouse bank left: user.mouse_vector_curve_turn("turn", -1, 0, 10)

# Wide gentle turns
mouse sweep down: user.mouse_vector_curve_turn("turn", 0, 1, 500)
mouse sweep up: user.mouse_vector_curve_turn("turn", 0, -1, 500)
mouse sweep right: user.mouse_vector_curve_turn("turn", 1, 0, 500)
mouse sweep left: user.mouse_vector_curve_turn("turn", -1, 0, 500)

mouse turn stop: user.mouse_vector_stop_turn()

# Spiral motion
mouse spiral: user.mouse_vector_spiral_turn("spiral", 0.5, 100, 3000)
mouse spiral fast: user.mouse_vector_spiral_turn("spiral", 1.0, 120, 2000)
mouse spiral slow: user.mouse_vector_spiral_turn("spiral", 0.3, 80, 4000)

# Physics-based turns that respect momentum
mouse turn down:
    # Gradually reduce current horizontal motion while adding downward acceleration
    user.mouse_vector("fade_horizontal", "v=(-100, 0); v_keyframes=[1.0, 0.5, 0.0]; duration=2000")
    user.mouse_vector("add_vertical", "a=(0, 80); a_keyframes=[0.0, 0.5, 1.0]; duration=2000")

mouse turn right:
    user.mouse_vector("fade_vertical", "v=(0, -100); v_keyframes=[1.0, 0.5, 0.0]; duration=2000")
    user.mouse_vector("add_horizontal", "a=(80, 0); a_keyframes=[0.0, 0.5, 1.0]; duration=2000")

# Smooth S-curve
mouse snake:
    user.mouse_vector("base", "v=(60, 0)")
    user.mouse_vector("wave", "a=(0, 50); a_keyframes=[0.0, 1.0, 0.0, -1.0, 0.0, 1.0, 0.0]; a_interpolation=cubic; duration=3000")

# Speed control commands
mouse speed up: user.mouse_vector_multiply_speed(2)
mouse speed down: user.mouse_vector_multiply_speed(0.5)
mouse speed double: user.mouse_vector_multiply_speed(2.0)
mouse speed triple: user.mouse_vector_multiply_speed(3.0)
mouse speed half: user.mouse_vector_multiply_speed(0.5)
mouse speed quarter: user.mouse_vector_multiply_speed(0.25)

# Alternative: Add velocity in current direction (temporary speed boost)
mouse turbo:
    user.mouse_vector("turbo", "a=(150, 0); duration=800")

# Alternative: Direct speed boost using current direction
mouse boost speed:
    user.mouse_vector("speed_boost", "v=(100, 0); duration=1000")

# Change direction of specific vectors while preserving their speed
mouse change <user.text> direction up: user.mouse_vector(text, "direction=(0, -1)")
mouse change <user.text> direction down: user.mouse_vector(text, "direction=(0, 1)")
mouse change <user.text> direction left: user.mouse_vector(text, "direction=(-1, 0)")
mouse change <user.text> direction right: user.mouse_vector(text, "direction=(1, 0)")
mouse change <user.text> direction up left: user.mouse_vector(text, "direction=(-0.707, -0.707)")
mouse change <user.text> direction up right: user.mouse_vector(text, "direction=(0.707, -0.707)")
mouse change <user.text> direction down left: user.mouse_vector(text, "direction=(-0.707, 0.707)")
mouse change <user.text> direction down right: user.mouse_vector(text, "direction=(0.707, 0.707)")
