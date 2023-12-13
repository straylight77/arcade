#!/usr/bin/env python

import pygame, sys, math, random
from pygame.locals import *

FPS = 30
MAX_X, MAX_Y = 1024, 768

#C_MAIN    = (128, 128, 128)
C_MAIN    = (192, 192, 192)
C_KEY     = (255,   0, 255)
C_BG      = (  0,   0,   0)



#---- class: GameObject --------------------------------------------------
class GameObject(pygame.sprite.Sprite):
    """
    Base class containing logic for objects in the game. Implements the physics
    of position and velocity.
    """
    def __init__(self, pos=(0,0), vel=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.vel_x = vel[0]
        self.vel_y = vel[1]
        self.angle = 0

    def update(self, *args):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.check_boundry()
        self.prepare_for_draw()

    def check_boundry(self):
        self.pos_x %= MAX_X
        self.pos_y %= MAX_Y
        self.angle %= 360

    def prepare_for_draw(self):
        self.image = pygame.transform.rotate(self.image_orig, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos_x, self.pos_y)

    def create_sprite(self, size=32, pts=None ):
        if pts is None:
            w = size-3
            # minus 3 because of the line thickness
            pts = ((0, 0),(0, w),(w, w),(w, 0))
        img = pygame.Surface((size,size))
        img.fill(C_KEY)
        img.set_colorkey(C_KEY)
        pygame.draw.polygon(img, C_MAIN, pts, 3)
        self.image_orig = img



#---- class: Ship --------------------------------------------------------
class Ship(GameObject):

    def __init__(self):
        GameObject.__init__(self)
        self.create_sprite( size=32, pts=((32,16), (0,28), (0,4)) )
        self.reset()
        self.prepare_for_draw()

    def reset(self):
        self.pos_x = MAX_X/2
        self.pos_y = MAX_Y/2
        self.angle = 270


    def update(self, cmd):
        # 10 -> turn_rate
        # 0.5 -> thrust_rate
        # 0.98 -> drag coeffecient
        self.angle += 10 * (cmd['right'] + cmd['left'])
        if cmd['thrust']:
            self.vel_x += math.cos(math.radians(self.angle)) * 0.5
            self.vel_y += math.sin(math.radians(self.angle)) * 0.5
        #else:
        #    self.vel[0] *= 0.98
        #    self.vel[1] *= 0.98
        GameObject.update(self)


#---- class: Asteroid ----------------------------------------------------
class Asteroid(GameObject):

    def __init__(self, pos=(0,0), vel=(0,0)):
        GameObject.__init__(self, pos, vel)


class SmallAsteroid(Asteroid):

    def __init__(self, pos, vel=(0,0)):
        Asteroid.__init__(self, pos, vel)
        self.create_sprite(32)


class MediumAsteroid(Asteroid):

    def __init__(self, pos, vel=(0,0)):
        Asteroid.__init__(self, pos, vel)
        self.create_sprite(64)


class LargeAsteroid(Asteroid):

    def __init__(self, pos, vel=(0,0)):
        Asteroid.__init__(self, pos, vel)
        self.create_sprite(128)


#---- class: Shot -------------------------------------------------------
class Shot(GameObject):
    pass


#---- class: Saucer -----------------------------------------------------
class Saucer(GameObject):
    pass



##########################################################################

def terminate():
    pygame.quit()
    sys.exit()


def init(max_x, max_y, title = 'pyGame Template'):
    pygame.init()
    clk = pygame.time.Clock()
    disp = pygame.display.set_mode((max_x, max_y))
    pygame.display.set_caption(title)
    random.seed()
    return disp, clk


def handle_events(cmd):
    for event in pygame.event.get():

        if event.type == QUIT:
            cmd['quit'] = True

        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                cmd['left'] = -1
            elif event.key == K_RIGHT:
                cmd['right'] = 1
            elif event.key == K_UP:
                cmd['thrust'] = 1

        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                cmd['quit'] = True
            elif event.key == K_LEFT:
                cmd['left'] = 0
            elif event.key == K_RIGHT:
                cmd['right'] = 0
            elif event.key == K_UP:
                cmd['thrust'] = 0



#---- main() -------------------------------------------------------------
def main():
    level = 1
    score = 0
    lives = 2
    highscore = 0
    commands = {'quit': False, 'left': 0, 'right': 0, 'thrust': 0, 'fire': 0}

    DISPLAY, CLOCK = init(MAX_X, MAX_Y, "Asteroid Classic")
    FONT1 = pygame.font.SysFont('courier', 45)
    FONT2 = pygame.font.SysFont('courier', 15)

    asteroids = pygame.sprite.RenderPlain()
    asteroids.add( LargeAsteroid((MAX_X/4, MAX_Y/4)) )
    asteroids.add( MediumAsteroid((MAX_X*3/4, MAX_Y/4)) )
    asteroids.add( SmallAsteroid((MAX_X*3/4, MAX_Y*3/4)) )
    ship = Ship()
    allsprites = pygame.sprite.Group(ship)

    #main game loop
    while True:

        handle_events(commands)

        if commands['quit']:
            terminate()

        allsprites.update(commands)
        asteroids.update(commands)

        # detect collisions
        #for a in pygame.sprite.spritecollide(ship, asteroids, False):
        #    if ship.alive():
        #        allsprites.add( Explosion(ship.pos) )
        #        ship.kill()


        # draw main screen
        DISPLAY.fill(C_BG)
        allsprites.draw(DISPLAY)
        asteroids.draw(DISPLAY)

        # advance game frame
        pygame.display.update()
        CLOCK.tick(FPS)


    terminate()

####
if __name__ == '__main__':
    main()


