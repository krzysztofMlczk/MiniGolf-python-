import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

import client.utils
from client.scenes.GameScene import GameScene
from client.resources.ResourcesManager import ResourcesManager
from client.scenes.MainMenuScene import MainMenuScene


class App:
    """Creating single window app with multiple scenes"""
    scenes = {}
    current_scene = None

    def __init__(self):

        # Setting up pygame
        pygame.init()
        info = pygame.display.Info()
        client.utils.screen_size = (info.current_w, info.current_h)

        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
        self.running = True

        # Setting up pymunk
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.dt = 1/120
        self.stepping = False

        # Loading Resources
        ResourcesManager.load_from_disk()

        # Setting up constant players
        players = [(255, 255, 255), (0, 255, 0)]

        # Setting up scenes and choosing first
        App.scenes["Menu"] = MainMenuScene(self.screen)
        App.scenes["Game"] = GameScene()
        App.current_scene = App.scenes["Menu"]

    def run(self):
        """Main app loop"""
        while self.running:

            # Delegating event handling to current scene
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                if event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    if width < 600:
                        width = 600
                    if height < 400:
                        height = 400

                    client.utils.screen_size = (width, height)
                    self.screen = pygame.display.set_mode((width, height), HWSURFACE | DOUBLEBUF | RESIZABLE)
                    App.current_scene.gui_mgr.resize_gui(self.screen)

                App.current_scene.handle_event(event)

            # Processing step in simulation
            if self.stepping:
                App.current_scene.get_space().step(self.dt)

            # Drawing updated scene
            self.draw()

            self.next_scene(self.current_scene.next)

        pygame.quit()

    def draw(self):
        """Delegating updating a scene to a current scene"""
        self.screen.fill(App.current_scene.fill_color)

        # To turn on debug mode on pure simulation underneath
        # uncomment line below and comment one after
        # if isinstance(App.current_scene, GameScene):
        #    App.current_scene.object_mgr.space.debug_draw(self.draw_options)

        App.current_scene.draw(self.screen)
        pygame.display.flip()

    def next_scene(self, next_index):
        if next_index in App.scenes.keys():
            self.stepping = True
            App.current_scene = App.scenes[next_index]
            App.current_scene.setup(players=[(255, 255, 255), (0, 255, 0)])

