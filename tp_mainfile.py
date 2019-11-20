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
currentTerrain = currentLevel["terrain"]

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
        
        # get_pressed inspired from https://stackoverflow.com/questions/9961563/how-can-i-make-a-sprite-move-when-key-is-held-down 
    keys = pygame.key.get_pressed()  #checking pressed keys
    if keys[pygame.K_UP]:
        player.move(0, -10)
        '''TO DO: make wall sticky - needs special attention'''
    if keys[pygame.K_DOWN]:
        player.move(0, 10)   
    if keys[pygame.K_LEFT]:
        if (player.x > 0):
            player.move(-10, 0)
        else:
            currentLevel = currentMission.getPreviousLevel(currentLevel)
            currentTerrain = currentLevel["terrain"]
            player.x = width - player.radius    
    if keys[pygame.K_RIGHT]: 
        if (player.x < width):
            player.move(10, 0)
        else:
            currentLevel = currentMission.getNextLevel(currentLevel)
            currentTerrain = currentLevel["terrain"]
            player.x = 0 + player.radius
                
        #     elif event.key == pygame.K_UP:
        #         player.move(0, -20)
        #         '''TO DO: make wall sticky - needs special attention'''
        #     elif event.key == pygame.K_DOWN:  
        #         player.move(0, 20)

    # ---check if we are somehow inside terrain---
    # this is where hitbox comes in
    

    # ---draw all the components--- #
    screen.fill((255, 255, 255))                
    for terrainType in currentTerrain:
        for terrain in currentTerrain[terrainType]:
            terrain.drawTerrain(screen)
    player.drawPlayer(screen)
    pygame.display.flip()
    
