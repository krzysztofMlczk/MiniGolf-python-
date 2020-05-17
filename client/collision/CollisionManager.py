import math

import pygame
import pymunk
from pymunk import autogeometry


class CollisionManager:
    @classmethod
    def create_collision_shape(cls, img, body, threshold=240):
        poly_points = []
        px_arr = pygame.PixelArray(img)

        min_y = img.get_height()
        min_x = img.get_width()

        for x in range(px_arr.shape[1]):
            for y in range(px_arr.shape[0]):
                px = 0xFF & px_arr[y][x]
                if px < threshold and px != 0:
                    if x < min_x:
                        min_x = x
                    if y < min_y:
                        min_y = y

                    poly_points.append((y, x))

        hull = autogeometry.to_convex_hull(poly_points, 0.1)

        return pymunk.shapes.Poly(body, hull, transform=pymunk.Transform(d=-1)), (min_y, min_x)
