import json
import pygame
from scripts.state import State
from scripts.dialogue_system import DialogueSystem
from scripts.utils import SCREEN_SIZE

BASE_JSON_PATH:str = 'assets/dialogue/'
CHARACTER_TALKING_POS:tuple = (650, 100)

class DialogueState(State):
    def __init__(self, game, speaker_name:str, filename:str):
        super().__init__(game)
        self.lines:list = []
        self.speaker_name:str = speaker_name
        self.json_filename:str = filename
        self.dialogue_data = {}
        self.aliza_dialogue_counter = 0
        self.load(BASE_JSON_PATH + self.json_filename)
        print(self.dialogue_data)


        # Dialogue testing

        self.dialogue_box_rect:pygame.FRect = pygame.Rect(0, 0, SCREEN_SIZE[0], 200)
        self.character_surf:pygame.Surface = pygame.transform.scale_by(self.game.assets[speaker_name + 'talk'], 1.5)

        self.dialogue_system:DialogueSystem = DialogueSystem(self.game, self.lines, self.dialogue_box_rect.width)

        pygame.mixer.music.load('assets/music/examiner.wav')

        pygame.mixer.music.play(-1,0.0)

    def update(self):
        self.dialogue_system.update()

        if self.game.state_interaction_options['left_click']['just_pressed'] and self.dialogue_system.dialogue_complete:
            # pygame.mixer.music.stop()
            self.exit_state()

    def render(self, surf):
        self.prev_state.render(surf) # type: ignore error due to prev state being None
        self.dialogue_box_rect.topleft = (0, 600)
        surf.blit(self.character_surf, CHARACTER_TALKING_POS)
        pygame.draw.rect(surf, ('black'), self.dialogue_box_rect)
        self.dialogue_system.render(surf, (self.dialogue_box_rect.x + 10, self.dialogue_box_rect.y + 10))

    def load(self, path):
        f = open(path, 'r')
        dialogue_dict = json.load(f)
        f.close()

        self.dialogue_data = dialogue_dict["dialogue_" + str(self.aliza_dialogue_counter)]
        # self.special_lines = dialogue_data['special']

    def on_enter(self):
        self.dialogue_system.reset()
