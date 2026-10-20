import pygame
from scripts.utils import SCREEN_SIZE
from scripts.state import State
from scripts.scrolling_text import ScrollingText
from scripts.dialogue_manager import DialogueManager

class Textbox(State):
    def __init__(self, game, asset:dict):
        super().__init__(game)
        # Annotate and initialize variables
        self.game = game
        self.asset_data = asset
        self.scrolling_text:ScrollingText = ScrollingText(self.game, SCREEN_SIZE)
        self.dialogue_manager:DialogueManager = DialogueManager(self.game)
