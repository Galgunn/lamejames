import pygame, sys
from scripts.scenemap import Scenemap
from scripts.utils import SCREEN_SIZE, load_image, load_images

pygame.init()

BASE_MAP_PATH: str = 'assets/maps/'

class Editor():
    def __init__(self):
        # Anotate variables
        self.screen: pygame.Surface
        self.display: pygame.Surface
        self.clock: pygame.time.Clock
        self.running: bool
        self.assets: dict
        self.scenemap: Scenemap
        self.surf_list: list
        self.surf_type: int
        self.surf_variant:int
        self.left_click: bool
        self.right_click: bool
        self.shift: bool

        pygame.display.set_caption('Editor')
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.display = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.clock = pygame.time.Clock()
        self.running = True
        self.assets = {
            'characters_far': load_images('characters_far'),
            'characters_talking': load_images('characters_talking'),
        }
        self.scenemap = Scenemap(self)

        self.surf_list = list(self.assets)
        self.surf_type = 0
        self.surf_variant = 0

        self.left_click = False
        self.right_click = False
        self.shift = False