import random
import math


def velocity_wobble(vel, friction):
    # Random wobble:
    b = random.randint(0, 4)
    if b == 0:
        vel.x += 1
    elif b == 1:
        vel.x -= 1
    elif b == 2:
        vel.y += 1
    elif b == 3:
        vel.y -= 1

    # Calculating friction vector
    friction_vec = -friction * vel / math.hypot(vel.x, vel.y)

    # Calculating new velocity with friction
    return vel + friction_vec


def velocity_default(vel, friction):
    # Calculating friction vector
    friction_vec = -friction * vel / math.hypot(vel.x, vel.y)

    # Calculating new velocity with friction
    return vel + friction_vec
