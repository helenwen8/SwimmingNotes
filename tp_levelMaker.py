######################################################
# levelMaker.py
# this includes all the music, terrains for each level
# ####################################################

# we will have 3 missions, 5 levels each?
# because we have the checkpoint feature, we want to make sure we store each 
# collectable in a separate list
# like we can initialize a new level class.... and then when we initialize it
# we can have a CLASS ATTRIBUTE!!!! of all the collectable
# and the one we havent collect yet

import copy
import pygame
from tp_terrains import *

terrainDict = {"normal": set(), "sticky": set(), "bad": set()}
musicDict = {1: [], 2: [], 3: []}

# -----make mission one-----#

class MissionOne(object):
    player = None
    # a happy, chill theme
    # faster bpm - 120? 130?
    collectibles = {}
    alreadyCollected = []
    def __init__(self, size):
        # we cna use level_oen to return some dictionary or something
        # to store all the data
        self.bpm = 120
        self.width, self.height = size

        self.levelOne()        # also set up player
        # self.levelTwo()
        # self.levelThree()
        self.levels = [self.levelOne]
        
        
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

    def setuplevels(self):
        self.levelOne
        self.levelTwo
        self.levelThree
        return [self.levelOne, self.levelTwo, self.levelThree]

    # because not randomized yet, we will just hardcode some level
    def levelOne(self):
        #first, set up player because this is level one
        MissionOne.player = Player((self.width // 5, self.height // 3 * 2))


        # we will have two lists (or sets? dictionary?)
        # one with a list of existable space - simply a list of boundaries
        # one will be just a list of objects 

        # set up terrain
        terrains = copy.deepcopy(terrainDict)

        '''to do: make this into a text file or smth or this program will be shit'''
        templist = []
        # a random blob
        terrain1 = [(0, self.height // 3), (50, self.height // 5),
                         (100, 0), (0, 0)]

        terrain1Existable = terrain1[:-1]
        templist.append(terrain1)
        # the ground terrain
        terrain2Existable = [(10 * i, self.height // 5 * 4) for i in range(0, self.width, 5)]
        terrain2 = [(0, self.height)] + terrain2Existable + [(self.width, self.height)]
        templist.append(terrain2)

        terrainList = [terrain1Existable, terrain2Existable]
        existableSpace = Terrain.mergeTerrainList(terrainList)
        for points in templist:
            terrains["normal"].add(Terrain(points, (0, 0, 0)))

        # get everything into the thing
        # (terrain, music, collectibles)
        # object at index 1, rects at index 2
        self.levelOne = {"terrainObjects": terrains, 
                         "existableSpace": existableSpace,
                         "music": None,
                         "collectibles": None}

    # def levelTwo(self):
    #     self.levelTwo = {"terrain": terrains, 
    #                      "music": None,
    #                      "collectibles": None}
    
    # def levelThree(self):
    #     self.levelThree = {"terrain": terrains, 
    #                        "music": None,
    #                        "collectibles": None}
                                               