# this is a file to assemble everyhign question mark

import sys, copy, random, time
import pygame, pygame.midi, pygame.mask
from tp_miscellaneous import * 
from tp_missions import *
from tp_levelMaker import *
from tp_gamemode import *

# -----initialize pygame/pygame.midi----- #
pygame.init()  
pygame.midi.init()
# there are different gamestate:
# strat - start screen      pause - pause screen
# win/lose - result ending screen
# and then different level state  
gamestate = "start"

WHITE = (255, 255, 255)
# -----initialize screen & music ------ #
size = width, height = 1000 , 500 
screen = pygame.display.set_mode(size)
'''TO DO: MAKE FULL SCREEN'''
midiOutput = pygame.midi.Output(pygame.midi.get_default_output_id())
'''TO DO: find ways to get around the midi error message'''

# -----initialize current level (to be changed)
currentMission = MissionTutorial(size, screen)
currentLevel = currentMission.levels[0]
currentExistables = currentLevel["existables"]
currentTerrain = currentLevel["terrains"]
currentCollectibles = currentLevel["collectibles"]
currentMusic = currentMission.music
player = currentMission.player
for (status, data1) in currentMusic["init"]:
    midiOutput.write_short(status, data1)

# -----main pygame loop----- # 
# modified from Pygame Introduction: https://www.pygame.org/docs/tut/PygameIntro.html

startTime = time.time()   
while 1:
    # different state, inspired by https://pythonprogramming.net/pause-game-pygame/ 

    if gamestate == "start":
        gamestate = startscreen(screen, size)
        
    # if gamestate == 0:
    #     gamestate = gamescreen(screen, size, midiOutput, 0)
    #while gamestate == "


    # actual game mode:
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
    # we will do all the moves, and then check legalness later
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_UP]:
        player.move(0, -player.jump, currentExistables)
        '''TO DO: make wall sticky - needs special attention''' 
    if keys[pygame.K_DOWN]:
        player.move(0, player.jump, currentExistables)   
    if keys[pygame.K_LEFT]:
        if (player.x > 0):
            player.move(-10, 0, currentExistables)
        else:
            '''todo: make this prettier?'''
            if currentMission.getPreviousLevel(currentLevel) != None:
                currentLevel = currentMission.getPreviousLevel(currentLevel)
                currentTerrain = currentLevel["terrains"]
                currentExistables = currentLevel["existables"]
                currentCollectibles = currentLevel["collectibles"]
                player.x = width - player.radius    
    if keys[pygame.K_RIGHT]: 
        if (player.x + 10 < width):
            player.move(10, 0, currentExistables) 
        else:
            if currentMission.getNextLevel(currentLevel) != None:
                currentLevel = currentMission.getNextLevel(currentLevel)
                currentTerrain = currentLevel["terrains"]
                currentExistables = currentLevel["existables"]
                currentCollectibles = currentLevel["collectibles"]
                player.x = 0 + player.radius
    # ---check gravity---       
    '''no wall climbing so far'''
    intersectCoord = None
    for i in currentExistables:
        if player.inExistableSpace(i) != None:
            intersectCoord = player.inExistableSpace(i)
    
    # either we are completely not in the terrain
    # or some part of us are in there 
    if intersectCoord == None:      # if in air
        player.doGravity(currentExistables)         
    else:                           # if any part is in terrain    
        player.y = player.getLowerHeight(currentLevel["terrainsDict"]) - player.radius + 1
        player.resetInAir()       

    # ---check for legalness---
    # somehow legalness justwork rn? we will see wtf happens

    # ---draw all the components--- 
    screen.fill(currentMission.colorDict["background"])                
    for terrainType in currentTerrain:
        for terrain in currentTerrain[terrainType]:
            terrain.drawTerrain(screen)
    for note in currentCollectibles:
        note.drawCollectibles(screen)
    player.drawPlayer(screen)
    # DEBUGGING ONLUY
    for i in currentExistables:
        pygame.draw.lines(screen, (204, 0, 102), False, i.outline())
    #print (currentExistables.outline())
    # DEBUGGING ONLY
    pygame.display.flip()

    # ---play music---
    currentTime = (time.time() - startTime) * 1000
    # randomized intervals ??
    music = currentMission.playMusic(currentTime)
    if music != None:
        for (level, (status, data1, data2)) in music:
            midiOutput.write_short(status, data1, data2)

    # ---check collision for music notes---
    # putting this after the draw part so we can get all the rects properly updated
    temp = []
    for note in currentLevel["collectibles"]:
        if player.rect.colliderect(note.rect):  temp.append(note)
    for note in temp:
        currentMission.addMusicNotes(note)
        currentCollectibles.remove(note)
