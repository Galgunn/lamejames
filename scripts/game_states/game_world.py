import pygame
from scripts.state import State
from scripts.utils import SCREEN_CENTER, SCREEN_SIZE
from scripts.button_builder import FontButton, SurfaceButton
from scripts.dialogue_manager import DialogueManager
from scripts.game_states.talking_state import TalkingState
from scripts.game_states.dialogue_states import DialogueState
from scripts.game_states.scene_state import SceneState
from scripts.cursor import Cursor
from scripts.scenemap import Scenemap

pygame.init()

class GameWorld(State):
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
        self.game = game
        self.scenemap: list # a list of dicts containing data like surfaces (i.e. background and characters), and rects
        self.scene_map = Scenemap(self.game)
        self.scene_map.load('street')
        self.cursor = Cursor(game, pygame.mouse.get_pos(), self.game.assets['cursor_default'])

        # Initializing variables
        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos(SCREEN_CENTER)

    def update(self):
        mpos = pygame.mouse.get_pos()
        self.cursor.update(self.scene_map, mpos)

    def render(self, surf):
        self.scene_map.render(surf)
        self.cursor.render(surf)

        