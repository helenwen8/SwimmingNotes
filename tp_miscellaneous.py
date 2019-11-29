####################################################
# miscellaneous.py
# this file includes: terrains, collectibles, player
# used by levelMaker.py and missions.py
####################################################

import copy, io, decimal
import pygame
pygame.init()

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
        # mainly for colectibles
        return self.rect.collidelist(others)

    # referenced from https://sivasantosh.wordpress.com/2012/07/23/using-masks-pygame/
    # for how to code mask.overlap and offsets
    def inExistableSpace(self, mask):
        return mask.overlap(self.mask, (self.x - self.radius, self.y - self.radius)) 

    # ---moving physics--- 
    def move(self, dx, dy, existableMask):
        self.x += dx
        self.y += dy
        # for lst in existableMask:
        #     while self.inExistableSpace(lst) != None:
        #         #rint (self.inExistableSpace(lst), lst)
                
        #         if dx > 0:      self.x -= 1
        #         elif dx < 0:    self.x += 1
        #         if dy > 0:      self.y -= 1
        #         elif dy < 0:    self.y += 1
 
    def resetInAir(self):
        self.isInAir = False
        self.count = 0

    def doGravity(self, existableList):
        self.count += 1
        self.move(0, 1 * self.count, existableList)

    # make sure we are at the ground, not another plane
    # so far this works pretty nicely
    def getLowerHeight(self, existables): 
        yList = existables[self.x]
        nearestY = yList[0]
        for y in reversed(yList):
            if abs(self.y - y) < abs(self.y - nearestY) and y > self.y:
            #if (self.y - y) < (self.y - nearestY) and y > self.y:
            #if y > self.y and y > nearestY:
                nearestY = y
        return nearestY    

# -----collectibles (basically music notes)----- #
class Collectibles(object):     
    radius = 10        
    def __init__(self, center, duration, statusByte, color):
        self.center = center  
        self.status = statusByte    
        self.duration = duration
        self.color = color

    def drawCollectibles(self, display):
        self.rect = pygame.draw.circle(display, self.color, self.center, self.radius)

    def changeCollected(self):
        # do this so we can do checkpoint!
        self.isCollected = not self.isCollected

# -----terrains (main class)----- #
class Terrain(object):
    def __init__(self, pointsList, color):
        self.pointsList = pointsList        # where to draw the things
        self.color = color

    def drawTerrain(self, display):
        pygame.draw.polygon(display, self.color, self.pointsList)

    # referenced from my own hw9 lol
    # also thanks to Prof. Taylor for a genius idea
    # this should take in masks and combine them into a list of outlines
    @staticmethod
    def mergeTerrainList(terrainList):
        d = {}
        for lst in terrainList:
            for (x, y) in lst:
                if y == 0:        pass  # ignore top line 
                elif x in d:      d[x].append(y)
                else:             d[x] = [y]
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
    color = (255, 51, 51)
    def __init__(self, pointsList):
        pass

    def drawTerrain(self, uyeet):
        pass

