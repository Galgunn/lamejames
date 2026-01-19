import json
import pygame
from scripts.state import State
from scripts.dialogue_system import DialogueSystem
from scripts.utils import SCREEN_SIZE

BASE_JSON_PATH:str = 'assets/dialogue/'
CHARACTER_TALKING_POS:tuple = (650, 100)

class DialogueState(State):
    def __init__(self, game, character_name:str, filename:str):
        super().__init__(game)
        self.lines:list = []
        self.special_lines:list = []
        self.character_name:str = character_name
        self.json_filename:str = filename
        self.load(BASE_JSON_PATH + self.json_filename)
        self.dialogue_box_rect:pygame.FRect = pygame.Rect(0, 0, SCREEN_SIZE[0], 200)
        self.character_surf:pygame.Surface = pygame.transform.scale_by(self.game.assets[character_name + 'talk'], 1.5)

        self.dialogue_system:DialogueSystem = DialogueSystem(self.game, self.lines, self.special_lines, self.dialogue_box_rect.width)

        pygame.mixer.pre_init(44100,-16, 2, 1)
        pygame.mixer.init()      
        pygame.mixer.music.load('assets/music/examiner.wav')
        
        pygame.mixer.music.play(-1,0.0)
        
    def update(self):
        self.dialogue_system.update()

        if self.game.state_interaction_options['left_click']['just_pressed'] and self.dialogue_system.dialogue_complete:
            pygame.mixer.music.stop()
            self.exit_state()

    def render(self, surf):
        self.prev_state.render(surf) # type: ignore error due to prev state being None
        self.dialogue_box_rect.topleft = (0, 600)
        surf.blit(self.character_surf, CHARACTER_TALKING_POS)
        pygame.draw.rect(surf, ('black'), self.dialogue_box_rect)
        self.dialogue_system.render(surf, (self.dialogue_box_rect.x + 10, self.dialogue_box_rect.y + 10))

    def load(self, path):
        f = open(path, 'r')
        dialogue_data = json.load(f)
        f.close()

        self.lines = dialogue_data[self.character_name]
        # self.special_lines = dialogue_data['special']

    def on_enter(self):
        self.dialogue_system.reset()
