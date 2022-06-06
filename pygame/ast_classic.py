#!/usr/bin/env python

import pygame, sys, math, random
from pygame.locals import *

FPS = 30
MAX_X = 1024
MAX_Y = 768

C_MAIN    = (128, 128, 128)
C_KEY     = (255,   0, 255)
C_BG      = (  0,   0,   0)



#---- class: GameObject --------------------------------------------------
class GameObject(pygame.sprite.Sprite):
    """
    Base class containing logic for objects in the game. Implements the physics
    of position and velocity.
    """
    def __init__(self, pos=[0,0], vel=[0,0]):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.vel = vel
        self.angle = 0
        self.drag = 1.0

    def update(self, *args):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[0] *= self.drag
        self.vel[1] *= self.drag
        self.check_boundry()

    def check_boundry(self):
        if self.pos[0] > MAX_X:
            self.pos[0] = 0
        if self.pos[0] < 0:
            self.pos[0] = MAX_X

        if self.pos[1] > MAX_Y:
            self.pos[1] = 0
        if self.pos[1] < 0:
            self.pos[1] = MAX_Y

        if self.angle < 0:
            self.angle += 360
        if self.angle > 360:
            self.angle -= 360


    def create_sprite(self, size = (32,32), pts=None ):
        if pts is None:
            pts = ( (0,0), (0,size[1]), size, (size[0],0), (0,0) )
        img = pygame.Surface(size)
        img.fill(C_KEY)
        img.set_colorkey(C_KEY)
        pygame.draw.polygon(img, C_MAIN, pts, 3)
        self.image_orig = img



#---- class: Ship --------------------------------------------------------
class Ship(GameObject):

    def __init__(self):
        GameObject.__init__(self)
        self.thrust_rate = 0.5
        self.turn_rate = 10
        self.create_sprite( pts=((32, 16), (0, 28), (0, 4)) )
        #self.drag = 0.97
        self.reset()
        self.prepare_for_draw()

    def reset(self):
        self.pos = [MAX_X/2, MAX_Y/2]
        self.angle = 270

    def prepare_for_draw(self):
        self.image = pygame.transform.rotate(self.image_orig, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


    def update(self, cmd):
        self.angle += self.turn_rate * (cmd['right'] + cmd['left'])
        if cmd['thrust']:
            self.vel[0] += math.cos(math.radians(self.angle)) * self.thrust_rate
            self.vel[1] += math.sin(math.radians(self.angle)) * self.thrust_rate
        GameObject.update(self)
        self.prepare_for_draw()


#---- class: Asteroid ----------------------------------------------------
class Asteroid(GameObject):

    def __init__(self):
        GameObject.__init__(self)


class SmallAsteroid(Asteroid):
    pass

class MediumAsteroid(Asteroid):
    pass


class LargeAsteroid(Asteroid):
    pass


#---- class: Saucer -----------------------------------------------------
class Saucer(GameObject):
    pass


#---- class: Shot -------------------------------------------------------
class Shot(GameObject):
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

    DISPLAY, CLOCK = init(MAX_X, MAX_Y)
    FONT1 = pygame.font.SysFont('courier', 45)
    FONT2 = pygame.font.SysFont('courier', 15)

    #asteroids = pygame.sprite.RenderPlain()
    #asteroids.add( Asteroid([140, 0], [3, 4]))
    ship = Ship()
    allsprites = pygame.sprite.Group(ship)

    #main game loop
    while True:

        handle_events(commands)

        if commands['quit']:
            terminate()

        allsprites.update(commands)
        #asteroids.update(commands)

        # detect collisions
        #for a in pygame.sprite.spritecollide(ship, asteroids, False):
        #    if ship.alive():
        #        allsprites.add( Explosion(ship.pos) )
        #        ship.kill()




        # draw main screen
        DISPLAY.fill(C_BG)
        allsprites.draw(DISPLAY)
        #asteroids.draw(DISPLAY)

        # advance game frame
        pygame.display.update()
        CLOCK.tick(FPS)


    terminate()

####
if __name__ == '__main__':
    main()


