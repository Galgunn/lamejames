import pygame, sys
from scripts.scenemap import Scenemap
from scripts.utils import SCREEN_SIZE

BASE_MAP_PATH: str = 'assets/maps/'

class Editor():
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Editor')
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.clock = pygame.time.Clock()
        self.assets = {
            
        }