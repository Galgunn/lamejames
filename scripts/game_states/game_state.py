import pygame
from scripts.state import State
from scripts.utils import SCREEN_CENTER, INTERACTABLE_ASSET_TYPES
from scripts.dialogue_manager import DialogueManager
from scripts.cursor import Cursor
from scripts.scenemap import Scenemap
from scripts.game_states.textbox_state import Textbox

class GameState(State):
    def __init__(self, game):
        super().__init__(game)

        # Annotating and initializing variables
        self.game = game
        self.scenemap:Scenemap = Scenemap(self.game)
        self.cursor:Cursor = Cursor(game, pygame.mouse.get_pos(), self.game.assets['cursor_default'])
        self.dialogue_manager:DialogueManager = DialogueManager(self.game)

        self.scenemap.load('street')
        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos(SCREEN_CENTER)

    def update(self):
        # Annotating and initializing variables
        talking:bool = False
        mpos:tuple = pygame.mouse.get_pos()
        asset_rect:pygame.FRect
        asset_dialogue:dict = {}
        interacting:bool = False

        self.cursor.update(self.scenemap, mpos)

        for asset in self.scenemap.get_assets_around(mpos):
            if asset['type'] in INTERACTABLE_ASSET_TYPES:
                asset_rect = pygame.FRect(asset['pos'], asset['size'])
                if asset_rect.collidepoint(mpos) and self.game.state_interaction_options['left_click']['just_pressed'] == True:
                    asset_dialogue = self.game.dialogue_data[asset['name']]
                    interacting = True

        if interacting:
            self.start_interaction(asset, asset_dialogue)
            interacting = False

    def render(self, surf):
        self.scenemap.render(surf)
        self.cursor.render(surf)

    def start_interaction(self, asset:dict, asset_dialogue:dict):
        # Annotating and initializing variable
        if asset['type'] == 'character_far':
            result:tuple = self.dialogue_manager.select_interaction(asset_dialogue)
            if result is None:
                    return 
            interaction_key = result[0]
            interaction_data = result[1]
            textbox_state = Textbox(self.game, self.cursor, asset, interaction_key, interaction_data)
        elif asset['type'] == 'evidence':
            interaction_key = asset_dialogue[asset['name']]
            textbox_state = Textbox(self.game, self.cursor, asset, )

        textbox_state.enter_state()