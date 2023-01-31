#imports
import os
import pygame

#logic
def LOAD_TEXTURE(path, width=False, height=False):
    image = pygame.image.load(os.path.exists(path) and path or "assets/textures/default.png").convert_alpha()
    if width and height:
        image = pygame.transform.scale(image, (width, height))
    return image
