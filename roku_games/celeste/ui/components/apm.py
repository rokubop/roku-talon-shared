from talon import actions, cron
import time

poll_job = None
timestamps = []
current_apm = 0

def on_noise(noise, command_name):
    global timestamps, current_apm
    if command_name:
        now = time.time()
        timestamps.append(now)

def on_poll():
    global current_apm, timestamps
    now = time.time()
    timestamps[:] = [t for t in timestamps if now - t <= 60]
    current_apm = len(timestamps)
    actions.user.ui_elements_set_text("apm", str(current_apm))

def on_mount():
    global current_apm, timestamps, poll_job
    current_apm = 0
    timestamps = []
    actions.user.parrot_config_event_register(on_noise)
    poll_job = cron.interval("1s", on_poll)

def on_unmount():
    global current_apm, timestamps, poll_job
    cron.cancel(poll_job)
    poll_job = None
    current_apm = 0
    timestamps = []
    actions.user.parrot_config_event_unregister(on_noise)

def apm(scale=1, **props):
    div, text, effect = actions.user.ui_elements(["div", "text", "effect"])

    effect(on_mount, on_unmount, [])

    return div(width=150 * scale, flex_direction="column", gap=int(8 * scale), padding_left=12, **props)[
        text("0", id="apm", font_size=int(40 * scale), font_family="renogare"),
        text("noise/min", font_size=int(24 * scale), font_family="roboto"),
    ]