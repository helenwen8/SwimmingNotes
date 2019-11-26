####################################################
# terrains.py
# this file includes: terrains, collectibles, player
# will be mostly used by levelMaker.py
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
    def __init__(self, center):
        self.radius = 30
        self.color = (255, 204, 204)    # to do: change this
        self.x, self.y = center[0], center[1]
        # ---for gravity & wall climbing--- 
        self.isInAir = True
        self.isClimbing = False
        self.count = 0
    
    def drawPlayer(self, display):
        # this should update rect as well as draw simultaneously
        self.rect = pygame.draw.circle(display, self.color, 
                    (int(self.x), int(self.y)), self.radius)
    
    def checkCollision(self, others):
        return self.rect.collidelist(others)

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
        self.move(0, 2 * self.count)

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
        #self.color = (204, 229, 255)
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
class Missions(object):
    # terrains grouped by types
    terrainDict = {"normal": set(), "sticky": set(), "bad": set()}
    # music, grouped by timing
    musicDict = {i: [] for i in range(0, 16)} 
    # overall level information
    # "terrain" = a list of Terrain objects, defined by ME
    # "existables" = a dictionary with key of x'es, values of all borders
    # "collectibles" = list of (x, y) of music notes as well as their midi data
    levelDict = {"terrains": None, "existables": None,
                 "collectRect": [],  "collectibles": set()}

    def __init__ (self, bpm, size):
        self.bpm = bpm
        self.width, self.height = size

    # the following staticmethods are used so we can get info from text files
    # I totally forgot eval is a thing, thanks 112 linter
    # but now life is much easier

    # referenced from 112 website on basic IO 
    @staticmethod
    def getLines(pathname):
        with open(pathname, "rt") as myFile:
            return myFile.readlines()

    @staticmethod
    def extractInfoFromSection(lines):
        # set up the keywords
        keywords = {"height": 500, "width": 1000}
        toRet = []
        # for list comprehensions
        for line in lines:
            if line.startswith("compr"):
                # THIS IS SO BAD HOLY SHIT
                toRet.append(eval(line[6:], keywords))  
            # to add: different terrains
            else:
                toRet.append(eval(line, keywords))
        return toRet

    @staticmethod
    def getLineIndex(keyword, lines):
        if keyword + "\n" in lines:
            start = lines.index(keyword + "\n")
            end = lines.index("END" + keyword + "\n")
            return start, end    # index of xxx and ENDxxx
        return -1       # if such keyword does not exist

    # the following should set up the level automatically
    @staticmethod
    def initiateLevel(pathname):
        # set up alllines and lists
        alllines = Missions.getLines(pathname)
        levelInfo = copy.deepcopy(Missions.levelDict)
        levelInfo["terrains"] = copy.deepcopy(Missions.terrainDict)

        # set up terrain:
        terrainStart, terrainEnd = Missions.getLineIndex("terrains", alllines)
        terrains = Missions.extractInfoFromSection(alllines[terrainStart + 1:terrainEnd])
        
        for points in terrains:
            # print (len(points)) might need to redo this bc we are making a lot of this
            levelInfo["terrains"]["normal"].add(Terrain(points, (0, 0, 0)))

        # set up existables:
        existStart, existEnd = Missions.getLineIndex("existables", alllines)
        existables = Missions.extractInfoFromSection(alllines[existStart + 1:existEnd])
        levelInfo["existables"] = Terrain.mergeTerrainList(existables)

        # set up collectibles
        collectStart, collectEnd = Missions.getLineIndex("collectibles", alllines)
        collectibles = Missions.extractInfoFromSection(alllines[collectStart + 1:collectEnd])
        for points in collectibles:
            levelInfo["collectibles"].add(Collectibles(points[0], points[1], points[2]))

        # set up collectibles' rect
        #for note in levelInfo["collectibles"]:


        return levelInfo

    @staticmethod
    def initiateMusic(pathname):
        # for initial program changes
        alllines = Missions.getLines(pathname)
        initStart, initEnd = Missions.getLineIndex("init", alllines)
        return Missions.extractInfoFromSection(alllines[initStart + 1:initEnd])

    @staticmethod
    def setupMusicDict(pathname):
        alllines = Missions.getLines(pathname)
        musicDict = copy.deepcopy(Missions.musicDict)
        # get all the music infos
        musicStart, musicEnd = Missions.getLineIndex("music", alllines)
        music = Missions.extractInfoFromSection(alllines[musicStart + 1:musicEnd])
        for note in music:  
            # format: (availble zones, (status, data1, data2))
            musicDict[note[0]].append(note[1])
        return musicDict

    # templates for level generations
    def levelOne(self):         pass
    def levelTwo(self):         pass
    def levelThree(self):       pass
    def setupLevels(self):
        # call the three function to set up the levels
        # return a list so its easier to swtich between levels
        self.levelOne()
        self.levelTwo()
        self.levelThree()
        return [self.levelOne, self.levelTwo, self.levelThree]

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

    @staticmethod
    def getTimeInterval(bpm):
        # we are going to get time interval for 16th notes
        msInMinute = 60 * 1000
        sixteen = 0.25     # because we count usually in 4th notes
        return msInMinute / bpm * sixteen

    def playMusic(self, currentTime):
        errorMargin = self.timeInterval * 0.2
        if currentTime % self.timeInterval <= 50:
            #print ((currentTime // self.timeInterval) % 16)
            index = int((currentTime / self.timeInterval) % 16)
            #print (self.music[index])
            return self.music[index]

    def addMusicNotes(self, note):
        for (time, statusByte) in note.status:
            self.music[time].append((note.duration, statusByte))