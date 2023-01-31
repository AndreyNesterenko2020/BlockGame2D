#imports
import modules.blockClass as blockClass
import modules.entityClass as entityClass

#logic
LOADED_BLOCKS = []
LOADED_ENTITIES = []
BLOCK_DISTANCE = 20
ENTITY_DISTANCE = 15

def check_blocks(player):
    blocks = []
    for y in range(0, 128):
        for x in range(int(player.x)-BLOCK_DISTANCE, int(player.x)+BLOCK_DISTANCE):
            block = blockClass.exists(x, y)
            if block:
                blocks.append(block)
    return blocks

def check_entities(player):
    entities = []
    for entity in entityClass.ENTITIES:
        if entity.x > int(player.x)-ENTITY_DISTANCE and entity.x < int(player.x)+ENTITY_DISTANCE:
            entities.append(entity)
    return entities

def UPDATE(player):
    #BLOCKS
    global LOADED_BLOCKS
    LOADED_BLOCKS = check_blocks(player)
    #ENTITIES
    global LOADED_ENTITIES
    LOADED_ENTITIES = check_entities(player)
