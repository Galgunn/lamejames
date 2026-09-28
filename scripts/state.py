import pygame
class State():
    def __init__(self, game):
        '''
        Docstring for __init__
        
        :param game: Passing game.py to have access to the event handler (for player input), and assets

        Initializer that initializes self.game and self.previous_state 
        '''
        self.game = game
        self.prev_state = None
        self.state_entered:bool = False
        self.state_exited:bool = False

    def update(self):
        '''
        Docstring for update
        
        Empty function. Here is where we want to check for any collisions, player input, variable changes, etc...
        '''
        self.state_entered = False
        self.state_exited = False

    def render(self, surf:pygame.Surface):
        '''
        Docstring for render
        
        :param surf: The pygame.Surface object that we are blitting to. In game.py this surface is self.display

        Empty function. Blits any pygame.Surface objects to self.display
        '''
        pass

    def on_enter(self):
        '''
        Docstring for on_enter
        
        Mostly an empty/placeholder function can be used to execute something right after enter_state() is called
        '''
        return self.state_entered
    
    def on_exit(self):
        '''
        Docstring for on_exit
        
        Mostly an empty/placeholder function can be used to excecute something right after exit_state() is called
        '''
        return self.state_exited

    def enter_state(self):
        '''
        Docstring for enter_state

        Adds the state class to the state stack list in game.py
        '''        
        if len(self.game.state_stack) >= 1:
            self.prev_state = self.game.state_stack[-1]
            self.prev_state.on_exit()
        self.game.state_stack.append(self)
        self.state_entered = True
        
    def exit_state(self):
        '''
        Docstring for exit_state
        
        Removes the state class from the state stack list in game.py
        '''
        self.state_exited = True
        self.game.state_stack.pop()

        if len(self.game.state_stack) >= 1:
            self.game.state_stack[-1].on_enter()