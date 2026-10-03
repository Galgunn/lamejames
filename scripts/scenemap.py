import pygame, json

BASE_SCENEMAP_PATH: str = 'assets/scene_maps/'
INTERACTABLE: set = {'far_characters', 'alizafar'}

class Scenemap():
    def __init__(self, game):
        # Annotate variables
        self.scene_name: str
        self.scene_map: list

        # Initialize variables
        self.game = game
        self.scene_name = ''
        self.scene_map = []

        self.scene_map = [
            {'type': 'background', 'pos': (0, 0)},
            {'type': 'alizafar', 'pos': (50, 50), 'size': (25, 25)}
        ]

    def get_interactable_surfs(self) -> list:
        rects = []
        for surf in self.scene_map:
            if surf['type'] in INTERACTABLE:
                rects.append(pygame.FRect(surf['pos'][0], surf['pos'][1], surf['size'][0], surf['size'][1]))
        return rects


    def save(self, scene_name, path):
        f = open(path, 'w')
        json.dump({'scene_name': scene_name, 'scene_map' : self.scene_map}, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        scene_data = json.load(f)
        f.close()

        self.scene_name = scene_data['scene_name']
        self.scene_map = scene_data['scene_map']

    def render(self, surf):
        for obj in self.scene_map:
            surf.blit(self.game.assets[obj['type']], (obj['pos'][0], obj['pos'][1]))