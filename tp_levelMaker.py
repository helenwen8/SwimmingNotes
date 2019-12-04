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

class MissionTutorial(Missions):
    currentCheckpoint = []
    def __init__(self, size, display):
        self.bpm = 120
        self.timeInterval = Missions.getTimeInterval(self.bpm)
        self.width, self.height = size
        self.display = display
        # this should set up all the levels
        self.initLevels()       # music and player
        self.setupLevels("level_info/m0", self.display, self.colorDict)

    def initLevels(self):
        # set up the music dictionary
        self.music = Missions.setupMusicDict("level_info/m0/init.txt")
        # this is so we can return the initial status bytes
        self.music["init"] = set()
        for (status, data1) in Missions.initiateMusic("level_info/m0/init.txt"):
            self.music["init"].add((status, data1))
        # set up color templates
        self.colorDict = Missions.initiateLevel("level_info/m0/init.txt")[0]

    def setupPlayer(self):
        # set up player and player.mask
        self.player = Player((self.width // 5, self.height // 3 * 2),
                                    self.colorDict["player"], self)
        self.player.mask, self.player.axis = Missions.initiatePlayer(self.player, self.display)
        return self.player

# -----make hardcoded levels----- #
'''change this'''
class MissionOne(Missions):
    player = None
    music = None
    def __init__(self, size):
        self.bpm = 160
        self.timeInterval = Missions.getTimeInterval(self.bpm)
        self.width, self.height = size
        # this should set up all the levels
        #self.levels = self.setupLevels()
        # set up music
        self.initMusic()

    def initMusic(self):
        # set up the music dictionary
        self.music = Missions.setupMusicDict("level_info/mission1_music.txt")
        # this is so we can return the initial status bytes
        self.music["init"] = set()
        for (status, data1) in Missions.initiateMusic("level_info/mission1_music.txt"):
            self.music["init"].add((status, data1))


