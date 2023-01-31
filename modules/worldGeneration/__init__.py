#imports
import math
import random
from modules.perlin_noise import perlin_noise
import modules.blockClass as blockClass
import modules.renderDistance as renderDistance
import modules.entityClass as entityClass

#logic
GENERATED_WORLD = []
noise = perlin_noise.PerlinNoise(octaves=3.5, seed=random.randint(-65536, 65536))

def column(x, height):
    blockClass.Block(x, height, "grass_block")
    blockClass.Block(x, height-1, "dirt")
    blockClass.Block(x, height-2, "dirt")
    blockClass.Block(x, height-3, "dirt")
    blockClass.Block(x, height-4, "dirt")
    blockClass.Block(x, height-5, "dirt")
    for y in range(3, height-5):
        blockClass.Block(x, y, "stone")
    blockClass.Block(x, 2, "lava")
    blockClass.Block(x, 1, "lava")
    blockClass.Block(x, 0, "barrier")

def getHeight(x):
    return math.floor(noise([x/75, 0])*25)+25

def UPDATE(player):
    for x in range(int(player.x)-renderDistance.BLOCK_DISTANCE, int(player.x)+renderDistance.BLOCK_DISTANCE):
        if not x in GENERATED_WORLD:
            column(x, getHeight(x))
            GENERATED_WORLD.append(x)
            if random.randint(1, 64) == 1:
                entityClass.Entity("cow", x, getHeight(x)+3)
