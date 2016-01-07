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

#---- class: Spritesheet -------------------------------------------------
class Spritesheet():
    def __init__(self):
        filename = 'assets/asteroid2.png'
        self.sheet = pygame.image.load(filename)
        self.decompose()

    def decompose(self):
        self.images = []
        s = 64
        for y in range(0,6):
            for x in range (0, 5):
                img = self.sheet.subsurface((x*s, y*s, s, s))
                self.images.append(img)

    def get_sprite(self, index):
        return self.images[index]



#---- class: AnimatedSprite ----------------------------------------------
class AnimatedSprite(pygame.sprite.Sprite):

    sheet = None

    @classmethod
    def set_spritesheet(cls, spritesheet):
        cls.sheet = spritesheet

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.image = self.sheet.get_sprite(0)
        self.rect = self.image.get_rect()


    def update(self, frames = 1):
        self.index += frames
        if self.index >= len(self.sheet.images):
            self.index = 0
        self.image = self.sheet.get_sprite(self.index)


#---- class: Asteroid ----------------------------------------------------
class Asteroid(AnimatedSprite):

    def __init__(self, pos = [0,0], index = 0):
        AnimatedSprite.__init__(self)
        self.pos = pos
        self.index = index
        self.vel = [0, 0]


    def update(self):
        AnimatedSprite.update(self)
        self.rect.center = self.pos


##### functions ##########################################################
def terminate():
    pygame.quit()
    sys.exit()

#---- main() -------------------------------------------------------------
def main():
    #init pygame
    pygame.init()
    CLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((MAX_X, MAX_Y))
    FONT1 = pygame.font.SysFont('courier', 15)
    pygame.display.set_caption('pyGame Template')
    random.seed()

    s = Spritesheet()
    AnimatedSprite.set_spritesheet(s)
    print len(s.images)

    grp = pygame.sprite.RenderPlain()
    grp.add( Asteroid([MAX_X/2, MAX_Y/2]) )
    grp.add( Asteroid([MAX_X/2+65, MAX_Y/2], 15) )

    #main game loop
    while True:
        #event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()

        #update game state
        grp.update()

        # draw frame
        DISPLAY.fill(BGCOLOR)
        grp.draw(DISPLAY)
        pygame.display.update()
        CLOCK.tick(FPS)


    terminate()

####
if __name__ == '__main__':
    main()




