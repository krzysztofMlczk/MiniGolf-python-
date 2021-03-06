import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

import client.utils
from client.scenes.AboutScene import AboutScene
from client.scenes.GameScene import GameScene
from client.resources.ResourcesManager import ResourcesManager
from client.scenes.MainMenuScene import MainMenuScene
from client.scenes.SetupScene import SetupScene
from client.scenes.ScoreScene import ScoreScene


class App:
    """Creating single window app with multiple scenes"""
    scenes = {}
    current_scene = None

    def __init__(self):

        # Setting up pygame
        pygame.init()
        info = pygame.display.Info()
        self.clock = pygame.time.Clock()
        client.utils.screen_size = (info.current_w, info.current_h)

        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
        self.running = True

        # Setting up pymunk
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.dt = 1/120
        self.stepping = False

        # Loading Resources
        ResourcesManager.load_from_disk()

        # Setting up scenes and choosing first
        App.scenes["Menu"] = MainMenuScene(self.screen)
        App.scenes["MultiSetup"] = SetupScene(self.screen, multi=True)
        App.scenes["SingleSetup"] = SetupScene(self.screen, multi=False)
        App.scenes["About"] = AboutScene(self.screen)
        App.scenes["Score"] = ScoreScene(self.screen)
        App.scenes["Game"] = GameScene()
        App.current_scene = App.scenes["Menu"]

    def run(self):
        """Main app loop"""
        while self.running:

            # Handling mutual events for all scenes
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                if event.type == pygame.VIDEORESIZE:
                    width, height = event.size

                    if width < 600:
                        width = 600
                    if height < 400:
                        height = 400

                    self.screen = pygame.display.set_mode((width, height), HWSURFACE | DOUBLEBUF | RESIZABLE)

                    client.utils.screen_size = (width, height)
                    App.current_scene.gui_mgr.resize_gui(self.screen)

                # Delegating specific event handling to current scene
                App.current_scene.handle_event(event)

            # Processing step in simulation
            if self.stepping:
                App.current_scene.get_space().step(self.dt)

            # Drawing updated scene
            self.draw()

            # Checking if new scene should be loaded
            self.next_scene()
            self.clock.tick(120)

            # Print fps
            # print(self.clock.get_fps())

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

    def next_scene(self):
        change_scene = App.current_scene.change_scene
        if change_scene and change_scene.scene_id in App.scenes.keys():

            if change_scene.scene_id == "Game":
                self.stepping = True
            else:
                self.stepping = False

            App.current_scene.change_scene = None
            App.current_scene = App.scenes[change_scene.scene_id]
            App.current_scene.setup(**change_scene.kwargs)
