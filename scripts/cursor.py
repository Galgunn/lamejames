import pygame
from scripts.scenemap import Scenemap

class Cursor():
    def __init__(self, game, start_pos:tuple, surf:pygame.Surface):
        self.game = game
        self.pos = start_pos
        self.surf = surf

    def update(self, scenemap:Scenemap, pos:tuple):
        self.pos = pos
        # # Checking for any rect collisions to update the pointer image
        # for rect in scenemap.get_rects_around(self.pos):
        #     if rect.collidepoint(self.pos):
        #         self.surf = self.game.assets['cursor_magnify']
        # else:
        #     for rect in scenemap.get_rects_around(self.pos):
        #         if not rect.collidepoint(self.pos):
        #             self.surf = self.game.assets['cursor_default']

        rects = scenemap.get_rects_around(self.pos)

        # Check if any rectangle collides with the cursor
        # if any(rect.collidepoint(self.pos) for rect in rects):
        if self.get_collisions(rects):
            self.surf = self.game.assets['cursor_magnify']
        else:
            self.surf = self.game.assets['cursor_default']

    def render(self, surf):
        surf.blit(self.surf, self.pos)

    def get_collisions(self, rects:list) -> bool:
        rect:pygame.FRect
        for rect in rects:
            if rect.collidepoint(self.pos):
                return True
        return False