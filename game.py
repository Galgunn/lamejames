import pygame, sys
from scripts.utils import *
from scripts.game_states.main_menu import MainMenu

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.clock = pygame.time.Clock()
        # self.display = pygame.Surface((DISPLAY_SIZE[0], DISPLAY_SIZE[1]))
        self.display = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]))
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
        while self.running:

            for key in self.state_interaction_options:
                self.state_interaction_options[key]['just_pressed'] = False

            self.event_handler()
            self.update()
            self.render()

    def update(self):
        self.state_stack[-1].update()

    def render(self):
        self.state_stack[-1].render(self.display)
        # self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        self.screen.blit(self.display, (0, 0))
        pygame.display.flip()
        self.clock.tick(60)

    def load_state(self):
        self.game_state = MainMenu(self)
        self.state_stack.append(self.game_state)
    
    def reset_keys(self):
        pass

    def event_handler(self):
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

if __name__ == '__main__':
    Game().run()