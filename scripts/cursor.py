import pygame
from scripts.scenemap import Scenemap

class Cursor():
    def __init__(self, game, start_pos:tuple, surf:pygame.Surface):
        self.game = game
        self.pos = start_pos
        self.surf = surf

    def update(self, scenemap:Scenemap, pos:tuple):
        self.pos = pos
        rects:list = scenemap.get_rects_around(self.pos)

        # Check if any rects collide with the cursor
        if any(rect.collidepoint(self.pos) for rect in rects):
            self.surf = self.game.assets['cursor_magnify']
        else:
            self.surf = self.game.assets['cursor_default']

    def render(self, surf):
        surf.blit(self.surf, self.pos)