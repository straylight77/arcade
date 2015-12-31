import pygame, sys, math, random
from pygame.locals import *

FPS = 30
MAX_X = 600
MAX_Y = 600

WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
GRAY      = (128, 128, 128)
DARKGRAY  = ( 40,  40,  40)
RED       = (255,  40,  40)
BGCOLOR   = BLACK


pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((MAX_X, MAX_Y))
BASICFONT = pygame.font.SysFont('courier', 15)
pygame.display.set_caption('pyGame Template')
random.seed()


def terminate():
    pygame.quit()
    sys.exit()

def advance_frame():
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def handle_events():
    pass


def main():

    while True:
        #event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()


        # draw frame
        DISPLAYSURF.fill(BGCOLOR)


        advance_frame()

    terminate()

if __name__ == '__main__':
    main()




