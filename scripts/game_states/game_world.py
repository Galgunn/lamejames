import pygame, json
from scripts.state import State
from scripts.utils import SCREEN_CENTER, SCREEN_SIZE
from scripts.button_builder import FontButton
from scripts.dialogue_manager import DialogueManager
from scripts.game_states.pause_state import PauseMenu
from scripts.game_states.dialogue_state import DialogueState, SceneState
from scripts.game_states.crime_scene_state import CrimeSceneState
from scripts.state_utils import *

BASE_JSON_PATH: str = 'assets/dialogue/'

pygame.init()

class GameWorld(State):
    def __init__(self, game):
        super().__init__(game)

        # Annotate variables
        self.bg_surf: pygame.Surface
        self.bg_rect: pygame.FRect
        self.natescale: int
        self.nateoriginscale: int
        self.enterdiag: int
        
        pygame.mouse.set_pos(SCREEN_CENTER)
        self.bg_surf:pygame.Surface = self.game.assets['background']
        self.bg_rect:pygame.FRect = self.bg_surf.get_frect(topleft = (0, 0))
        self.natescale = 2
        self.nateoriginscale = 2
       # self.nateoriginpos = (250,425)
        self.enterdiag = 0
        self.aliza_surf:pygame.Surface = pygame.transform.scale_by(self.game.assets['alizafar'], 2)
        self.aliza_rect:pygame.FRect = self.aliza_surf.get_frect(topleft= (800, 450))
        self.nate_surf:pygame.Surface = pygame.transform.scale_by(self.game.assets['natefar'], self.natescale)
        self.nate_rect:pygame.FRect = self.nate_surf.get_frect(topleft= (250, 425))
        self.paul_surf:pygame.Surface = pygame.transform.scale_by(self.game.assets['paulfar'], 3)
        self.paul_rect:pygame.FRect = self.paul_surf.get_frect(topleft= (575, 450))

        # Variables for dialogue transition 
        self.alpha_value:int = 255

        self.enter_house_button = FontButton(self.game, 'enter house', (100, 100))

        self.dialogue_manager: DialogueManager = DialogueManager(self.game)
        self.dialogue_data: dict = {
            'aliza': self.game.dialogue_data['aliza'],
            'nate': self.game.dialogue_data['nate'],
            'paul': self.game.dialogue_data['paul'],
            'street': self.game.dialogue_data['scenes']
        }

    def update(self):
        # Annotate variables
        # character_surf: pygame.Surface
        character_name: str

        if self.on_enter():
            self.start_scene('street', self.dialogue_data['street'])

        self.nate_surf:pygame.Surface = pygame.transform.scale_by(self.game.assets['natefar'], self.natescale)
        mpos = pygame.mouse.get_pos()
        if self.aliza_rect.collidepoint(mpos) and self.game.state_interaction_options['left_click']['just_pressed']:
            self.enterdiag = 1 
            character_surf = self.aliza_surf
            character_name = 'aliza'
        if self.nate_rect.collidepoint(mpos) and self.game.state_interaction_options['left_click']['just_pressed']:
            self.enterdiag = 1 
            character_surf = self.nate_surf
            character_name = 'nate'
        if self.paul_rect.collidepoint(mpos) and self.game.state_interaction_options['left_click']['just_pressed']:
            self.enterdiag = 1 
            character_surf = self.paul_surf
            character_name = 'paul'

        if self.enterdiag == 1:
            # interaction_id = self.get_aliza_interaction(self.game)
            # trigger_character_dialogue(self.game, character_name, interaction_id)
            # self.alpha_value = 255
            # character_surf.set_alpha(self.alpha_value)
            self.start_dialogue(character_name, self.dialogue_data[character_name])
            self.enterdiag = 0

        self.enter_house_button.update(mpos)
        if  self.enter_house_button.get_mouse_pressed():
            self.crime_scene_state = CrimeSceneState(self.game)
            self.crime_scene_state.enter_state()
            return

        # interactions = list(self.diag_counter.values())
        # for x in interactions:

        # if self.game.testing_keys['i']:
        #     self.inventory.append('cigarette')
        #     print('added cig to inventory')

        # if self.enterdiag == 1:   # sprite fly-in transition before dialogue
        #     self.natescale += 0.5
        #     self.nate_rect.x += 20
        #     self.nate_rect.y -= 20
        #     # if self.alpha_value <= 0:
        #     #     self.enterdiag = 0
        #     #     self.trigger_dialogue('nate', 'nate_test.json')
        #     #     self.alpha_value = 255

        #     if self.natescale >= 5 and self.nate_rect.x >= 250 and self.nate_rect.y <= 100:
        #         self.enterdiag = 0
        #         self.nate_surf.set_alpha(0)
        #         self.nate_rect.x = 250
        #         self.nate_rect.y = 425
        #         self.natescale = self.nateoriginscale
        #         self.trigger_dialogue('nate')

        if self.game.state_interaction_options['escape']['just_pressed']:
            pause_menu_state = PauseMenu(self.game)
            pause_menu_state.enter_state()
            return
        
        # if get_flag(self.game, 'street_intro_done') == False:
        #     self.start_scene(self.game, 'street')
        # if get_flag(self.game, 'house_intro_done') == True:
        #     self.start_scene(self.game, 'street')

    def render(self, surf):
        surf.blit(self.bg_surf, self.bg_rect)
        if get_flag(self.game, 'street_intro_done'):
            self.enter_house_button.render(surf)
            surf.blit(self.aliza_surf, self.aliza_rect)
            surf.blit(self.nate_surf, self.nate_rect)
            surf.blit(self.paul_surf, self.paul_rect)

    def on_enter(self):
        return True
    
    def on_exit(self):
        return True

    def trigger_dialogue_anim(self, character_surf:pygame.Surface, character_name:str):
        self.alpha_value -= 15
        character_surf.set_alpha(self.alpha_value)
        if self.alpha_value <= 0:
            self.trigger_dialogue(character_name)
            self.enterdiag = 0
    
    def get_aliza_interaction(self, game) -> int:
        if "aliza_intro_done" in game.flags:
            return 1
        return 0
    
    def get_scene_interaction(self, game):
        return 0
    
    def start_dialogue(self, char_name:str, data:dict):
        result = self.dialogue_manager.select_interaction(data)

        if result is None:
            return 
        
        interaction_key, interaction_data = result
        dialogue_state = DialogueState(self.game, char_name, interaction_key, interaction_data)
        dialogue_state.enter_state()

    def start_scene(self, scene:str, data:dict):
        result = self.dialogue_manager.select_scene_interaction(scene, data)

        if result is None:
            return 
        
        interaction_key, interaction_data = result
        dialogue_state = SceneState(self.game, interaction_key, interaction_data)
        dialogue_state.enter_state()
