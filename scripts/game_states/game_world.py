from scripts.state import State
from scripts.utils import *
from scripts.menu_builder import MenuBuilder
from scripts.game_states.pause_state import PauseMenu
from scripts.game_states.dialogue_state import DialogueState
import pygame

pygame.init()

class GameWorld(State):
    def __init__(self, game):
        super().__init__(game)
        # self.scaled_bg = pygame.transform.scale(self.game.assets['background'], (SCREEN_SIZE[0], SCREEN_SIZE[1]))
        pygame.mouse.set_pos(SCREEN_CENTER)
        self.bg_surf:pygame.Surface = self.game.assets['background']
        self.bg_rect:pygame.FRect = self.bg_surf.get_frect(topleft = (0, 0))
        self.aliza_surf:pygame.Surface = pygame.transform.scale_by(self.game.assets['alizafar'], 2)
        self.aliza_rect:pygame.FRect = self.aliza_surf.get_frect(topleft= (800, 450))
        self.nate_surf:pygame.Surface = pygame.transform.scale_by(self.game.assets['natefar'], 2)
        self.nate_rect:pygame.FRect = self.nate_surf.get_frect(topleft= (250, 425))
        self.paul_surf:pygame.Surface = pygame.transform.scale_by(self.game.assets['paulfar'], 3)
        self.paul_rect:pygame.FRect = self.paul_surf.get_frect(topleft= (575, 450))

    def update(self):
        mpos = pygame.mouse.get_pos()
        if self.aliza_rect.collidepoint(mpos) and self.game.state_interaction_options['left_click']['just_pressed']:
            self.trigger_dialogue('aliza', 'aliza_test.json')
        if self.nate_rect.collidepoint(mpos) and self.game.state_interaction_options['left_click']['just_pressed']:
            self.trigger_dialogue('nate', 'nate_test.json')
        if self.paul_rect.collidepoint(mpos) and self.game.state_interaction_options['left_click']['just_pressed']:
            self.trigger_dialogue('paul', 'paul_test.json')

        if mpos[0] >= int(SCREEN_CENTER[0] + 300): # moving right
            self.bg_rect.x -= 2
            if self.bg_rect.right <= SCREEN_SIZE[0]:
                self.bg_rect.right = SCREEN_SIZE[0]
        elif mpos[0] <= int(SCREEN_CENTER[0] - 300): # moving left
            self.bg_rect.x += 2
            if self.bg_rect.left >= 0:
                self.bg_rect.left = 0

        
        if self.game.state_interaction_options['escape']['just_pressed']:
            pause_menu_state = PauseMenu(self.game)
            pause_menu_state.enter_state()

    def render(self, surf):
        # surf.blit(self.scaled_bg, (0, 0))
        surf.blit(self.bg_surf, self.bg_rect)
        surf.blit(self.aliza_surf, self.aliza_rect)
        surf.blit(self.nate_surf, self.nate_rect)
        surf.blit(self.paul_surf, self.paul_rect)

    def trigger_dialogue(self, character_name, filename):
        dialogue_box = DialogueState(self.game, character_name, filename)
        dialogue_box.enter_state()