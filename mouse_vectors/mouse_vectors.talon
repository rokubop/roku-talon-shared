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
mouse right: user.mouse_vector("direction=(1, 0); default_speed=50")
mouse left: user.mouse_vector("direction=(-1, 0); default_speed=50")
mouse up: user.mouse_vector("direction=(0, -1); default_speed=50")
mouse down: user.mouse_vector("direction=(0, 1); default_speed=50")

#* Stop movement
mouse stop: user.mouse_vector_stop()
mouse pause: user.mouse_vector_disable()

mouse test: user.mouse_vector("v=(100, 0); duration=400;")

# Acceleration-based movement
mouse thrust right: user.mouse_vector("name=thrust; a=(100, 0); duration=1000")
mouse thrust left: user.mouse_vector("name=thrust; a=(-100, 0); duration=1000")
mouse thrust up: user.mouse_vector("name=thrust; a=(0, -100); duration=1000")
mouse thrust down: user.mouse_vector("name=thrust; a=(0, 100); duration=1000")

# Boost commands (temporary acceleration)
# mouse setup: user.mouse_vector_settings({
#     "default_speed": 50,
#     "default_acceleration": 100, stop
#     "default_duration": 1000,
#     "default_interpolation": "ease_in_out"
# })
mouse move: user.mouse_vector("v=(100, 100); duration=1000; v_interpolation=ease_out")
mouse scale: user.mouse_vector_scale(2)
mouse rotate: user.mouse_vector_rotate(180)

mouse boost right: user.mouse_vector("name=boost; a=(200, 0); duration=500")
mouse boost left: user.mouse_vector("name=boost; a=(-200, 0); duration=500")
mouse boost up: user.mouse_vector("name=boost; a=(0, -200); duration=500")
mouse boost down: user.mouse_vector("name=boost; a=(0, 200); duration=500")

# Brake/slow down
mouse brake: user.mouse_vector("name=brake; a=(-50, 0); duration=800")

# Target-based movement (displacement)
mouse target right: user.mouse_vector("d=(100, 0); duration=300")
mouse target left: user.mouse_vector("d=(-100, 0); duration=300")
mouse target up: user.mouse_vector("d=(0, -100); duration=300")
mouse target down: user.mouse_vector("d=(0, 100); duration=300")

# Larger displacement movements
mouse jump right: user.mouse_vector("d=(200, 0); duration=1000")
mouse jump left: user.mouse_vector("d=(-200, 0); duration=1000")
mouse jump up: user.mouse_vector("d=(0, -200); duration=1000")
mouse jump down: user.mouse_vector("d=(0, 200); duration=1000")

# Animated displacement
mouse slide right: user.mouse_vector("d=(150, 0); d_keyframes=[0.0, 0.8, 1.0]; d_interpolation=ease_out; duration=2000")
mouse slide left: user.mouse_vector("d=(-150, 0); d_keyframes=[0.0, 0.8, 1.0]; d_interpolation=ease_out; duration=2000")

# Wobble effect
mouse wobble:
    user.mouse_vector("name=wobble; a=(0, 30); a_keyframes=[1.0, -1.0, 1.0, -1.0]; duration=1000; a_interpolation=linear; duration=2000")

# Pulse effect
mouse pulse:
    user.mouse_vector("name=pulse; a=(80, 0); a_keyframes=[0.0, 1.0, 0.0, 1.0, 0.0]; a_interpolation=ease_in_out; duration=1500")

# Remove specific vectors
mouse remove <user.text>: user.mouse_vector_remove(text)

# Smooth movement (using direction + speed interface)
mouse smooth right: user.mouse_vector("name=smooth; direction=(1, 0); speed=30")
mouse smooth left: user.mouse_vector("name=smooth; direction=(-1, 0); speed=30")
mouse smooth up: user.mouse_vector("name=smooth; direction=(0, -1); speed=30")
mouse smooth down: user.mouse_vector("name=smooth; direction=(0, 1); speed=30")

