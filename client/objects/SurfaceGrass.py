import math

from client.objects.Surface import Surface
from client.resources.ResourcesManager import ResourcesManager


class SurfaceGrass(Surface):
    def __init__(self, position, dimension, obj_mgr, id=-1):
        super().__init__(position, dimension, ResourcesManager.get_image('surf_grass'), 3.0, id, obj_mgr)

    def draw(self, display):
        display.blit(self.image, self.position)

    def change_velocity(self, vel):
        # Calculating friction vector
        friction_vec = -self.friction * vel / math.hypot(vel.x, vel.y)

        # Calculating new velocity with friction
        return vel + friction_vec
