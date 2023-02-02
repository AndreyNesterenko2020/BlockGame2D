#imports
import modules.blockClass as blockClass

#player entity AI
ticks = 0
lastLavaDamage = 0
lastHeal = 0

def onspawn(self):
    #entity spawn event
    "nothing here."

def tick(self):
    #entity tick event
    global ticks, lastLavaDamage, lastHeal
    ticks += 1
    if blockClass.exists(round(self.x), round(self.y-1)):
        if blockClass.exists(round(self.x), round(self.y-1)).type == "lava":
            if ticks - lastLavaDamage > 30:
                lastLavaDamage = ticks
                self.applyDamage(1)
        else:
            self.y += 1
    if ticks - lastHeal > 1000:
        self.health += 0.5
        lastHeal = ticks
        
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
    
def onCollideNegY(self):
    #entity negative y collision event
    if self.vely < -8:
        self.applyDamage(-self.vely-8)
