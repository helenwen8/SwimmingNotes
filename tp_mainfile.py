# this is a file to assemble everyhign question mark

import sys, copy, random
import pygame, pygame.midi 
from tp_terrains import * 
from tp_levelMaker import *

# -----initialize pygame/pygame.midi----- #
pygame.init()  
pygame.midi.init()          

# -----initialize screen & music ------ #
size = width, height = 1000 , 500 
screen = pygame.display.set_mode(size)  
'''TO DO: MAKE FULL SCREEN'''
midiOutput = pygame.midi.Output(pygame.midi.get_default_output_id())
'''TO DO: find ways to get around the midi error message'''

# -----initialize current level (to be changed)
currentMission = MissionOne(size)
currentLevel = currentMission.levelOne
currentTerrain = currentLevel["terrains"]
currentExistables = currentLevel["existables"]
# currentMusic = something

player = MissionOne.player

# -----function to play music----- #

'''to be added lol'''

# -----main pygame loop----- # 
# modified from Pygame Introduction: https://www.pygame.org/docs/tut/PygameIntro.html

while 1:
    # check for many things
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            del midiOutput              # so we safely exit the midi module
            pygame.midi.quit    
            sys.exit()                  
        
    # checking pressed keys, inspired from 
    # https://stackoverflow.com/questions/9961563/how-can-i-make-a-sprite-move-when-key-is-held-down 
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_UP]:
        player.move(0, -10)
        '''TO DO: make wall sticky - needs special attention''' # not mvp so fuck it
    if keys[pygame.K_DOWN]:
        # we check if player is below terrain in a later code
        player.move(0, 10)   
    if keys[pygame.K_LEFT]:
        if (player.x > 0):
            player.move(-10, 0)
        else:
            '''todo: make this prettier?'''
            if currentMission.getPreviousLevel(currentLevel) != None:
                currentLevel = currentMission.getPreviousLevel(currentLevel)
                currentTerrain = currentLevel["terrains"]
                currentExistables = currentLevel["existables"]
                player.x = width - player.radius    
    if keys[pygame.K_RIGHT]: 
        if (player.x < width):
            player.move(10, 0)
        else:
            if currentMission.getNextLevel(currentLevel) != None:
                currentLevel = currentMission.getNextLevel(currentLevel)
                currentTerrain = currentLevel["terrains"]
                currentExistables = currentLevel["existables"]
                player.x = 0 + player.radius
                
    # ---check gravity---       
    '''no wall climbing so far'''
    currentlyInAir = player.isExistable(currentExistables)
    if currentlyInAir:
        player.doGravity()
    else:
        player.resetInAir()
        player.y = player.getHeight(currentExistables) - player.radius

    # ---draw all the components--- #
    screen.fill((255, 255, 255))                
    for terrainType in currentTerrain:
        for terrain in currentTerrain[terrainType]:
            terrain.drawTerrain(screen)
    player.drawPlayer(screen)
    pygame.display.flip()
    