# Diagonal movement
mouse diagonal up right: user.mouse_vector("name=diag; direction=(1, -1); speed=50")
mouse diagonal up left: user.mouse_vector("name=diag; direction=(-1, -1); speed=50")
mouse diagonal down right: user.mouse_vector("name=diag; direction=(1, 1); speed=50")
mouse diagonal down left: user.mouse_vector("name=diag; direction=(-1, 1); speed=50")

# Gaming-style controls
mouse strafe right: user.mouse_vector("name=strafe; a=(80, 0); max_speed=200")
mouse strafe left: user.mouse_vector("name=strafe; a=(-80, 0); max_speed=50")
mouse strafe stop: user.mouse_vector("name=strafe; a=(0, 0); max_speed=50")

# Projectile motion
mouse launch:
    user.mouse_vector("name=launch; v=(200, -200)")
    user.mouse_vector("name=gravity; a=(0, 200)")

# Complex multi-vector example
mouse dance:
    user.mouse_vector("name=base; v=(20, 0)")
    user.mouse_vector("name=wobble1; a=(0, 40); a_keyframes=[1.0, -1.0, 1.0, -1.0]; duration=1000")
    user.mouse_vector("name=wobble2; a=(30, 0); a_keyframes=[0.0, 1.0, 0.0, -1.0, 0.0]; duration=1500")

# Enable/disable specific vectors
mouse enable <user.text>: user.mouse_vector("name={text}; enabled=true")
mouse disable <user.text>: user.mouse_vector("name={text}; enabled=false")

# Debug commands
mouse list:
    print(user.mouse_vector_list())

mouse state:
    print(user.mouse_vector_get_state())

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
    user.mouse_vector("name=fade_horizontal; v=(-100, 0); v_keyframes=[1.0, 0.5, 0.0]; duration=2000")
    user.mouse_vector("name=add_vertical; a=(0, 80); a_keyframes=[0.0, 0.5, 1.0]; duration=2000")

mouse turn right:
    user.mouse_vector("name=fade_vertical; v=(0, -100); v_keyframes=[1.0, 0.5, 0.0]; duration=2000")
    user.mouse_vector("name=add_horizontal; a=(80, 0); a_keyframes=[0.0, 0.5, 1.0]; duration=2000")

# Smooth S-curve
mouse snake:
    user.mouse_vector("name=base; v=(60, 0)")
    user.mouse_vector("name=wave; a=(0, 50); a_keyframes=[0.0, 1.0, 0.0, -1.0, 0.0, 1.0, 0.0]; a_interpolation=cubic; duration=3000")

# Speed control commands
mouse speed up: user.mouse_vector_multiply_speed(2)
mouse speed down: user.mouse_vector_multiply_speed(0.5)
mouse speed double: user.mouse_vector_multiply_speed(2.0)
mouse speed triple: user.mouse_vector_multiply_speed(3.0)
mouse speed half: user.mouse_vector_multiply_speed(0.5)
mouse speed quarter: user.mouse_vector_multiply_speed(0.25)

# Alternative: Add velocity in current direction (temporary speed boost)
mouse turbo:
    user.mouse_vector("name=turbo; a=(150, 0); duration=800")

# Alternative: Direct speed boost using current direction
mouse boost speed:
    user.mouse_vector("name=speed_boost; v=(100, 0); duration=1000")

# Speed-capped acceleration using mouse_vector directly
mouse accelerate right: user.mouse_vector("name=accel; direction=(1, 0); speed=0; a=(120, 0); max_speed=200")
mouse accelerate left: user.mouse_vector("name=accel; direction=(-1, 0); speed=0; a=(120, 0); max_speed=200")
mouse accelerate up: user.mouse_vector("name=accel; direction=(0, -1); speed=0; a=(120, 0); max_speed=200")
mouse accelerate down: user.mouse_vector("name=accel; direction=(0, 1); speed=0; a=(120, 0); max_speed=200")

