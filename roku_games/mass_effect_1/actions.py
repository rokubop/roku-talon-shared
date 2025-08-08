from talon import actions, cron

full_tracking = False
is_tracking = False
cron_camera = None
x_mode = "camera"
y_mode = "walk"

def location():
    print("location")

def click():
    stopper()
    actions.mouse_click(0)

def toggle_parrot_v6():
    actions.user.parrot_mode_v6_toggle()

def mouse_move_continuous(dir: str):
    tracking_halt()
    if dir == "left":
        actions.user.mouse_move_continuous(-1, 0)
    elif dir == "right":
        actions.user.mouse_move_continuous(1, 0)
    elif dir == "up":
        actions.user.mouse_move_continuous(0, -1)
    elif dir == "down":
        actions.user.mouse_move_continuous(0, 1)

def mouse_jump_and_move_continuous(dir: str):
    actions.tracking.jump()
    mouse_move_continuous(dir)

def mouse_move_smooth_to_gaze():
    tracking_halt()
    actions.tracking.jump()
    gaze_x = actions.mouse_x()
    gaze_y = actions.mouse_y()
    screen_center_x = 980
    screen_center_y = 540
    actions.user.mouse_move_smooth_from_to(screen_center_x, screen_center_y, gaze_x, gaze_y, mouse_api_type="windows")

def mouse_move_smooth_from_gaze():
    tracking_halt()
    actions.tracking.jump()
    gaze_x = actions.mouse_x()
    gaze_y = actions.mouse_y()
    screen_center_x = 980
    screen_center_y = 540
    actions.user.mouse_move_smooth_from_to(gaze_x, gaze_y, screen_center_x, screen_center_y, mouse_api_type="windows")

def shove_modifier():
    tracking_halt()
    amount = 200
    info = actions.user.mouse_move_info()
    unit_vector = info["last_unit_vector"]

    def continue_slowly():
        actions.user.mouse_move_continuous(unit_vector.x, unit_vector.y)

    actions.user.mouse_move_smooth_delta(
        unit_vector.x * amount,
        unit_vector.y * amount,
        callback_stop=continue_slowly
    )

def scan_modifier():
    tracking_halt()
    actions.user.mouse_scroll_down()

def roaming_a():
    if actions.user.game_xbox_state_held("right_stick"):
        camera_speed_boost("350ms")
    else:
        actions.user.game_xbox_button_press("a")

def roaming_x():
    if actions.user.game_xbox_state_held("right_stick"):
        camera_speed_boost("150ms")
    else:
        actions.user.game_xbox_button_press("x")

def roaming_y():
    if actions.user.game_xbox_state_held("right_stick"):
        camera_speed_boost("50ms")
    else:
        actions.user.game_xbox_button_press("y")

def roaming_b():
    if actions.user.game_xbox_state_held("right_stick"):
        actions.user.game_xbox_stop_all()
    else:
        actions.user.game_xbox_button_press("b")

def roaming_switch_left():
    roaming_switch_x_mode()
    roaming_left_walk_or_camera()

def roaming_switch_right():
    roaming_switch_x_mode()
    roaming_right_walk_or_camera()

def roaming_switch_up():
    roaming_switch_y_mode()
    roaming_up_walk_or_camera()

def roaming_switch_down():
    roaming_switch_y_mode()
    roaming_down_walk_or_camera()

def roaming_switch_x_mode():
    global x_mode
    if x_mode == "walk":
        x_mode = "camera"
    else:
        x_mode = "walk"

def roaming_switch_y_mode():
    global y_mode
    if y_mode == "walk":
        y_mode = "camera"
    else:
        y_mode = "walk"

def roaming_left_walk_or_camera():
    if x_mode == "walk":
        actions.user.game_xbox_left_stick_hold_dir("left")
    else:
        actions.user.game_xbox_right_stick_hold_dir("left")

def roaming_right_walk_or_camera():
    if x_mode == "walk":
        actions.user.game_xbox_left_stick_hold_dir("right")
    else:
        actions.user.game_xbox_right_stick_hold_dir("right")

def roaming_up_walk_or_camera():
    if y_mode == "walk":
        if actions.user.game_xbox_state_held("right_stick"):
            actions.user.game_xbox_right_stick_stop()
        actions.user.game_xbox_left_stick_hold_dir("up")
    else:
        actions.user.game_xbox_right_stick_hold_dir("up")

def roaming_down_walk_or_camera():
    if y_mode == "walk":
        actions.user.game_xbox_left_stick_hold_dir("down")
    else:
        actions.user.game_xbox_right_stick_hold_dir("down")

def zoom_toggle_and_stop():
    actions.user.game_xbox_left_stick_stop()
    actions.user.game_xbox_right_stick_stop()
    actions.user.game_xbox_button_toggle("LT")

def shoot_and_stop():
    actions.user.game_xbox_right_stick_stop()
    actions.user.game_xbox_button_press("RT")

def camera_speed_default():
    global cron_camera
    if cron_camera:
        cron_camera = None
    actions.user.game_xbox_right_stick_set_gear(2)

def camera_speed_boost(time_ms):
    global cron_camera
    if cron_camera:
        cron.cancel(cron_camera)
    actions.user.game_xbox_right_stick_set_gear(5)
    cron_camera = cron.after(time_ms, camera_speed_default)

def mouse_shove_and_move(dir: str):
    shove_modifier()
    mouse_move_continuous(dir)

def stopper():
    actions.user.game_xbox_stopper()
    mouse_move_stop()
    tracking_halt()

def mouse_move_stop():
    actions.user.mouse_move_continuous_stop()

def jump_to_gaze_and_head_track():
    global is_tracking
    mouse_move_stop()
    if not actions.tracking.control_enabled():
        actions.tracking.control_toggle(True)
    actions.tracking.control_head_toggle(False)
    actions.tracking.control_gaze_toggle(True)
    actions.sleep("30ms")
    actions.tracking.control_gaze_toggle(False)
    actions.tracking.control_head_toggle(True)
    is_tracking = True

def tracking_halt():
    global is_tracking
    if is_tracking:
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(False)
        is_tracking = False

def toggle_full_tracking():
    global full_tracking
    if full_tracking:
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(False)
    else:
        actions.tracking.control_gaze_toggle(True)
        actions.tracking.control_head_toggle(True)
    full_tracking = not full_tracking