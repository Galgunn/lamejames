from scripts.state import State
from scripts.utils import *
from scripts.game_states.game_world import GameWorld
# from scripts.game_states.setting_menu import SettingMenu
# from scripts.game_states.credits_state import Credits 
from scripts.menu_builder import MenuBuilder
import pygame

pygame.init()

class MainMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu_text_options = ['Start', 'Settings', 'Credits', 'Editor', 'Exit']
        self.font_options = MenuBuilder(game, self.menu_text_options, SCREEN_CENTER)
        self.font_dict = self.font_options.font_dict

    def update(self):
        mpos = pygame.mouse.get_pos()
        self.font_options.update(mpos)
        if self.font_options.get_mouse_pressed('Start'):
            game_running_state = GameWorld(self.game)
            game_running_state.enter_state()
        if self.font_options.get_mouse_pressed('Settings'):
            # settings_menu_state = SettingMenu(self.game)
            # settings_menu_state.enter_state()
            pass
        if self.font_options.get_mouse_pressed('Credits'):
            # credits_state = Credits(self.game)
            # credits_state.enter_state()
            pass
        if self.font_options.get_mouse_pressed('Exit'):
            pass

    def render(self, surf):
        surf.fill(('green'))
        self.font_options.render(surf)