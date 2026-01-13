from scripts.state import State
from scripts.utils import *
from scripts.menu_builder import MenuBuilder

pygame.init()

class PauseMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.pause_surf = pygame.Surface((SCREEN_SIZE[0] / 3, SCREEN_SIZE[1] / 3))
        self.pause_rect = self.pause_surf.get_frect(center = DISPLAY_CENTER)
        menu_options = ['Continue', 'Settings', 'Back to Main Menu']
        self.menu = MenuBuilder(game, menu_options, SCREEN_CENTER)

    def update(self):
        mpos = pygame.mouse.get_pos()
        # mpos = (mpos[0] / 2, mpos[1] / 2)
        self.menu.update(mpos)

        if self.menu.get_mouse_pressed('Continue') or self.menu.get_key_pressed():
            self.exit_state()
        if self.menu.get_mouse_pressed('Back to Main Menu'):
            self.prev_state.exit_state() # type: ignore
            self.exit_state()

    def render(self, surf):
        self.prev_state.render(surf) # type: ignore error due to prev_state being None
        self.pause_surf.fill('red')
        surf.blit(self.pause_surf, self.pause_rect)
        self.menu.render(surf)