#Sanyukta Prkash Mudakannavar
#Period 6
#yi_spaceInvaders.py
#14/6/18
import pygame, sys, time, random
from pygame.locals import *

#set up clock/time
mainClock = pygame.time.Clock()

# BUG- keeps shooting until shield is gone for some reason
pygame.init()
# set up the window
WINDOWWIDTH = 700
WINDOWHEIGHT = 700
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Space Invaders')


# set up direction variables
RIGHT = 'right'
LEFT = 'left'
STOP = 'stop'


MOVESPEED = 6
PLAYERSPEED = 8
BULLETSPEED = 15
# set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

#Bullet Height & Width
BWIDTH= 5
BHEIGHT = 15

#Bullet Height & Width
EWIDTH= 10
EHEIGHT = 15

#Bomb Height & Width
BBWIDTH= 10
BBHEIGHT = 15

#Player Width & Height
PWIDTH= 50
PHEIGHT = 20 

#Shield Width & Height
SWIDTH= 65
SHEIGHT = 40 

# Invader Width & Height
INVWIDTH=40
INVHEIGHT=40

# Height to stop the game
STOPHEIGHT=WINDOWHEIGHT - 200
#
invaders = {'rect':pygame.Rect(0, 0, 0, 0), 'color':GREEN, 'dir':0, 'hit':'N'}

#Number of space invaders
NOROWS=4
NOCOLUMNS=5

invadersList = [[invaders for x in range(NOCOLUMNS)] for y in range(NOROWS)]

# the coordinate where the space invaders will start painting
# 
STARTPOINTLEFT=(WINDOWWIDTH/3) - (INVWIDTH * NOCOLUMNS)
STARTPOINTHEIGHT= (WINDOWHEIGHT/3) - (INVHEIGHT * NOROWS)

# STARTPOINTHEIGHT=400
# set up pygame


