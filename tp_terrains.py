####################################################
# terrains.py
# this file includes: terrains, collectibles, player
# will be mostly used by levelMaker.py
####################################################

import pygame
pygame.init()

# -----initialize player class----- #

class Player(object):
    def __init__(self, center):
        self.radius = 30
        self.color = (255, 204, 204)    # to do: change this
        self.rect = None
        self.x, self.y= center[0], center[1]
        # ---for gravity & wall climbing--- 
        self.isInAir = True
        self.isClimbing = False
        self.count = 0
    
    def drawPlayer(self, display):
        # this should update rect as well as draw simultaneously
        self.rect = pygame.draw.circle(display, self.color, (self.x, self.y), self.radius)
    
    def getRect(self):
        return self.rect    # do we need this?

    # ---moving physics--- 
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    # check in bound
    def isExistable(self, existableSpace):
        leftX = self.x - (self.x % 50)
        pointsBelow = 0
        for pointY in reversed(existableSpace[leftX]):
            if pointY > self.y + self.radius:     # because y axis is like opposite
                pointsBelow += 1
        return pointsBelow % 2 == 1

    def resetInAir(self):
        self.isInAir = False
        self.count = 0

    def doGravity(self):
        self.count += 1
        self.move(0, 1 * self.count)

# -----collectibles (basically music notes)----- #

class Collectibles(object):     
    radius = 10                 # they will all be the same
    def __init__(self, pitch, center):
        self.pitch = pitch
        self.center = center
        self.color = 0, 0, 0

    def drawCollectibles(self, display):
        self.rect = pygame.draw.circle(display, self.color, self.center, self.radius)

# -----terrains (main class)----- #
class Terrain(object):
    # type - sharp edges or smooth arcs
    # pointsList - know where to draw the things
    def __init__(self, pointsList, color):
        self.pointsList = pointsList
        self.color = color
        #self.type = terrainType     # normal, sticky, bad

    def drawTerrain(self, display):
        pygame.draw.polygon(display, self.color, self.pointsList)

    # referenced from my own hw9
    # also thanks to Prof. Taylor for a genius idea

    @staticmethod
    def mergeTerrainList(terrainList):
        d = {}
        for lst in terrainList:
            for (x, y) in lst:
                if x in d:
                    d[x].append(y)
                else:
                    d[x] = [y]
        return d

    @staticmethod
    def getHeight(self, x):
        # we are assuming each point has a gap of 50px
        lleftIndex = int(playerX // 50)
        remainder = playerX % 50
        dHeight = ((self.pointsList[leftIndex] - self.pointsList[leftIndex + 1])
                  / 50) * remainder
        
        return self.height[leftIndex] - dHeight
        
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



