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


class Asteroid(pygame.sprite.Sprite):

    ast_spritesheet = None
    ast_img = []
    pos = (0, 0)
    vel = (0, 0)
    frame = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos = (random.randint(48, MAX_X-48), random.randint(48, MAX_Y-48))
        s = random.randint(3, 10)
        self.vel = (random.randint(-s, s), random.randint(-s, s))

        #TODO: have only 1 instance of the spritesheet.  use a class variable?

        #load asteroid sprite
        self.ast_spritesheet = pygame.image.load('assets/asteroid2.png')
        self.ast_img = []
        s = 64
        for y in range(0,6):
            for x in range (0, 5):
                self.ast_img.append(self.ast_spritesheet.subsurface( (x*s,y*s,s,s) ))

        self.frame = 0
        self.rect = pygame.Rect( 0, 0, 64, 64 )
        self.rect.center = self.pos
        self.image = self.ast_img[self.frame]

    def update(self):
        x = self.pos[0] + self.vel[0]
        y = self.pos[1] + self.vel[1]
        if x >= MAX_X:  x = 0
        if x < 0:       x = MAX_X
        if y >= MAX_Y:  y = 0
        if y < 0:       y = MAX_Y
        self.pos = (x, y)

        self.rect.center = self.pos
        self.image = self.ast_img[self.frame]
        self.frame += 1
        if self.frame >= len(self.ast_img):
            self.frame = 0




class Explosion(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.rect.center = pos
        self.frame = 0

        #load explosion sprite
        self.exp_spritesheet = pygame.image.load('assets/explosion1_64x64.png')
        self.exp_img = []
        s = 64
        for y in range(0, 5):
            for x in range (0, 5):
                self.exp_img.append(self.exp_spritesheet.subsurface( (x*s,y*s,s,s) ))
        self.image = self.exp_img[self.frame]


    def update(self):
        if self.frame < len(self.exp_img):
            self.image = self.exp_img[self.frame]
            self.frame += 1


    def is_done(self):
        return self.frame >= len(self.exp_img)




def load_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def terminate():
    pygame.quit()
    sys.exit()

def advance_frame():
    #pygame.display.update()
    pygame.display.flip()
    FPSCLOCK.tick(FPS)



#### main ########################################
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((MAX_X, MAX_Y))
BASICFONT = pygame.font.SysFont('courier', 15)
pygame.display.set_caption('pyGame Template')
random.seed()


a = Asteroid()
asteroids = pygame.sprite.RenderPlain(a)
explosions = pygame.sprite.RenderPlain()


#main game loop
while True:

    #event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

        elif event.type == KEYUP:
            if event.key == K_SPACE:
                if len(asteroids) > 0:
                    a = asteroids.sprites()[0]
                    explosions.add( Explosion(a.pos) )
                    a.kill()
            if event.key == K_n:
                asteroids.add( Asteroid() )
            if event.key == K_ESCAPE:
                terminate()


    #update game objects
    asteroids.update()
    explosions.update()
    for exp in explosions.sprites():
        if exp.is_done():
            exp.kill()

    # draw frame
    DISPLAYSURF.fill(BGCOLOR)
    asteroids.draw(DISPLAYSURF)
    explosions.draw(DISPLAYSURF)

    advance_frame()

terminate()   # won't actually get called




