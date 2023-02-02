#imports
import math
import modules.blockClass as blockClass
import modules.renderDistance as renderDistance

#modified raycast function that supports entity AND block raycasting
def raycast(self, type_=False):
        distance = 0
        result = False
        x = self.x
        y = self.y
        normalx = math.cos((not self.flipped and self.rotation or -self.rotation+180)/57.2957795)
        normaly = math.sin((not self.flipped and self.rotation or -self.rotation+180)/57.2957795)
        while distance < self.reach:
            x += normalx/10
            y += normaly/10
            distance = math.sqrt(pow(self.x-x, 2)+pow(self.y-y, 2))

            if blockClass.exists(round(x), round(y)):
                0#result = blockClass.exists(round(x), round(y))
                break

            for entity in renderDistance.LOADED_ENTITIES:
                if type_ and not entity.type == type_ or entity == self or entity.health == 0:
                    continue
                if x >= entity.x and x <= entity.x + entity.width and y >= entity.y - entity.height and y <= entity.y:
                    result = entity
                    break
        return result
