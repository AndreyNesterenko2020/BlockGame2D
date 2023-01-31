#imports
import pygame

#logic
def RENDER_BLOCK(player, block, display):
    display.blit(block.texture, (block.x*64+display.get_size()[0]/2-player.x*64-player.width*64/2, -block.y*64+display.get_size()[1]/2+player.y*64))

def RENDER(player, blocks, display):
    for x in blocks:
        RENDER_BLOCK(player, x, display)
