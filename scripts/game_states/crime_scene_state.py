from scripts.state import State
from scripts.utils import *
from scripts.game_states.pause_state import PauseMenu
from scripts.game_states.dialogue_state import DescriptionState
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
        self.interaction_obj: pygame.Surface
        self.interaction_obj_rect: pygame.FRect
        self.on_obj: bool
        self.interaction_obj_desc: list
        self.enter_diag: bool

        self.evidence_objs: dict

        # Initializing variables
        self.bg_surf = pygame.Surface((1000, 750)).convert_alpha()
        self.bg_surf.fill('brown')
        self.bg_rect = self.bg_surf.get_frect()
        self.cursor_surf = self.game.assets['cursor_test']
        self.mpos = pygame.mouse.get_pos()
        self.interaction_obj = pygame.Surface((50, 50))
        self.interaction_obj_rect = self.interaction_obj.get_frect(topleft = (100, 100))
        self.on_obj = False
        self.interaction_obj_desc = ["It's a white box", "still a white box", "when will you learn think man think omg its the lolsdjflsakdfl"]
        self.enter_diag = False

        self.evidence_objs = {
            'white_box': {
                'surf': self.game.assets['test_surf'],
                'rect': self.interaction_obj_rect,
                'description': [
                    "It's a white box", "still a white box"
                ]
            }
        }

    def update(self):
        enter_diag:bool = False
        self.mpos = pygame.mouse.get_pos()
        if self.interaction_obj_rect.collidepoint(self.mpos):
            pygame.mouse.set_visible(False)
            self.on_obj = True
        else:
            pygame.mouse.set_visible(True)
            self.on_obj = False

        if self.interaction_obj_rect.collidepoint(self.mpos) and self.game.state_interaction_options['left_click']['just_pressed']:
            enter_diag = True

        if enter_diag:
            description_state = DescriptionState(self.game, self.interaction_obj_desc)
            description_state.enter_state()
    
    def render(self, surf):
        surf.blit(self.bg_surf, (0,0))
        self.interaction_obj.fill('white')
        surf.blit(self.interaction_obj, self.interaction_obj_rect)
        if self.on_obj:
            surf.blit(self.cursor_surf, self.mpos)