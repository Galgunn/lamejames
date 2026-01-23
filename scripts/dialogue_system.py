from scripts.utils import FONT
import pygame, json

BASE_JSON_PATH:str = 'assets/dialogue/dialogue_'

class DialogueSystem:
    def __init__(self, game, lines:list, wrap_length: int):
        '''
        Docstring for __init__
        
        :param game: The game.py file 
        :param lines: a list of str containing the dialogue lines
        :type lines: list
        :param special_lines: For testing. Trying to have special lines render in a different color
        :type special_lines: list
        :param wrap_length: A int value, most like the screen width, in which the text goes to a new line
        :type wrap_length: int

        The dialogue system that applies a type writer effect to any text we feed it. It's a wip to get it to do what we need it
        to do. 
        '''
        # Annotating variables
        self.dialogue_lines: list
        self.wrap_length: int
        self.font: pygame.Font
        self.snip:pygame.Surface
        self.counter: int
        self.speed: int
        self.line_done: bool
        self.current_line: int
        self.line: str
        self.dialogue_complete: bool

        # Initalizing variables
        self.game = game
        self.dialogue_lines = lines
        self.wrap_length = int(wrap_length)
        self.font = FONT
        self.snip = self.font.render('', True, (255, 255, 255))
        self.counter = 0
        self.speed = 3
        self.line_done = False
        self.current_line = 0
        self.line = self.dialogue_lines[self.current_line]
        self.dialogue_complete = False

    # def __init__(self, game, scene, character, wraplength):
    #     self.game = game
    #     self.scene = scene
    #     self.character = character
    #     self.scene_dialogue: list = [] # list of dicts
    #     self.index = 0
    #     self.id: str = ''
    #     self.next_id: str = ''
    #     self.speaker: str = ''
    #     self.dialogue_lines: list = []
    #     self.special_variables: str = ''
    #     self.load_json(BASE_JSON_PATH)
    #     self.wrap_length = int(wraplength)
    #     self.font = FONT
    #     self.snip = self.font.render('', True, (255, 255, 255))
    #     self.counter = 0
    #     self.speed = 3
    #     self.line_done = False
    #     self.current_line = 0
    #     self.line = self.dialogue_lines[self.current_line]
    #     self.dialogue_complete = False

    def update(self):
        '''
        Docstring for update
        
        Handles the typewriting effect by rendering letters of an entire line.
        - Splits a line list using a counter (need better understanding of this)
        - Displays a line instantly if the current line isn't complete
        - Proceeds to a next line if there is more than one dilogue line
        - Checks if dialogue is complete
        - Creates a surface object thats updates each letter (need better understanding of this)
        '''
        # Handles the type writer effect
        if self.counter < self.speed * len(self.line):
            self.counter += 1
        elif self.counter >= self.speed * len(self.line):
            self.line_done = True
        # Display line instantly if player click on screen
        if self.game.state_interaction_options['left_click']['just_pressed'] and not self.line_done:
            self.counter = self.speed * len(self.line)
        # Proceed to the next line if list has more than one line
        elif self.game.state_interaction_options['left_click']['just_pressed'] and self.line_done and self.current_line < len(self.dialogue_lines) - 1:
            self.current_line += 1
            self.line_done = False
            self.line = self.dialogue_lines[self.current_line]
            self.counter = 0
        
        # Checks if there is no more dialogue lines
        # elif self.current_line == len(self.dialogue_lines) - 1 and self.line_done:
            # self.dialogue_complete = True
        
        # Proceeds to the next id
        elif self.current_line == len(self.dialogue_lines) - 1 and self.line_done and self.special_variables != 'complete':
            pass
        
        # Checks for any special variables like 'complete'

        # Creates the surface object by rendering part of the current line by letters
        self.snip = self.font.render(self.line[0:self.counter//self.speed], True, 'white', None, self.wrap_length)

    def render(self, surf:pygame.Surface, text_starting_pos:tuple):
        '''
        Docstring for render
        
        :param surf: The surface object that the text is being rendered to
        :type surf: pygame.Surface
        :param text_starting_pos: Position of where the text starts to render
        :type text_starting_pos: tuple

        Renders the surface self.snip to the given surf arg
        '''
        surf.blit(self.snip, text_starting_pos)

    def reset(self):
        '''
        Docstring for reset
        
        Resets all the values for the following variables:
        - self.counter
        - self.line_done
        - self.current_line
        - self.line
        - self.dialogue_complete
        - self.snip
        '''
        self.counter = 0
        self.line_done = False
        self.current_line = 0
        self.line = self.dialogue_lines[self.current_line]
        self.dialogue_complete = False        
        self.snip = self.font.render('', True, (255, 255, 255))
    
    def load_json(self, path: str):
        f = open(path, 'r')
        dialogue_data = json.load(f)
        f.close()

    #     self.scene_dialogue = dialogue_data[self.scene, self.character + '_dialogue']
    #     self.id = dialogue_data[self.scene][self.character + '_dialogue'][self.index]['id']
    #     self.next_id = dialogue_data[self.scene][self.character + '_dialogue'][self.index]['next_id']
    #     self.speaker = dialogue_data[self.scene][self.character + '_dialogue'][self.index]['speaker']
    #     self.line = dialogue_data[self.scene][self.character + '_dialogue'][self.index]['lines']
    #     self.special_variables = dialogue_data[self.scene][self.character + '_dialogue'][self.index]['special_variables']

    # def get_nextline(self):
    #     self.index += 1
    #     self.id = self.scene_dialogue[self.index]['next_id']
    #     self.next_id = self.scene_dialogue[self.index]['next_id']
