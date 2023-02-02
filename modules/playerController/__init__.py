#imports
import math
import time
import modules.blockClass as blockClass
import modules.entityClass as entityClass
import modules.renderDistance as renderDistance
import modules.raycastUtility as raycastUtility

#class
lastData = [0, 0]

class Controller:
    def __init__(self, entity, screen):
        self.entity = entity
        self.mouseX = 0
        self.mouseY = 0
        self.screen = screen
        self.selectedBlock = "stone"
        self.SCORE_DIAMONDS = 0
        self.SCORE_TIME = 0
        self.SCORE_KILLS = 0
        self.TOTAL_SCORE = 0
        self.start_time = time.time()
    def update(self, data):
        #health check
        if self.entity.health == 0:
            return

        #rotate player
        self.mouseX = data[2][0]
        self.mouseY = data[2][1]

        x = self.screen.get_size()[0]/2-self.mouseX
        y = self.screen.get_size()[1]/2-self.mouseY
        rotation = math.atan2(x, y)*57.2958+90
        self.entity.flipped = rotation > 90
        self.entity.rotation = not self.entity.flipped and rotation or -rotation+180

        #move player
        self.entity.left = data[0]
        self.entity.right = data[1]

        #animations
        if data[0] or data[1] and not self.entity.animation == "hit" and not self.entity.animation == "hurt":
            self.entity.animation = "walk"
        if not data[0] and self.entity.velx < 0:
            self.entity.stop()
            self.entity.flipped = False
            self.entity.animation = None
        if not data[1] and self.entity.velx > 0:
            self.entity.stop()
            self.entity.animation = None

        #scorekeeping
        for entity in renderDistance.LOADED_ENTITIES:
            if entity.type == "diamond":
                if entityClass.collide(self.entity, [entity]):
                    entity.delete()
                    self.SCORE_DIAMONDS += 1
        if self.entity.health > 0:
            self.SCORE_TIME = round((time.time() - self.start_time)/180)
        self.TOTAL_SCORE = self.SCORE_DIAMONDS*2+self.SCORE_TIME+self.SCORE_KILLS*2
                    

        global lastData
        lastData = [x,y]
    def jump(self, data):
        data and self.entity.jump(renderDistance.LOADED_BLOCKS)
    def LMB(self):
        #health check
        if self.entity.health == 0:
            return

        #hitbox update
        self.entity.updateHitbox()
        
        self.entity.animationFrame = 1
        self.entity.animation = "hit"
        result = self.raycast()
        if result and result.breakable:
            if result.type == "diamond_ore":
                entityClass.Entity("diamond", result.x, result.y)
            result.delete()

        #attack
        result = raycastUtility.raycast(self.entity, "zombie")
        if result:
            result.applyDamage(self.entity)
            if result.type == "zombie" and result.health == 0:
                self.SCORE_KILLS += 1
    def RMB(self):
        #health check
        if self.entity.health == 0:
            return

        #hitbox update
        self.entity.updateHitbox()
        
        self.entity.animation = "hit"
        result = self.raycast()
        if result:
            normalx = math.cos(math.atan2(lastData[0], lastData[1])+1.5708)
            normaly = math.sin(math.atan2(lastData[0], lastData[1])+1.5708)
            x = result.x-round(abs(normalx) > abs(normaly) and normalx or 0)
            y = result.y-round(abs(normaly) > abs(normalx) and normaly or 0)
            if blockClass.exists(x, y):
                return
            block = blockClass.Block(x, y, self.selectedBlock)
            for entity in renderDistance.LOADED_ENTITIES:
                if entityClass.collide(entity, [block])and entity.health > 0:
                    block.delete()
    def raycast(self):
        distance = 0
        result = False
        x = self.entity.x
        y = self.entity.y
        normalx = math.cos(math.atan2(lastData[0], lastData[1])+1.5708)
        normaly = math.sin(math.atan2(lastData[0], lastData[1])+1.5708)
        while distance < self.entity.reach:
            x += normalx/10
            y += normaly/10
            distance = math.sqrt(pow(self.entity.x-x, 2)+pow(self.entity.y-y, 2))

            if blockClass.exists(round(x), round(y)):
                result = blockClass.exists(round(x), round(y))
                break
        return result
        
