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
import pygame, pygame.midi
from tp_miscellaneous import *
from tp_missions import *


# make start screen
class StartScreen(object):
    pass

class MissionTutorial(Missions):
    currentCheckpoint = []
    def __init__(self, size, display):
        self.bpm = 100
        self.timeInterval = Missions.getTimeInterval(self.bpm)
        self.width, self.height = size
        self.display = display
        # this should set up all the levels
        self.levels = self.setupLevels()
        
        # set up music
        #self.initMusic()

    def initMusic(self):
        # set up the music dictionary
        self.music = Missions.setupMusicDict("level_info/mission0_music.txt")
        # this is so we can return the initial status bytes
        self.music["init"] = set()
        for (status, data1) in Missions.initiateMusic("level_info/mission0_music.txt"):
            self.music["init"].add((status, data1))

    def levelOne(self):
        # set up player because this is level one
        self.player = Player((self.width // 5, self.height // 3 * 2),
                                    (160, 141, 127))
        self.player.mask = Missions.initiatePlayer(self.player, self.display)

        # return a level data dictionary
        self.levelOne = Missions.initiateLevel("level_info/mission0_1.txt", self.display)

    # def levelTwo(self):
    #     self.levelTwo = Missions.initiateLevel("level_info/mission1_level2.txt")
    
    # def levelThree(self):
    #     self.levelThree = Missions.initiateLevel("level_info/mission1_level3.txt")



# -----make hardcoded levels----- #

class MissionOne(Missions):
    player = None
    music = None
    alreadyCollected = []
    def __init__(self, size):
        self.bpm = 160
        self.timeInterval = Missions.getTimeInterval(self.bpm)
        self.width, self.height = size
        # this should set up all the levels
        self.levels = self.setupLevels()
        # set up music
        self.initMusic()

    def initMusic(self):
        # set up the music dictionary
        self.music = Missions.setupMusicDict("level_info/mission1_music.txt")
        # this is so we can return the initial status bytes
        self.music["init"] = set()
        for (status, data1) in Missions.initiateMusic("level_info/mission1_music.txt"):
            self.music["init"].add((status, data1))

    def levelOne(self):
        # set up player because this is level one
        MissionOne.player = Player((self.width // 5, self.height // 3 * 2),
                                    (204, 255, 255))
        # return a level data dictionary
        self.levelOne = Missions.initiateLevel("level_info/mission1_level1.txt")

    def levelTwo(self):
        self.levelTwo = Missions.initiateLevel("level_info/mission1_level2.txt")
    
    def levelThree(self):
        self.levelThree = Missions.initiateLevel("level_info/mission1_level3.txt")

