import pygame, sys, math, random, os
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

#### Class: Asteroid ########################################################
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



#### Class: Explosion ############################################
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


#### class: Ship #################################################
class Ship(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos = (MAX_X/2, MAX_Y/2)
        self.angle = 0
        self.vel = (0, 0)
        #self.image_orig, self.rect = load_image("ship1_32x32.png")

        self.image_orig = pygame.image.load('assets/ship1_32x32.png')
        self.rect = self.image_orig.get_rect()

        self.rect.center = self.pos
        self.image = self.image_orig

    def update(self, thrust, left, right):
        if left:
            self.angle += 10
        if right:
            self.angle -= 10
        if thrust:
            vel_x = self.vel[0] + math.cos(math.radians(self.angle))*0.5
            vel_y = self.vel[1] - math.sin(math.radians(self.angle))*0.5
            self.vel = (vel_x, vel_y)

        if self.angle >= 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

        x = self.pos[0] + self.vel[0]
        y = self.pos[1] + self.vel[1]
        if x >= MAX_X:  x = 0
        if x < 0:       x = MAX_X
        if y >= MAX_Y:  y = 0
        if y < 0:       y = MAX_Y
        self.pos = (x, y)

        print self.vel, self.pos

        self.image = pygame.transform.rotate(self.image_orig, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos



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

s = Ship()
ships = pygame.sprite.RenderPlain(s)

cmd_thrust = False
cmd_left = False
cmd_right = False

#main game loop
while True:

    #event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

        elif event.type == KEYDOWN:
            if event.key == K_UP:    cmd_thrust = True
            if event.key == K_LEFT:  cmd_left = True
            if event.key == K_RIGHT: cmd_right = True

        elif event.type == KEYUP:
            if event.key == K_UP:    cmd_thrust = False
            if event.key == K_LEFT:  cmd_left = False
            if event.key == K_RIGHT: cmd_right = False

            if event.key == K_SPACE:
                if asteroids:
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
    ships.update(cmd_thrust, cmd_left, cmd_right)
    for exp in explosions.sprites():
        if exp.is_done():
            exp.kill()

    # draw frame
    DISPLAYSURF.fill(BGCOLOR)
    explosions.draw(DISPLAYSURF)
    asteroids.draw(DISPLAYSURF)
    ships.draw(DISPLAYSURF)

    #advance frame
    #pygame.display.update()
    pygame.display.flip()
    FPSCLOCK.tick(FPS)


terminate()   # won't actually get called




