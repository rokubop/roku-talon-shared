mode: user.fly
and mode: command
and tag: browser
and tag: user.rango_direct_clicking
-
# Enable if you have Talon beta
# parrot(pop): user.use_parrot_config('pop')
# parrot(hiss): user.use_parrot_config('hiss')
# parrot(hiss:stop): user.use_parrot_config('hiss:stop')

up:                         user.fly_up()
down:                       user.fly_down()
right:                      user.fly_right()
left:                       user.fly_left()
up right | right up:        user.fly_up_right()
up left | left up:          user.fly_up_left()
down right | right down:    user.fly_down_right()
down left | left down:      user.fly_down_left()
