import os
import copy
import yaml
import math

import pygame
import pymunk

from client.scenes.Scene import Scene
from client.resources.ResourcesManager import ResourcesManager
from editor.Structures import Object, Button, ToolIcon, MapTile
from editor import FileUtils


class EditorScene(Scene):
    def __init__(self, screen_dim):
        super().__init__(pymunk.Space())
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        # Distance of mouse pointer from screen border that forces camera movement:
        self.dist_camera_mv = 200

        self.grid_size = None
        self.grid_dimension = None
        self.block_size = 32
        self.grid_pos = (0, 0)
        self.grid = []
        self.screen_dim = screen_dim
        self.generate_grid()

        self.dragging = None

        self.text_current_orig = (5, 5)
        self.text_current = self.font.render('Current object:', False, (255, 255, 255))
        self.text_obj_orig = (self.text_current_orig[0], self.text_current_orig[1] + self.text_current.get_height())

        self.toolbox = self.load_objects(self.text_obj_orig[0] + self.text_current.get_width() + 50)
        self.curr_obj = ToolIcon(None, None)

        self.button_export = Button(ResourcesManager.get_image('export_icon'), (self.screen_dim[0] - 184, 10))
        self.button_save = Button(ResourcesManager.get_image('save_icon'), (self.screen_dim[0] - 142, 10))
        self.button_load = Button(ResourcesManager.get_image('load_icon'), (self.screen_dim[0] - 100, 10))

    def draw(self, screen):
        self.move_camera(pygame.mouse.get_pos())

        self.display.fill((0, 0, 0))
        self.draw_grid(screen)

        if self.dragging is not None:
            hover = self.get_grid_tile(pygame.mouse.get_pos())

            if hover is not None:
                width = self.grid[hover].rect[0] - self.grid[self.dragging[0]].rect[0]
                if width < 0:
                    width = 0
                height = self.grid[hover].rect[1] - self.grid[self.dragging[0]].rect[1]
                if height < 0:
                    height = 0
                pygame.draw.rect(screen, (200, 0, 0), pygame.Rect(self.grid[self.dragging[0]].rect[0],
                                                                  self.grid[self.dragging[0]].rect[1],
                                                                  (width + self.block_size * (width >= 0)),
                                                                  (height + self.block_size * (height >= 0))), 2)

        self.display_gui(screen)

    def handle_event(self, event):
        """Handling specific scene events"""
        mouse_pos = pygame.mouse.get_pos()
        shift = pygame.key.get_pressed()[pygame.K_LSHIFT]

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                # Button click:
                if self.button_save.clicked(mouse_pos):
                    FileUtils.save(self.grid)
                elif self.button_load.clicked(mouse_pos):
                    FileUtils.load(self.grid)
                elif self.button_export.clicked(mouse_pos):
                    FileUtils.export(self.grid)

                # Placing new object:
                clicked_toolbox = self.get_toolbox_tile(mouse_pos)
                clicked_tile_index = self.get_grid_tile(mouse_pos)

                if clicked_toolbox is not None:
                    self.curr_obj = clicked_toolbox
                elif clicked_tile_index is not None and self.curr_obj.object is not None:
                    if shift:
                        self.dragging = [clicked_tile_index, None]
                    else:
                        obj = copy.copy(self.curr_obj.object)
                        obj.rotation = 0
                        self.grid[clicked_tile_index].add_object(obj)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                clicked_tile_index = self.get_grid_tile(mouse_pos)

                if self.dragging is not None:
                    if clicked_tile_index is None:
                        self.dragging = None
                    else:
                        self.dragging[1] = clicked_tile_index
                        start_cords = [self.dragging[0] // self.grid_dimension[1],
                                       self.dragging[0] % self.grid_dimension[1]]
                        end_cords = [self.dragging[1] // self.grid_dimension[1],
                                     self.dragging[1] % self.grid_dimension[1]]

                        if start_cords[0] == end_cords[0] and start_cords[1] == end_cords[1]:
                            obj = copy.copy(self.curr_obj.object)
                            obj.rotation = 0
                            self.grid[clicked_tile_index].add_object(obj)

                        elif start_cords[0] <= end_cords[0] and start_cords[1] <= end_cords[1]:

                            obj = copy.copy(self.curr_obj.object)
                            obj.rotation = 0
                            obj.vertical = abs(end_cords[1] - start_cords[1]) + \
                                           int(math.copysign(1, end_cords[1] - start_cords[1]))
                            obj.horizontal = abs(end_cords[0] - start_cords[0]) + \
                                             int(math.copysign(1, end_cords[0] - start_cords[0]))

                            self.grid[self.dragging[0]].add_object(obj)

                        self.dragging = None

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
        self.grid_dimension = dim
        self.block_size = block_size

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
                for obj in tile.objects:
                    if obj.vertical != 1 or obj.horizontal != 1:
                        screen.blit(pygame.transform.rotate(obj.overlap_image(), obj.rotation),
                                    (tile.rect[0], tile.rect[1]))
                        pygame.draw.rect(screen, (200, 200, 0), tile.rect, 3)
                    else:
                        screen.blit(pygame.transform.rotate(obj.image, obj.rotation),
                                    (tile.rect[0], tile.rect[1]))

    def get_tile(self, x, y):
        index = y + x * self.grid_dimension[1]
        if 0 <= index < self.grid_dimension[0] * self.grid_dimension[1]:
            return self.grid[index]
        return None

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
    def load_objects(origin):
        objects = {}
        off = 0
        for root, dirnames, filenames in os.walk('./client/objects/templates'):
            for filename in filenames:
                if filename.endswith('.yaml'):
                    name = os.path.splitext(filename)[0]

                    yaml_file = open(os.path.join(root, filename))
                    parsed_yaml_file = yaml.load(yaml_file, Loader=yaml.FullLoader)
                    t = parsed_yaml_file["type"]
                    yaml_file.close()

                    obj = Object(pygame.transform.scale(ResourcesManager.get_image(name), (32, 32)), name, 0, t)
                    icon = ToolIcon(obj, pygame.Rect(origin + off * 32, 5, 32, 32))

                    objects[name] = icon
                    off += 1

        objects['cup'] = ToolIcon(
            Object(pygame.transform.scale(
                ResourcesManager.get_image('obj_hole'), (32, 32)
            ), 'obj_hole', 0, 'cup'), pygame.Rect(origin + off * 32, 5, 32, 32)
        )
        off += 1

        objects['ball'] = ToolIcon(
            Object(pygame.transform.scale(
                ResourcesManager.get_image('obj_ball_white'), (32, 32)
            ), 'obj_ball_white', 0, 'ball'), pygame.Rect(origin + off * 32, 5, 32, 32)
        )
        off += 1

        return objects

    def display_gui(self, screen):
        if self.curr_obj.object is not None:
            name = self.curr_obj.object.name
        else:
            name = 'None'

        # Draw object description:

        screen.blit(self.text_current, self.text_current_orig)
        screen.blit(self.font.render(name, False, (255, 200, 200)), self.text_obj_orig)

        # Draw toolbox:
        for tool in self.toolbox.values():
            screen.blit(tool.object.image, (tool.rect[0], tool.rect[1]))

        # Draw save/load buttons:
        screen.blit(self.button_export.image, self.button_export.pos)
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
