from scripts.state import State
from scripts.utils import *
from scripts.game_states.pause_state import PauseMenu
from scripts.game_states.dialogue_state import DialogueState
import pygame

pygame.init()

class CrimeSceneState(State):
    def __init__(self, game):
        super().__init__(game)
        # Declaring variables
        self.bg_surf: pygame.Surface
        self.bg_rect: pygame.FRect
        self.cursor_surf: pygame.Surface
        self.cursor_rect: pygame.FRect
        self.mpos: tuple

        # Initializing variables
        self.bg_surf = pygame.Surface((1000, 750)).convert_alpha()
        self.bg_surf.fill('brown')
        self.bg_rect = self.bg_surf.get_frect()
        self.cursor_surf = self.game.assets['cursor_test']
        self.mpos = pygame.mouse.get_pos()
        pygame.mouse.set_visible(False)

    def update(self):
        self.mpos = pygame.mouse.get_pos()
    
    def render(self, surf):
        surf.blit(self.bg_surf, (0,0))
        surf.blit(self.cursor_surf, self.mpos)