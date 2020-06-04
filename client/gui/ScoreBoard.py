import pygame

from client.gui.GUIElement import GUIElement


class ScoreBoard(GUIElement):
    def __init__(self, name, dimension, position, image, obj_mgr, default_res=None):
        super().__init__(position, dimension, image, name, obj_mgr, default_res)

    def set_score(self, player):
        pass