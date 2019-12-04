# gamemodes

import pygame, sys, io, os
from tp_levelMaker import *
pygame.init()



# the screen player sees at first
def startscreen(screen, size):
    width, height = size
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                #sys.exit() 
                running = False
                pygame.quit()
                os._exit(0)
            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_RETURN: 
                    return "name"

        welcomeTextFont = pygame.font.SysFont("monospace", 50)
        welcomeText = welcomeTextFont.render("welcome to this shitty game!", 1, (214, 198, 163))
        welcomeTextSize = welcomeTextFont.size("welcome to this shitty game!")

        tutorialTextFont = pygame.font.SysFont("monospace", 30)
        tutorialText = tutorialTextFont.render("press ENTER/RETURN to start this shitty game", 1, (214, 198, 163))
        tutorialTextSize = tutorialTextFont.size("press ENTER/RETURN to start this shitty game")

        # for fonts with color https://stackoverflow.com/questions/10077644/python-display-text-with-font-color
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
                sys.exit()  
            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_RETURN: 
                    return userInput
                elif event.key == pygame.K_BACKSPACE:   
                    if len(userInput) > 0: 
                        userInput = userInput[:-1]
                else:
                    userInput += chr(event.key)

        nameTextFont = pygame.font.SysFont("monospace", 50)
        nameText = nameTextFont.render("Please enter your name: ", 1, (214, 198, 163))
        nameTextSize = nameTextFont.size("Please enter your name: ")

        enterTextFont = pygame.font.SysFont("monospace", 50)
        enterText = enterTextFont.render("press ENTER/RETURN when done", 1, (214, 198, 163))
        enterTextSize = enterTextFont.size("press ENTER/RETURN when done")

        inputTextFont = pygame.font.SysFont("monospace", 50)
        inputText = inputTextFont.render(userInput, 1, (214, 198, 163))
        inputTextSize = inputTextFont.size(userInput)

        screen.fill((172, 156, 156))
        screen.blit(nameText, (width//2 - nameTextSize[0]//2, height // 5))
        screen.blit(inputText, (width//2 - inputTextSize[0]//2, height // 5 * 3))
        screen.blit(enterText, (width//2 - enterTextSize[0]//2, height // 5 * 4))
        pygame.display.update()

# referenced from 112 website for file io
def getLevels():
    levels = []
    for path in os.listdir("level_info"):
        if not os.path.isfile("level_info" + os.sep + path):
            if path == "m0":
                levels.append((path, "Tutorial"))
            elif path.startswith("m"):
                levels.append((path, "Level" + path[1]))
    return levels

def levelSelectScreen(screen, size, userInput): 
    textFont = pygame.font.SysFont("comfortaa", 50) 
    width, height = size
    levelText, levelTextSize = [], []
    margin = 50
    levels = getLevels()
    numberOfLevels = len(levels)
    for i in range(numberOfLevels):
        level = levels[i]
        levelText.append(textFont.render(level[1], 1, (214, 198, 163)))
        levelTextSize.append(textFont.size(level[1]))
        
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()  
            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_RETURN: 
                    return 0
  
        welcomeTextFont = pygame.font.SysFont("monospace", 50)
        welcomeText = welcomeTextFont.render(f"Welcome, {userInput}", 1, (214, 198, 163))
        welcomeTextSize = welcomeTextFont.size(f"Welcome, {userInput}")

        enterTextFont = pygame.font.SysFont("monospace", 50)
        enterText = enterTextFont.render("press ENTER/RETURN to go to game", 1, (214, 198, 163))
        enterTextSize = enterTextFont.size("press ENTER/RETURN to go to game")

        screen.fill((172, 156, 156))
        screen.blit(welcomeText, (width//2 - welcomeTextSize[0]//2, height // 5))
        screen.blit(enterText, (width//2 - enterTextSize[0]//2, height // 5 * 3))

        # levelText, levelTextSize = [], []
        # margin = 50
        # numberOfLevels = len(getLevels())
        
        # for i in range(numberOfLevels):
        #     level = numberOfLevels[i]
        #     levelText.render(textFont.render(level[1], 1, (214, 198, 163)))
        #     levelTextSize.append(textFont.size(level[1]))
        
        #or levelNumber in range(numberOfLevels):


        
        pygame.display.update()

# the ending screen when the player gets to the end   
def endingScreen(screen, size):     
    width, height = size
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()  
            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_RETURN: 
                    return levelSelectScreen(screen, size, "yeet")
  
        congratsTextFont = pygame.font.SysFont("monospace", 50)
        congratsText = congratsTextFont.render(f"Good job!!", 1, (214, 198, 163))
        congratsTextSize = congratsTextFont.size(f"Good job!!")

        enterTextFont = pygame.font.SysFont("monospace", 50)
        enterText = enterTextFont.render("press ENTER/RETURN to go back to level selection", 1, (214, 198, 163))
        enterTextSize = enterTextFont.size("press ENTER/RETURN to go back to level selection")

        screen.fill((172, 156, 156))
        screen.blit(congratsText, (width//2 - congratsTextSize[0]//2, height // 5))
        screen.blit(enterText, (width//2 - enterTextSize[0]//2, height // 5 * 3))
        pygame.display.update()

# for when player wants to pause the
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

        pauseFont = pygame.font.SysFont("monospace", 50)
        pauseText = pauseFont.render("Paused", 1, (214, 198, 163))
        pauseTextSize = pauseFont.size("Paused")

        resumeFont = pygame.font.SysFont("monospace", 50)
        resumeText = resumeFont.render("press P to resume", 1, (214, 198, 163))
        resumeTextSize = resumeFont.size("press P to resume")
        
        screen.fill((172, 156, 156))
        screen.blit(pauseText, (width//2 - pauseTextSize[0]//2, height // 5))
        screen.blit(resumeText, (width//2 - resumeTextSize[0]//2, height // 5*3))
        pygame.display.update()
