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
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# -----initialize screen & music ------ #
size = width, height = 1000 , 500 
screen = pygame.display.set_mode(size)
'''TO DO: MAKE FULL SCREEN'''
midiOutput = pygame.midi.Output(pygame.midi.get_default_output_id())

# -----main pygame loop----- # 
# modified from Pygame Introduction: https://www.pygame.org/docs/tut/PygameIntro.html
startTime = time.time()   
while 1:
    # different state, inspired by https://pythonprogramming.net/pause-game-pygame/ 
    if gamestate == "start":
        gamestate = startscreen(screen, size)
        if gamestate == 0:
            currentMission = MissionTutorial(size, screen)
            player = currentMission.setupPlayer()
            for (status, data1) in player.currentMusic["init"]:
                midiOutput.write_short(status, data1)

    # actual game mode:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            for index in range(0, 16):
                for (status, data1, data2) in player.currentMusic[index]:
                    midiOutput.note_off(data1)      
            midiOutput.close()
            del midiOutput              # so we safely exit the midi module
            pygame.midi.quit    
            sys.exit()     
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_p:     # for pausing!
                gamestate = pauseScreen(screen, size)


    # checking pressed keys, inspired from 
    # https://stackoverflow.com/questions/9961563/how-can-i-make-a-sprite-move-when-key-is-held-down 
    # we will do all the moves, and then check legalness later
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_UP]:
        player.move(0, -player.jump, player.currentExistables)
        '''TO DO: make wall sticky - needs special attention''' 
    if keys[pygame.K_DOWN]:
        player.move(0, player.jump, player.currentExistables)   
    if keys[pygame.K_LEFT]:
        if (player.x > 0):
            player.move(-15, 0, player.currentExistables)
        else:
            if currentMission.getPreviousLevel(player.currentLevel) != None:
                levelIndex = currentMission.getPreviousLevel(player.currentLevel)
                player.setupCurrentLevel(currentMission, levelIndex)
                player.x = width - player.radius    
    if keys[pygame.K_RIGHT]: 
        if (player.x + 8 < width):
            player.move(15, 0, player.currentExistables) 
        else:
            if currentMission.getNextLevel(player.currentLevel) != None:
                levelIndex = currentMission.getNextLevel(player.currentLevel)
                player.setupCurrentLevel(currentMission, levelIndex)
                player.x = 0 + player.radius

    # ---check gravity and climbing---   
    intersectSticky = None
    intersectNormal = None  
    for terrain in player.currentExistables["sticky"]:
        if player.inExistableSpace(terrain) != None:
            intersectSticky = player.inExistableSpace(terrain)
            break
    for terrain in player.currentExistables["normal"]:
        if player.inExistableSpace(terrain) != None:
            intersectNormal = player.inExistableSpace(terrain)
            break

    # situation 1: we encounter just solid object:
    if intersectNormal != None:
        player.y = player.getLowerHeight(player.currentLevel["terrainsDict"]) - player.radius + 1
        #player.move(0, 0, player.currentExistables)
        player.resetInAir() 
    # situation 2: we encounter neither
    elif intersectNormal == None and intersectSticky == None:
        player.doGravity(player.currentExistables) 


    # intersectCoord = None
    # intersectType = None
    # for terrainType in player.currentExistables:
    #     for i in player.currentExistables[terrainType]:
    #         if player.inExistableSpace(i) != None:
    #             intersectCoord = player.inExistableSpace(i)
    #             intersectType = terrainType


    # either we are completely not in the terrain
    # or some part of us are in there 
    # if intersectCoord == None:      # if in air
    #     player.doGravity(player.currentExistables)         
    # elif intersectType == "sticky":     # if we encounter a thing where we can wallclimb
    #     pass
    # else:                           # if any part is in terrain    
    #     player.y = player.getLowerHeight(player.currentLevel["terrainsDict"]) - player.radius + 1
    #     player.resetInAir()       

    # ---check if we somehow died---
    intersectCoord = None
    for i in player.currentExistables["dangerous"]:
        if player.inExistableSpace(i) != None:
            index = player.death(screen)
            player.setupCurrentLevel(currentMission, index)

    # ---

    # ---draw all the components--- 
    screen.fill(currentMission.colorDict["background"])   
    for tType in player.currentExistables:          # drawing a maybe pretty outline
        if tType == "dangerous": continue
        for mask in player.currentExistables[tType]:
            pygame.draw.lines(screen, currentMission.colorDict["outline"], False, mask.outline(), 10)             
    #for terrainType in player.currentTerrain:       # draw terrain
    # 1. draw normal terrain
    for terrain in player.currentTerrain["normal"]:    
        terrain.drawTerrain(screen)
    # 2. draw sticky terrain
    for terrain in player.currentTerrain["sticky"]:
        terrain.drawTerrain(screen)
    # 3. draw scary terrain
    for terrain in player.currentTerrain["dangerous"]:
        terrain.drawTerrain(screen)
    # draw collectibles
    for note in player.currentCollectibles:   note.drawCollectibles(screen)
    if player.currentLevel["checkpoint"] != None:   # draw checkpoint
        player.currentLevel["checkpoint"].drawCheckpoint(screen)
    '''DEBUGGING ONLY'''
    #screen.blit(player.deathSprite, (0,0))
    '''DEBUGGING ONLY'''
    player.drawPlayer(screen)                       # draw player
    pygame.display.flip()

    # ---play music---
    currentTime = (time.time() - startTime) * 1000
    music = currentMission.playMusic(currentTime)
    if music != None:
        for (status, data1, data2) in music:
            midiOutput.write_short(status, data1, data2)

    # ---check collision for music notes---
    # putting this after the draw part so we can get all the rects properly updated
    temp = []
    for note in player.currentLevel["collectibles"]:
        if player.rect.colliderect(note.rect):  temp.append(note)
    for note in temp:
        currentMission.addMusicNotes(note)
        player.currentCollectibles.remove(note)
        currentIndex = player.getLevelIndex(currentMission)
        player.uncheckedCollectibles.append((currentIndex, note))     # add to backup

    # ---check collision for checkpoints---
    checkpoint = player.currentLevel["checkpoint"]
    if checkpoint != None:
        if player.rect.colliderect(checkpoint.rect):
            player.toCheckpoint(checkpoint)
