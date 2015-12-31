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
    #event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()

    return None


def main():

    img = pygame.image.load('assets/explosion1_64x64.png')
    sprites = []
    s = 64
    for y in range(0, 5):
        for x in range (0, 5):
            sprites.append(img.subsurface( (x*s,y*s,s,s) ))

    i = 0
    sprite_done = False
    pos = (random.randint(48, MAX_X-48), random.randint(48, MAX_Y-48))
    while True:
        handle_events()

        # draw frame
        DISPLAYSURF.fill(BGCOLOR)

        DISPLAYSURF.blit(sprites[i], pos)

        i += 1
        if i >= len(sprites):
            i = 0
            pos = (random.randint(48, MAX_X-48), random.randint(48, MAX_Y-48))

        #pygame.display.update()
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

    terminate()

if __name__ == '__main__':
    main()




