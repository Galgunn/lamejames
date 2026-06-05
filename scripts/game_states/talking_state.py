import pygame
from scripts.state import State
from scripts.dialogue_system import DialogueSystem
from scripts.utils import FONT, DIALOGUE_BOX_POS, DIALOGUE_BOX_SIZE

CHARACTER_TALKING_POS: tuple = (650, 100)
CHARACTER_FONT_COLORS: dict = {
    'Aliza': (157, 232, 202),
    'Nate': (253, 121, 142),
    'Paul': (252, 209, 6),
    'Player': (255, 255, 255)
}

class TalkingState(State):
    def __init__(self, game, char_name:str, interaction_key:str, interaction_data:dict):
        super().__init__(game)

        # Annotate variables
        self.interaction_key: str
        self.interaction_data:dict
        self.dialogue_nodes: dict
        self.current_node: str
        self.speaker_name: str
        self.next_node: str
        self.lines: list
        self.flags: str
        self.text_color: tuple
        self.dialogue_box_rect: pygame.FRect
        self.character_surf: pygame.Surface
        self.dialogue_system: DialogueSystem
        self.speaker_name_surf: pygame.Font

        # Initializing variables
        self.interaction_key = interaction_key
        self.interaction_data = interaction_data
        self.dialogue_nodes = interaction_data.get('nodes', [])
        self.current_node = '0'
        self.speaker_name = ''
        self.next_node = ''
        self.lines = []
        self.flags = ''
        self.text_color = ()
        self.dialogue_box_rect = pygame.FRect(DIALOGUE_BOX_POS, DIALOGUE_BOX_SIZE)
        self.character_surf = pygame.transform.scale_by(self.game.assets[char_name + 'talk'], 1.5)
        self.dialogue_system = DialogueSystem(self.game, DIALOGUE_BOX_SIZE[0])

        # Loading dialogue data
        self.load_dialogue()
        self.dialogue_system.get_lines(self.lines, self.text_color)
        self.speaker_name_surf = FONT.render(self.speaker_name, True, self.text_color, (0, 0, 0))

        # pygame.mixer.music.load('assets/music/examiner.wav')
        # pygame.mixer.music.play(-1,0.0)

    def update(self):
        self.dialogue_system.update()

        if self.game.state_interaction_options['left_click']['just_pressed']:
            self.dialogue_system.advance()
            
            if self.dialogue_system.dialogue_complete:
            # pygame.mixer.music.stop()
                if self.next_node != "":
                    self.get_next_node()
                    self.dialogue_system.get_lines(self.lines, self.text_color)
                if self.next_node == "" and self.dialogue_system.dialogue_complete:
                    for flag in self.flags:
                        if flag != "":
                            self.game.flags.add(flag)
                    self.exit_state()

    def render(self, surf):
        self.prev_state.render(surf) # type: ignore error due to prev state being None
        self.dialogue_box_rect.topleft = DIALOGUE_BOX_POS
        surf.blit(self.character_surf, CHARACTER_TALKING_POS)
        surf.blit(self.speaker_name_surf, (self.dialogue_box_rect.x + 10, self.dialogue_box_rect.y - 25))
        pygame.draw.rect(surf, (0, 0, 0), self.dialogue_box_rect)
        self.dialogue_system.render(surf, (self.dialogue_box_rect.x + 10, self.dialogue_box_rect.y + 10))

    def load_dialogue(self):
        self.speaker_name = self.dialogue_nodes[self.current_node]['speaker']
        self.next_node = self.dialogue_nodes[self.current_node]['next_node']
        self.lines = self.dialogue_nodes[self.current_node]['lines']
        self.flags = self.interaction_data['flags']
        self.text_color = CHARACTER_FONT_COLORS[self.speaker_name]

    def get_next_node(self):
        self.current_node = self.next_node
        self.speaker_name = self.dialogue_nodes[self.current_node]['speaker']
        self.next_node = self.dialogue_nodes[self.current_node]['next_node']
        self.lines = self.dialogue_nodes[self.current_node]['lines']
        self.flags = self.interaction_data['flags']
        self.text_color = CHARACTER_FONT_COLORS[self.speaker_name]
        self.speaker_name_surf = FONT.render(self.speaker_name, True, self.text_color, (0, 0, 0))
    
    def get_flag(self):
        return self.flags