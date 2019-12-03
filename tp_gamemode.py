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
                if event.key == pygame.K_RETURN: 
                    return nameScreen(screen, size)

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
                    return levelSelectScreen(screen, size, userInput)
                    #return 0
                elif event.key == pygame.K_BACKSPACE:   # 
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


def levelSelectScreen(screen, size, userInput):  
    width, height = size
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
        pygame.display.update()

# the ending screen when the player gets to the end
#     
def endingScreen(screen, size):     pass

# for when player wants to pause the
def pauseScreen(screen, size):  
    width, height = size
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()  
            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_RETURN: 
                    return 0 

        pauseFont = pygame.font.SysFont("monospace", 50)
        pauseText = welcomeTextFont.render("paused or some shit", 1, (214, 198, 163))
        pauseTextSize = welcomeTextFont.size("paused or some shit")

        resumeFont = pygame.font.SysFont("press ENTER/RETURN to resume", 50)
        resumeText = welcomeTextFont.render("press ENTER/RETURN to resume", 1, (214, 198, 163))
        resumeTextSize = welcomeTextFont.size("press ENTER/RETURN to resume")
        
        screen.fill((172, 156, 156))
        screen.blit(pauseFont, (width//2 - pauseTextSize[0]//2, height // 5))
        screen.blit(resumeFont, (width//2 - resumeTextSize[0]//2, height // 5*3))
        pygame.display.update()

