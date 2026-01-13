import pygame, os

pygame.init()

SCREEN_SIZE:tuple = (1000, 750)
DISPLAY_SIZE:tuple = (600, 600) # Half of screen size 
DISPLAY_CENTER:tuple = (DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 2)
SCREEN_CENTER:tuple = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
FONT:pygame.Font = pygame.font.SysFont('consolas', 20)
BASE_IMG_PATH:str = 'assets/images/'

def load_image(path, colorkey=(1, 1, 1)):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey(colorkey)
    return img

def load_images(path, colorkey=(0, 0, 0)):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, colorkey))
    return images