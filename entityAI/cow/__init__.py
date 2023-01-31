#imports
import random
import modules.blockClass as blockClass

#cow entity AI
lastDirectionChange = 0
ticks = 0
random_ = 100

def onspawn(self):
    #entity spawn event
    self.right = True

def tick(self):
    #entity tick event
    global ticks
    ticks += 1
    global lastDirectionChange
    global random_
    if ticks - lastDirectionChange > random_:
        lastDirectionChange = ticks
        self.left = not self.left
        self.right = not self.right
        self.flip()
        random_ = random.randint(512, 1024)
    if self.left or self.right:
        self.animation = "walk"
    else:
        self.animation = None

    if blockClass.exists(round(self.x)+2, round(self.y)-1):
        self.jump()
    if blockClass.exists(round(self.x)-1, round(self.y)-1):
        self.jump()
