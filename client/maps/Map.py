from client.objects.ObstacleBrickWallSegment import ObstacleBrickWallSegment
from client.objects.ObjectCup import ObjectCup
from client.objects.Ball import Ball
from client.objects.ObstacleRock import ObstacleRock
from client.objects.SurfaceGrass import SurfaceGrass
from client.objects.SurfaceIce import SurfaceIce
from client.objects.SurfaceDirt import SurfaceDirt
from client.objects.SurfaceLava import SurfaceLava
from client.objects.particles.ParticlesFire import ParticlesFire


class Map:
    def __init__(self, obj_mgr):
        # TODO
        # Upload map from file by index, perhaps some loader required
        self.id = 1

        SurfaceGrass((0, 0), (64, 64), obj_mgr=obj_mgr)
        SurfaceIce((300, 0), (64, 64), obj_mgr=obj_mgr)
        SurfaceDirt((600, 0), (64, 64), obj_mgr=obj_mgr)
        SurfaceLava((900, 0), (64, 64), obj_mgr=obj_mgr)

        self.cup = ObjectCup((700, 340), (48, 48), obj_mgr=obj_mgr)
        ObstacleBrickWallSegment((150, 150), (63, 64), obj_mgr=obj_mgr)
        ObstacleRock((500, 500), (128, 128), obj_mgr=obj_mgr)
