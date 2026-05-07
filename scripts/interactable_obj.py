import pygame

class SurfaceObj():
    def __init__(self, game, surf:pygame.Surface, pos:tuple):
        self.game = game
        self.surf = surf
        self.pos = pos
        self.rect = self.surf.get_frect(topleft = pos)

    def update(self, mpos:tuple):
        pass
