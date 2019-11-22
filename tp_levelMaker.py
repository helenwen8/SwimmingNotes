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

# -----make hardcoded levels----- #

class MissionOne(Missions):
    player = None
    # a happy, chill theme, bpm - 120? 130?
    collectibles = {}
    alreadyCollected = []
    def __init__(self, size):
        self.bpm = 120
        self.width, self.height = size
        # this should set up all the levels
        self.levels = self.setupLevels()

    def levelOne(self):
        # set up player because this is level one
        MissionOne.player = Player((self.width // 5, self.height // 3 * 2))

        # set up terrain
        terrains = copy.deepcopy(Missions.terrainDict)

        templist = []
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

        # return a level data dictionary
        self.levelOne = copy.deepcopy(Missions.levelDict)
        self.levelOne = {"terrains": terrains, 
                         "existables": existableSpace,
                         "music": None,
                         "collectibles": None}

    def levelTwo(self):
        # lets do this hoe


        terrain1Existable =  [(10 * i, self.height // 5) for i in range(0, self.width, 5)]
        terrain2 = [(0, 0)] + terrain2Existable + [(self.width, 0)]
        # the ground terrain
        terrain2Existable = [(10 * i, self.height // 5 * 4) for i in range(0, self.width, 5)]
        terrain2 = [(0, self.height)] + terrain2Existable + [(self.width, self.height)]
        templist.append(terrain2)


        self.levelTwo = copy.deepcopy(Missions.levelDict)
        self.levelTwo = {"terrain": terrains, 
                         "music": None,
                         "collectibles": None}
    
    # def levelThree(self):
    #     self.levelThree = {"terrain": terrains, 
    #                        "music": None,
    #                        "collectibles": None}
                                               