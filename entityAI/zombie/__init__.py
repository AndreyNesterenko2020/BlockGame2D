#imports
import math
import random
import threading
import modules.blockClass as blockClass
import modules.renderDistance as renderDistance
import modules.raycastUtility as raycastUtility

#zombie entity AI
lastDirectionChange = 0
lastLavaDamage = 0
lastAttack = 0
ticks = 0
random_ = 100
target = False

def onspawn(self):
    #entity spawn event
    self.right = True

def tick(self):
    #entity tick event
    global ticks
    ticks += 1
    global lastDirectionChange
    global random_
    global target
    global lastAttack
    if ticks - lastDirectionChange > random_ and not target:
        lastDirectionChange = ticks
        self.left = not self.left
        self.right = not self.right
        self.flip()
        random_ = random.randint(512, 1024)
    if not self.animation == "hurt" and not self.animation == "hit":
        if self.left or self.right:
            self.animation = "walk"
        else:
            self.animation = None
    if target:
        x = target.x - self.x
        y = target.y - self.y
        rotation = math.atan2(x, y)*57.2958+90
        self.flipped = rotation < 90
        self.rotation = not self.flipped and -rotation+180 or rotation

        if x < 0:
            self.left = True
            self.right = False
        if x > 0:
            self.left = False
            self.right = True
        if target.health == 0:
            target = False
    else:
        self.rotation = 0

    closest = float('inf')
    closestEntity = False
    for ent in renderDistance.LOADED_ENTITIES:
        dist = math.sqrt(pow(ent.x-self.x, 2)+pow(ent.y-self.y, 2))
        if ent.type == "player" and dist < closest and ent.health > 0:
            closest = dist
            closestEntity = ent
    target = closestEntity
    
    if blockClass.exists(round(self.x)+1, round(self.y)-1):
        self.jump()
    if blockClass.exists(round(self.x)-1, round(self.y)-1):
        self.jump()
        
    global lastLavaDamage
    if blockClass.exists(round(self.x), round(self.y-1)):
        if blockClass.exists(round(self.x), round(self.y-1)).type == "lava":
            if ticks - lastLavaDamage > 30:
                lastLavaDamage = ticks
                self.applyDamage(1)
        else:
            self.y += 1
            
    e = raycastUtility.raycast(self, "player")
    if e:
        if ticks - lastAttack > 100:
            lastAttack = ticks
            target.applyDamage(self)
            self.animationFrame = 1
            self.animation = "hit"
    
def damage(self, entity):
    #entity damage event
    self.animationFrame = 1
    self.animation = "hurt"
    self.vely = 0.7
    
def death(self, entity):
    #entity death event
    self.animationFrame = 1
    self.animation = "death"
    self.hideHead = True
    threading.Timer(1, self.delete).start()
    
def onCollideNegY(self):
    #entity negative y collision event
    if self.vely < -8:
        self.applyDamage(-self.vely-8)
