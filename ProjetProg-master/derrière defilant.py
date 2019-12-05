import pygame, random, sys
from pygame.locals import *

###faire truc défilant
def events():
    for event in pygame.event.get():
        if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
            pygame.quit()
            sys.exit()

#define display surface
WINDOWWIDTH = 900
WINDOWHEIGHT = 600
WINDOWHEIGHTWINDOWWIDTH, WINDOWHEIGHTWINDOWHEIGHT= WINDOWWIDTH /2 , WINDOWHEIGHT/2
AREA = WINDOWWIDTH*WINDOWHEIGHT

#Setup pygame
pygame.init()
CLOCK=pygame.time.Clock()
DS=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pygame.display.set_caption("code.Pylet - Seamless Background Scrolling")
FPS = 60

BACKGROUND=pygame.image.load("background.png").convert()
x=0

while True:
    events()

    rel_x = x % BACKGROUND.get_rect().width
    DS.blit(BACKGROUND, (rel_x - BACKGROUND.get_rect().width, 0))
    if rel_x < WINDOWWIDTH:
        DS.blit(BACKGROUND, (rel_x, 0))
    x -= 1

    pygame.display.update()
    CLOCK.tick(FPS)

events()

        rel_x = a % BACKGROUND.get_rect().width
        windowSurface.blit(BACKGROUND, (rel_x - BACKGROUND.get_rect().width, 0))
        if rel_x < WINDOWWIDTH:
            windowSurface.blit(BACKGROUND, (rel_x, 0))
        a -= 1