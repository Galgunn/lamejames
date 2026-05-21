from scripts.state import State
from scripts.utils import *
from scripts.game_states.pause_state import PauseMenu
from scripts.game_states.dialogue_state import DescriptionState, SceneState
from scripts.button_builder import SurfaceButton, FontButton
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
        self.first_enter: bool = True

    def update(self):
        enter_diag:bool = False
        self.mpos = pygame.mouse.get_pos()
        self.on_background = True

        if self.first_enter:
            self.first_enter = False
            self.trigger_scene_dialogue('house', 0)

        for evidence in self.evidence_objs:
            self.evidence_objs[evidence]['obj'].update(self.mpos)
            if self.evidence_objs[evidence]['obj'].get_on_rect():
                self.on_background = False
            if self.evidence_objs[evidence]['obj'].get_mouse_press():
                enter_diag = True
                obj = evidence
                # Checking to see if it's the first time its getting interacted with
                if not self.evidence_objs[evidence]['interacted']:
                    # Update the counter
                    self.true_counter += 1
                # Setting to true so that we don't go into this loop 
                self.evidence_objs[evidence]['interacted'] = True

        if enter_diag:
            self.trigger_description_dialogue(obj)

        self.return_to_street_button.update(self.mpos)
        if self.return_to_street_button.get_mouse_pressed():
            self.exit_state()

######### Tried to make the return button to appear after player interacts with all the items
######### issue is that it resets the self.interacted_all_items each time 
        if self.true_counter == len(self.evidence_objs):
            self.interacted_all_items = True
                
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

        if not self.first_enter:
            self.return_to_street_button.render(surf)
            for evidence in self.evidence_objs:
                self.evidence_objs[evidence]['obj'].render(surf)
        if not self.on_background:
            surf.blit(self.cursor_surf, self.mpos)
    
    def trigger_description_dialogue(self, obj):
        description_state = DescriptionState(self.game, self.evidence_objs[obj]['desc'])
        description_state.enter_state()
        return
    
    def trigger_scene_dialogue(self, scene, interaction_id):
        self.dialogue_box = SceneState(self.game, 'dialogue_test.json', scene, interaction_id)
        self.dialogue_box.enter_state()
        return