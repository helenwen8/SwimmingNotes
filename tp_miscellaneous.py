####################################################
# miscellaneous.py
# this file includes: terrains, collectibles, player
# used by levelMaker.py and missions.py
####################################################

import copy, io, decimal
import pygame
pygame.init()

# helper functions from 112 homework
# thanks, 112!
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

# -----initialize player class----- #

class Player(object):
    radius = 30
    jump = 22
    def __init__(self, center, color):
        self.color = color    
        self.x, self.y = center[0], center[1]
        # ---for gravity & wall climbing--- 
        self.isInAir = True
        self.isClimbing = False
        self.count = 0
        self.mask = None
    
    def drawPlayer(self, display):
        # this should update rect as well as draw simultaneously
        self.rect = pygame.draw.circle(display, self.color, 
                    (int(self.x), int(self.y)), self.radius)
    
    def checkCollision(self, others):
        return self.rect.collidelist(others)

    # credit to https://sivasantosh.wordpress.com/2012/07/23/using-masks-pygame/
    # for inspiration and some code idea
    def checkMaskCollision(self, mask):
        return mask.overlap(self.mask, self.rect.left, self.rect.top) != None


    # ---moving physics--- 
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

   
    # check in bound
    def isExistable(self, existableSpace):
        leftX = self.x - (self.x % 50)
        pointsBelow = 0
        for pointY in reversed(existableSpace[leftX]):
            # (existableSpace[leftX], leftX)
            if pointY > self.y + self.radius:     # because y axis is like opposite
                pointsBelow += 1
        return pointsBelow % 2 == 1

    def resetInAir(self):
        self.isInAir = False
        self.count = 0

    def doGravity(self):
        self.count += 1
        self.move(0, 1 * self.count)

    # the following code works, not sure if they will still work later lmao
    # def getNearestY(self, index, existables):
    #     yList = existables[index]
    #     nearestY = yList[0]
    #     for y in yList:
    #         if abs(self.y - y) <= abs(self.y - nearestY):
    #             pass
    #     pass

    # def getNearestX(self, existables):
    #     nearestX = 0
    #     for x in existables:
    #         pass
    #     pass

    def getHeight(self, existables):   
        # we are assuming each point has a gap of 50px
        remainder = self.x % 50
        leftIndex = self.x - remainder
        
        yList = existables[leftIndex]
        nearestY = yList[0]
        for y in yList:
            if abs(self.y - y) <= abs(self.y - nearestY):
                nearestY = y
        #dHeight = ((existables[leftIndex][yIndex] - existables[leftIndex + 50][yIndex])
        #          / 50) * remainder
        return nearestY     #existables[leftIndex][yIndex]# - dHeight

# -----collectibles (basically music notes)----- #

class Collectibles(object):     
    radius = 10                 # they will all be the same
    color = (204, 229, 255)
    def __init__(self, center, duration, statusByte):
        #self.pitch = pitch
        self.center = center  
        self.status = statusByte    
        self.duration = duration
        
        #Collectibles.color = color
        self.isCollected = False

    def drawCollectibles(self, display):
        if not self.isCollected:
            self.rect = pygame.draw.circle(display, self.color, self.center, self.radius)

    def changeCollected(self):
        # do this so we can do checkpoint!
        self.isCollected = not self.isCollected

# -----terrains (main class)----- #
class Terrain(object):
    def __init__(self, pointsList, color):
        self.pointsList = pointsList        # where to draw the things
        self.color = color
        #self.type = terrainType     # normal, sticky, bad

    def drawTerrain(self, display):
        pygame.draw.polygon(display, self.color, self.pointsList)

    # referenced from my own hw9 lol
    # also thanks to Prof. Taylor for a genius idea
    @staticmethod
    def mergeTerrainList(terrainList):
        d = {}
        for lst in terrainList:
            for (x, y) in lst:
                if x in d:      d[x].append(y)
                else:           d[x] = [y]
        return d

''' dont do the following because you need all the time to do other shit'''       
# so this is the type of terrain where you can climb wall on
# this is the one that really really really need attention on the hitbox thing
class StickyTerrain(Terrain):
    def __init__(self, pointsList, type):
        pass

# so this is bad terrain
# if you touch this you die lel
class ScaryTerrain(Terrain):
    def __init__(self, pointsList):
        pass

    def drawTerrain(self, uyeet):
        pass

# so we make everything easier, I guess
