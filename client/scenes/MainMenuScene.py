import pygame

from client.gui.Label import Label
from client.gui.Cloud import Cloud
from client.gui.Button import Button
from client.scenes.Scene import Scene
from client.resources.ResourcesManager import ResourcesManager


class MainMenuScene(Scene):
    """Scene for drawing main menu game events"""
    def __init__(self, screen):
        super().__init__(None)
        self.setup_components()
        self.change_scene = None

        self.gui_mgr.resize_gui(screen)

    def setup_components(self):
        """setting up and registering(happens automatically) components"""

        width, height = 1920, 1080

        # Setup up background, title and clouds
        background = Label(
            name="background",
            dimension=(width, height),
            position=(0, 0),
            image=ResourcesManager.get_image("background"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        left_cloud = Cloud(
            position=(92, 175),
            dimension=(595, 259),
            height_coefficient=(176 / 1080),
            width_coefficient=(186 / 1920),
            image=ResourcesManager.get_image("left_cloud"),
            name="left_cloud",
            move_dir="right",
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        right_cloud = Cloud(
            position=(1392, 66),
            dimension=(476, 207),
            height_coefficient=(66 / 1080),
            width_coefficient=(1052 / 1920),
            image=ResourcesManager.get_image("right_cloud"),
            name="right_cloud",
            move_dir="left",
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        title = Label(
            name="title",
            dimension=(width, height),
            position=(0, 0),
            image=ResourcesManager.get_image("title"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        # setup buttons
        button_names = ["single", "multi", "about", "quit"]
        button_size = (416, 98)
        offset = 30

        for i, name in enumerate(button_names):
            Button(
                name=name,
                dimension=button_size,
                position=((width - button_size[0]) // 2 + offset, height // 2 + button_size[1] * (i - 1) + offset),
                image=ResourcesManager.get_image(name),
                image_hover=ResourcesManager.get_image(name + "_hover"),
                obj_mgr=self.gui_mgr,
                default_res=(width, height)
            )

    def handle_event(self, event):
        for elem in self.gui_mgr.gui_elements:

            # Buttons:
            if isinstance(elem, Button):
                if elem.get_rect().collidepoint(pygame.mouse.get_pos()):

                    # Mouse click:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        elem.on_mouse_clicked()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.change_scene = elem.on_mouse_released()
                    else:
                        elem.on_mouse_enter()
                else:
                    elem.on_mouse_quit()

    def draw(self, screen):
        self.gui_mgr.update_gui()
        self.gui_mgr.draw_gui(screen)

    def setup(self, **kwargs):
        pass






