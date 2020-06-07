import pygame
import random

from client.gui.Label import Label
from client.models.scene_init import SceneInit
from client.scenes.Scene import Scene
from client.gui.Cloud import Cloud
from client.gui.Button import Button
from client.resources.ResourcesManager import ResourcesManager
from client.models.player import Player


class SetupScene(Scene):
    """Scene for drawing scene for setting up multiplayer game"""

    available_colors = ["yellow", "orange", "blue", "pink", "white"]
    available_players_id = [0, 1, 2, 3, 4]

    def __init__(self, screen, multi):
        super().__init__(None)
        self.change_scene = None
        self.multi = multi
        self.setup_components()
        self.players_amount = 2
        self.maps_to_play = 1
        self.players = []


        self.gui_mgr.resize_gui(screen)

    def setup_components(self):
        """Setting up and registering (happens automatically) components"""
        width, height = 1920, 1080

        # Setup up background, title and clouds
        self.add_label("background", (width, height), (0, 0), "background", (width, height))
        
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
        
        self.add_label("title", (width, height), (0, 0), "title", (width, height))

        # setup labels
        etiquette_size = (416, 100)
        numbers_size = (100, 100)

        # setup buttons
        up_down_btn_size = (50, 50)

        # setup lower buttons
        lower_button_size = (268, 100)

        # Setting up players choice
        if self.multi:
            self.add_label("players_label", etiquette_size, (702, 467), "players_label", (width, height))
            self.add_label("players_amount", numbers_size, (1118, 467), "amount_2", (width, height))
            self.add_button("players_up", up_down_btn_size, (1218, 467), "btn_up", (width, height))
            self.add_button("players_down", up_down_btn_size, (1218, 517), "btn_down", (width, height))

        # Setting up maps choice
        self.add_label("maps_label", etiquette_size, (702, 617), "maps_label", (width, height))
        self.add_label("maps_amount", numbers_size, (1118, 617), "amount_1", (width, height))
        self.add_button("maps_up", up_down_btn_size, (1218, 617), "btn_up", (width, height))
        self.add_button("maps_down", up_down_btn_size, (1218, 667), "btn_down", (width, height))

        # Setting up lower buttons
        self.add_button("play_btn", lower_button_size, (1000, 767), "btn_play", (width, height))
        self.add_button("cancel_btn", lower_button_size, (702, 767), "btn_cancel", (width, height))
    
    def add_label(self, name, dim, pos, image, res):
        Label(
            name=name,
            dimension=dim,
            position=pos,
            image=ResourcesManager.get_image(image),
            obj_mgr=self.gui_mgr,
            default_res=res
        )
    
    def add_button(self, name, dim, pos, image, res):
        Button(
            name=name,
            dimension=dim,
            position=pos,
            image=ResourcesManager.get_image(image),
            image_hover=ResourcesManager.get_image(image + "_hover"),
            obj_mgr=self.gui_mgr,
            default_res=res
        )
        
    def handle_event(self, event):
        for elem in self.gui_mgr.gui_elements:

            # Buttons:
            if isinstance(elem, Button):
                if elem.get_rect().collidepoint(pygame.mouse.get_pos()):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        elem.on_mouse_clicked()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        outcome = elem.on_mouse_released(self.players, self.maps_to_play)
                        if isinstance(outcome, SceneInit):
                            self.change_scene = outcome
                        elif isinstance(outcome, int):
                            if elem.name == "players_up" and self.players_amount < 5:
                                self.players_amount += outcome
                                self.add_player()
                            elif elem.name == "players_down" and self.players_amount > 2:
                                self.players_amount += outcome
                                self.remove_player()
                            elif elem.name == "maps_up" and self.maps_to_play < 5:
                                self.maps_to_play += 1
                            elif elem.name == "maps_down" and self.maps_to_play > 1:
                                self.maps_to_play -= 1
                    else:
                        elem.on_mouse_enter()
                else:
                    elem.on_mouse_quit()

    def draw(self, screen):
        self.update_images()
        self.gui_mgr.update_gui()
        self.gui_mgr.draw_gui(screen)

    def add_player(self):
        player_id = self.available_players_id.pop(0)
        color = random.choice(self.available_colors)
        self.available_colors.remove(color)
        self.players.append(Player(player_id, color))

    def remove_player(self):
        # always remove latest added player
        to_remove = self.players.pop()
        self.available_players_id.append(to_remove.id)
        self.available_colors.append(to_remove.color)

    def update_images(self):
        """function to change numbers while clicking on up/down buttons"""
        for element in self.gui_mgr.gui_elements:
            if isinstance(element, Label):

                if element.name == "players_amount":
                    new_image = ResourcesManager.get_image("amount_" + str(self.players_amount))
                    element.set_image_original(new_image)
                    element.set_size(element.get_size())

                elif element.name == "maps_amount":
                    new_image = ResourcesManager.get_image("amount_" + str(self.maps_to_play))
                    element.set_image_original(new_image)
                    element.set_size(element.get_size())

    def setup(self, screen=None, **kwargs):
        self.players = []

        SetupScene.available_colors = ["yellow", "orange", "blue", "pink", "white"]
        SetupScene.available_players_id = [0, 1, 2, 3, 4]

        # Add one player
        self.add_player()

        if self.multi:
            self.add_player()

