import pygame, os

pygame.init()

# Annotate constants
SCREEN_SIZE: tuple
DISPLAY_SIZE : tuple
SCREEN_CENTER: tuple
DISPLAY_CENTER: tuple
FONT: pygame.Font
BASE_IMG_PATH: str

# Initialize constants
SCREEN_SIZE = (1000, 750)
DISPLAY_SIZE = (1000, 750)
DISPLAY_CENTER = (DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 2)
SCREEN_CENTER = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
FONT = pygame.font.SysFont('consolas', 20)
BASE_IMG_PATH = 'assets/images/'

def load_image(path:str, colorkey:tuple=(1, 1, 1)):
    '''
    Docstring for load_image
    
    :param path: name of the image file or path to the image file. Must include image file name
    :param colorkey: RGB value to set as transparent
    
    Loads a single image file and converts it into a pygame.Surface object

    Returns -> a pygame.Surface object
    '''
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey(colorkey)
    return img

def load_images(path:str, colorkey:tuple=(1, 1, 1)):
    '''
    Docstring for load_images
    
    :param path: name of the folder or path to the folder containing the image files
    :param colorkey: RGB value to set as transparent

    Takes a folder containing multiple image files and converts them into pygame.Surface objects
    - Format for the image files inside of the folder must be: 00.png 01.png 02.png
    - Useful for animation frames

    Returns -> a list containing the pygame.Surface objects
    '''
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, colorkey))
    return images