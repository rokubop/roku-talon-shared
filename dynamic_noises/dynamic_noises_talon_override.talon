tag: user.dynamic_noises_talon_noise_override
mode: all
-
# "wish" word will not trigger hiss sound
# making it a decent alterative word
pop: skip()
(hiss | wish): skip()

pop <phrase>: skip()
(hiss | wish) <phrase>: skip()

pop {user.dynamic_noise_special_actions}: user.private_dynamic_noises_action("pop", dynamic_noise_special_actions)
(hiss | wish) {user.dynamic_noise_special_actions}: user.private_dynamic_noises_action("hiss", dynamic_noise_special_actions)

<phrase> pop: mimic(phrase)
<phrase> (hiss | wish): mimic(phrase)

{user.dynamic_noise_mode}: user.dynamic_noises_use_mode(dynamic_noise_mode)