'''
Not necessary anymore had to split it 
'''
import pygame
from scripts.state import State
from scripts.dialogue_system import DialogueSystem
from scripts.dialogue_manager import DialogueManager
from scripts.utils import SCREEN_SIZE, FONT

BASE_JSON_PATH:str = 'assets/dialogue/'
CHARACTER_TALKING_POS:tuple = (650, 100)
CHARACTER_FONT_COLORS:dict = {
    'Aliza': (157, 232, 202),
    'Nate': (253, 121, 142),
    'Paul': (252, 209, 6),
    'Player': (255, 255, 255)
}
DIALOGUE_BOX_SIZE:tuple = (SCREEN_SIZE[0], 200)
DIALOGUE_BOX_POS:tuple = (0, 600)
    
class DialogueState(State):
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
        self.text_color: str
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
        self.text_color = ''
        self.dialogue_box_rect = pygame.FRect(0, 0, SCREEN_SIZE[0], 200)
        self.character_surf = pygame.transform.scale_by(self.game.assets[char_name + 'talk'], 1.5)
        self.dialogue_system = DialogueSystem(self.game, self.dialogue_box_rect.width)

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
        self.dialogue_box_rect.topleft = (0, 600)
        surf.blit(self.character_surf, CHARACTER_TALKING_POS)
        surf.blit(self.speaker_name_surf, (self.dialogue_box_rect.x + 10, self.dialogue_box_rect.y - 25))
        pygame.draw.rect(surf, ('black'), self.dialogue_box_rect)
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
    
class DescriptionState(State):
    def __init__(self, game, interaction_key:str, interaction_data:dict):
        super().__init__(game)
        
        self.interaction_key: str
        self.interaction_data: dict
        self.dialogue_nodes: dict
        self.current_node: str
        self.next_node: str
        self.lines: list
        self.flags: str
        self.text_color: str
        self.dialogue_box_surf: pygame.Surface
        self.dialogue_box_rect: pygame.FRect
        self.dialogue_system: DialogueSystem

        self.interaction_key = interaction_key
        self.interaction_data = interaction_data
        self.dialogue_nodes = {}
        self.current_node = ''
        self.next_node = ''
        self.lines = []
        self.flags = ''
        self.text_color = CHARACTER_FONT_COLORS['Player']
        self.dialogue_box_surf = pygame.Surface(DIALOGUE_BOX_SIZE)
        self.dialogue_box_rect = self.dialogue_box_surf.get_frect(topleft= DIALOGUE_BOX_POS)
        self.dialogue_system = DialogueSystem(self.game, DIALOGUE_BOX_SIZE[0])

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
        self.prev_state.render(surf)
        surf.blit(self.dialogue_box_surf, self.dialogue_box_rect)
        self.dialogue_system.render(surf, (DIALOGUE_BOX_POS[0] + 10, DIALOGUE_BOX_POS[1] + 10))

    def load_dialogue(self):
        self.next_node = self.dialogue_nodes[self.current_node]['next_node']
        self.lines = self.dialogue_nodes[self.current_node]['lines']
        self.flags = self.interaction_data['flags']

    def get_next_node(self):
        self.current_node = self.next_node
        self.speaker_name = self.dialogue_nodes[self.current_node]['speaker']
        self.next_node = self.dialogue_nodes[self.current_node]['next_node']
        self.lines = self.dialogue_nodes[self.current_node]['lines']
        self.flags = self.interaction_data['flags']
        self.speaker_name_surf = FONT.render(self.speaker_name, True, self.text_color, (0, 0, 0))
    
    def get_flag(self):
        return self.flags

# class SceneState(State):
#     def __init__(self, game, filename, scene, interaction_id):
#         super().__init__(game)

#         # Annotate variables
#         self.lines: list
#         self.json_filename: str
#         self.dialogue_data: dict
#         self.scene: str
#         self.speaker_name: str
#         self.current_id: str
#         self.next_id: str
#         self.lines: list
#         self.flags: str
#         self.text_color: tuple
#         self.dialogue_box_rect: pygame.FRect
#         self.dialogue_system: DialogueSystem
#         self.speaker_name_surf = pygame.Surface

#         # Initializing variables
#         self.lines = []
#         self.json_filename = filename
#         self.dialogue_data = {}
#         self.scene = scene
#         self.speaker_name = ''
#         self.current_id = '0'
#         self.next_id = ''
#         self.lines = []
#         self.flags = ''
#         self.text_color = (255, 255, 255)
#         self.dialogue_box_rect = pygame.FRect(0, 0, SCREEN_SIZE[0], 200)
#         self.dialogue_system = DialogueSystem(self.game, self.dialogue_box_rect.width)

#         self.load(BASE_JSON_PATH + self.json_filename, scene, interaction_id)
#         self.dialogue_system.get_lines(self.lines, self.text_color)
    
