#!/usr/bin/env python

import pygame, sys, math, random
from pygame.locals import *

FPS = 30
MAX_X = 1024
MAX_Y = 768

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

#---- class: GameObject --------------------------------------------------
class GameObject(pygame.sprite.Sprite):
    """
    Base class containing logic for objects in the game. Implements the physics
    of position (pos) and velocity (vel) within the game world.
    pos ->
    vel ->
    angle ->
    drag ->
    """
    def __init__(self, pos=(0,0), vel=(0,0)):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.vel = vel
        self.angle = 0
        self.drag = 0.9

    def __str__(self):
        return f"pos: ({self.pos[0]:.1f}, {self.pos[1]:.1f}, {self.angle:.1f})"

    def update(self, *args):
        x = self.pos[0] + self.vel[0]
        y = self.pos[1] + self.vel[1]
        self.pos = (x,y)



#---- class: Player --------------------------------------------------------
class Player(GameObject):

    def __init__(self, pos=(0,0)):
        super().__init__(self)
        self.load_sprite()
        self.pos = pos
        #self.pos = [ MAX_X/2, MAX_Y/2 ]
        self.angle = 270

        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect.center = [ MAX_X/2, MAX_Y/2 ]

    def load_sprite(self):
        img = pygame.Surface((32, 32))
        img.fill(VIOLET)
        img.set_colorkey(VIOLET)
        pts = ( (32, 16), (0, 28), (0, 4) )
        #pts = ( (32, 16), (4, 28), (4, 4) )
        pygame.draw.polygon(img, WHITE, pts, 4)
        self.image_orig = img


    def update(self, cmd):
        self.angle += 10 * (cmd['right'] + cmd['left'])
        if cmd['thrust']:
            dx = self.vel[0] + math.cos(math.radians(self.angle))*0.5
            dy = self.vel[1] + math.sin(math.radians(self.angle))*0.5
            self.vel = (dx, dy)

        super().update(self)

        # prep for draw
        self.image = pygame.transform.rotate(self.image_orig, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = [ MAX_X/2, MAX_Y/2 ]


#---- class: Asteroid --------------------------------------------------------
class Asteroid(GameObject):

    def __init__(self, pos=(0,0), vel=(0,0)):
        super().__init__(pos, vel)
        self.load_sprite()

    def load_sprite(self):
        img = pygame.Surface((32, 32))
        img.fill(VIOLET)
        img.set_colorkey(VIOLET)
        pts = ( (31, 31), (0, 31), (0, 0), (31, 0) )
        pygame.draw.polygon(img, RED, pts, 4)
        self.image_orig = img

    def update(self, coords):
        super().update(self)

        # prep for draw
        self.image = pygame.transform.rotate(self.image_orig, -self.angle)
        self.rect = self.image.get_rect()
        x = MAX_X/2 + self.pos[0] - coords[0]
        y = MAX_Y/2 + self.pos[1] - coords[1]
        self.rect.center = (x, y)




#---- class: Station --------------------------------------------------------
class Station(GameObject):

    def __init__(self, pos=(0,0)):
        super().__init__(pos)
        self.load_sprite()

    def load_sprite(self):
        w = 128
        img = pygame.Surface((w, w))
        img.fill(VIOLET)
        img.set_colorkey(VIOLET)
        pts = ( (w-1, w-1), (0, w-1), (0, 0), (w-1, 0) )
        pygame.draw.polygon(img, BLUE, pts, 4)
        self.image_orig = img

    def update(self, coords):
        super().update(self, coords)

        # prep for draw
        self.image = pygame.transform.rotate(self.image_orig, -self.angle)
        self.rect = self.image.get_rect()
        x = MAX_X/2 + self.pos[0] - coords[0]
        y = MAX_Y/2 + self.pos[1] - coords[1]
        self.rect.center = (x, y)


#-------------------------------------------------------------------------
class PolarObject(GameObject):
    """Extension of the base GameObject to use polar coordinates."""
    def __init__(self, angle=0, radius=100, vel=1):
        super().__init__(self)
        self.angle = angle
        self.radius = radius
        self.vel = vel

    def update(self):
        self.angle += self.vel

    def get_xy(self):
        x = self.radius * math.cos(math.radians(self.angle))
        y = self.radius * math.sin(math.radians(self.angle))
        return (x, y)


#-------------------------------------------------------------------------
class PolarAsteroid(PolarObject):

    def __init__(self, angle=0, radius=100, vel=1):
        super().__init__(angle, radius, vel)
        self.load_sprite()

    def load_sprite(self):
        img = pygame.Surface((32, 32))
        img.fill(VIOLET)
        img.set_colorkey(VIOLET)
        pts = ( (31, 31), (0, 31), (0, 0), (31, 0) )
        pygame.draw.polygon(img, YELLOW, pts, 4)
        self.image_orig = img
        self.image = img

    def update(self, coords):
        super().update()

        # prep for draw
        #self.image = pygame.transform.rotate(self.image_orig, -self.angle)
        self.rect = self.image.get_rect()
        pos = self.get_xy()
        x = MAX_X/2 + pos[0] - coords[0]
        y = MAX_Y/2 + pos[1] - coords[1]
        self.rect.center = (x, y)




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
    FONT1 = pygame.font.SysFont('arial', 20)
    FONT2 = pygame.font.SysFont('courier', 15)

    player = Player(pos=(-145, 130))
    allsprites = pygame.sprite.Group(player)

    station = Station()
    allsprites.add(station)

    asteroids = pygame.sprite.Group()
    asteroids.add( Asteroid(vel=(-2,1), pos=(200,-200)) )
    asteroids.add( Asteroid(vel=(1,1)) )
    allsprites.add(asteroids)

    asteroids2 = pygame.sprite.Group()
    asteroids2.add( PolarAsteroid(vel=1, radius=250) )
    asteroids2.add( PolarAsteroid(angle=90, vel=0.5, radius=270) )
    asteroids2.add( PolarAsteroid(angle=45, vel=0.25, radius=270) )
    allsprites.add(asteroids2)


    #main game loop
    while True:

        handle_events(commands)

        if commands['quit']:
            terminate()

        player.update(commands)
        asteroids.update(player.pos)
        station.update(player.pos)
        asteroids2.update(player.pos)

        # draw main screen
        DISPLAY.fill(BGCOLOR)
        allsprites.draw(DISPLAY)

        i = 0
        for s in asteroids.sprites():
            msg = f"pos: ({s.pos[0]:.1f}, {s.pos[1]:.1f}, {s.angle:.1f})"
            msg_disp = FONT1.render(msg, True, RED, BLACK)
            DISPLAY.blit(msg_disp, (10, 10+i*30))
            i += 1

        for s in asteroids2.sprites():
            msg = f"pos: ({s.angle:.1f}, {s.radius:.1f}, {s.vel:.1f})"
            msg_disp = FONT1.render(msg, True, YELLOW, BLACK)
            DISPLAY.blit(msg_disp, (10, 10+i*30))
            i += 1



        # advance game frame
        pygame.display.update()
        CLOCK.tick(FPS)


    terminate()

####
if __name__ == '__main__':
    main()



