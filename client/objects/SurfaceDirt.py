import random
import math

from client.objects.Surface import Surface
from client.resources.ResourcesManager import ResourcesManager


class SurfaceDirt(Surface):
    def __init__(self, position, dimension, obj_mgr, id=-1):
        super().__init__(position, dimension, ResourcesManager.get_image('surf_dirt'), 4.0, id, obj_mgr)

    def draw(self, display):
        display.blit(self.image, self.position)

    def change_velocity(self, vel):

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
        friction_vec = -self.friction * vel / math.hypot(vel.x, vel.y)

        # Calculating new velocity with friction
        return vel + friction_vec
