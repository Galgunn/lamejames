from scripts.utils import *
class MenuBuilder():
    def __init__(self, game, text_options:list, starting_pos:tuple=DISPLAY_CENTER, orientation:str='portrait') -> None:
        '''
        Docstring for __init__
        
        :param text_options: a list of strings with the options a player can choose
        :type text_options: list
        :param starting_pos: the position where the meno options be placed
        :type starting_pos: tuple
        :param orientation: Used to render the menu options in either orientation
        :type orientation: str
        
        Creates a menu with options that have a small highlight when the cursor is over it
        - Requires a list of strings that creates font objects of the stings
        - Created to make menu options "buttons"
        NOTE: orientation argument does not work
        '''
        # Annotate variables
        self.text_options: list
        self.font: pygame.Font
        self.starting_pos: tuple
        self.font_dict: dict
        self.orientation = str

        # Initialize variables
        self.game = game
        self.text_options = text_options
        self.font = FONT
        self.starting_pos = starting_pos
        self.font_dict = {}
        self.orientation = orientation
        self.init_fonts()

    def init_fonts(self):
        '''
        Docstring for init_fonts
        
        Creates a dict of font objects with the following keys:
        - text
        - highlight
        - rect
        - on_font
        '''
        
        pos = self.starting_pos
        for option in self.text_options:
            font_surf = self.font.render(option, True, 'black')
            font_highlight_surf = self.font.render(option, True, 'white')
            font_rect = font_surf.get_frect(center = pos)
            self.font_dict[option] = {'text': font_surf, 'highlight': font_highlight_surf, 'rect': font_rect, 'on_font': False}
            if self.orientation == 'portrait':
                pos = (pos[0], pos[1] + 25)
            if self.orientation == 'landscape':
                pos = (pos[0] + 50, pos[1])

    def update(self, mpos:tuple):
        '''
        Docstring for update
        
        :param mpos: position of the mouse cursor
        :type mpos: tuple

        Check for collision with any of the font rects and add a small with highlight if there is
        '''
        for option in self.font_dict:
            self.font_dict[option]['on_font'] = False
            if self.font_dict[option]['rect'].collidepoint(mpos):
                self.font_dict[option]['on_font'] = True

    def get_mouse_pressed(self, text_option:str) -> bool:
        '''
        Docstring for get_mouse_pressed
        
        :param text_option: the menu option that is also the dict key
        :type text_option: str
        :return: Either True or False if the mouse clicked on the option
        :rtype: bool

        Used to see if a menu option was clicked 
        '''
        if self.game.state_interaction_options['left_click']['just_pressed'] and self.font_dict[text_option]['on_font']:
            return True
        return False
    
    def get_key_pressed(self) -> bool:
        '''
        Docstring for get_key_pressed
        
        :return: Either True or False if a key was pressed
        :rtype: bool

        Used to see if a key was pressed 
        '''
        if self.game.state_interaction_options['escape']['just_pressed']:
            return True
        return False
    
    def get_font_dict(self):
        return self.font_dict
    
    def render(self, surf):
        '''
        Docstring for render
        
        :param surf: The pygame.Surface object that this is being rendered to

        Renders all the menu options and if a cursor is on the options rect it adds a white highlight
        '''
        for option in self.font_dict:
            if self.font_dict[option]['on_font']:
                surf.blit(self.font_dict[option]['highlight'], (self.font_dict[option]['rect'].x + 1, self.font_dict[option]['rect'].y + 1))
            surf.blit(self.font_dict[option]['text'], self.font_dict[option]['rect'])

class SurfaceButton():
    def __init__(self, game, surf:pygame.Surface, pos:tuple):
        self.game = game
        self.surf = surf
        self.rect = self.surf.get_frect(topleft= pos)
        self.pos = pos
        self.on_rect = False

    def update(self, mpos:tuple):
        self.on_rect = False
        if self.rect.collidepoint(mpos):
            self.on_rect = True

    def get_mouse_press(self):
        if self.game.state_interaction_options['left_click']['just_pressed'] and self.on_rect:
            return True
        return False
    
    def get_on_rect(self):
        return self.on_rect

    def render(self, surf):
        surf.blit(self.surf, self.rect)

class FontButton():
    def __init__(self, game, text:str, pos:tuple):
        # Annotate variables
        self.text: str
        self.pos: tuple
        self.font: pygame.Font
        self.font_dict: dict


        # Initialize variables
        self.game = game
        self.text = text
        self.pos = pos
        self.font = FONT
        self.font_dict = {}
        self.init_font()

    def init_font(self):
        font_surf = self.font.render(self.text, True, (0, 0, 0))
        highlight_surf = self.font.render(self.text, True, (255, 255, 255))
        font_rect = font_surf.get_frect(center = self.pos)

        self.font_dict[self.text] = {
            'text': font_surf,
            'highlight': highlight_surf,
            'rect': font_rect,
            'on_font': False
        }
    
    def update(self, mpos):
        self.font_dict[self.text]['on_font'] = False
        if self.font_dict[self.text]['rect'].collidepoint(mpos):
            self.font_dict[self.text]['on_font'] = True

    def render(self, surf):
        if self.font_dict[self.text]['on_font']:
            surf.blit(self.font_dict[self.text]['highlight'], (self.font_dict[self.text]['rect'].x + 1, self.font_dict[self.text]['rect'].y + 1))
        surf.blit(self.font_dict[self.text]['text'], self.font_dict[self.text]['rect'])

    def get_mouse_pressed(self):
        if self.game.state_interaction_options['left_click']['just_pressed'] and self.font_dict[self.text]['on_font']:
            return True
        return False
    
