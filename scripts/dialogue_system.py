from scripts.utils import FONT
import pygame, json

class DialogueSystem:
    def __init__(self, game, lines:list, special_lines:list, wrap_length: int):
        self.game = game
        self.dialogue_lines:list = lines
        self.wrap_length:int = int(wrap_length)
        self.font:pygame.Font = FONT
        self.snip:pygame.Surface = self.font.render('', True, (255, 255, 255))
        self.counter:int = 0
        self.speed:int = 3
        self.line_done:bool = False
        self.current_line:int = 0
        self.line:str = self.dialogue_lines[self.current_line]
        self.dialogue_complete:bool = False

        # Testing
        self.special_lines:list = special_lines

    def update(self):
        # Handles the type writer effect
        if self.counter < self.speed * len(self.line):
            self.counter += 1
        elif self.counter >= self.speed * len(self.line):
            self.line_done = True
        # Display line instantly
        if self.game.state_interaction_options['left_click']['just_pressed'] and not self.line_done:
            self.counter = self.speed * len(self.line)
        # Proceed to the next line
        elif self.game.state_interaction_options['left_click']['just_pressed'] and self.line_done and self.current_line < len(self.dialogue_lines) - 1:
            self.current_line += 1
            self.line_done = False
            self.line = self.dialogue_lines[self.current_line]
            self.counter = 0
        elif self.current_line == len(self.dialogue_lines) - 1 and self.line_done:
            self.dialogue_complete = True

        self.snip = self.font.render(self.line[0:self.counter//self.speed], True, 'white', None, self.wrap_length)

    def render(self, surf, text_starting_pos:tuple):
        surf.blit(self.snip, text_starting_pos)

    def reset(self):
        self.counter = 0
        self.line_done = False
        self.current_line = 0
        self.line = self.dialogue_lines[self.current_line]
        self.dialogue_complete = False        
        self.snip = self.font.render('', True, (255, 255, 255))
