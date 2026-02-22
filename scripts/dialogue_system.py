from scripts.utils import FONT
import pygame, json

BASE_JSON_PATH:str = 'assets/dialogue/dialogue_'

class DialogueSystem:
    def __init__(self, game, wrap_length: int, speed: int = 3, text_color: tuple = (255, 255, 255)):
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
        self.text_color: tuple
        self.snip:pygame.Surface
        self.counter: int
        self.speed: int
        self.line_done: bool
        self.current_line: int
        self.dialogue_complete: bool

        # Initalizing variables
        self.game = game
        self.dialogue_lines = []
        self.wrap_length = int(wrap_length)
        self.font = FONT
        self.text_color = text_color
        self.snip = self.font.render('', True, self.text_color)
        self.counter = 0
        self.speed = speed
        self.line_done = False
        self.current_line = 0
        self.dialogue_complete = False

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
        # Declaring func variables
        line: str

        # Initializing variables
        line = self.dialogue_lines[self.current_line]
        
        # Handles the type writer effect
        if self.counter < self.speed * len(line):
            self.counter += 1
        elif self.counter >= self.speed * len(line):
            self.line_done = True
        # Display line instantly if player click on screen
        if self.game.state_interaction_options['left_click']['just_pressed'] and not self.line_done:
            self.counter = self.speed * len(line)
        # Proceed to the next line if list has more than one line
        elif self.game.state_interaction_options['left_click']['just_pressed'] and self.line_done and self.current_line < len(self.dialogue_lines) - 1:
            self.current_line += 1
            self.line_done = False
            line = self.dialogue_lines[self.current_line]
            self.counter = 0
        # Checks if there is no more dialogue lines
        if self.current_line == len(self.dialogue_lines) - 1 and self.line_done:
            self.dialogue_complete = True
        
        # Creates the surface object by rendering part of the current line by letters
        self.snip = self.font.render(line[0:self.counter//self.speed], True, self.text_color, None, self.wrap_length)

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
        self.dialogue_complete = False        
        self.snip = self.font.render('', True, self.text_color)
    
    def get_lines(self, lines, color):
        self.dialogue_lines = lines
        self.text_color = color
