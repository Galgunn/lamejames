import pygame, json
from scripts.utils import BASE_SCENE_MAP_PATH

INTERACTABLE: set = {'characters_far'}

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

    def get_asset_around(self, pos:tuple):
        assets = []
        cursor_rect = pygame.FRect(0, 0, 75, 75)
        cursor_rect.center = pos
        for asset in self.scene_map:
            asset_rect = pygame.FRect(asset['pos'][0], asset['pos'][1], asset['size'][0], asset['size'][1])
            if asset_rect.colliderect(cursor_rect):
                assets.append(asset)
        return assets

    def get_rects_around(self, pos:tuple):
        rects = []
        for asset in self.get_asset_around(pos):
            if asset['type'] in INTERACTABLE:
                rects.append(pygame.FRect(asset['pos'][0], asset['pos'][1], asset['size'][0], asset['size'][1]))    
        return rects

    def save(self, scene_name):
        f = open(BASE_SCENE_MAP_PATH + scene_name + '.json', 'w')
        json.dump({'scene_name': scene_name, 'scene_bg': self.scene_bg, 'scene_map' : self.scene_map}, f)
        f.close()

    def load(self, scene_name):
        f = open(BASE_SCENE_MAP_PATH + scene_name + '.json', 'r')
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