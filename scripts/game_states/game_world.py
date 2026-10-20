import pygame
from scripts.state import State
from scripts.utils import SCREEN_CENTER, INTERACTABLE_ASSET_TYPES
from scripts.dialogue_manager import DialogueManager
from scripts.cursor import Cursor
from scripts.scenemap import Scenemap

pygame.init()

class GameWorld(State):
    def __init__(self, game):
        super().__init__(game)

        # Annotating and initializing variables
        self.game = game
        self.scenemap:Scenemap = Scenemap(self.game)
        self.cursor:Cursor = Cursor(game, pygame.mouse.get_pos(), self.game.assets['cursor_default'])
        self.dialogue_manager:DialogueManager

        self.scenemap.load('street')
        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos(SCREEN_CENTER)

    def update(self):
        # Annotating and initializing variables
        talking:bool = False
        mpos:tuple = pygame.mouse.get_pos()
        asset_rect:pygame.FRect
        asset_name:str = ''
        asset_dialogue:dict = {}

        self.cursor.update(self.scenemap, mpos)

        for asset in self.scenemap.get_assets_around(mpos):
            if asset['type'] in INTERACTABLE_ASSET_TYPES:
                asset_rect = pygame.FRect(asset['pos'], asset['size'])
                if asset_rect.collidepoint(mpos) and self.game.state_interaction_options['left_click']['just_pressed'] == True:
                    talking = True

        if talking:
            self.start_interaction(asset)
            talking = False

    def render(self, surf):
        self.scenemap.render(surf)
        self.cursor.render(surf)

    def start_interaction(self, asset):
        print(asset)
        # in here we pass the asset so that the text box state can get data such as surf, name, and dialogue 

        