from scripts.state import State
from scripts.utils import SCREEN_CENTER, SCREEN_SIZE
from scripts.button_builder import FontButton
from scripts.game_states.pause_state import PauseMenu
from scripts.game_states.dialogue_state import DialogueState, SceneState
from scripts.game_states.crime_scene_state import CrimeSceneState
import pygame

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
        self.aliza_surf: pygame.Surface
        self.aliza_rect: pygame.FRect
        self.nate_surf: pygame.Surface
        self.nate_rect: pygame.FRect
        self.paul_surf: pygame.Surface
        self.paul_rect: pygame.FRect
        self.dialogue_box = DialogueState
        
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
        self.dialogue_box = DialogueState(self.game, 'aliza', 'aliza_test.json', 0)

        # Variables for dialogue transition 
        self.alpha_value:int = 255

        self.diag_counter: dict = {
            'aliza': {
                'counter': 0,
            },
            'nate': {
                'counter': 0,
            },
            'paul': {
                'counter': 0,
            },
            'dialogue': {
                'counter': 0,
            }
        }

        self.enter_house_button = FontButton(self.game, 'enter house', (100, 100))
        self.introduction:bool = False

    def update(self):
        # Annotate variables
        character_surf: pygame.Surface
        character_name: str

        # test = "ya"
        # if test:
        #     print('yep a non empty string is true')
        # elif test == 'ya':
        #     print('yep comparing would also be true')

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
            self.trigger_dialogue(character_name, self.diag_counter[character_name]['counter'])
            self.alpha_value = 255
            character_surf.set_alpha(self.alpha_value)
            if self.dialogue_box.get_flag():
                self.enterdiag = 0
            else:
                self.diag_counter[character_name]['counter'] += 1
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
                
        # if mpos[0] >= int(SCREEN_CENTER[0] + 400): # moving right
        #     self.bg_rect.x -= 2
        #     if self.bg_rect.right <= SCREEN_SIZE[0]:
        #         self.bg_rect.right = SCREEN_SIZE[0]
        # elif mpos[0] <= int(SCREEN_CENTER[0] - 400): # moving left
        #     self.bg_rect.x += 2
        #     if self.bg_rect.left >= 0:
        #         self.bg_rect.left = 0

        if self.game.state_interaction_options['escape']['just_pressed']:
            pause_menu_state = PauseMenu(self.game)
            pause_menu_state.enter_state()
            return

        if not self.introduction:
            self.introduction = True
            self.trigger_scene_dialogue('street', 0)

    def render(self, surf):
        surf.blit(self.bg_surf, self.bg_rect)
        if self.introduction:
            self.enter_house_button.render(surf)
            surf.blit(self.aliza_surf, self.aliza_rect)
            surf.blit(self.nate_surf, self.nate_rect)
            surf.blit(self.paul_surf, self.paul_rect)

    def trigger_dialogue_anim(self, character_surf:pygame.Surface, character_name:str):
        self.alpha_value -= 15
        character_surf.set_alpha(self.alpha_value)
        if self.alpha_value <= 0:
            self.trigger_dialogue(character_name)
            self.enterdiag = 0

    def trigger_dialogue(self, character_name:str, interaction_id:int):
        self.dialogue_box = DialogueState(self.game, character_name, character_name + '_test.json', interaction_id)
        self.dialogue_box.enter_state()
        return

    def trigger_scene_dialogue(self, scene, interaction_id):
        self.dialogue_box = SceneState(self.game, 'dialogue_test.json', scene, interaction_id)
        self.dialogue_box.enter_state()
        return
