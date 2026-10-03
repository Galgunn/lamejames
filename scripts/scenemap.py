import pygame, json

BASE_SCENEMAP_PATH: str = 'assets_editor/scenes/'
INTERACTABLE: set = {'far_characters', 'alizafar'}

class Scenemap():
    def __init__(self, game):
        # Annotate variables
        self.scene_name: str
        self.scene_map: list

        # Initialize variables
        self.game = game
        self.scene_name = ''
        self.scenemap = []

    def get_interactable_surfs(self) -> list:
        rects = []
        for surf in self.scenemap:
            if surf['type'] in INTERACTABLE:
                rects.append(pygame.FRect(surf['pos'][0], surf['pos'][1], surf['size'][0], surf['size'][1]))
        return rects

    def save(self, scene_name):
        f = open(BASE_SCENEMAP_PATH + scene_name + '.json', 'w')
        json.dump({'scene_name': scene_name, 'scene_map' : self.scenemap}, f)
        f.close()

    def load(self, scene_name):
        f = open(BASE_SCENEMAP_PATH + scene_name + '.json', 'r')
        scene_data = json.load(f)
        f.close()

        self.scene_name = scene_data['scene_name']
        self.scenemap = scene_data['scene_map']

    def render(self, surf):
        for obj in self.scenemap:
            surf.blit(self.game.assets[obj['type']][obj['variant']], (obj['pos'][0], obj['pos'][1]))