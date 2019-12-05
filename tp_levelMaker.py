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

class MissionSetup(Missions):
    def __init__(self, size, display, pathname):
        self.width, self.height = size
        self.display = display
        self.pathname = "game_info/level_info/" + pathname
        # this should set up all the levels
        self.initLevels()       # music and player
        self.setupLevels(self.pathname, self.display, self.colorDict)
        self.tonic = Missions.getTonic(self.pathname + "/init.txt")[0]
        self.bpm = Missions.getBPM(self.pathname + "/init.txt")[0]
        self.timeInterval = Missions.getTimeInterval(self.bpm)

    def initLevels(self):
        # set up the music dictionary
        self.music = Missions.setupMusicDict(self.pathname + "/init.txt")
        # this is so we can return the initial status bytes
        self.music["init"] = set()
        for (status, data1) in Missions.initiateMusic(self.pathname + "/init.txt"):
            self.music["init"].add((status, data1))
        # set up color templates
        self.colorDict = Missions.initiateLevel(self.pathname + "/init.txt")[0]

    def setupPlayer(self):
        # set up player and player.mask
        self.player = Player((self.width // 5, self.height // 3 * 2),
                                    self.colorDict["player"], self)
        self.player.mask, self.player.axis = Missions.initiatePlayer(self.player, self.display)
        return self.player

