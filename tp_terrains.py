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
        self.x, self.y = center[0], center[1]
        # ---for gravity & wall climbing--- 
        self.isInAir = True
        self.isClimbing = False
        self.count = 0
    
    def drawPlayer(self, display):
        # this should update rect as well as draw simultaneously
        self.rect = pygame.draw.circle(display, self.color, 
                    (int(self.x), int(self.y)), self.radius)
    
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

    @staticmethod
    def getHeight(x, yIndex, existables):   
        # we are assuming each point has a gap of 50px
        remainder = x % 50
        leftIndex = x - remainder
        dHeight = ((existables[leftIndex][yIndex] - existables[leftIndex + 50][yIndex])
                  / 50) * remainder
        
        return existables[leftIndex][yIndex] - dHeight




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
class Missions(object):
    # for easier 
    terrainDict = {"normal": set(), "sticky": set(), "bad": set()}
    musicDict = {1: [], 2: [], 3: []}
    # "terrain" = a list of Terrain objects, defined by ME
    # "existables" = a dictionary with key of x'es, values of all borders
    # 
    levelDict = {"terrains": None, "existables": None,
                 "music": None,  "collectibles": None}

    def __init__ (self, bpm, size):
        self.bpm = bpm
        self.width, self.height = size
        pass

    # the following should set up the level automatically
    # no need to return anything
    def levelOne(self):     pass
    def levelTwo(self):     pass
    def levelThree(self):   pass

    def setupLevels(self):
        # call the three function to set up the levels
        # return a list so its easier to swtich between levels
        self.levelOne()
        self.levelTwo()
        self.levelThree()
        #return [self.levelOne, self.levelTwo, self.levelThree]
        return [self.levelOne]

    # for moving between levels/scenes
    def getNextLevel(self, currentLevel): 
        if currentLevel != self.levelThree:
            index = self.levels.index(currentLevel)
            return self.levels[index + 1]
        else: return None

    def getPreviousLevel(self, currentLevel):
        if currentLevel != self.levelOne:
            index = self.levels.index(currentLevel)
            return self.levels[index - 1]
        else: return None

    def playMusic(self):
        pass    # lol 