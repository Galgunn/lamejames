import pygame

class Pointer():
    def __init__(self, game, pos, surf):
        self.game = game
        self.pos = pos
        self.surf = surf

    def update(self, pos):
        self.pos = pos

        # Checking for any rect collisions to update the pointer image
        pass

        # Checking for any MOUSEBUTTONUP events and rect collision with other objects
        pass


    def render(self, surf):
        surf.blit(self.surf, self.pos)