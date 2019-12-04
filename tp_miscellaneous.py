####################################################
# miscellaneous.py
# this file includes: terrains, collectibles, player
# used by levelMaker.py and missions.py
####################################################

import copy, io, time
import pygame
pygame.init()

# -----initialize player class----- #

class Player(object):
    radius = 30
    jump = 30
    def __init__(self, center, color, currentMission):
        self.color = color    
        self.x, self.y = center[0], center[1]
        self.leftX, self.rightX = self.x - self.radius, self.x + self.radius
        # ---for gravity & wall climbing--- 
        self.isInAir = True
        self.count = 0
        self.mask = None
        #self.xSensor = 
        # ---for level specific things---
        self.setupCurrentLevel(currentMission, 0)
        # ---for checkpoints---
        self.uncheckedCollectibles = [] # any notes acquired after the checkpoint
        self.checkedCollectibles = copy.deepcopy(self.currentMusic) # before the checkpoint
        self.lastCheckpoint = (center, 0)       # ((x, y), level index)
        self.currentMission = currentMission
        # set up shit
        sprite = pygame.image.load("death_sprite_maybe.png")
        self.deathSprite = pygame.transform.scale(sprite, (480, 360))

    def setupCurrentLevel(self, currentMission, level):
        self.currentLevel = currentMission.levels[level]
        self.currentExistables = self.currentLevel["existables"]
        self.currentTerrain = self.currentLevel["terrains"]
        self.currentCollectibles = self.currentLevel["collectibles"]
        self.currentTerrainsDict = self.currentLevel["terrainsDict"]
        self.currentMusic = copy.deepcopy(currentMission.music)
        
    def setupDeathAnimation(self):
        pass

    # draw and update rect 
    def drawPlayer(self, display):
        self.rect = pygame.draw.circle(display, self.color, 
                    (int(self.x), int(self.y)), self.radius)
    
    # for collectibles, checkpoint, endpoint
    def checkCollision(self, others):
        return self.rect.collidelist(others)

    # referenced from https://sivasantosh.wordpress.com/2012/07/23/using-masks-pygame/
    # for how to code mask.overlap and offsets
    def inExistableSpace(self, mask, xOffset = None, yOffset = None):
        if xOffset == None:
            xOffset = self.x - self.radius
        if yOffset == None:
            yOffset = self.y - self.radius
        return mask.overlap(self.mask, (xOffset, yOffset)) 
    def inExistableAxis(self, mask, xOffset = None, yOffset = None):
        if xOffset == None:
            xOffset = self.x - self.radius
        if yOffset == None:
            yOffset = self.y - self.radius
        return mask.overlap(self.axis, (xOffset, yOffset))     
 
    # ---death and checkpoints and respawn---
    # image crop tutorial https://stackoverflow.com/questions/6239769/how-can-i-crop-an-image-with-pygame
    def death(self, screen):        # morbid much?
        #surface = pygame.Surface(int(self.radius * 2), int(self.radius * 2))
        deathTopLeft = (self.x - self.radius, self.y - self.radius)
        #spriteWidth, spriteHeight = 1985 / 8, 1312 / 6
        for x in range(8):
            for y in range(6):
                #xOffset, yOffset = x * spriteWidth, y * spriteHeight
                screen.blit(self.deathSprite, deathTopLeft, (60 * x, 60 * y, 60, 60))
                pygame.display.flip()
                #print ("yay")
                time.sleep(0.01)

        self.x, self.y = self.lastCheckpoint[0] # go back to last place
        self.currentMusic = self.currentMission.music = copy.deepcopy(self.checkedCollectibles)  # go back to old music
        for (level, notes) in self.uncheckedCollectibles:
            self.currentMission.levels[level]["collectibles"].add(notes)
        self.uncheckedCollectibles = []
        return self.lastCheckpoint[1]   # the level we need to go back to

    # saves progress 
    def toCheckpoint(self, checkpoint):
        if not checkpoint.isChecked:
            checkpoint.isChecked = True
            self.uncheckedCollectibles = []
            self.checkedCollectibles = copy.deepcopy(self.currentMusic)
            self.lastCheckpoint = (checkpoint.center, checkpoint.level) 

    # ---moving physics--- 
    def move(self, dx, dy, existableMask):
        self.x += dx
        self.y += dy
        for lst in existableMask["normal"]:
            while (self.inExistableSpace(lst) != None and
                (abs(self.inExistableSpace(lst)[0] - self.x) < self.radius*0.8) and
                (abs(self.inExistableSpace(lst)[1] - self.y) < self.radius*0.8)):
                crash = self.inExistableSpace(lst)
                if crash[0] > self.x: self.x -= 1
                if crash[0] < self.x: self.x += 1
                if crash[1] > self.y: self.y -= 1
                if crash[1] < self.y: self.y += 1


    def resetInAir(self):
        self.isInAir = False
        self.count = 0

    def doGravity(self, existableList):
        self.count += 1
        self.move(0, 1 * self.count, existableList)

    # make sure we are at the ground, not another plane
    # so far this works pretty nicely
    def getLowerHeight(self, existables): 
        # not only lowerst but also existable!!
        if self.x < 0: self.x = 0
        yList = existables[self.x]
        nearestY = yList[0]
        count = 0
        for y in reversed(yList):
            #print (yList)
            count += 1

            for i in self.currentExistables["normal"]:
                if self.inExistableSpace(i, None, y) != None:
                    count -= 1
            if y > self.y and count % 2 != 0:
            # if (abs(self.y - y) < abs(self.y - nearestY) and 
            #     y > self.y and count % 2 == 0):
                # for i in self.currentExistables["normal"]:
                #     if self.inExistableSpace(i) == None:
            # if abs(self.y - y) < abs(self.y - nearestY) and y > self.y:
            #if (self.y - y) < (self.y - nearestY) and y > self.y:
            #if y > self.y and y > nearestY:
                nearestY = y
        return nearestY    
        # # not only lowerst but also existable!!
        # if self.x < 0: self.x = 1
        # elif self.x > 999: self.x = 998
        # #while len(yList[self.x]) < 
        # # (existables)
        # yList = existables[self.x]
        # lowestY = 500
        # for y in reversed(yList):
        #     if y > self.y:
        #         lowestY = y
        # return lowestY   
        #         # not only lowerst but also existable!!
        # if self.x < 0: self.x = 0
        # yList = existables[self.x]
        # nearestY = yList[0]
        # count = 0
        # for y in reversed(yList):
        #     #print (yList)
        #     count += 1

        #     for i in self.currentExistables["normal"]:
        #         if self.inExistableSpace(i, None, y) != None:
        #             count -= 1
        #     if y > self.y and count % 2 != 0:
        #     # if (abs(self.y - y) < abs(self.y - nearestY) and 
        #     #     y > self.y and count % 2 == 0):
        #         # for i in self.currentExistables["normal"]:
        #         #     if self.inExistableSpace(i) == None:
        #     # if abs(self.y - y) < abs(self.y - nearestY) and y > self.y:
        #     #if (self.y - y) < (self.y - nearestY) and y > self.y:
        #     #if y > self.y and y > nearestY:
        #         nearestY = y
        # return nearestY 

    def getLevelIndex(self, currentMission):
        return currentMission.levels.index(self.currentLevel)

