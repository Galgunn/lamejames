import pygame, sys
from scripts.utils import *
from scripts.game_states.main_menu import MainMenu

pygame.init()

class Game:
    def __init__(self):
        '''
        Docstring for __init__
        
        Basic pygame setup. self.load_state() adds the main_menu state to the state_stack
        '''
        # Annotating variables
        self.screen: pygame.Surface
        self.display: pygame.Surface
        self.clock: pygame.Clock
        self.running: bool
        self.state_stack: list
        self.state_interaction_options: dict
        self.assets: dict      

        # Initializing variables
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.display = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state_stack = []

        self.state_interaction_options = {
            'escape': {'just_pressed': False},
            'left_click': {'just_pressed': False},
        }

        self.assets = {
            'background': load_image('salem.png'),
            'alizafar': load_image('alizafar.png'),
            'alizatalk': load_image('alizatalk.png'),
            'natefar': load_image('natefar.png'),
            'natetalk': load_image('natetalk.png'),
            'paulfar': load_image('paulfar.png'),
            'paultalk': load_image('paultalk.png'),
        }

        self.load_state()

    def run(self):
        '''
        Docstring for run
        
        A while loop that keeps on looping while the var self.running is True. 
        - Resets any state interaction options back to false
        - Runs the event handler for any pygame events
        - Calls update() and render() for state objects in the state stack

        '''
        while self.running:

            for key in self.state_interaction_options:
                self.state_interaction_options[key]['just_pressed'] = False

            self.event_handler()
            self.update()
            self.render()

    def update(self):
        '''
        Docstring for update
        
        Calls the update() fucntion for the last state object in the state stack
        '''
        self.state_stack[-1].update()

    def render(self):
        '''
        Docstring for render
        
        Calls the render() function for the last state object in the state stack
        - Passes the arg self.display to the state object render() function
        - Blits self.display to the window/screen
        - pygame.display.flip() updates the screen
        - self.clock.tick(60) sets the framerate to 60 fps
        '''
        self.state_stack[-1].render(self.display)
        self.screen.blit(self.display, (0, 0))
        pygame.display.flip()
        self.clock.tick(60)

    def load_state(self):
        '''
        Docstring for load_state
        
        Creates the main menu state object and adds it to the state stack
        '''
        self.game_state = MainMenu(self)
        self.state_stack.append(self.game_state)
    
    def reset_keys(self):
        '''
        Docstring for reset_keys
        
        Empty/placeholder function. Was originally supposed to reset any of the state_interaction_options values to False
        '''
        pass

    def event_handler(self):
        '''
        Docstring for event_handler
        
        The pygame event handler.
        - Checks for a quit event that closes the game when the player click on the x on the pygame window
        - Checks for a keydown and keyup event
        - Checks for a mousebuttondown event

        Has some unnecesary events that are not needed. I did take this from a previous project so thats why it's there
        :p
        '''
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.state_interaction_options['enter']['just_pressed'] = True
                    if event.key == pygame.K_ESCAPE:
                        self.state_interaction_options['escape']['just_pressed'] = True
                    if event.key == pygame.K_a:
                        self.movement['left'] = True
                    if event.key == pygame.K_d:
                        self.movement['right'] = True
                    if event.key == pygame.K_w:
                        self.movement['up'] = True
                    if event.key == pygame.K_s:
                        self.movement['down'] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement['left'] = False
                    if event.key == pygame.K_d:
                        self.movement['right'] = False
                    if event.key == pygame.K_w:
                        self.movement['up'] = False
                    if event.key == pygame.K_s:
                        self.movement['down'] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.state_interaction_options['left_click']['just_pressed'] = True

# Runs the game.py file as a script
if __name__ == '__main__':
    Game().run()