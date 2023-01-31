#imports
import math
import json
import pygame
import importlib
import modules.textureLoader as textureLoader
import modules.blockClass as blockClass

#class
ENTITIES = []
ENTITY_TYPES = json.loads(open("types/entity.json", "r").read())
GRAVITY = -9.8
ticks = 0

def getAI(type_):
    e = False
    try:
        e = importlib.import_module("entityAI."+type_)
    except:
        "nothing here..."
    return e

def collide(entity, blocks):
    collisions = []
    for block in blocks:
        if block.hitbox and entity.hitbox.rect.colliderect(block.hitbox.rect):
            collisions.append(block)
    return collisions

def rot_center(image, rect, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

def UPDATE(delta, entities=ENTITIES, blocks=blockClass.BLOCKS):
    #ticks
    global ticks
    ticks += 1

    #update entities
    for entity in entities:
        #health
        if entity.health > entity.maxhealth:
            entity.health = entity.maxhealth
        if entity.health < 0:
            entity.health = 0
        if entity.health == 0 and not entity.AI:
            entity.delete()
        
        #rotation
        entity.head = entity.basehead and pygame.transform.flip(entity.basehead and rot_center(entity.basehead, entity.basehead.get_rect(), entity.rotation)[0], entity.flipped, False)
            
        #animation
        if entity.animation and entity.animation in ENTITY_TYPES[entity.type]["animations"]:
            if ENTITY_TYPES[entity.type]["animations"][entity.animation]["frames"] < entity.animationFrame:
                entity.animationFrame = 1
                #only reset animation thay plays once when entity is alive
                if ENTITY_TYPES[entity.type]["animations"][entity.animation]["once"]:
                    if entity.health > 0:
                        entity.animation = None
                    else:
                        entity.animationFrame = ENTITY_TYPES[entity.type]["animations"][entity.animation]["frames"]
                    return
            entity.texture = pygame.transform.flip(textureLoader.LOAD_TEXTURE("assets/textures/entity/"+entity.type+"/"+entity.animation+"/"+str(entity.animationFrame)+".png", entity.texture.get_rect().width, entity.texture.get_rect().height), entity.flipped, False)
            entity.textureflipped = False
            if ticks - entity.lastFrame >= ENTITY_TYPES[entity.type]["animations"][entity.animation]["frameduration"]:
                entity.animationFrame += 1
                entity.lastFrame = ticks
        else:
            entity.texture = pygame.transform.flip(entity.basetexture, entity.flipped, False)
            entity.textureflipped = False
        
        #gravity
        entity.calculateGravity(delta)
        
        #movement
        if entity.left and entity.health > 0:
            entity.velx = -entity.speed
        if entity.right and entity.health > 0:
            entity.velx = entity.speed
        
        #x velocity and hitbox update
        entity.x += entity.velx*delta
        entity.updateHitbox()

        #x collisions
        block_hit_list = collide(entity, blocks)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if entity.velx > 0:
                try:
                    entity.health > 0 and entity.AI.onCollidePosX(entity)
                except:
                    "nothing here..."
                entity.x = block.x-entity.width
            elif entity.velx < 0:
                try:
                    entity.health > 0 and entity.AI.onCollideNegX(entity)
                except:
                    "nothing here..."
                # Otherwise if we are moving left, do the opposite.
                entity.x = block.x+1
        
        #y velocity and hitbox update
        entity.y += entity.vely*delta
        entity.updateHitbox()

        #y collisions
        block_hit_list = collide(entity, blocks)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if entity.vely > 0:
                try:
                    entity.health > 0 and entity.AI.onCollidePosY(entity)
                except:
                    "nothing here..."
                entity.y = block.y-1
                entity.jumping = False
            elif entity.vely < 0:
                try:
                    entity.health > 0 and entity.AI.onCollideNegY(entity)
                except:
                    "nothing here..."
                entity.y = block.y+entity.height
 
            # Stop our vertical movement
            entity.vely = 0

        #jumping
        if entity.jumping and entity.vely < entity.jumpVel and entity.health > 0:
            entity.vely += 60*delta
        else:
            if entity.jumping:
                entity.vely -= 1
            entity.jumping = False

        #events
        if entity.AI and entity.health > 0:
            try:
                entity.AI.tick(entity)
            except:
                "nothing here..."
            if not entity.createEventFired:
                try:
                    entity.AI.onspawn(entity)
                except:
                    "nothing here..."
                entity.createEventFired = True

class Hitbox(pygame.sprite.Sprite):
    def __init__(self, entity):
        super().__init__()
        self.rect = pygame.Rect(math.floor(entity.x*100), math.floor(-entity.y*100), math.floor(entity.width*100), math.floor(entity.height*100))

class Entity:
    def __init__(self, entityType, x=0, y=0, AI=True):
        if not entityType in ENTITY_TYPES:
            return
        self.x = x
        self.y = y
        self.rotation = 0
        self.type = entityType
        self.maxhealth = ENTITY_TYPES[entityType]['health']
        self.health = self.maxhealth
        self.damage = ENTITY_TYPES[entityType]['damage']
        self.speed = ENTITY_TYPES[entityType]['speed']
        self.jumpVel = ENTITY_TYPES[entityType]['jumpVel']
        self.reach = ENTITY_TYPES[entityType]['reach']
        self.width = ENTITY_TYPES[entityType]['hitbox']['x']
        self.height = ENTITY_TYPES[entityType]['hitbox']['y']
        self.basetexture = textureLoader.LOAD_TEXTURE("assets/textures/entity/"+self.type+"/main.png", ENTITY_TYPES[entityType]['texture']['size']['x']*64, ENTITY_TYPES[entityType]['texture']['size']['y']*64)
        self.texture = self.basetexture
        self.basehead = ENTITY_TYPES[entityType]['head'] and textureLoader.LOAD_TEXTURE("assets/textures/entity/"+self.type+"/head.png", ENTITY_TYPES[entityType]['head']['size']['x']*64, ENTITY_TYPES[entityType]['head']['size']['y']*64)
        self.head = ENTITY_TYPES[entityType]['head'] and rot_center(self.basehead, self.basehead.get_rect(), self.rotation)[0]
        self.textureOffsetX = ENTITY_TYPES[entityType]['texture']['position']['x']
        self.textureOffsetY = ENTITY_TYPES[entityType]['texture']['position']['y']
        self.headOffsetX = ENTITY_TYPES[entityType]['head'] and ENTITY_TYPES[entityType]['head']['position']['x']
        self.headOffsetY = ENTITY_TYPES[entityType]['head'] and ENTITY_TYPES[entityType]['head']['position']['y']
        self.flipped = False
        self.hideHead = False
        self.textureflipped = False
        self.animation = None
        self.animationFrame = 1
        self.lastFrame = 0
        self.lastDamage = 0
        self.createEventFired = False
        self.velx = 0
        self.vely = 0
        self.jumping = False
        self.left = False
        self.right = False
        self.spawnx = x
        self.spawny = y
        self.AI = AI and getAI(self.type)
        self.hitbox = Hitbox(self)
        ENTITIES.append(self)

    def jump(self, blocks=blockClass.BLOCKS):
        self.y -= 0.05
        self.updateHitbox()
        if collide(self, blocks) and not self.jumping:
            self.jumping = True
        self.y += 0.05
        self.updateHitbox()
                
    def stop(self):
        self.velx = 0

    def calculateGravity(self, delta):
        self.vely += GRAVITY*delta

    def updateHitbox(self):
        self.hitbox.rect.x = self.x*100
        self.hitbox.rect.y = -self.y*100

    def flip(self):
        self.flipped = not self.flipped

    def delete(self):
        self in ENTITIES and ENTITIES.remove(self)

    def applyDamage(self, damageOrEntity):
        if ticks - self.lastDamage < 8 or self.health == 0:
            return
        self.lastDamage = ticks
        entity = None
        if type(damageOrEntity).__name__ == "int" or type(damageOrEntity).__name__ == "float":
            self.health -= damageOrEntity
        if type(damageOrEntity).__name__ == "Entity":
            self.health -= damageOrEntity.damage
            entity = damageOrEntity
        if self.health < 0:
            self.health = 0
        if self.AI:
            try:
                self.AI.damage(self, entity)
            except:
                "nothing here..."
            try:
                if self.health == 0:
                    self.stop()
                    self.AI.death(self, entity)
            except:
                self.delete()

    def respawn(self):
        self.x = self.spawnx
        self.y = self.spawny
        self.health = self.maxhealth
        self.createEventFired = False
        self.flipped = False
        self.hideHead = False
        self.textureflipped = False
        self.animation = None
        self.animationFrame = 1
        self.lastFrame = 0
        self.lastDamage = 0
        self.velx = 0
        self.vely = 0
