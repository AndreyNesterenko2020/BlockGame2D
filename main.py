#imports
import os
import time
import json
import pygame
import modules.textureLoader as textureLoader
import modules.blockClass as blockClass
import modules.entityClass as entityClass
import modules.blockRenderer as blockRenderer
import modules.entityRenderer as entityRenderer
import modules.renderDistance as renderDistance
import modules.worldGeneration as worldGeneration
import modules.playerController as playerController
import modules.UI as UI

#version number
VERSION = "1.1.0"

#pygame setup
pygame.init()
size = [920, 600]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("BlockGame2D v"+VERSION)
pygame.display.set_icon(textureLoader.LOAD_TEXTURE("assets/textures/UI/icon.png"))

#variables
delta = 0
DEBUG = False

#create player entity and attach a controller
player = entityClass.Entity("player", 0, worldGeneration.getHeight(0)+2)
controller = playerController.Controller(player, screen)

#initialize UI
UI.initialize(player, screen, controller)

#create clock
clock = pygame.time.Clock()

#main loop
while True:
    #update player controller
    controller.update([pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT], pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT], pygame.mouse.get_pos()])
    controller.jump(pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE])
    
    #render game
    pygame.display.flip()
    screen.fill("#53d6ed")
    worldGeneration.UPDATE(player)
    renderDistance.UPDATE(player)
    blockRenderer.RENDER(player, renderDistance.LOADED_BLOCKS, screen)
    entityRenderer.RENDER(player, renderDistance.LOADED_ENTITIES, screen, DEBUG)
    entityClass.UPDATE(delta, renderDistance.LOADED_ENTITIES, renderDistance.LOADED_BLOCKS)

    #update UI
    UI.update(player, screen, [pygame.key.get_pressed()[pygame.K_1], pygame.key.get_pressed()[pygame.K_2], pygame.key.get_pressed()[pygame.K_3], pygame.key.get_pressed()[pygame.K_4]], controller)
        
    #system update
    delta = clock.tick(60)/1000
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            #LEFT MOUSE CONTROLLER UPDATE
            event.button == 1 and controller.LMB()
            #RIGHT MOUSE CONTROLLER UPDATE
            event.button == 3 and controller.RMB()
            #UI CLICK EVENT
            UI.checkButtons(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            #DEBUG OPTION
            if pygame.key.get_pressed()[pygame.K_SLASH]:
                DEBUG = not DEBUG
        if event.type == pygame.QUIT:
            pygame.quit()
