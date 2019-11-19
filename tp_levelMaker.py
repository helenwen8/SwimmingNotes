# this is the file where I do some level generating shit
# for now I guess this will just be a bunch of fixed levels
# yeet

# in this file, we want to
#   generate the data for terrains
#   generate the music we want (or at least the data for it
#   even the color scheme... which can be useful

# we will have 3 missions, 5 levels each?]
# because we have the checkpoint feature, we want to make sure we store each 
# collectable in a separate list
# like we can initialize a new level class.... and then when we initialize it
# we can have a CLASS ATTRIBUTE!!!! of all the collectable
# and the one we havent collect yet

# lets just try this? yeet?
# yeet some getter methods lmao 

import pygame

class Mission_One(object):
    hasCollect = []
    newCollect = []
    def __init__(self):
        pass

    def level_one(self):
        # because not randomized yet, we will just hardcode some level
        wackPointsList = [(0 , 0), (0, 1000), (300, 1000), (0, 0)]
        wack = Terrain(wackPointsList, (255, 12, 32), "polygon")
        pass