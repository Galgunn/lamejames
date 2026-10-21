import pygame
from scripts.scenemap import Scenemap

class Cursor():
    def __init__(self, game, pos, surf):
        self.game = game
        self.pos = pos
        self.surf = surf

    def update(self, scenemap:Scenemap, pos:tuple):
        self.pos = pos

        # Checking for any rect collisions to update the pointer image
        for rect in scenemap.get_rects_around(self.pos):
            if rect.collidepoint(self.pos):
                self.surf = self.game.assets['cursor_magnify']
            else:
                self.surf = self.game.assets['cursor_default']

        # Checking for any MOUSEBUTTONUP events and rect collision with other objects
        pass

    def update_interaction(self, pos):
        self.pos = pos

    def render(self, surf):
        surf.blit(self.surf, self.pos)