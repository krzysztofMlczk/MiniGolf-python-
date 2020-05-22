import os

import pygame
import pymunk

from client.scenes.Scene import Scene
from client.resources.ResourcesManager import ResourcesManager


class EditorScene(Scene):
    """Scene for drawing and handling game events"""

    def __init__(self, screen_dim):
        super().__init__(pymunk.Space())
        self.dist_camera_mv = 200

        self.grid_size = None
        self.grid_pos = (0, 0)
        self.grid = []
        self.screen_dim = screen_dim
        self.generate_grid()

        self.objects = self.load_objects()
        self.curr_obj = (None, None, 'None')

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

    def draw(self, screen):
        self.move_camera(pygame.mouse.get_pos())

        self.display.fill((0, 0, 0))
        self.draw_grid(screen)

        self.display_gui(screen)

    def handle_event(self, event):
        """Handling specific scene events"""
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                clicked_toolbox = self.get_toolbox_tile(mouse_pos)
                clicked_tile_index = self.get_grid_tile(mouse_pos)

                if clicked_toolbox is not None:
                    self.curr_obj = clicked_toolbox
                elif clicked_tile_index is not None and self.grid[clicked_tile_index][1] is None:
                    self.grid[clicked_tile_index] = (self.grid[clicked_tile_index][0], self.curr_obj, 0)

            elif event.button == pygame.BUTTON_RIGHT:
                clicked_tile_index = self.get_grid_tile(mouse_pos)
                if clicked_tile_index is not None:
                    self.grid[clicked_tile_index] = (self.grid[clicked_tile_index][0], None, 0)

            elif event.button == pygame.BUTTON_MIDDLE:
                clicked_tile_index = self.get_grid_tile(mouse_pos)
                if clicked_tile_index is not None and self.grid[clicked_tile_index][1] is not None:
                    self.grid[clicked_tile_index] = (self.grid[clicked_tile_index][0],
                                                     self.grid[clicked_tile_index][1],
                                                     (self.grid[clicked_tile_index][2] + 90) % 360)

        elif event.type == pygame.MOUSEBUTTONUP:
            pass

    def generate_grid(self, block_size=32, dim=(60, 32)):
        width, height = dim
        self.grid.clear()

        for x in range(0, width * block_size, block_size):
            for y in range(0, height * block_size, block_size):
                rect = pygame.Rect(x, y, block_size, block_size)
                self.grid.append((rect, None, 0))

        self.grid_size = (dim[0] * block_size, dim[1] * block_size)

    def apply_offset(self, offset):
        for i in range(len(self.grid)):
            tile = self.grid[i]
            self.grid[i] = (pygame.Rect(tile[0][0] + offset[0], tile[0][1] + offset[1],
                                        tile[0][2], tile[0][3]), tile[1], tile[2])
        self.grid_pos = (self.grid[0][0][0], self.grid[0][0][1])

    def draw_grid(self, screen):
        for tile in self.grid:
            if tile[1] is None or tile[1][0] is None:
                pygame.draw.rect(screen, (255, 255, 255), tile[0], 1)
            else:
                screen.blit(pygame.transform.rotate(tile[1][0], tile[2]), (tile[0][0], tile[0][1]))

    def move_camera(self, mouse_pos):
        cam_mv = (0, 0)
        speed = 5
        margin = 200

        if mouse_pos[0] < self.dist_camera_mv:
            cam_mv = (cam_mv[0] + 1, cam_mv[1])
        if mouse_pos[1] < self.dist_camera_mv:
            cam_mv = (cam_mv[0], cam_mv[1] + 1)
        if self.screen_dim[0] - mouse_pos[0] < self.dist_camera_mv:
            cam_mv = (cam_mv[0] - 1, cam_mv[1])
        if self.screen_dim[1] - mouse_pos[1] < self.dist_camera_mv:
            cam_mv = (cam_mv[0], cam_mv[1] - 1)

        if cam_mv == (0, 0):
            return

        offset = (cam_mv[0] * speed, cam_mv[1] * speed)
        new_pos = (self.grid_pos[0] + offset[0],
                   self.grid_pos[1] + offset[1])

        if self.screen_dim[0] - self.grid_size[0] - margin <= new_pos[0] <= margin \
                and self.screen_dim[1] - self.grid_size[1] - margin <= new_pos[1] <= margin:
            self.apply_offset(offset)

    @staticmethod
    def load_objects():
        objects = {}
        off = 0
        for root, dirnames, filenames in os.walk('./client/objects/templates'):
            for filename in filenames:
                if filename.endswith('.yaml'):
                    name = os.path.splitext(filename)[0]
                    objects[name] = (pygame.transform.scale(ResourcesManager.get_image(name), (32, 32)),
                                     pygame.Rect(200 + off * 32, 5, 32, 32), name)
                    off += 1
        return objects

    def display_gui(self, screen):
        screen.blit(self.font.render('Current object:', False, (255, 255, 255)), (5, 5))

        for val in self.objects.values():
            screen.blit(val[0], (val[1][0], val[1][1]))

        screen.blit(self.font.render(self.curr_obj[2], False, (255, 200, 200)), (5, 30))

    def get_grid_tile(self, pos):
        for tile in self.grid:
            if tile[0].collidepoint(pos):
                return self.grid.index(tile)
        return None

    def get_toolbox_tile(self, pos):
        for tile in self.objects.values():
            if tile[1].collidepoint(pos):
                return tile
        return None
