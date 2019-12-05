# tp_gamemodes.py
# make different modes for different screens

import pygame, sys, io, os
from tp_levelMaker import *
pygame.init()

FONT = pygame.font.SysFont("helvetica", 50)

# for fonts with color https://stackoverflow.com/questions/10077644/python-display-text-with-font-color

# the screen player sees at first
def startscreen(screen, size):
    width, height = size
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                os._exit(0)
            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_RETURN: 
                    return "name"

        welcomeText = FONT.render("Welcome to Swimming Notes", 1, (214, 198, 163))
        welcomeTextSize = FONT.size("Welcome to Swimming Notes")
        tutorialText = FONT.render("press ENTER/RETURN to begin", 1, (214, 198, 163))
        tutorialTextSize = FONT.size("press ENTER/RETURN to begin")
        screen.fill((172, 156, 156))
        screen.blit(welcomeText, (width//2 - welcomeTextSize[0]//2, height // 5))
        screen.blit(tutorialText, (width//2 - tutorialTextSize[0]//2, height // 5*3))
        pygame.display.update()

def nameScreen(screen, size):
    width, height = size
    userInput = ""
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                os._exit(0)
            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_RETURN: 
                    return userInput
                elif event.key == pygame.K_BACKSPACE:   
                    if len(userInput) > 0: 
                        userInput = userInput[:-1]
                else:
                    userInput += chr(event.key)

        nameText = FONT.render("Please enter your name: ", 1, (214, 198, 163))
        nameTextSize = FONT.size("Please enter your name: ")
        enterText = FONT.render("press ENTER/RETURN when done", 1, (214, 198, 163))
        enterTextSize = FONT.size("press ENTER/RETURN when done")

        inputText = FONT.render(userInput, 1, (214, 198, 163))
        inputTextSize = FONT.size(userInput)

        screen.fill((172, 156, 156))
        screen.blit(nameText, (width//2 - nameTextSize[0]//2, height // 5))
        screen.blit(inputText, (width//2 - inputTextSize[0]//2, height // 5 * 3))
        screen.blit(enterText, (width//2 - enterTextSize[0]//2, height // 5 * 4))
        pygame.display.update()

# referenced from 112 website for file io
def getLevels():
    levels = []
    for path in sorted(os.listdir("game_info/level_info")):
        if not os.path.isfile("game_info/level_info" + os.sep + path):
            if path == "m0":
                levels.append((path, "Tutorial"))
            elif path.startswith("m"):
                levels.append((path, "Level" + path[1]))
    return levels

def levelSelectScreen(screen, size, userInput): 
    width, height = size
    levelText, levelTextSize = [], []
    levels = getLevels()
    numberOfLevels = len(levels)
    numberOfGaps = numberOfLevels * 3 + 1 
    gap = width // numberOfGaps
    selected = 0        # first select the tutorial level  
    # get the renders ready
    for i in range(numberOfLevels):
        level = levels[i]
        levelTextSize.append(FONT.size(level[1]))
        
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                os._exit(0) 
            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_RETURN: 
                    return levels[selected][0]  # return a path
                if event.key == pygame.K_RIGHT:
                    if selected < numberOfLevels - 1:
                        selected += 1
                if event.key == pygame.K_LEFT:
                    if selected > 0:
                        selected -= 1
  
        welcomeText = FONT.render(f"Welcome, {userInput}", 1, (214, 198, 163))
        welcomeTextSize = FONT.size(f"Welcome, {userInput}")
        selectText = FONT.render("use LEFT/RIGHT to select levels", 1, (214, 198, 163))
        selectTextSize = FONT.size("use LEFT/RIGHT to select levels")
        enterText = FONT.render("press ENTER/RETURN to go to game", 1, (214, 198, 163))
        enterTextSize = FONT.size("press ENTER/RETURN to go to game")

        screen.fill((172, 156, 156))
        screen.blit(welcomeText, (width//2 - welcomeTextSize[0]//2, height // 5 * 0.8))
        screen.blit(selectText, (width//2 - selectTextSize[0]//2, height // 5 * 3.5))
        screen.blit(enterText, (width//2 - enterTextSize[0]//2, height // 5 * 4))

        # draw the boxes and the texts
        for i in range(1, numberOfGaps, 3):
            coord = ( (i * gap, height//5*1.8) , ((i+2) * gap, height//5*1.8),
                    ((i+2) * gap, height//5*2.8), (i * gap, height//5*2.8) )
            index = i // 3      
            text = FONT.render(levels[index][1], 1, (85, 110, 111))
            if index == selected:      # draw the box differently
                pygame.draw.polygon(screen, (217, 211, 143), coord)
            else:
                pygame.draw.polygon(screen, (234, 235, 235), coord)
            screen.blit(text, ( ((i+1)*gap - levelTextSize[index][0]//2), 
                             height//5*2.3 - levelTextSize[index][1]//2) )

        pygame.display.update()

# the ending screen when the player gets to the end   
def endingScreen(screen, size):     
    width, height = size
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                os._exit(0) 
            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_RETURN: 
                    return "level select"
  
        congratsText = FONT.render(f"Good job!!", 1, (214, 198, 163))
        congratsTextSize = FONT.size(f"Good job!!")
        enterText = FONT.render("press ENTER/RETURN to go back to level selection", 1, (214, 198, 163))
        enterTextSize = FONT.size("press ENTER/RETURN to go back to level selection")

        screen.fill((172, 156, 156))
        screen.blit(congratsText, (width//2 - congratsTextSize[0]//2, height // 5))
        screen.blit(enterText, (width//2 - enterTextSize[0]//2, height // 5 * 3))
        pygame.display.update()

# teach you how to play the game - shows up on the tutorial screen
def helpScreen(screen, size):
    width, height = size
    helpFont = pygame.font.SysFont("helvetica", 30)
    helpTexts = []

    helpTexts.append(FONT.render("Help Screen", 1, (214, 198, 163)))
    helpTexts.append(helpFont.render("Your goal is to collect all the music notes!", 1, (214, 198, 163)))
    helpTexts.append(helpFont.render("As you collect more musical notes...", 1, (214, 198, 163)))
    helpTexts.append(helpFont.render("...the soundtrack would get more complex!", 1, (214, 198, 163)))
    helpTexts.append(helpFont.render("Do not touch anything that is red - they will kill you.", 1, (214, 198, 163)))
    helpTexts.append(helpFont.render("Use anything not red to your advantage...", 1, (214, 198, 163)))
    helpTexts.append(helpFont.render(" ...you can swim through them and get to where you want!", 1, (214, 198, 163)))
    helpTexts.append(helpFont.render("Use arrow keys to move your player", 1, (214, 198, 163)))
    helpTexts.append(helpFont.render("Press p if you need to pause.", 1, (214, 198, 163)))
    helpTexts.append(helpFont.render("Press h if you need to pull up this help screen.", 1, (214, 198, 163)))
    helpTexts.append(FONT.render("press h to go to game", 1, (214, 198, 163)))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                os._exit(0) 
            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_h: 
                    return "game"
        
        screen.fill((172, 156, 156))
        for i in range(len(helpTexts)):
           screen.blit(helpTexts[i], (100, height // (len(helpTexts)+1) * (i+1)))
        pygame.display.update()

# for when player wants to pause the game
def pausescreen(screen, size):  
    width, height = size
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                os._exit(0) 
            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_p: 
                    return "game"

        pauseText = FONT.render("Game Paused", 1, (214, 198, 163))
        pauseTextSize = FONT.size("Game Paused")

        resumeText = FONT.render("press P to resume", 1, (214, 198, 163))
        resumeTextSize = FONT.size("press P to resume")
        
        screen.fill((172, 156, 156))
        screen.blit(pauseText, (width//2 - pauseTextSize[0]//2, height // 5))
        screen.blit(resumeText, (width//2 - resumeTextSize[0]//2, height // 5*3))
        pygame.display.update()
