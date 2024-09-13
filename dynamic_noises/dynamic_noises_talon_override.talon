tag: user.dynamic_noises_talon_noise_override
not mode: sleep
-
pop <phrase>: skip()
(hiss | wish) <phrase>: skip()

pop {user.dynamic_noise_special_actions}: user.dynamic_noises_special_action("pop", dynamic_noise_special_actions)
(hiss | wish) {user.dynamic_noise_special_actions}: user.dynamic_noises_special_action("hiss", dynamic_noise_special_actions)
dynamic clear: user.dynamic_noises_reset()

view left: user.dynamic_noises_tester_ui_position("left")
view right: user.dynamic_noises_tester_ui_position("right")
view hide: user.dynamic_noises_tester_ui_position("hide")
view show: user.dynamic_noises_tester_ui_position("right")

{user.dynamic_noise_mode}: user.dynamic_noises_set_mode(dynamic_noise_mode)