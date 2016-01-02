import pygame, sys, math, random
from pygame.locals import *

FPS = 30
MAX_X = 800
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


class Asteroid():

    ast_spritesheet = None
    ast_img = []
    exp_spritesheet = None
    exp_img = []
    pos = (0, 0)
    vel = (0, 0)
    state = 1
    NORMAL = 1
    EXPLODING = 2
    DONE = 3
    frame = 0

    def __init__(self):
        self.pos = (random.randint(48, MAX_X-48), random.randint(48, MAX_Y-48))
        s = random.randint(3, 10)
        self.vel = (random.randint(-s, s), random.randint(-s, s))
        self.state = self.NORMAL

        #TODO: have only 1 instance of the spritesheet.  use a class variable?

        #load asteroid sprite
        self.ast_spritesheet = pygame.image.load('assets/asteroid2.png')
        self.ast_img = []
        s = 64
        for y in range(0,6):
            for x in range (0, 5):
                self.ast_img.append(self.ast_spritesheet.subsurface( (x*s,y*s,s,s) ))

        #load explosion sprite
        self.exp_spritesheet = pygame.image.load('assets/explosion1_64x64.png')
        self.exp_img = []
        s = 64
        for y in range(0, 5):
            for x in range (0, 5):
                self.exp_img.append(self.exp_spritesheet.subsurface( (x*s,y*s,s,s) ))

    def is_normal(self):
        return self.state == self.NORMAL

    def is_done(self):
        return self.state == self.DONE

    def is_exploding(self):
        return self.state == self.EXPLODING

    def start_exploding(self):
        if self.state == self.NORMAL:
            self.state = self.EXPLODING
            self.vel = (0, 0)
            self.frame = 0

    def update(self):
        x = self.pos[0] + self.vel[0]
        y = self.pos[1] + self.vel[1]
        if x >= MAX_X:  x = 0
        if x < 0:       x = MAX_X
        if y >= MAX_Y:  y = 0
        if y < 0:       y = MAX_Y
        self.pos = (x, y)

    def draw(self):
        x = self.pos[0] - 32
        y = self.pos[1] - 32

        if self.state == self.NORMAL:
            img = self.ast_img[self.frame]
            DISPLAYSURF.blit(img, (x, y))
            self.frame += 1
            if self.frame >= len(self.ast_img):
                self.frame = 0

        elif self.state == self.EXPLODING:
            img = self.exp_img[self.frame]
            DISPLAYSURF.blit(img, (x, y))
            self.frame += 1
            if self.frame >= len(self.exp_img):
                self.frame = 0
                self.state = self.DONE

        else:
            pass


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

    sprites = []
    sprites.append( Asteroid() )

    #main game loop
    while True:

       #event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    for i in range(0, len(sprites)):
                        if sprites[i].is_normal():
                            sprites[i].start_exploding()
                            break;

                if event.key == K_n:
                    sprites.append( Asteroid() )
                if event.key == K_ESCAPE:
                    terminate()


        #update game objects
        if len(sprites) > 0 and sprites[0].is_done():
            sprites = sprites[1:]
        for s in sprites:
            s.update()

        # draw frame
        DISPLAYSURF.fill(BGCOLOR)
        for s in sprites:
            s.draw()

        #pygame.display.update()
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

    terminate()

if __name__ == '__main__':
    main()




