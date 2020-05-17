from client.objects.particles.Particles import Particles
from client.resources.ResourcesManager import ResourcesManager


class ParticlesFire(Particles):
    def __init__(self, position, dimension, follow=None, id=-1, obj_mgr=None):
        image_set = [ResourcesManager.get_image('part_fire01'),
                     ResourcesManager.get_image('part_fire02'),
                     ResourcesManager.get_image('part_fire03'),
                     ResourcesManager.get_image('part_fire04')]

        super().__init__(position, dimension, image_set, 0.3, follow=follow, id=id, obj_mgr=obj_mgr)