# -----collectibles (basically music notes)----- #
class Collectibles(object):     
    radius = 20        
    image = pygame.image.load("level_info/music_note.png")
    image = pygame.transform.smoothscale(image, (30, 30))
    image = pygame.transform.rotate(image, -20)
    def __init__(self, center, statusByte, color):
        self.center = int(center[0]), int(center[1])
        self.status = statusByte    
        self.color = color

    def drawCollectibles(self, screen):
        
        self.rect = pygame.draw.circle(screen, self.color, self.center, self.radius)
        screen.blit(Collectibles.image, (self.center[0] - 18, self.center[1] - 18)) 

class Checkpoints(object):
    radius = 40
    image = pygame.image.load("level_info/quarter_rest.png")
    image = pygame.transform.smoothscale(image, (70, 70))
    def __init__(self, center, level, notCheckedColor, checkedColor):
        self.center = center
        self.notCheckedColor = notCheckedColor
        self.checkedColor = checkedColor
        self.isChecked = False      # true when player reach that checkpoint
        self.level = level
    
    def drawCheckpoint(self, screen):
        if self.isChecked:      color = self.checkedColor
        else:                   color = self.notCheckedColor
        self.rect = pygame.draw.circle(screen, color, self.center, self.radius) 
        screen.blit(Checkpoints.image, (self.center[0] - 35, self.center[1] - 35))

class Endpoint(object):
    radius = 40
    def __init__(self, center, color):
        self.center = center
        self.color = color
    
    def drawEndpoint(self, display):
        #print (self.color, self.center, self.radius)
        self.rect = pygame.draw.circle(display, self.color, self.center, self.radius)
     
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
        #for lst in terrainList:
        for (x, y) in terrainList:
            if x in d:      
                d[x].add(y)
            else:             
                d[x] = {y}
            # if y < Player.radius * 2 or y > 500 - Player.radius * 2: 
            #     d[x].pop()
        for key in d:
            d[key] = sorted(d[key])
        return d

# so this is bad terrain
# if you touch this you die lel
class DangerousTerrain(Terrain):
    color = (255, 51, 51)
    def __init__ (self, pointsList):
        super().__init__(pointsList, DangerousTerrain.color)

