import pygame, json

BASE_SCENEMAP_PATH: str = 'assets_editor/scenes/'
INTERACTABLE: set = {'far_characters', 'alizafar'}

class Scenemap():
    def __init__(self, game):
        # Annotate variables
        self.scene_name: str
        self.scene_bg: list
        self.scene_map: list

        # Initialize variables
        self.game = game
        self.scene_name = ''
        self.scene_bg = []
        self.scene_map = []

    def get_interactable_surfs(self) -> list:
        rects = []
        for surf in self.scene_map:
            if surf['type'] in INTERACTABLE:
                rects.append(pygame.FRect(surf['pos'][0], surf['pos'][1], surf['size'][0], surf['size'][1]))
        return rects

    def save(self, scene_name):
        f = open(BASE_SCENEMAP_PATH + scene_name + '.json', 'w')
        json.dump({'scene_name': scene_name, 'scene_bg': self.scene_bg, 'scene_map' : self.scene_map}, f)
        f.close()

    def load(self, scene_name):
        f = open(BASE_SCENEMAP_PATH + scene_name + '.json', 'r')
        scene_data = json.load(f)
        f.close()

        self.scene_name = scene_data['scene_name']
        self.scene_bg = scene_data['scene_bg']
        self.scene_map = scene_data['scene_map']

    def render(self, surf):
        for bg in self.scene_bg:
            surf.blit(self.game.assets['backgrounds'][bg['variant']], (bg['pos'][0], bg['pos'][1]))
        for obj in self.scene_map:
            surf.blit(self.game.assets[obj['type']][obj['variant']], (obj['pos'][0], obj['pos'][1]))