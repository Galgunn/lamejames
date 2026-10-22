import pygame
from scripts.utils import SCREEN_SIZE, TEXT_BOX_POS, FONT, TEXT_BOX_SIZE, CHARACTER_TALKING_POS
from scripts.state import State
from scripts.scrolling_text import ScrollingText
from scripts.cursor import Cursor
from scripts.scenemap import Scenemap

CHARACTER_FONT_COLORS:dict = {
    'Aliza': (157, 232, 202),
    'Nate': (253, 121, 142),
    'Paul': (252, 209, 6),
    'Player': (255, 255, 255)
}

class Textbox(State):
    def __init__(self, game, cursor:Cursor, asset:dict, interaction_key:str, interaction_data:dict):
        super().__init__(game)
        # Annotate and initialize variables
        self.game = game
        self.scenemap:Scenemap = Scenemap(self.game)
        self.cursor:Cursor = cursor
        self.asset:dict = asset
        self.interaction_key:str = interaction_key
        self.interaction_data:dict = interaction_data
        self.interaction_nodes:dict = self.interaction_data.get('nodes', [])
        self.current_node:str = '0'
        self.next_node:str = ''
        self.speaker_name:str = ''
        self.speaker_name_surf:pygame.Surface
        self.speaker_surf:pygame.Surface = pygame.transform.scale_by(self.game.assets['characters_talking'][self.asset['variant']], 1.5)
        self.lines:list = []
        self.flags:str = ''
        self.text_color:str = ''
        self.textbox_rect:pygame.FRect = pygame.FRect(TEXT_BOX_POS, TEXT_BOX_SIZE)
        self.scrolling_text:ScrollingText = ScrollingText(self.game, SCREEN_SIZE[0], 2)
        
        self.load_nodes()
        self.scrolling_text.get_lines(self.lines, self.text_color)

        print(self.asset)

    def update(self):
            mpos = pygame.mouse.get_pos()
            self.cursor.update(self.scenemap, mpos)
            self.scrolling_text.update()
    
            if self.game.state_interaction_options['left_click']['just_pressed']:
                self.scrolling_text.advance()
                
                if self.scrolling_text.dialogue_complete:
                # pygame.mixer.music.stop()
                    if self.next_node != "":
                        self.get_next_node()
                        self.scrolling_text.get_lines(self.lines, self.text_color)
                    if self.next_node == "" and self.scrolling_text.dialogue_complete:
                        for flag in self.flags:
                            if flag != "":
                                self.game.flags.add(flag)
                        self.exit_state()
    
    def render(self, surf):
        self.prev_state.render(surf) # type: ignore error due to prev state being None
        # self.dialogue_box_rect.topleft = (0, 600)
        surf.blit(self.speaker_surf, CHARACTER_TALKING_POS)
        surf.blit(self.speaker_name_surf, (self.textbox_rect.x + 10, self.textbox_rect.y - 25))
        pygame.draw.rect(surf, ('black'), self.textbox_rect)
        self.scrolling_text.render(surf, (self.textbox_rect.x + 10, self.textbox_rect.y + 10))
        self.cursor.render(surf)

    def load_nodes(self):
        self.speaker_name = self.interaction_nodes[self.current_node]['speaker']
        self.next_node = self.interaction_nodes[self.current_node]['next_node']
        self.lines = self.interaction_nodes[self.current_node]['lines']
        self.flags = self.interaction_data['flags']
        self.text_color = CHARACTER_FONT_COLORS[self.speaker_name]
        self.speaker_name_surf = FONT.render(self.speaker_name, True, self.text_color, (0, 0, 0))

    def get_next_node(self):
        self.current_node = self.next_node
        self.speaker_name = self.interaction_nodes[self.current_node]['speaker']
        self.next_node = self.interaction_nodes[self.current_node]['next_node']
        self.lines = self.interaction_nodes[self.current_node]['lines']
        self.flags = self.interaction_data['flags']
        self.text_color = CHARACTER_FONT_COLORS[self.speaker_name]
        self.speaker_name_surf = FONT.render(self.speaker_name, True, self.text_color, (0, 0, 0))
