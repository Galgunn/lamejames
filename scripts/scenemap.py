import pygame, json

BASE_SCENEMAP_PATH: str = 'assets/scene_maps/'

class Scenemap():
    def __init__(self, game):
        # Annotate variables
        self.scene_name: str
        self.scene_map: list

        # Initialize variables
        self.game = game
        self.scene_name = ''
        self.scene_map = []

    def get_interactable_rect(self) -> list:
        rects = []


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