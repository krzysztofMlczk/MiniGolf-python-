import os
import copy

import pygame
import pymunk

from client.scenes.Scene import Scene
from client.resources.ResourcesManager import ResourcesManager
from editor import FileUtils


class Object:
    def __init__(self, image, name, rot):
        self.image = image
        self.name = name
        self.rotation = rot


class Button:
    def __init__(self, image, pos):
        self.image = image
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], image.get_width(), image.get_height())

    def clicked(self, pos):
        return self.rect.collidepoint(*pos)


class ToolIcon:
    def __init__(self, obj, rect):
        self.object = obj
        self.rect = rect


class MapTile:
    def __init__(self, rect, obj):
        self.rect = rect

        self.objects = []
        if obj is not None:
            self.add_object(obj)

    def add_object(self, obj):
        for o in self.objects:
            if o.name == obj.name:
                return
        self.objects.append(obj)

    def remove_object(self, obj):
        for o in self.objects:
            if o.name == obj.name:
                self.objects.remove(o)

    def clear_objects(self):
        self.objects.clear()

    def has_object(self):
        return len(self.objects) > 0

    def rotate_object(self, obj, rot):
        for o in self.objects:
            if o.name == obj.name:
                o.rotation = (o.rotation + rot) % 360


class EditorScene(Scene):
    def __init__(self, screen_dim):
        super().__init__(pymunk.Space())
        # Distance of mouse pointer from screen border that forces camera movement:
        self.dist_camera_mv = 200

        self.grid_size = None
        self.grid_pos = (0, 0)
        self.grid = []
        self.screen_dim = screen_dim
        self.generate_grid()

        self.toolbox = self.load_objects()
        self.curr_obj = ToolIcon(None, None)

        self.button_save = Button(ResourcesManager.get_image('save_icon'), (self.screen_dim[0] - 142, 10))
        self.button_load = Button(ResourcesManager.get_image('load_icon'), (self.screen_dim[0] - 100, 10))

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
                # Button click:
                if self.button_save.clicked(mouse_pos):
                    FileUtils.save()
                elif self.button_load.clicked(mouse_pos):
                    FileUtils.load()

                # Placing new object:
                clicked_toolbox = self.get_toolbox_tile(mouse_pos)
                clicked_tile_index = self.get_grid_tile(mouse_pos)

                if clicked_toolbox is not None:
                    self.curr_obj = clicked_toolbox
                elif clicked_tile_index is not None and self.curr_obj.object is not None:
                    obj = copy.copy(self.curr_obj.object)
                    obj.rotation = 0
                    self.grid[clicked_tile_index].add_object(obj)

            # Deleting object:
            elif event.button == pygame.BUTTON_RIGHT:
                clicked_tile_index = self.get_grid_tile(mouse_pos)
                if clicked_tile_index is not None:
                    self.grid[clicked_tile_index].clear_objects()

            # Rotating object:
            elif event.button == pygame.BUTTON_MIDDLE:
                clicked_tile_index = self.get_grid_tile(mouse_pos)
                if clicked_tile_index is not None and self.grid[clicked_tile_index].has_object():
                    self.grid[clicked_tile_index].rotate_object(self.curr_obj.object, 90)

        elif event.type == pygame.MOUSEBUTTONUP:
            pass

    def generate_grid(self, block_size=32, dim=(60, 32)):
        width, height = dim
        self.grid.clear()

        for x in range(0, width * block_size, block_size):
            for y in range(0, height * block_size, block_size):
                rect = pygame.Rect(x, y, block_size, block_size)
                self.grid.append(MapTile(rect, None))

        self.grid_size = (dim[0] * block_size, dim[1] * block_size)

    def apply_offset(self, offset):
        for i in range(len(self.grid)):
            rect = self.grid[i].rect
            self.grid[i].rect = pygame.Rect(rect[0] + offset[0], rect[1] + offset[1],
                                            rect[2], rect[3])

        self.grid_pos = (self.grid[0].rect[0], self.grid[0].rect[1])

    def draw_grid(self, screen):
        for tile in self.grid:
            if not tile.has_object():
                pygame.draw.rect(screen, (255, 255, 255), tile.rect, 1)
            else:
                img = pygame.Surface(tile.objects[0].image.get_size())
                for obj in tile.objects:
                    img.blit(pygame.transform.rotate(obj.image, obj.rotation), (0, 0))

                screen.blit(img,
                            (tile.rect[0], tile.rect[1]))

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
                    obj = Object(pygame.transform.scale(ResourcesManager.get_image(name), (32, 32)), name, 0)
                    icon = ToolIcon(obj, pygame.Rect(200 + off * 32, 5, 32, 32))

                    objects[name] = icon
                    off += 1

        objects['cup'] = ToolIcon(Object(pygame.transform.scale(ResourcesManager.get_image('obj_hole'),
                                                                (32, 32)), 'cup', 0),
                                  pygame.Rect(200 + off * 32, 5, 32, 32))
        off += 1
        objects['ball'] = ToolIcon(Object(pygame.transform.scale(ResourcesManager.get_image('obj_ball_white'),
                                                                 (32, 32)), 'ball', 0),
                                   pygame.Rect(200 + off * 32, 5, 32, 32))
        off += 1

        return objects

    def display_gui(self, screen):
        # Draw toolbox:
        screen.blit(self.font.render('Current object:', False, (255, 255, 255)), (5, 5))

        for tool in self.toolbox.values():
            screen.blit(tool.object.image, (tool.rect[0], tool.rect[1]))

        if self.curr_obj.object is not None:
            name = self.curr_obj.object.name
        else:
            name = 'None'

        screen.blit(self.font.render(name, False, (255, 200, 200)), (5, 30))

        # Draw save/load buttons:
        screen.blit(self.button_save.image, self.button_save.pos)
        screen.blit(self.button_load.image, self.button_load.pos)

    def get_grid_tile(self, pos):
        for tile in self.grid:
            if tile.rect.collidepoint(pos):
                return self.grid.index(tile)
        return None

    def get_toolbox_tile(self, pos):
        for tool in self.toolbox.values():
            if tool.rect.collidepoint(pos):
                return tool
        return None
