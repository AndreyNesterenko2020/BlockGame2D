#imports
import math
import random
import pygame
import modules.textureLoader as textureLoader

#logic and classes
blockKeys = ["stone", "dirt", "planks", "log"]
buttons = []

def initialize(player, screen):
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
    def respawn():
        player.respawn()
        respawn_button.visible = False
    respawn_button = Button(text="respawn", width=80, height=40, centered=True, x=screen.get_size()[0]/2-35, y=200, command=respawn, visible=False)

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

def renderDeathScreen(player, screen):
    screen.blit(death_screen, (0, 0))
    screen.blit(death, (screen.get_size()[0]/2-death.get_rect().width/2, 100))
    respawn_button.visible = True

def update(player, screen, keys, controller):
    checkKeys(keys, controller)
    renderHearts(player, screen)
    renderSelection(controller, screen)
    if player.health == 0:
        renderDeathScreen(player, screen)
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
