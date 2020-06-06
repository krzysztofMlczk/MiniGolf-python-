import json

import tkinter as tk
from tkinter import filedialog, simpledialog
import pygame

from client.resources.ResourcesManager import ResourcesManager
from editor.Structures import Object, Button, ToolIcon, MapTile


def export(map):
    root = tk.Tk()
    root.withdraw()

    map_id = simpledialog.askinteger(title="Map ID",
                                     prompt="Enter the map ID:")

    file_path = filedialog.asksaveasfilename(defaultextension='.json')

    if len(file_path) == 0 or file_path == "()":
        return

    data = {
        "id": map_id,
        "obstacles": [],
        "surfaces": [],
        "cup": {},
        "ball": {}
    }

    for tile in map:
        if tile.has_object():
            for obj in tile.objects:
                if obj.type == 'cup':
                    pos = (tile.rect[0] + obj.image.get_width() // 2,
                           tile.rect[1] + obj.image.get_height() // 2)
                    dim = obj.image.get_size()

                    data['cup']['name'] = obj.name
                    data['cup']['pos'] = pos
                    data['cup']['dim'] = dim
                    data['cup']['rotation'] = obj.rotation

                elif obj.type == 'ball':
                    pos = (tile.rect[0] + obj.image.get_width() // 2,
                           tile.rect[1] + obj.image.get_height() // 2)
                    dim = (obj.image.get_width() // 2, obj.image.get_height() // 2)

                    data['ball']['name'] = obj.name
                    data['ball']['pos'] = pos
                    data['ball']['dim'] = dim
                    data['ball']['rotation'] = obj.rotation
                else:
                    pos = (tile.rect[0], tile.rect[1])
                    dim = (obj.image.get_width(), obj.image.get_height())

                    data[obj.type].append({
                        'name': obj.name,
                        'pos': pos,
                        'dim': dim,
                        'rotation': obj.rotation,
                        'vertical': obj.vertical,
                        'horizontal': obj.horizontal
                    })

    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)


def save(map):
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(defaultextension='.json')

    if len(file_path) == 0 or file_path == "()":
        return

    data = {
        'map': []
    }

    for tile in map:
        obj_list = []

        for obj in tile.objects:
            obj_list.append({
                'name': obj.name,
                'rect': (tile.rect[0], tile.rect[1], tile.rect[2], tile.rect[3]),
                'dim': obj.image.get_size(),
                'vertical': obj.vertical,
                'horizontal': obj.horizontal,
                'rotation': obj.rotation,
                'type': obj.type
            })

        data['map'].append(obj_list)

    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)


def load(map):
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    if len(file_path) == 0 or file_path == "()":
        return

    with open(file_path) as file:
        data = json.load(file)

    map_data = data['map']

    for i in range(len(map)):
        obj_list = map_data[i]

        if len(obj_list) > 0:
            tile = MapTile(map[i].rect, None)

            for obj in obj_list:
                tile.add_object(Object(pygame.transform.scale(ResourcesManager.get_image(obj['name']),
                                                              obj['dim']), obj['name'], obj['rotation'], obj['type'],
                                       horiz=obj['horizontal'], vert=obj['vertical']))

            map[i] = tile
