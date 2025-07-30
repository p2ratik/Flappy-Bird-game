import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import time 
import pygame
from pygame.locals import * # Basic pygame imports

# Initializing pygame 
FPS = 32
GAME_SPIRITS = {}
SCREENHEIGHT = 512
SCREENWIDTH = 288
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
BACKGROUND = 'assets/background-night.png'
BASE = 'assets/base.png'
PLAYER = 'assets/redbird-midflap.png'

def welcome_screen():
    """
    Welcome Screen for the flappy bird game 
    """
    playerx = 60
    playery = SCREENHEIGHT//4.8
    base_y = GAME_SPIRITS['background'].get_height()-GAME_SPIRITS['base'].get_height()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == K_ESCAPE or event.type==K_DOWN):
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:    
                SCREEN.blit(GAME_SPIRITS['background'], (0,0))
                SCREEN.blit(GAME_SPIRITS['base'], (0, base_y))
                SCREEN.blit(GAME_SPIRITS['welcome'], (SCREENWIDTH//4, SCREENHEIGHT//4))
                SCREEN.blit(GAME_SPIRITS['player'], (playerx, playery))
                pygame.display.update()
                FPSCLOCK.tick(FPS)    

def maingame():
    """
    Includes the core logic of the game , such as movement of pipes, bird, calculating scores and blitting it on the screen
    """
    playerx = 20
    playery = SCREENHEIGHT // 5


    pipe1 = getRandomPipe()
    pipe2 = getRandomPipe()

    score = 0

    upperPipes = [pipe1[0], pipe2[0]]
    lowerPipes = [pipe1[1], pipe2[1]]

    upperPipes[1]['x'] = SCREENWIDTH//2
    lowerPipes[1]['x'] = SCREENWIDTH//2

    base_y = GAME_SPIRITS['background'].get_height()-GAME_SPIRITS['base'].get_height()

    veloPlayer = -8         #Velocity when bird goes up
    veloPipe = -6.5         #Velocity at which pipe moves
    accPlayer = 1           #Gravity on the bird (downwards)
    velomax = 9             #Maximum velocity of the bird
    playerFlap = False      

    while True:
        veloPipe -=0.025    #Increasing velocity of the pipe every iteration
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == K_ESCAPE or event.type==K_DOWN):
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery>0:
                    veloPlayer = -8                   
                    playerFlap = True

        #Applying gravity for downward motion
        if veloPlayer<velomax and not playerFlap :
            veloPlayer +=accPlayer

        else:
                playerFlap = False

        #Updating bird's y coordinate
        if(playery+veloPlayer<base_y):
            playery = playery +veloPlayer     

        #Checking for collision
        if(isCollide(playerx,playery, upperPipes, lowerPipes, base_y)):
            SCREEN.blit(GAME_SPIRITS['gameover'], (50, 50))
            pygame.display.update()
            FPSCLOCK.tick(FPS) 
            time.sleep(2)   
            sys.exit()

        #Calculating score of the user
        playerMidPos = playerx + GAME_SPIRITS['player'].get_width()/2
        pipeMidPos = lowerPipes[0]['x'] + GAME_SPIRITS['pipe'][0].get_width()/2

        if(pipeMidPos<= playerMidPos< pipeMidPos+4):
            score+=1
            print(f"Your score is {score}")

       
        #Applying velocity on the pipes
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] +=veloPipe
            lowerPipe['x'] +=veloPipe

        #Adding new pipes 
        if upperPipes[-1]['x']< GAME_SPIRITS['pipe'][0].get_width():
            new_pipe = getRandomPipe()
            upperPipes.append(new_pipe[0])
            lowerPipes.append(new_pipe[1])

        #Removing the current pipe when it reaches outside the screen 
        if upperPipes[0]['x'] < - GAME_SPIRITS['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)


        #Blitting everything             
        SCREEN.blit(GAME_SPIRITS['background'], (0,0))
        SCREEN.blit(GAME_SPIRITS['base'], (0, base_y))
        SCREEN.blit(GAME_SPIRITS['player'], (playerx, playery))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            
            SCREEN.blit(GAME_SPIRITS['pipe'][0], (upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPIRITS['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        pygame.display.update()
        FPSCLOCK.tick(FPS)      
    


def getRandomPipe():
    """
    Generates a random set of upper and lower pipes which will be used in the flappy bird game 
    """
    #Setting gap between the uper and lower pipe
    gap = 150       
    y_lower = random.randrange(int(SCREENHEIGHT*0.4), int(SCREENHEIGHT*0.7))
    y_upper = (y_lower)-(GAME_SPIRITS['pipe'][0].get_height()+gap)

    return [
        {'x':SCREENWIDTH-30, 'y':y_upper},
        {'x':SCREENWIDTH-30, 'y':y_lower}
    ]

def isCollide(playerx, playery, upperPipes, lowerPipes, base_y):
    """
    Function to check collision of the bird with the ground or any pipes
    """
    if (playery<0 or playery+GAME_SPIRITS['player'].get_height()>base_y):
        return True
    
    #Checking collision with lower pipe
    if (playery+GAME_SPIRITS['player'].get_height()>lowerPipes[0]['y'] and abs(playerx-lowerPipes[0]['x'])<50):
        return True

    #Checking collison with upper pipe
    if (playery<upperPipes[0]['y']+GAME_SPIRITS['pipe'][0].get_height() and abs(playerx-upperPipes[0]['x'])<50):
        return True

     
if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Pratik')

    #Loading images and background for the game
    GAME_SPIRITS['background'] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPIRITS['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPIRITS['base'] = pygame.image.load('assets/base.png').convert_alpha()
    GAME_SPIRITS['welcome'] = pygame.image.load('assets/message.png').convert_alpha()
    GAME_SPIRITS['gameover'] = pygame.image.load('assets/gameover.png').convert_alpha()
    GAME_SPIRITS['pipe'] = (pygame.image.load('assets/pipe-red.png').convert_alpha(), pygame.image.load('assets/pipe-green.png').convert_alpha())

    #Game loop
    while True:
        welcome_screen()
        maingame()
