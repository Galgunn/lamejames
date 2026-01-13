class State():
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def update(self):
        pass

    def render(self, surf):
        pass

    def on_enter(self):
        pass
    
    def on_exit(self):
        pass

    def enter_state(self):
        if len(self.game.state_stack) >= 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)
        self.on_enter() # Sometimes this does nothing only usefull for dialogue state
        
    def exit_state(self):
        self.game.state_stack.pop()
        self.on_exit() # Same as the on_enter() func