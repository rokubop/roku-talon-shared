tag: user.dynamic_actions_talon_noise_override
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