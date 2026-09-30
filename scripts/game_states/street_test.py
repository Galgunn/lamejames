import pygame
from scripts.state import State
from scripts.utils import SCREEN_CENTER, SCREEN_SIZE
from scripts.button_builder import FontButton, SurfaceButton
from scripts.dialogue_manager import DialogueManager
from scripts.game_states.talking_state import TalkingState
from scripts.game_states.dialogue_states import DialogueState
from scripts.game_states.scene_state import SceneState

pygame.init()

class StreetTest(State):
    def __init__(self, game):
        super().__init__(game)

        # Declaring variables
        self.bg_surf: pygame.Surface
        self.cursor_surf: pygame.Surface
        self.cursor_rect: pygame.FRect
        self.talking: bool
        self.characters: dict
        self.dialogue_manager: DialogueManager

        # What im focusing on
        self.scenemap: list # a list of dicts containing data like surfaces (i.e. background and characters), and rects

        # Initializing variables
        pygame.mouse.set_pos(SCREEN_CENTER)

        # What im focusing on as
        # dict data structure is {type: str, pos: tuple, size: tuple} EXCLUDE width and height is the type in non interactable
        self.scenemap = [
            {'type': 'background', 'pos': (0, 0)},
            {'type': 'alizafar', 'pos': (50, 50), 'size': (25, 25)}
        ]

        # self.bg_surf = self.game.assets['background']
        # self.bg_surf = pygame.Surface((100, 200))
        # self.cursor_surf = self.game.assets['cursor_test']
        # self.cursor_rect = self.cursor_surf.get_frect()
        # self.talking = False
        # self.characters = {
        #     "aliza": {
        #         "surf": SurfaceButton(game, pygame.transform.scale_by(self.game.assets['alizafar'], 2), (800, 450)),
        #         "dialogue": self.game.dialogue_data['aliza']
        #     },
        #     "nate": {
        #         "surf": SurfaceButton(game, pygame.transform.scale_by(self.game.assets['natefar'], 2), (250, 425)),
        #         "dialogue": self.game.dialogue_data["nate"]
        #     },
        #     "paul": {
        #         "surf": SurfaceButton(game, pygame.transform.scale_by(self.game.assets['paulfar'], 3), (575, 450)),
        #         "dialogue": self.game.dialogue_data["paul"]
        #     }
        # }
        # self.dialogue_manager: DialogueManager = DialogueManager(self.game)

    def update(self):
        # Annotate variables
        # character_name: str
        # dialogue_data: dict
        # mpos: tuple

        # mpos = pygame.mouse.get_pos()

        # for character in self.characters:
        #     self.characters[character]['surf'].update(mpos)
        #     if self.characters[character]['surf'].get_mouse_press():
        #         self.talking = True
        #         character_name = character
        #         dialogue_data = self.characters[character]['dialogue']

        # if self.talking:
        #     self.start_dialogue(character_name, dialogue_data)
        #     self.talking = False
        pass

    def render(self, surf):
        for obj in self.scenemap:
             surf.blit(self.game.assets[obj['type']], (obj['pos'][0], obj['pos'][1]))

    # def start_dialogue(self, char_name:str, data:dict):
    #         result = self.dialogue_manager.select_interaction(data)
    
    #         if result is None:
    #             return 
            
    #         interaction_key, interaction_data = result
    #         dialogue_state = DialogueState(self.game, char_name, interaction_key, interaction_data)
    #         dialogue_state.enter_state()
        