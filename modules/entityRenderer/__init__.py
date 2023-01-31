#imports
import pygame

#logic
def RENDER_ENTITY(player, entity, display, debug=False):
    #render hitbox
    debug and pygame.draw.rect(display, "#ffffff", (entity.x*64+display.get_size()[0]/2-player.x*64-player.width*64/2, -entity.y*64+display.get_size()[1]/2+player.y*64, entity.width*64, entity.height*64), 3)

    #render body
    display.blit(entity.texture, (entity.x*64+display.get_size()[0]/2-player.x*64-player.width*64/2+entity.width*64/2-entity.texture.get_rect().width/2+entity.textureOffsetX*64, -entity.y*64+display.get_size()[1]/2+player.y*64+entity.height*64/2-entity.texture.get_rect().height/2-entity.textureOffsetY*64, entity.texture.get_rect().width, entity.texture.get_rect().height))

    #render head
    entity.head and not entity.hideHead and display.blit(entity.head, (entity.x*64+display.get_size()[0]/2-player.x*64-player.width*64/2+entity.width*64/2-entity.head.get_rect().width/2+entity.headOffsetX*64, -entity.y*64+display.get_size()[1]/2+player.y*64+entity.height*64/2-entity.head.get_rect().height/2-entity.headOffsetY*64, entity.head.get_rect().width, entity.head.get_rect().height))
def RENDER(player, entities, display, debug=False):
    for x in entities:
        RENDER_ENTITY(player, x, display, debug)
