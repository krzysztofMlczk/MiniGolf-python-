import pygame
import pymunk
from pygame.locals import *
import pymunk.pygame_util

from client.resources.ResourcesManager import ResourcesManager
from editor.EditorScene import EditorScene


class Editor:
    def __init__(self):
        # Setting up pygame
        pygame.init()
        info = pygame.display.Info()

        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)

        # Loading Resources
        ResourcesManager.load_from_disk()

        self.scene = EditorScene((info.current_w, info.current_h))
        self.running = True

        # Setting up pymunk
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.dt = 1 / 80
        self.stepping = False

    def run(self):
        """Main app loop"""
        while self.running:

            # Handling mutual events for all scenes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.VIDEORESIZE:
                    width, height = event.size

                    if width < 600:
                        width = 600
                    if height < 400:
                        height = 400

                    self.screen = pygame.display.set_mode((width, height), HWSURFACE | DOUBLEBUF | RESIZABLE)
                    self.scene.gui_mgr.resize_gui(self.screen)

                # Delegating specific event handling to current scene
                self.scene.handle_event(event)

            # Processing step in simulation
            if self.stepping:
                self.scene.get_space().step(self.dt)

            # Drawing updated scene
            self.draw()

        pygame.quit()

    def draw(self):
        """Delegating updating a scene to a current scene"""
        self.screen.fill(self.scene.fill_color)

        # To turn on debug mode on pure simulation underneath
        # uncomment line below and comment one after
        # if isinstance(App.current_scene, GameScene):
        #    App.current_scene.object_mgr.space.debug_draw(self.draw_options)

        self.scene.draw(self.screen)
        pygame.display.flip()