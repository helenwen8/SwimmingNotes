# missions.py
# this helps generate each level through reading the files

import sys, copy, random, time, os
import pygame
from tp_miscellaneous import * 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Missions(object):
    # terrains grouped by types
    terrainDict = {"normal": set(), "dangerous": set()}
    # music, grouped by timing (eighth note)
    musicDict = {i: [] for i in range(0, 8)} 
    # overall level information
    # terrains: terrain objects     existables: terrain masks
    # terrainsDict: dictionary with x as key and y values as values
    # collectibles: all the music notes object
    # checkpoint/endpoint: corresponding objects
    levelDict = {"terrains": None, "existables": None, "terrainsDict": None, 
                 "collectibles": set(), "checkpoint": None, "endpoint": None}
    colorDict = {"terrains": None, "background": None, "collectibles": None, "endpoint": None,
                 "checkpoint": None, "outline": None, "decorations": None}

    def __init__ (self, bpm, size):
        self.bpm = bpm
        self.width, self.height = size

    # referenced from 112 website on basic IO 
    @staticmethod
    def getLines(pathname):
        with open(pathname, "rt") as myFile:
            return myFile.readlines()

    # the following used so we can get info from text files
    # I totally forgot eval is a thing, thanks 112 linter
    @staticmethod
    def extractInfoFromSection(lines):
        # set up the keywords
        keywords = {"height": 500, "width": 1000, "jump": 22}
        toRet = []
        for line in lines:      
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
    def createLevel(pathname, tempDisplay, colors):
        # set up alllines and lists
        alllines = Missions.getLines(pathname)
        levelInfo = copy.deepcopy(Missions.levelDict)
        levelInfo["terrains"] = copy.deepcopy(Missions.terrainDict)
        levelInfo["existables"] = copy.deepcopy(Missions.terrainDict)
        # set up dangerous terrain:
        dangerousStart, dangerousEnd = Missions.getLineIndex("dangerous", alllines)
        terrains = Missions.extractInfoFromSection(alllines[dangerousStart + 1:dangerousEnd])
        for points in terrains:
            levelInfo["terrains"]["dangerous"].add(DangerousTerrain(points))
        # set up dangerous terrain mask:
        for terrain in levelInfo["terrains"]["dangerous"]:
            tempDisplay.fill(WHITE)
            terrain.drawTerrain(tempDisplay)
            temp = pygame.display.get_surface()
            temp.set_colorkey(WHITE)
            levelInfo["existables"]["dangerous"].add(pygame.mask.from_surface(temp))
        # set up terrain: 
        terrainStart, terrainEnd = Missions.getLineIndex("terrains", alllines)
        terrains = Missions.extractInfoFromSection(alllines[terrainStart + 1:terrainEnd])
        for points in terrains:
            levelInfo["terrains"]["normal"].add(Terrain(points, colors["terrain"]))
        # set up terrain masks
        for terrain in levelInfo["terrains"]["normal"]:
            tempDisplay.fill(WHITE)
            terrain.drawTerrain(tempDisplay)
            temp = pygame.display.get_surface()
            temp.set_colorkey(WHITE)
            levelInfo["existables"]["normal"].add(pygame.mask.from_surface(temp))
        #set up terrainDict for checking above/below
        existableList = []
        for existObject in levelInfo["existables"]["normal"]:
            existableList.extend(existObject.outline())
        levelInfo["terrainsDict"] = Terrain.mergeTerrainList(existableList)
        # set up collectibles
        collectStart, collectEnd = Missions.getLineIndex("collectibles", alllines)
        collectibles = Missions.extractInfoFromSection(alllines[collectStart + 1:collectEnd])
        for points in collectibles:
            levelInfo["collectibles"].add(Collectibles(points[0], points[1], colors["collectibles"]))
        # set up checkpoint - one per level max
        checkStart, checkEnd = Missions.getLineIndex("checkpoint", alllines)
        checkpoint = Missions.extractInfoFromSection(alllines[checkStart + 1:checkEnd])
        if checkpoint != []:
            levelInfo["checkpoint"] = Checkpoints(checkpoint[0][0], checkpoint[0][1], colors["checkpoint"])
        # set up end goal
        if Missions.getLineIndex("endpoint", alllines) != -1:
            endStart, endEnd = Missions.getLineIndex("endpoint", alllines)
            endpoint = Missions.extractInfoFromSection(alllines[endStart + 1:endEnd])
            levelInfo["endpoint"] = Endpoint(endpoint[0], colors["endpoint"])
        return levelInfo

    @staticmethod
    def initiatePlayer(player, tempDisplay):
        tempDisplay.fill(WHITE)
        player.rect = pygame.draw.circle(tempDisplay, BLACK, (30, 30), 27)
        temp = pygame.display.get_surface()
        temp.set_colorkey(WHITE)
        mask1 = pygame.mask.from_surface(temp)
        # a collision axis thing that is not completely useful
        tempDisplay.fill(WHITE)
        pygame.draw.line(tempDisplay, BLACK, (30,1),(30,30), 1)
        pygame.draw.line(tempDisplay, BLACK, (30,60),(30,30), 1)
        pygame.draw.line(tempDisplay, BLACK, (1,30),(30,30), 1)
        pygame.draw.line(tempDisplay, BLACK, (30,60),(30,30), 1)
        temp = pygame.display.get_surface()
        temp.set_colorkey(WHITE)
        mask2 = pygame.mask.from_surface(temp)
        return mask1, mask2

    # set up color palette
    @staticmethod
    def initiateLevel(pathname):
        alllines = Missions.getLines(pathname)
        colorStart, colorEnd = Missions.getLineIndex("color", alllines)
        return Missions.extractInfoFromSection(alllines[colorStart + 1:colorEnd])

    # set up the initial program changes
    @staticmethod
    def initiateMusic(pathname):
        alllines = Missions.getLines(pathname)
        initStart, initEnd = Missions.getLineIndex("init", alllines)
        return Missions.extractInfoFromSection(alllines[initStart + 1:initEnd])

    # get all the music infos
    @staticmethod
    def setupMusicDict(pathname):
        alllines = Missions.getLines(pathname)
        musicDict = copy.deepcopy(Missions.musicDict)
        musicStart, musicEnd = Missions.getLineIndex("music", alllines)
        music = Missions.extractInfoFromSection(alllines[musicStart + 1:musicEnd])
        for note in music: 
            musicDict[note[0]].append(note[1])  # (status, data1, data2)
        return musicDict

    def getBPM(pathname):
        alllines = Missions.getLines(pathname)
        # for initial program changes
        start, end = Missions.getLineIndex("bpm", alllines)
        return Missions.extractInfoFromSection(alllines[start + 1:end])

    def getTonic(pathname):
        alllines = Missions.getLines(pathname)
        # for initial program changes
        start, end = Missions.getLineIndex("tonic", alllines)
        return Missions.extractInfoFromSection(alllines[start + 1:end])

    # saves a list of all levels
    def setupLevels(self, path, display, colorDict):
        self.levels = []
        # basic IO referenced from 112
        for filename in sorted(os.listdir(path)):
            if filename == "init.txt": continue
            levelInfo = Missions.createLevel(path + '/' + filename, display, colorDict)
            self.levels.append(levelInfo)

    # for moving between levels/scenes
    def getNextLevel(self, currentLevel): 
        index = self.levels.index(currentLevel)
        if index < len(self.levels) - 1:
            return index + 1
        else: return None
    def getPreviousLevel(self, currentLevel):
        index = self.levels.index(currentLevel)
        if index > 0:
            return index - 1
        else: return None

    @staticmethod
    def getTimeInterval(bpm):
        # we are going to get time interval for 8th notes
        msInMinute = 60 * 1000
        eighth = 0.5     # because we count usually in 4th notes
        return msInMinute / bpm * eighth

    def playMusic(self, currentTime):
        if currentTime % self.timeInterval <= 50:
            index = int((currentTime / self.timeInterval) % 8)
            return self.music[index]

    def addMusicNotes(self, note):
        for (time, statusByte) in note.status:
            self.music[time].append(statusByte)

    def drawMusicDecorations(self, currentTime, screen, size):  
        index = currentTime // self.timeInterval % 8
        xGap = size[0] / 8
        yGap = size[1] / 24
        if self.music[index] != None:
            for i in range(len(self.music[index])):
                status, data1, data2 = self.music[index][i]
                if status >= 0x90 and status <= 0x9F:
                    noteValue = (data1 - 60) % 24
                    pygame.draw.circle(screen, self.colorDict["decorations"], 
                                    (int(xGap * index), int(yGap * noteValue)), 28)
                    pygame.draw.circle(screen, self.colorDict["outline"],
                        (int(xGap * index), int(yGap * noteValue)), 30, 5)

    def transpose(self, melody):
        newMelody = []
        transposeCount = self.tonic - 60
        for i in melody:
            newMelody.append(i + transposeCount)
        return newMelody
