#imports
import os
import sys
import math
import time
import random
import pygame
import modules.textureLoader as textureLoader

#logic and classes
blockKeys = ["stone", "dirt", "planks", "log"]
buttons = []

def initialize(player, screen, controller):
    global heart_full
    heart_full = textureLoader.LOAD_TEXTURE("assets/textures/UI/heart_full.png", 25, 25)
    global heart_half
    heart_half = textureLoader.LOAD_TEXTURE("assets/textures/UI/heart_half.png", 25, 25)
    global heart_empty
    heart_empty = textureLoader.LOAD_TEXTURE("assets/textures/UI/heart_empty.png", 25, 25)
    global death_screen
    death_screen = textureLoader.LOAD_TEXTURE("assets/textures/UI/death_screen.png", screen.get_size()[0], screen.get_size()[1])

    #various texts and buttons
    global death
    death = createText("You died!")
    global respawn_button
    global quit_button
    def respawn():
        player.respawn()
        respawn_button.visible = False
        quit_button.visible = False
        controller.SCORE_DIAMONDS = 0
        controller.start_time = time.time()
        controller.SCORE_KILLS = 0
    def save_and_quit():
        score = getHighScore()
        if controller.TOTAL_SCORE > int(score):
            SCORE_FILE = open(os.path.dirname(__file__) + "/../../../SCORE_DATA.txt", "w")
            SCORE_FILE.write(str(controller.TOTAL_SCORE))
            SCORE_FILE.close()
        sys.exit()
    respawn_button = Button(text="respawn", width=140, height=40, centered=True, x=screen.get_size()[0]/2-70, y=315, command=respawn, visible=False)
    quit_button = Button(text="save and quit", width=140, height=40, centered=True, x=screen.get_size()[0]/2-70, y=365, command=save_and_quit, visible=False)

def createText(text, size=32, color="#ffffff"):
    font = pygame.font.Font("assets/font/blockbuilder3D.ttf", size)
    return font.render(text, True, color)

#button class
class Button:
    def __init__(self, text="Button", command=False, width=70, height=30, color="#ffffff", color_clicked="#f0f0f0", text_color="#000000", x=20, y=20, centered=False, visible=True):
        #initialize
        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.color = color
        self.color_clicked = color_clicked
        self.text_color = text_color
        self.x = x
        self.y = y
        self.centered = centered
        self.clicked = False
        self.lastClicked = 0
        self.visible = visible
        buttons.append(self)
    def render(self, canvas):
        #render
        pygame.draw.rect(canvas, not self.clicked and self.color or self.color_clicked, [self.x, self.y, self.width, self.height])
        text = createText(self.text, 20, self.text_color)
        canvas.blit(text, (not self.centered and self.x or self.x+self.width/2-text.get_rect()[2]/2, not self.centered and self.y or self.y+self.height/2-text.get_rect()[3]/2, self.width, self.height))

        #update
        if pygame.time.get_ticks() - self.lastClicked >= 300:
            self.clicked = False
    def click(self):
        if self.command:
            self.command()
        self.clicked = True
        self.lastClicked = pygame.time.get_ticks()
    def checkClick(self, position):
        if (position[0] > self.x and position[0] < self.x+self.width and position[1] > self.y and position[1] < self.y+self.height):
            self.click()
    def delete(self):
        if self in buttons:
            buttons.remove(self)

def renderHearts(player, screen):
    for x in range(0, player.maxhealth):
        if math.ceil(player.health*2)/2-1 >= x:
            screen.blit(heart_full, (25*x,player.health <= 2 and random.randint(-2, 2)))
        elif math.ceil(player.health*2)/2-1 >= x-0.5:
            screen.blit(heart_half, (25*x,player.health <= 2 and random.randint(-2, 2)))
        else:
            screen.blit(heart_empty, (25*x,player.health <= 2 and random.randint(-2, 2)))

def renderDeathScreen(player, screen, controller):
    screen.blit(death_screen, (0, 0))
    screen.blit(death, (screen.get_size()[0]/2-death.get_rect().width/2, 100))
    respawn_button.visible = True
    quit_button.visible = True
    text1 = createText(text="Score: "+str(controller.TOTAL_SCORE), size=18)
    screen.blit(text1, (screen.get_size()[0]/2-text1.get_rect().width/2, 170))
    text2 = createText(text="Diamonds Collected: "+str(controller.SCORE_DIAMONDS)+" ("+str(controller.SCORE_DIAMONDS*2)+" points)", size=18)
    screen.blit(text2, (screen.get_size()[0]/2-text2.get_rect().width/2, 195))
    text3 = createText(text="Zombies Killed: "+str(controller.SCORE_KILLS)+" ("+str(controller.SCORE_KILLS*2)+" points)", size=18)
    screen.blit(text3, (screen.get_size()[0]/2-text3.get_rect().width/2, 220))
    text4 = createText(text="Time Survived: "+str(controller.SCORE_TIME*3)+" minutes ("+str(controller.SCORE_TIME)+" points)", size=18)
    screen.blit(text4, (screen.get_size()[0]/2-text4.get_rect().width/2, 245))
    text5 = createText(text="High Score: "+str(getHighScore()), size=18)
    screen.blit(text5, (screen.get_size()[0]/2-text5.get_rect().width/2, 270))

def update(player, screen, keys, controller):
    checkKeys(keys, controller)
    renderHearts(player, screen)
    renderSelection(controller, screen)
    if player.health == 0:
        renderDeathScreen(player, screen, controller)
    for button in buttons:
        button.visible and button.render(screen)

def checkButtons(position):
    for button in buttons:
        button.visible and button.checkClick(position)

def checkKeys(keys, controller):
    for block in blockKeys:
        if len(keys) > blockKeys.index(block) and keys[blockKeys.index(block)]:
            controller.selectedBlock = block

def renderSelection(controller, screen):
    text = createText(text="Selected block: "+controller.selectedBlock, size=16, color="black")
    screen.blit(text, (screen.get_size()[0]-180, 8))

def getHighScore():
    score = 0
    try:
        SCORE_FILE_READ = open(os.path.dirname(__file__) + "/../../../SCORE_DATA.txt", "r")
        score = int(SCORE_FILE_READ.read())
        SCORE_FILE_READ.close()
    except:
        "do nothing"
    return score