#     def update(self):
#         self.dialogue_system.update()

#         if self.game.state_interaction_options['left_click']['just_pressed']:
#             self.dialogue_system.advance()
            
#             if self.dialogue_system.dialogue_complete:
#             # pygame.mixer.music.stop()
#                 if self.next_id != "":
#                     self.get_next_id()
#                     self.dialogue_system.get_lines(self.lines, self.text_color)
#                 if self.next_id == "" and self.dialogue_system.dialogue_complete:
#                     for flag in self.flags:
#                         if flag != "":
#                             self.game.flags.add(flag)
#                     self.exit_state()

#     def load(self, path:str, scene:str, interaction_id:int):
#         f = open(path, 'r')
#         self.dialogue_json = json.load(f)
#         f.close()

#         self.dialogue_data = self.dialogue_json[scene][scene + '_' +str(interaction_id)]
#         self.speaker_name = self.dialogue_data[self.current_id]['speaker']
#         self.next_id = self.dialogue_data[self.current_id]['next_id']
#         self.lines = self.dialogue_data[self.current_id]['lines']
#         self.flags = self.dialogue_data['flags']
#         if self.speaker_name == "":
#             self.text_color = (255, 255, 255)
#         else:
#             self.text_color = CHARACTER_FONT_COLORS[self.speaker_name]

#     def get_next_id(self):
#         self.current_id = self.next_id
#         self.speaker_name = self.dialogue_data[self.current_id]['speaker']
#         self.next_id = self.dialogue_data[self.current_id]['next_id']
#         self.lines = self.dialogue_data[self.current_id]['lines']
#         self.flags = self.dialogue_data['flags']
#         if self.speaker_name == "":
#             self.text_color = (255, 255, 255)
#         else: 
#             self.text_color = CHARACTER_FONT_COLORS[self.speaker_name]
#             self.speaker_name_surf = FONT.render(self.speaker_name, True, self.text_color, (0, 0, 0))

#     def render(self, surf):
#         # self.prev_state.render(surf) # type: ignore error due to prev state being None
#         self.dialogue_box_rect.topleft = (0, 600)
#         if self.speaker_name != "":
#             surf.blit(self.speaker_name_surf, (self.dialogue_box_rect.x + 10, self.dialogue_box_rect.y - 25))
#         pygame.draw.rect(surf, ('black'), self.dialogue_box_rect)
#         self.dialogue_system.render(surf, (self.dialogue_box_rect.x + 10, self.dialogue_box_rect.y + 10))

class SceneState(State):
    def __init__(self, game, interaction_key:str, interaction_data:dict):
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
        self.text_color: str
        self.dialogue_box_rect: pygame.FRect
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
        self.text_color = ''
        self.dialogue_box_rect = pygame.FRect(0, 0, SCREEN_SIZE[0], 200)
        self.dialogue_system = DialogueSystem(self.game, self.dialogue_box_rect.width)

        # Loading interaction data
        self.load_dialogue()

        # Get dialogue data
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
                        self.game.used_interactions.add(self.interaction_key)
                    self.exit_state()

    def render(self, surf):
        # self.prev_state.render(surf) # type: ignore error due to prev state being None
        self.dialogue_box_rect.topleft = (0, 600)
        if self.speaker_name != "":
            surf.blit(self.speaker_name_surf, (self.dialogue_box_rect.x + 10, self.dialogue_box_rect.y - 25))
        pygame.draw.rect(surf, ('black'), self.dialogue_box_rect)
        self.dialogue_system.render(surf, (self.dialogue_box_rect.x + 10, self.dialogue_box_rect.y + 10))

    def load_dialogue(self):
        self.speaker_name = self.dialogue_nodes[self.current_node]['speaker']
        self.next_node = self.dialogue_nodes[self.current_node]['next_node']
        self.lines = self.dialogue_nodes[self.current_node]['lines']
        self.flags = self.interaction_data['flags']
        if self.speaker_name == "":
            self.text_color = (255, 255, 255)
        else: 
            self.text_color = CHARACTER_FONT_COLORS[self.speaker_name]
            self.speaker_name_surf = FONT.render(self.speaker_name, True, self.text_color, (0, 0, 0))

    def get_next_node(self):
        self.current_node = self.next_node
        self.speaker_name = self.dialogue_nodes[self.current_node]['speaker']
        self.next_node = self.dialogue_nodes[self.current_node]['next_node']
        self.lines = self.dialogue_nodes[self.current_node]['lines']
        self.flags = self.interaction_data['flags']
        if self.speaker_name == "":
            self.text_color = (255, 255, 255)
        else: 
            self.text_color = CHARACTER_FONT_COLORS[self.speaker_name]
            self.speaker_name_surf = FONT.render(self.speaker_name, True, self.text_color, (0, 0, 0))
    
    def get_flag(self):
        return self.flags