# Fast acceleration with higher cap
mouse accelerate fast right: user.mouse_vector("name=fast_accel; direction=(1, 0); speed=0; a=(200, 0); max_speed=350")
mouse accelerate fast left: user.mouse_vector("name=fast_accel; direction=(-1, 0); speed=0; a=(200, 0); max_speed=350")
mouse accelerate fast up: user.mouse_vector("name=fast_accel; direction=(0, -1); speed=0; a=(200, 0); max_speed=350")
mouse accelerate fast down: user.mouse_vector("name=fast_accel; direction=(0, 1); speed=0; a=(200, 0); max_speed=350")

# Gentle acceleration with low cap
mouse accelerate gentle right: user.mouse_vector("name=gentle_accel; direction=(1, 0); speed=0; a=(60, 0); max_speed=120")
mouse accelerate gentle left: user.mouse_vector("name=gentle_accel; direction=(-1, 0); speed=0; a=(60, 0); max_speed=120")
mouse accelerate gentle up: user.mouse_vector("name=gentle_accel; direction=(0, -1); speed=0; a=(60, 0); max_speed=120")
mouse accelerate gentle down: user.mouse_vector("name=gentle_accel; direction=(0, 1); speed=0; a=(60, 0); max_speed=120")

# Starting with initial speed and acceleration
mouse accelerate boost right: user.mouse_vector("name=boost_accel; direction=(1, 0); speed=50; a=(100, 0); max_speed=250")
mouse accelerate boost left: user.mouse_vector("name=boost_accel; direction=(-1, 0); speed=50; a=(100, 0); max_speed=250")
mouse accelerate boost up: user.mouse_vector("name=boost_accel; direction=(0, -1); speed=50; a=(100, 0); max_speed=250")
mouse accelerate boost down: user.mouse_vector("name=boost_accel; direction=(0, 1); speed=50; a=(100, 0); max_speed=250")

# Deceleration using keyframes
mouse decelerate: user.mouse_vector("name=main; v_keyframes=[1.0, 0.0]; v_interpolation=ease_out; duration=2000")
mouse decelerate fast: user.mouse_vector("name=main; v_keyframes=[1.0, 0.0]; v_interpolation=ease_out; duration=1000")
mouse decelerate slow: user.mouse_vector("name=main; v_keyframes=[1.0, 0.0]; v_interpolation=ease_out; duration=3000")
mouse decelerate linear: user.mouse_vector("name=main; v_keyframes=[1.0, 0.0]; v_interpolation=linear; duration=2000")

# Decelerate specific vectors
mouse decelerate <user.text>: user.mouse_vector("name={text}; v_keyframes=[1.0, 0.0]; v_interpolation=ease_out; duration=2000")
mouse decelerate <user.text> fast: user.mouse_vector("name={text}; v_keyframes=[1.0, 0.0]; v_interpolation=ease_out; duration=1000")
mouse decelerate <user.text> slow: user.mouse_vector("name={text}; v_keyframes=[1.0, 0.0]; v_interpolation=ease_out; duration=3000")

# Manual speed-capped vectors using string syntax
mouse manual cap right: user.mouse_vector("name=manual; direction=(1, 0); speed=30; a=(80, 0); max_speed=150")
mouse manual cap left: user.mouse_vector("name=manual; direction=(-1, 0); speed=30; a=(80, 0); max_speed=150")
mouse manual cap up: user.mouse_vector("name=manual; direction=(0, -1); speed=30; a=(80, 0); max_speed=150")
mouse manual cap down: user.mouse_vector("name=manual; direction=(0, 1); speed=30; a=(80, 0); max_speed=150")

# High-performance capped acceleration
mouse rocket right: user.mouse_vector("name=rocket; direction=(1, 0); speed=0; a=(300, 0); max_speed=500")
mouse rocket left: user.mouse_vector("name=rocket; direction=(-1, 0); speed=0; a=(300, 0); max_speed=500")
mouse rocket up: user.mouse_vector("name=rocket; direction=(0, -1); speed=0; a=(300, 0); max_speed=500")
mouse rocket down: user.mouse_vector("name=rocket; direction=(0, 1); speed=0; a=(300, 0); max_speed=500")