def drawWords(surface,desiredWord,coordinateX,coordinateY):
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj = fontObj.render(desiredWord, True, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (coordinateX, coordinateY)
    surface.blit(textSurfaceObj,textRectObj)

def bulletShieldCheck(shield,bullet,edge):
    if bullet['rect'].colliderect(shield['rect']) and shield['color'] == RED:
        bullet['rect'].left = edge['rect'].left + (EWIDTH/2)
        bullet['rect'].top = edge['rect'].top 
        bulletFired = False
        shield['rect'].height -=5
        if shield['rect'].height == 10:
            shield['color'] = BLACK
         
def bombShieldCheck(shield,bomb,bombActive):
    if bomb['rect'].colliderect(shield['rect']) and shield['color'] == RED:
        bombActive = False
        shield['rect'].height -=5
        if shield['rect'].height == 10:
            shield['color'] = BLACK
    return bombActive
                
    
def main():
    
    score=0
    lEdge=False
    rEdge=False
    direction=RIGHT
    isInContact = False
    bulletFired = False
    player = {'rect':pygame.Rect((WINDOWWIDTH/2), (WINDOWHEIGHT-(PHEIGHT+5)), PWIDTH, PHEIGHT), 'color':BLUE}
    edge = {'rect':pygame.Rect((WINDOWWIDTH/2 + EWIDTH/2), (WINDOWHEIGHT-(PHEIGHT+5)- EHEIGHT), EWIDTH, EHEIGHT), 'color':BLUE}
    #this hides the bullet before it is shot
    bullet = {'rect':pygame.Rect((WINDOWWIDTH/2 + EWIDTH/2), (WINDOWHEIGHT-(PHEIGHT+5)- EHEIGHT), BWIDTH, BHEIGHT), 'color':WHITE}
    shield1= {'rect':pygame.Rect((WINDOWWIDTH/4 + 20 ), (edge['rect'].top-100),SWIDTH,SHEIGHT), 'color':RED}
    shield2= {'rect':pygame.Rect((WINDOWWIDTH/2 + 20), (edge['rect'].top-100),SWIDTH,SHEIGHT),'color':RED}
    shield3= {'rect':pygame.Rect(((3*WINDOWWIDTH)/4 + 20),(edge['rect'].top-100),SWIDTH,SHEIGHT), 'color':RED}
    shield4= {'rect':pygame.Rect((20), (edge['rect'].top-100),SWIDTH,SHEIGHT), 'color':RED}
    #sheild2= {'rect':pygame.Rect((WINDOWWIDTH/2 + 20), (edge['rect'].top-100),SWIDTH,SHEIGHT),'color':RED}
    shield3= {'rect':pygame.Rect(((3*WINDOWWIDTH)/4 + 20),(edge['rect'].top-100),SWIDTH,SHEIGHT), 'color':RED}
    shield4= {'rect':pygame.Rect((20), (edge['rect'].top-100),SWIDTH,SHEIGHT), 'color':RED}
    #
    
    bomb = {'rect':pygame.Rect(0, 0, BBWIDTH, BBHEIGHT), 'color':WHITE}
    lives = 5
    livesBoard = 'Lives:'+str(lives)
    # Drop bombs 
    #  
    invWidth=INVWIDTH
    invHeight=INVHEIGHT
    
# run the game loop
    firstLoad=True
    edge['rect'].left = player['rect'].left + (PWIDTH/2)
    bullet['rect'].left = edge['rect'].left + (EWIDTH/2)
    bombActive = False
    
    while True:
        # check for the QUIT event
        # draw the black background onto the surface
        lEdge=False
        rEdge=False
        windowSurface.fill(BLACK)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if bullet['rect'].top < 0:
            bulletFired = False
            
        if event.type == KEYDOWN: #and block['dir'] != STOP:
              # check the keyboard press
            if event.key == K_LEFT:
                if player['rect'].left > 0:
                    player['rect'].left -= PLAYERSPEED
            if event.key == K_RIGHT:
                if player['rect'].right < WINDOWWIDTH:
                    player['rect'].right += PLAYERSPEED
            edge['rect'].left = player['rect'].left  + PWIDTH/2
            edge['rect'].height = EHEIGHT
            if event.key == K_SPACE:
                if bulletFired == False:
                    bullet['rect'].left = edge['rect'].left + (EWIDTH/2)
                    bullet['rect'].top = edge['rect'].top 
                    bulletFired = True


        if bulletFired == True:
            bullet['rect'].top -= BULLETSPEED
            bullet['rect'].bottom -= BULLETSPEED
            pygame.draw.rect(windowSurface, bullet['color'], bullet['rect']) 
                    
# draw invaders

        # noOfRowsLeft=len(invadersList[:])
        i=0
        continueFlag = True 
        while i < NOCOLUMNS and continueFlag:
            if firstLoad :
                invLeft=STARTPOINTLEFT +(2*i*INVWIDTH) 
            j=0
            while ( j < NOROWS) and continueFlag:
                if firstLoad :
                    invTop=STARTPOINTHEIGHT +(2*j*INVHEIGHT)
                    invaders={'rect':pygame.Rect(invLeft, invTop, invWidth, invHeight), 'color':GREEN, 'dir':direction, 'hit':'N'}
                else:
                    invaders=invadersList[j][i]

                # check if the bouncer has move out of the window
                if invaders['rect'].left < (invWidth +1):
                    lEdge=True
                    
                if invaders['rect'].right > (WINDOWWIDTH-(invWidth+1)):
                    rEdge=True

                if direction == RIGHT and rEdge == True:
                    k=0
                    l=0
                    while (l <= NOCOLUMNS-1):
                        k=0
                        while k <= NOROWS-1:
                            invaders=invadersList[k][l]
                            if (l != NOCOLUMNS-1):
                                invaders['rect'].left -= MOVESPEED
                            invaders['rect'].top += MOVESPEED
                            invadersList[k][l]=invaders
                            k = k + 1
                        l = l + 1
                    continueFlag=False
               
                elif direction == LEFT and lEdge == True:
                    l=NOCOLUMNS-1
                   
                    while (l > -1):
                        k=NOROWS-1
                        while k > -1:
                            invaders=invadersList[k][l]
                            invaders['rect'].right += MOVESPEED
                            invaders['rect'].top += MOVESPEED
                            invadersList[k][l]=invaders
                            k = k - 1
                        l = l - 1
                    continueFlag=False
                    
                elif direction == LEFT and lEdge == False:
                     invaders['rect'].left -= MOVESPEED
                     invadersList[j][i]=invaders
                    
                elif direction == RIGHT and rEdge == False:
                     invaders['rect'].right += MOVESPEED
                     invadersList[j][i]=invaders

                if lEdge:
                    direction = RIGHT
                elif rEdge:
                    direction = LEFT
                 
                #  

                j = j + 1
                lEdge=False
                rEdge=False
                
            i= i + 1
            
        firstLoad=False
        #  
        #  

        for i in range(NOROWS):
            for j in range (NOCOLUMNS):
                if bullet['rect'].colliderect(invadersList[i][j]['rect']) and invadersList[i][j]['color'] == GREEN:
                    invadersList[i][j]['color'] = BLACK
                    bullet['rect'].left = edge['rect'].left + (EWIDTH/2)
                    bullet['rect'].top = edge['rect'].top 
                    bulletFired = False
                    score += 1

        #checks for collision with each shield        
        bulletShieldCheck(shield1,bullet,edge)
        bulletShieldCheck(shield2,bullet,edge)
        bulletShieldCheck(shield3,bullet,edge)
        bulletShieldCheck(shield4,bullet,edge)        
                    
        scoreBoard = 'Score:'+str(score)
        drawWords(windowSurface,scoreBoard,(WINDOWWIDTH/2),(30))
        # Success criteria
        gameOver=True
        for i in range(NOROWS):
            for j in range (NOCOLUMNS):
                invaders= invadersList[i][j]
                if invaders['color'] !=BLACK:
                   gameOver=False
                   
        if (gameOver):
            drawWords(windowSurface,'You have Won..!',(WINDOWWIDTH/2),(WINDOWHEIGHT/2))
            pygame.display.update()
            mainClock.tick(15)
            pygame.quit()

        # Random bomb generation   
        successful=False
        numberOfTries=0
        bottomRow = -1
        for i in range(NOROWS):
            for j in range (NOCOLUMNS):
                if invadersList[i][j]['color'] == GREEN:
                    bottomRow = i

        while successful==False and bombActive == False and bottomRow > -1 and numberOfTries <= (NOCOLUMNS-1):
            # draw the window onto the screen
            #invaders= invadersList[NOROWS-1][random.randint(0, NOCOLUMNS-1)]
            invaders= invadersList[NOROWS-1][random.randint(0, bottomRow)]
            # see if the invader has been shot already
            if invaders['color'] !=BLACK:
               successful=True
            else:
                numberOfTries += 1
                
        if successful and bombActive == False:
            bomb['rect'].left = invaders['rect'].left
            bomb['rect'].top  = invaders['rect'].bottom
            bombActive = True
        else:
            bomb['rect'].bottom += BULLETSPEED
            bomb['rect'].top  += BULLETSPEED
            if  bomb['rect'].bottom > WINDOWHEIGHT:
                bombActive = False
                
            # check for the bombing of sheilds
        bombActive=bombShieldCheck(shield1,bomb,bombActive)
        bombActive=bombShieldCheck(shield2,bomb,bombActive)                   
        bombActive=bombShieldCheck(shield3,bomb,bombActive)                   
        bombActive=bombShieldCheck(shield4,bomb,bombActive)                   
            # check for the bombing of players
            
        if bomb['rect'].colliderect(player['rect']):
            lives-=1
            livesBoard = 'Lives:'+str(lives)
            if lives < 0:
                drawWords(windowSurface,'You Lost..!',(WINDOWWIDTH/2),(WINDOWHEIGHT/2))
                pygame.display.update()
                mainClock.tick(15)
                pygame.quit()
                
                   
        # is Game Over?
        for i in range(NOROWS):
            for j in range (NOCOLUMNS):
                pygame.draw.rect(windowSurface, invadersList[i][j]['color'], invadersList[i][j]['rect'])
                invaders= invadersList[i][j]

                                
                if (invaders['rect'].bottom >= (shield1['rect'].top-30)) and (invaders['color'] != BLACK):
                        drawWords(windowSurface,'You Lost..!',(WINDOWWIDTH/2),(WINDOWHEIGHT/2))
                        pygame.display.update()
                        mainClock.tick(15)
                        pygame.quit()
                        sys.exit()
                        
                if (len(invadersList) == 0) and (lives > 0):
                    drawWords(windowSurface,'You Won..!',(WINDOWWIDTH/2),(WINDOWHEIGHT/2))
                    pygame.display.update()
                    pygame.quit()
                    mainClock.tick(15)
                    pygame.quit()
                    sys.exit()
                        
#       Draw other remaining components than the invaders 
        pygame.draw.rect(windowSurface, player['color'], player['rect'])
        pygame.draw.rect(windowSurface, edge['color'], edge['rect'])
        pygame.draw.rect(windowSurface, shield1['color'], shield1['rect'])
        pygame.draw.rect(windowSurface, shield2['color'], shield2['rect'])
        pygame.draw.rect(windowSurface, shield3['color'], shield3['rect'])
        pygame.draw.rect(windowSurface, shield4['color'], shield4['rect'])
        pygame.draw.rect(windowSurface, bomb['color'], bomb['rect'])
        drawWords(windowSurface,livesBoard,(WINDOWWIDTH-90),(30))
#
        pygame.display.update() 
        mainClock.tick(15)
main()


