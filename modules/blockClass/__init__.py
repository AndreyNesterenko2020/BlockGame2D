#imports
import json
import pygame
import modules.textureLoader as textureLoader

#class
BLOCKS = []
BLOCK_GRID = {}
BLOCK_TYPES = json.loads(open("types/block.json", "r").read())

def exists(x, y):
    if not x in BLOCK_GRID:
        BLOCK_GRID[x] = {}
    if y in BLOCK_GRID[x]:
        return BLOCK_GRID[x][y]
    if not y in BLOCK_GRID[x]:
        return False

class Hitbox(pygame.sprite.Sprite):
    def __init__(self, block):
        super().__init__()
        self.rect = pygame.Rect(block.x*100, -block.y*100, 100, 100)
        self.block = block

class Block:
    def __init__(self, x, y, blockType):
        self.x = x
        self.y = y
        self.type = blockType
        self.texture = textureLoader.LOAD_TEXTURE('assets/textures/block/'+self.type+'.png', 64, 64)
        self.collide = True
        self.breakable = True
        if self.type in BLOCK_TYPES:
            if "collide" in BLOCK_TYPES[self.type]:
                self.collide = BLOCK_TYPES[self.type]["collide"]
            if "breakable" in BLOCK_TYPES[self.type]:
                self.breakable = BLOCK_TYPES[self.type]["breakable"]
        self.hitbox = self.collide and Hitbox(self)
        if not exists(x, y):
            BLOCK_GRID[x][y] = self
        else:
            return
        BLOCKS.append(self)
    def delete(self):
        self in BLOCKS and BLOCKS.remove(self)
        BLOCK_GRID[self.x][self.y] = False
