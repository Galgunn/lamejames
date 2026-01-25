import json
import pygame
from scripts.state import State
from scripts.dialogue_system import DialogueSystem
from scripts.utils import SCREEN_SIZE

BASE_JSON_PATH:str = 'assets/dialogue/'
CHARACTER_TALKING_POS:tuple = (650, 100)
CHARACTER_FONT_COLORS:dict = {
    'Aliza': (255, 0, 0),
    'Nate': (0, 255, 0),
    'Paul': (0, 0, 255),
    'Player': (255, 255, 255)
}

class DialogueState(State):
    def __init__(self, game, char_name:str, filename:str):
        super().__init__(game)
        self.lines:list = []
        self.json_filename:str = filename
        self.dialogue_data = {}
        self.aliza_dialogue_counter = 0
        self.current_id = '0'
        self.speaker_name = ''
        self.next_id = ''
        self.lines = []
        self.load(BASE_JSON_PATH + self.json_filename)

        # Dialogue testing

        self.dialogue_box_rect:pygame.FRect = pygame.Rect(0, 0, SCREEN_SIZE[0], 200)
        self.character_surf:pygame.Surface = pygame.transform.scale_by(self.game.assets[char_name + 'talk'], 1.5)

        self.dialogue_system:DialogueSystem = DialogueSystem(self.game, self.dialogue_box_rect.width)
        self.dialogue_system.get_lines(self.lines, self.text_color)

        pygame.mixer.music.load('assets/music/examiner.wav')

        pygame.mixer.music.play(-1,0.0)

    def update(self):
        self.dialogue_system.update()

        if self.game.state_interaction_options['left_click']['just_pressed'] and self.dialogue_system.dialogue_complete:
            # pygame.mixer.music.stop()
            if self.next_id != "":
                self.get_next_id()
                self.dialogue_system.get_lines(self.lines, self.text_color)
                self.dialogue_system.reset()
            else:
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
        self.speaker_name = self.dialogue_data[self.current_id]['speaker']
        self.next_id = self.dialogue_data[self.current_id]['next_id']
        self.lines = self.dialogue_data[self.current_id]['lines']
        self.text_color = CHARACTER_FONT_COLORS[self.speaker_name]

    def get_next_id(self):
        self.current_id = self.next_id
        self.speaker_name = self.dialogue_data[self.current_id]['speaker']
        self.next_id = self.dialogue_data[self.current_id]['next_id']
        self.lines = self.dialogue_data[self.current_id]['lines']
        self.text_color = CHARACTER_FONT_COLORS[self.speaker_name]
