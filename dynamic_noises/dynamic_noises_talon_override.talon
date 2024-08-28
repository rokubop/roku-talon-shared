tag: user.dynamic_noises_talon_noise_override
mode: all
-
# "wish" word will not trigger hiss sound
# making it a decent alterative word
pop: skip()
(hiss | wish): skip()

pop <phrase>: skip()
(hiss | wish) <phrase>: skip()

<phrase> pop: mimic(phrase)
<phrase> (hiss | wish): mimic(phrase)

{user.dynamic_noise_mode}: user.dynamic_noises_set_mode(dynamic_noise_mode)