# this is a file to assemble everyhign question mark

import sys, copy, random, time
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

# a small helper function for setting all the correct things
def setVariables(level):
    pass

# -----initialize current level (to be changed)
currentMission = MissionOne(size)
currentLevel = currentMission.levelOne
currentTerrain = currentLevel["terrains"]
currentExistables = currentLevel["existables"]
currentCollectibles = currentLevel["collectibles"]
currentMusic = currentMission.music
player = MissionOne.player
for (status, data1) in currentMusic["init"]:
    midiOutput.write_short(status, data1)

# -----function to play music----- #

'''to be added lol'''

# -----main pygame loop----- # 
# modified from Pygame Introduction: https://www.pygame.org/docs/tut/PygameIntro.html

startTime = time.time()   
while 1:
    # check for many things
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            for index in range(0, 16):
                for (level, (status, data1, data2)) in currentMusic[index]:
                    midiOutput.note_off(data1)      # this works for now but..
            midiOutput.close()
            del midiOutput              # so we safely exit the midi module
            pygame.midi.quit    
            sys.exit()                  
    
    # checking pressed keys, inspired from 
    # https://stackoverflow.com/questions/9961563/how-can-i-make-a-sprite-move-when-key-is-held-down 
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_UP]:
        player.move(0, -20)
        '''TO DO: make wall sticky - needs special attention''' # not mvp so fuck it
    if keys[pygame.K_DOWN]:
        # we check if player is below terrain in a later code
        player.move(0, 20)   
    if keys[pygame.K_LEFT]:
        if (player.x > 0):
            player.move(-10, 0)
        else:
            '''todo: make this prettier?'''
            if currentMission.getPreviousLevel(currentLevel) != None:
                currentLevel = currentMission.getPreviousLevel(currentLevel)
                currentTerrain = currentLevel["terrains"]
                currentExistables = currentLevel["existables"]
                currentCollectibles = currentLevel["collectibles"]
                player.x = width - player.radius    
    if keys[pygame.K_RIGHT]: 
        if (player.x < width):
            player.move(10, 0)
        else:
            if currentMission.getNextLevel(currentLevel) != None:
                currentLevel = currentMission.getNextLevel(currentLevel)
                currentTerrain = currentLevel["terrains"]
                currentExistables = currentLevel["existables"]
                currentCollectibles = currentLevel["collectibles"]
                player.x = 0 + player.radius
                
    # ---check gravity---       
    '''no wall climbing so far'''
    currentlyInAir = player.isExistable(currentExistables)
    if currentlyInAir:
        player.doGravity()
    else:
        player.resetInAir()
        player.y = player.getHeight(currentExistables) - player.radius

    # ---play music---
    currentTime = (time.time() - startTime) * 1000
    # randomized intervals 
    music = currentMission.playMusic(currentTime)
    if music != None:
        for (level, (status, data1, data2)) in music:
            midiOutput.write_short(status, data1, data2)

    # ---draw all the components--- 
    screen.fill((255, 255, 255))                
    for terrainType in currentTerrain:
        for terrain in currentTerrain[terrainType]:
            terrain.drawTerrain(screen)
    for note in currentCollectibles:
        note.drawCollectibles(screen)
    player.drawPlayer(screen)
    pygame.display.flip()
      # ---check collision---
    temp = []
    for note in currentLevel["collectibles"]:
        if player.rect.colliderect(note.rect):
            temp.append(note)
    for note in temp:
        currentMission.addMusicNotes(note)
        currentCollectibles.remove(note)
