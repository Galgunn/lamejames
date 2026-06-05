import pygame, json
from scripts.state import State
from scripts.utils import *
from scripts.game_states.pause_state import PauseMenu
from scripts.game_states.dialogue_states import DescriptionState, SceneState
from scripts.button_builder import SurfaceButton, FontButton
from scripts.state_utils import trigger_description_dialogue, trigger_scene_dialogue, get_flag
from scripts.dialogue_manager import DialogueManager

pygame.init()

BASE_JSON_PATH: str = 'assets/dialogue/'

class CrimeSceneState(State):
    def __init__(self, game):
        super().__init__(game)
        # Declaring variables
        self.bg_surf: pygame.Surface
        self.bg_rect: pygame.FRect
        self.cursor_surf: pygame.Surface
        self.cursor_rect: pygame.FRect
        self.mpos: tuple
        self.interaction_obj_desc: list
        self.enter_diag: bool
        self.on_background: bool
        self.evidence_objs: dict

        # Initializing variables
        self.bg_surf = pygame.Surface((1000, 750)).convert_alpha()
        self.bg_surf.fill('brown')
        self.bg_rect = self.bg_surf.get_frect()
        self.cursor_surf = self.game.assets['cursor_test']
        self.mpos = pygame.mouse.get_pos()
        self.enter_diag = False
        self.on_background = True

        self.evidence_objs = {
            'test': {
                'obj': SurfaceButton(self.game, self.game.assets['test_surf'], (300, 300)),
                'desc': [
                    'Hopefully this works', 
                    'pls work'
                ],
                'interacted': False
            },
            'test1': {
                'obj': SurfaceButton(self.game, self.game.assets['test_surf'], (100, 100)),
                'desc': [
                    "This is another box",
                    "Tee hee ^o^"
                ],
                'interacted': False
            }
        }

        self.interacted_all_items = False
        self.true_counter = 0
        self.return_to_street_button: FontButton = FontButton(self.game, 'return to street', (900, 700))

        self.dialogue_manager: DialogueManager = DialogueManager(self.game)
        self.dialogue_data: dict = {
            "house": self.game.dialogue_data['scenes']
        }

    def update(self):
        # Annotate and initialize variables
        enter_diag:bool = False
        self.mpos = pygame.mouse.get_pos()
        self.on_background = True

        if self.on_enter():
            self.start_scene('house', self.dialogue_data['house'])

        # if get_flag(self.game, 'house_intro_done') == False:
        #     self.start_scene(self.game, 'house')

        for evidence in self.evidence_objs:
            self.evidence_objs[evidence]['obj'].update(self.mpos)
            if self.evidence_objs[evidence]['obj'].get_on_rect():
                self.on_background = False
            if self.evidence_objs[evidence]['obj'].get_mouse_press():
                enter_diag = True
                obj = evidence
                # # Checking to see if it's the first time its getting interacted with
                # if not self.evidence_objs[evidence]['interacted']:
                #     # Update the counter
                #     self.true_counter += 1
                # # Setting to true so that we don't go into this loop 
                # self.evidence_objs[evidence]['interacted'] = True

        if enter_diag:
            trigger_description_dialogue(self.game, self.evidence_objs[obj]['desc'])

        self.return_to_street_button.update(self.mpos)
        if self.return_to_street_button.get_mouse_pressed():
            self.exit_state()

######### Tried to make the return button to appear after player interacts with all the items
######### issue is that it resets the self.interacted_all_items each time 
        # if self.true_counter == len(self.evidence_objs):
        #     self.interacted_all_items = True
                
        # if self.interacted_all_items:        
        #     self.return_to_street_button.update(self.mpos)
        #     if self.return_to_street_button.get_mouse_pressed():
        #         self.exit_state()
    
    def render(self, surf):
        surf.blit(self.bg_surf, (0,0))
        pygame.mouse.set_visible(self.on_background)
        
        # Part of the condition to see the return button
        # if self.interacted_all_items:
        #     self.return_to_street_button.render(surf)

        if get_flag(self.game, 'house_intro_done'):
            self.return_to_street_button.render(surf)
            for evidence in self.evidence_objs:
                self.evidence_objs[evidence]['obj'].render(surf)
        if not self.on_background:
            surf.blit(self.cursor_surf, self.mpos)
    
    def get_scene_interaction(self, game):
        return 0
    
    # def start_dialogue(self, game, filepath, char_name):
    #     with open(filepath) as f:
    #         data = json.load(f)

    #     manager = DialogueManager(self.game)
    #     result = manager.select_interaction(data)

    #     if result is None:
    #         return 
        
    #     interaction_key, interaction_data = result

    #     dialogue_state = 

    def start_scene(self, scene:str, data:dict):
        result = self.dialogue_manager.select_scene_interaction(scene, data)

        if result is None:
            return 
        
        interaction_key, interaction_data = result
        dialogue_state = SceneState(self.game, interaction_key, interaction_data)
        dialogue_state.enter_state()

    # def on_exit(self):
    #     print('out')