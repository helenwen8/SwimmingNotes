# gamemodes

import pygame, sys
from tp_levelMaker import *
pygame.init()

# the screen player sees at first
def startscreen(screen, size):
    width, height = size
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()  
            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_0: 
                    return 0

        welcomeTextFont = pygame.font.SysFont("monospace", 50)
        welcomeText = welcomeTextFont.render("welcome to this shitty game!", 1, (214, 198, 163))
        welcomeTextSize = welcomeTextFont.size("welcome to this shitty game!")

        tutorialTextFont = pygame.font.SysFont("monospace", 30)
        tutorialText = tutorialTextFont.render("press 0 to start this shitty game", 1, (214, 198, 163))
        tutorialTextSize = tutorialTextFont.size("press 0 to start this shitty game")


        # for fonts with color https://stackoverflow.com/questions/10077644/python-display-text-with-font-color
        screen.fill((172, 156, 156))
        #print ("wtf")
        screen.blit(welcomeText, (width//2 - welcomeTextSize[0]//2, height // 5))
        screen.blit(tutorialText, (width//2 - tutorialTextSize[0]//2, height // 5*3))
        pygame.display.update()
    

#def getMission(level):
    
# def gamescreen(screen, size, midiOutput, level):
#     currentMission = MissionTutorial(size, screen)
#     currentLevel = currentMission.levelOne
#     currentExistables = currentLevel["existables"]
#     currentTerrain = currentLevel["terrains"]
#     currentCollectibles = currentLevel["collectibles"]
#     currentMusic = currentMission.music
#     player = currentMission.player
#     for (status, data1) in currentMusic["init"]:
#         midiOutput.write_short(status, data1)
#         # actual game mode:

#     while 1: 
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT: 
#                 for index in range(0, 16):
#                     for (level, (status, data1, data2)) in currentMusic[index]:
#                         midiOutput.note_off(data1)      # this works for now but..
#                 midiOutput.close()
#                 del midiOutput              # so we safely exit the midi module
#                 pygame.midi.quit    
#                 sys.exit()                  

#         # checking pressed keys, inspired from 
#         # https://stackoverflow.com/questions/9961563/how-can-i-make-a-sprite-move-when-key-is-held-down 
#         # we will do all the moves, and then check legalness later
#         keys = pygame.key.get_pressed() 
#         if keys[pygame.K_UP]:
#             player.move(0, -player.jump, currentExistables)
#             '''TO DO: make wall sticky - needs special attention''' 
#         if keys[pygame.K_DOWN]:
#             player.move(0, player.jump, currentExistables)   
#         if keys[pygame.K_LEFT]:
#             if (player.x > 0):
#                 player.move(-10, 0, currentExistables)
#             else:
#                 '''todo: make this prettier?'''
#                 if currentMission.getPreviousLevel(currentLevel) != None:
#                     currentLevel = currentMission.getPreviousLevel(currentLevel)
#                     currentTerrain = currentLevel["terrains"]
#                     currentExistables = currentLevel["existables"]
#                     currentCollectibles = currentLevel["collectibles"]
#                     player.x = width - player.radius    
#         if keys[pygame.K_RIGHT]: 
#             if (player.x + 10 < width):
#                 player.move(10, 0, currentExistables) 
#             else:
#                 if currentMission.getNextLevel(currentLevel) != None:
#                     currentLevel = currentMission.getNextLevel(currentLevel)
#                     currentTerrain = currentLevel["terrains"]
#                     currentExistables = currentLevel["existables"]
#                     currentCollectibles = currentLevel["collectibles"]
#                     player.x = 0 + player.radius
#         # ---check gravity---       
#         '''no wall climbing so far'''
#         intersectCoord = None
#         for i in currentExistables:
#             if player.inExistableSpace(i) != None:
#                 intersectCoord = player.inExistableSpace(i)
        
#         # either we are completely not in the terrain
#         # or some part of us are in there 
#         if intersectCoord == None:      # if in air
#             player.doGravity(currentExistables)         
#         else:                           # if any part is in terrain 
#             # -1 so it doesn't keep bouncing        
#             player.y = player.getLowerHeight(currentLevel["terrainsDict"]) - player.radius + 1
#             player.resetInAir()       

#         # ---check for legalness---



#         # ---draw all the components--- 
#         screen.fill(currentMission.colorDict["background"])                
#         for terrainType in currentTerrain:
#             for terrain in currentTerrain[terrainType]:
#                 terrain.drawTerrain(screen)
#         for note in currentCollectibles:
#             note.drawCollectibles(screen)
#         player.drawPlayer(screen)

#         # DEBUGGING ONLUY
#         for i in currentExistables:
#             pygame.draw.lines(screen, (204, 0, 102), False, i.outline())
#         #print (currentExistables.outline())
#         # DEBUGGING ONLY
#         pygame.display.flip()

#         # ---play music---
#         currentTime = (time.time() - startTime) * 1000
#         # randomized intervals ??
#         music = currentMission.playMusic(currentTime)
#         if music != None:
#             for (level, (status, data1, data2)) in music:
#                 midiOutput.write_short(status, data1, data2)


            

#         # ---check collision---
#         # putting this after the draw part so we can get all the rects properly updated
#         #pygame.draw.lines(screen, (200, 150, 150), 1, currentExistables.outline())
#         temp = []
#         for note in currentLevel["collectibles"]:
#             if player.rect.colliderect(note.rect):  temp.append(note)
#         for note in temp:
#             currentMission.addMusicNotes(note)
#             currentCollectibles.remove(note)

