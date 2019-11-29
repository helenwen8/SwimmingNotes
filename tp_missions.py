# yay

import sys, copy, random, time
import pygame
from tp_miscellaneous import * 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Missions(object):
    # terrains grouped by types
    terrainDict = {"normal": set(), "sticky": set(), "bad": set()}
    # music, grouped by timing
    musicDict = {i: [] for i in range(0, 16)} 
    # overall level information
    # "terrain" = a list of Terrain objects, defined by ME
    # "existables" = a dictionary with key of x'es, values of all borders
    # "collectibles" = list of (x, y) of music notes as well as their midi data
    levelDict = {"terrains": None, "existables": None, "terrainsDict": None,
                 "collectRect": [],  "collectibles": set()}
    colorDict = {"terrains": None, "background": None, "collectibles": None}

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
        keywords = {"height": 500, "width": 1000, "jump": 22}
        toRet = []
        # for list comprehensions
        for line in lines:
            if line.startswith("compr"):
                # THIS IS SO BAD HOLY SHIT
                toRet.append(eval(line[6:], keywords))  
            # to add: different terrains
            else:

                toRet.append(eval(line, keywords))
                #print (eval(line, keywords))
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
    def createLevel(pathname, tempDisplay, colors):
        tempDisplay.fill(WHITE)
        
        # set up alllines and lists
        alllines = Missions.getLines(pathname)
        levelInfo = copy.deepcopy(Missions.levelDict)
        levelInfo["terrains"] = copy.deepcopy(Missions.terrainDict)

        # set up terrain: 
        terrainStart, terrainEnd = Missions.getLineIndex("terrains", alllines)
        terrains = Missions.extractInfoFromSection(alllines[terrainStart + 1:terrainEnd])
        for points in terrains:
            # print (len(points)) might need to redo this bc we are making a lot of this
            levelInfo["terrains"]["normal"].add(Terrain(points, colors["terrain"]))
            #print (len(levelInfo["terrains"]["normal"]))

        # set up terrain masks
        for terrain in levelInfo["terrains"]["normal"]:
            terrain.drawTerrain(tempDisplay)
        temp = pygame.display.get_surface()
        temp.set_colorkey((colors["terrain"]))
        levelInfo["existables"] = pygame.mask.from_surface(temp)
        #print (len(levelInfo["existables"] ))

        # set up terrainDict for checking above/below
        existableList = levelInfo["existables"].outline()
        #print (existableList)
        levelInfo["terrainsDict"] = Terrain.mergeTerrainList(existableList)

        # set up collectibles
        collectStart, collectEnd = Missions.getLineIndex("collectibles", alllines)
        collectibles = Missions.extractInfoFromSection(alllines[collectStart + 1:collectEnd])
        for points in collectibles:
            levelInfo["collectibles"].add(Collectibles(points[0], points[1], points[2], colors["collectibles"]))

        return levelInfo

    @staticmethod
    def initiatePlayer(player, tempDisplay):
        tempDisplay.fill(WHITE)
        player.rect = pygame.draw.circle(tempDisplay, BLACK, (30, 30), 30)
        temp = pygame.display.get_surface()
        # pygame.image.save(tempDisplay, "level_info/temp/hmm.png")
        # temp = pygame.image.load('level_info/temp/hmm.png').convert()
        temp.set_colorkey(WHITE)
        mask = pygame.mask.from_surface(temp)

        return mask

    @staticmethod
    def initiateLevel(pathname):
        alllines = Missions.getLines(pathname)
        colorStart, colorEnd = Missions.getLineIndex("color", alllines)
        return Missions.extractInfoFromSection(alllines[colorStart + 1:colorEnd])

    @staticmethod
    def initiateMusic(pathname):
        alllines = Missions.getLines(pathname)

        # for initial program changes
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
            index = int((currentTime / self.timeInterval) % 16)
            return self.music[index]

    def addMusicNotes(self, note):
        for (time, statusByte) in note.status:
            self.music[time].append((note.duration, statusByte))