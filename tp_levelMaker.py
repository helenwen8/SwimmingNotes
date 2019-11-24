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

import copy, io
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
        # return a level data dictionary
        self.levelOne = Missions.initiateLevel("level_info/mission1_level1.txt")

    def levelTwo(self):
        # lets do this hoe
        self.levelTwo = Missions.initiateLevel("level_info/mission1_level2.txt")
    
    def levelThree(self):
        self.levelThree = Missions.initiateLevel("level_info/mission1_level3.txt")

