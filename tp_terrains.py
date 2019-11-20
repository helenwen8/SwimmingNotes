####################################################
# terrains.py
# this file includes: terrains, collectibles, player
# will be mostly used by levelMaker.py
####################################################

import pygame
pygame.init()

# -----initialize player class-----#

class Player(object):
    def __init__(self, center):
        self.radius = 30
        self.color = (255, 204, 204)
        self.rect = None
        self.x, self.y= center[0], center[1]
    
    def drawPlayer(self, display):
        # this should update rect as well as draw simultaneously

        self.rect = pygame.draw.circle(display, self.color, (self.x, self.y), self.radius)
    
    def getRect(self):
        return self.rect

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

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
    def __init__(self, pointsList, color, outlineType):
        self.pointsList = pointsList
        self.color = color
        self.type = outlineType

    def drawTerrain(self, display):
        if self.type == "polygon":
            pygame.draw.polygon(display, self.color, self.pointsList)
        
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



