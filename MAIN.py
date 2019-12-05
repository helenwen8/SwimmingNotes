# MAIN.py
# this is the file to assemble everything together 

import sys, copy, random, time
import pygame, pygame.midi, pygame.mask
from tp_miscellaneous import * 
from tp_missions import *
from tp_levelMaker import *
from tp_gamemode import *

# -----initialize pygame/pygame.midi----- #
pygame.init()  
pygame.midi.init()
gamestate = "start"
name = None
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
# some fun notes
WIN_NOTES = (0, 2, 4, 5, 7, 9, 11, 12)    #  it is a major scale!

# -----initialize screen & music ------ #
size = width, height = 1000 , 500 
screen = pygame.display.set_mode(size)
midiOutput = pygame.midi.Output(pygame.midi.get_default_output_id())

# -----main pygame loop----- # 
# modified from Pygame Introduction: https://www.pygame.org/docs/tut/PygameIntro.html
startTime = time.time()   
while 1:
    # ---different state---
    # inspired by https://pythonprogramming.net/pause-game-pygame/ 
    if gamestate == "start":
        gamestate = startscreen(screen, size)
    if gamestate == "name":
        name = nameScreen(screen, size)
        gamestate = "level select"
    if gamestate == "level select":
        gamestate = levelSelectScreen(screen, size, name)
    if gamestate == "pause":
        gamestate = pausescreen(screen, size)
    if gamestate == "help":
        gamestate = helpScreen(screen, size)
    if gamestate.startswith("m"):
        currentMission = MissionSetup(size, screen, gamestate)
        player = currentMission.setupPlayer()
        # set up the instruments
        for (status, data1) in player.currentMusic["init"]:
            midiOutput.write_short(status, data1)
        if gamestate == "m0":
            gamestate = helpScreen(screen, size)
        gamestate = "game"

    # actual game mode:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            for i in range(8):          # turn off all the notes
                for (status, data1, data2) in player.currentMusic[i]:
                    if (status >= 0x80 and status <= 0x8F):
                        midiOutput.write_short(status, data1, data2)
            midiOutput.close()
            del midiOutput              # so we safely exit the midi module
            pygame.midi.quit  
            pygame.quit()  
            os._exit(0)                 # elegantly closing our window
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_p:     # for pausing!
                gamestate = "pause"

    # ---movement---
    # checking pressed keys, inspired from 
    # https://stackoverflow.com/questions/9961563/how-can-i-make-a-sprite-move-when-key-is-held-down 
    # we will do all the moves, and then check legalness later
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_UP]:
        player.move(0, -1)
    if keys[pygame.K_DOWN]:
        player.move(0, 1)
    if keys[pygame.K_LEFT]:
        if (player.x > 0):
            player.move(-1, 0)
        else:
            if currentMission.getPreviousLevel(player.currentLevel) != None:
                levelIndex = currentMission.getPreviousLevel(player.currentLevel)
                player.setupCurrentLevel(currentMission, levelIndex)
                player.x = width - player.radius    
    if keys[pygame.K_RIGHT]: 
        if (player.x + 15 < width):
            player.move(1, 0)
        else:
            if currentMission.getNextLevel(player.currentLevel) != None:
                levelIndex = currentMission.getNextLevel(player.currentLevel)
                player.setupCurrentLevel(currentMission, levelIndex)
                player.x = 0 + player.radius
    player.checkLegal()

    # ---check if we died---
    intersectCoord = None
    if not player.isDead:
        for i in player.currentExistables["dangerous"]:
            if player.inExistableAxis(i) != None:
                for (status, data1, data2) in player.currentMusic[index]:
                    if status >= 0x80 and status <= 0x8F:
                        midiOutput.write_short(status, data1, data2)
                midiOutput.write_short(0x90, currentMission.tonic, 127)
                midiOutput.write_short(0x90, currentMission.tonic + 1, 127)
                midiOutput.write_short(0x90, currentMission.tonic + 2, 127)
                deathtime = time.time()
                player.isDead = True

    # ---draw all the components--- 
    # draw background
    screen.fill(currentMission.colorDict["background"])   
    # draw decorations
    currentTime = (time.time() - startTime) * 1000
    currentMission.drawMusicDecorations(currentTime, screen, size)               
    # draw normal terrain
    for terrain in player.currentTerrain["normal"]:    
        terrain.drawTerrain(screen)
    # draw scary terrain to overlay on top of normal terrains
    for terrain in player.currentTerrain["dangerous"]:
        terrain.drawTerrain(screen)
    # draw collectibles
    for note in player.currentCollectibles:   
        note.drawCollectibles(screen)
    # draw checkpoint
    if player.currentLevel["checkpoint"] != None:   
        player.currentLevel["checkpoint"].drawCheckpoint(screen)
    # draw endgoal
    if player.currentLevel["endpoint"] != None:    
        player.currentLevel["endpoint"].drawEndpoint(screen)
    # draw player
    player.drawPlayer(screen) 
    # update screen
    pygame.display.flip()   
    # sleep for a little bit if player is dead
    if player.isDead and (time.time() - deathtime) >= 1.1:
        player.isDead = False
        index = player.death(screen)
        player.setupCurrentLevel(currentMission, index) 
    # play ending tone!    
    if player.win:
        if (time.time() - endtime) >= 1.6:
            # turn notes off after we played it
            for i in range(0, 8):       
                midiOutput.write_short(0x80, WIN_NOTES[index] + currentMission.tonic, 127)
            gamestate = endingScreen(screen, size)      # select another level
            currentMission = None
            continue                # start from beginning of the loop
        # we just won - play ending tone
        elif (time.time() - endtime) * 1000 % 200 <= 50:   
            index = int((time.time() - endtime) * 1000 // 200 % 8)
            midiOutput.write_short(0x90,WIN_NOTES[index] + currentMission.tonic, 127)

    # ---play music--- using currentTime from the drawing part
    music = currentMission.playMusic(currentTime)
    if music != None:
        for (status, data1, data2) in music:
            midiOutput.write_short(status, data1, data2)

    # ---collision stuff---
    # music notes
    temp = []
    for note in player.currentLevel["collectibles"]:
        if player.rect.colliderect(note.rect):  temp.append(note)
    for note in temp:
        currentMission.addMusicNotes(note)
        player.currentCollectibles.remove(note)
        currentIndex = player.getLevelIndex(currentMission)
        player.uncheckedCollectibles.append((currentIndex, note))     # add to backup
    # checkpoints
    checkpoint = player.currentLevel["checkpoint"]
    if checkpoint != None:
        if player.rect.colliderect(checkpoint.rect):
            if checkpoint.isChecked == False:
                player.toCheckpoint(checkpoint)
                # play some sounds
                midiOutput.write_short(0x90, currentMission.tonic, 127)
                midiOutput.write_short(0x90, currentMission.tonic + 12, 127)
                midiOutput.write_short(0x90, currentMission.tonic + 4, 127)
                midiOutput.write_short(0x90, currentMission.tonic + 7, 127)
            
    # endpoint
    index = player.getLevelIndex(currentMission)
    if index == len(currentMission.levels) - 1:
        if (player.rect.colliderect(player.currentLevel["endpoint"].rect) and
            not player.win):
            # turn off all the notes
            for i in range(8):              
                for (status, data1, data2) in player.currentMusic[i]:
                    if (status >= 0x80 and status <= 0x8F): 
                        midiOutput.write_short(status, data1, data2)
            player.win = True
            player.x, player.y = player.currentLevel["endpoint"].center   
            endtime = time.time()
