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
    def __init__(self, center, color, currentMission):
        self.color = color    
        self.x, self.y = center[0], center[1]
        self.dx, self.dy = 15, -15
        self.jump = 15
        # ---for gravity & flying--- 
        self.isInAir = True
        self.count = 0
        self.mask = None
        self.swimming = False
        # ---for level specific things---
        self.setupCurrentLevel(currentMission, 0)
        # ---for checkpoints---
        self.uncheckedCollectibles = [] # any notes acquired after the checkpoint
        self.checkedCollectibles = copy.deepcopy(self.currentMusic) # before the checkpoint
        self.lastCheckpoint = (center, 0)       # ((x, y), level index)
        self.currentMission = currentMission
        self.isDead = False
        # set up shit
        # sprite = pygame.image.load("death_sprite_maybe.png")
        # self.deathSprite = pygame.transform.scale(sprite, (480, 360))
        self.currentSprite = self.setupSprite()

    def setupCurrentLevel(self, currentMission, level):
        self.currentLevel = currentMission.levels[level]
        self.currentExistables = self.currentLevel["existables"]
        self.currentTerrain = self.currentLevel["terrains"]
        self.currentCollectibles = self.currentLevel["collectibles"]
        self.currentTerrainsDict = self.currentLevel["terrainsDict"]
        self.currentMusic = copy.deepcopy(currentMission.music)
        
    def setupSprite(self):
        WHITE = (255, 255, 255)
        self.sprite0, self.sprite1 = [], []
        tempList = ["front", "up", "down", "side"]
        sprite1 = (pygame.image.load("game_info/" + path + "_1.png") for path in tempList)
        for sprite in sprite1:
            self.sprite1.append(pygame.transform.smoothscale(sprite, (60,60)))
        sprite0 = (pygame.image.load("game_info/" + path + "_0.png") for path in tempList)
        for sprite in sprite0:
            self.sprite0.append(pygame.transform.smoothscale(sprite, (60,60)))
        return self.sprite0[0]


    def drawDeath(self):
        #surface = pygame.Surface(int(self.radius * 2), int(self.radius * 2))
        deathTopLeft = (self.x - self.radius, self.y - self.radius)
        #spriteWidth, spriteHeight = 1985 / 8, 1312 / 6
        for x in range(8):
            for y in range(6):
                #xOffset, yOffset = x * spriteWidth, y * spriteHeight
                #screen.blit(self.deathSprite, deathTopLeft, (60 * x, 60 * y, 60, 60))
                screen.blit(Checkpoints.image, deathTopLeft)
                pygame.display.flip()
                #print ("yay")
                time.sleep(0.01)

    # draw and update rect 
    def drawPlayer(self, screen):
        self.rect = pygame.draw.circle(screen, self.color, 
                    (int(self.x), int(self.y)), self.radius)
        screen.blit(self.currentSprite, (int(self.x - self.radius), int(self.y - self.radius)))
    # for collectibles, checkpoint, endpoint
    def checkCollision(self, others):
        return self.rect.collidelist(others)

    # referenced from https://sivasantosh.wordpress.com/2012/07/23/using-masks-pygame/
    # for how to code mask.overlap and offsets
    def inExistableAxis(self, mask, xOffset = None, yOffset = None):
        if xOffset == None:
            xOffset = self.x - self.radius
        if yOffset == None:
            yOffset = self.y - self.radius
        return mask.overlap(self.axis, (xOffset, yOffset))     
 
    # ---death and checkpoints and respawn---
    # image crop tutorial https://stackoverflow.com/questions/6239769/how-can-i-crop-an-image-with-pygame
    def death(self, screen):        # morbid much?
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
    def move(self, dx, dy):
        # dx, dy can either be -1, 0, or 1
        if self.swimming:
            self.x += dx * 9
            self.y += dy * 9
            spriteSet = self.sprite1
        else:
            self.x += dx * 15
            self.y += dy * 15
            spriteSet = self.sprite0

        if dx > 0:      self.currentSprite = spriteSet[3]
        elif dx < 0:    self.currentSprite = pygame.transform.flip(spriteSet[3], True, False)
        elif dy > 0:      self.currentSprite = spriteSet[1]
        elif dy < 0:    self.currentSprite = spriteSet[2]
        
        # self.x += dx * 30
        # self.y += dy * 30

    def checkLegal(self):
        intersectCoord = None
        for i in self.currentExistables["normal"]:
            if self.inExistableAxis(i) != None:
                intersectCoord = self.inExistableAxis(i)
                break
        
        if intersectCoord != None:
            if (intersectCoord[1] > self.y and
                (intersectCoord[1] - self.y) > self.radius * 0.85):  # pop them up 
                self.resetInAir()
                self.swimming = False
                self.y = self.getLowerHeight(self.currentTerrainsDict) - self.radius - 2
            elif intersectCoord[1] < self.y: 
                self.swimming = True
                self.doGravity()
        else:
            self.swimming = False
            self.doGravity()    

    def resetInAir(self):
        self.isInAir = False
        self.count = 0

    def doGravity(self):
        if self.swimming:
            self.y -= 1
        else:
            self.count += 1
            self.y += self.count


    # make sure we are at the ground
    # so far this works pretty nicely
    def getLowerHeight(self, existables): 
        if self.x < 0: self.x = 0
        yList = existables[self.x]
        nearestY = yList[-1]
        count = 0
        for y in reversed(yList):
            count += 1
            if y > self.y and count % 2 == 0:
                if abs(y - self.y) < abs(nearestY - self.y):
                    nearestY = y
        return nearestY  

    def getUpperHeight(self, existables): 
        if self.x < 0: self.x = 0
        yList = existables[self.x]
        nearestY = yList[0]
        count = 0
        print (yList)
        for y in (yList):
            count += 1
            if y < self.y and count % 2 == 0:
                if abs(y - self.y) < abs(nearestY - self.y):
                    nearestY = y
        return nearestY      
        

    def getLevelIndex(self, currentMission):
        return currentMission.levels.index(self.currentLevel)

# -----collectibles (basically music notes)----- #
class Collectibles(object):     
    radius = 20        
    image = pygame.image.load("game_info/music_note.png")
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
    image = pygame.image.load("game_info/quarter_rest.png")
    image = pygame.transform.smoothscale(image, (70, 70))
    def __init__(self, center, level, color):
        self.center = center
        self.color = color
        self.isChecked = False      # true when player reach that checkpoint
        self.level = level
    
    def drawCheckpoint(self, screen):
        if self.isChecked:      
            self.rect = pygame.draw.circle(screen, self.color, self.center, self.radius) 
        else:                   
            self.rect = pygame.draw.circle(screen, self.color, self.center, self.radius, 5)
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
    color = (178, 34, 34)
    def __init__ (self, pointsList):
        super().__init__(pointsList, DangerousTerrain.color)

