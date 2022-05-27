#!/usr/bin/env python

import pygame, sys, math, random
from pygame.locals import *

FPS = 30
MAX_X = 800
MAX_Y = 600

WHITE     = (255, 255, 255)
GRAY      = (128, 128, 128)
DARKGRAY  = ( 40,  40,  40)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
ORANGE    = (255, 128,   0)
YELLOW    = (255, 255,   0)
GREEN     = (40,  255,   0)
BLUE      = ( 0,    0, 255)
VIOLET    = (255,   0, 255)
BGCOLOR = BLACK




def terminate():
    pygame.quit()
    sys.exit()


def main():
    #init pygame
    pygame.init()
    CLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((MAX_X, MAX_Y))
    FONT1 = pygame.font.SysFont('courier', 15)
    pygame.display.set_caption('pyGame Template')
    random.seed()

    #main game loop
    while True:
        #event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()


        # draw frame
        DISPLAY.fill(BGCOLOR)

        pygame.display.update()
        CLOCK.tick(FPS)


    terminate()

if __name__ == '__main__':
    main()
