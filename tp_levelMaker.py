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
        self.levels = [self.levelOne, self.levelTwo, self.levelThree]
        
        
    def getNextLevel(self, currentLevel): 
        if currentLevel != self.levelThree:
            index = self.levels.index(currentLevel)
            return self.levels[index + 1]
        else: return self.levelThree

    def getPreviousLevel(self, currentLevel):
        if currentLevel != self.levelOne:
            index = self.levels.index(currentLevel)
            return self.levels[index - 1]
        else: return self.levelOne


    # because not randomized yet, we will just hardcode some level
    def levelOne(self):
        #first, set up player because this is level one
        MissionOne.player = Player((self.width // 5, self.height // 3 * 2))

        # set up terrain
        terrains = copy.deepcopy(terrainDict)
        tempList = []
        tempList.append([(0, self.height / 3), (self.width / 6, self.height / 5),
                          (self.width / 5, 0), (0, 0)])
        tempList.append([(0, self.height/5 * 4), (self.width, self.height / 6 * 5),
                          (self.width, self.height), (0, self.height)])
        tempList.append([(self.width, self.height / 3), (self.width / 6 * 5, self.height / 5),
                          (self.width / 5 * 4, 0), (self.width, 0)])

        for points in tempList:
            terrains["normal"].add(Terrain(points, (0, 0, 0), "polygon"))

        # get everything into the thing
        # (terrain, music, collectibles)
        self.levelOne = {"terrain": terrains, 
                         "music": None,
                         "collectibles": None}

    def levelTwo(self):
        self.levelTwo = {"terrain": terrains, 
                         "music": None,
                         "collectibles": None}
    
    def levelThree(self):
        self.levelThree = {"terrain": terrains, 
                           "music": None,
                           "collectibles": None}
    

'''
do we want to do staticmethod or nah
static method: access each level by calling classname
which is prob better
not static method: gotta make a whole instance

'''