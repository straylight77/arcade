#!/usr/bin/env python

import pygame, sys, math, random
from pygame.locals import *

FPS = 30
#MAX_X, MAX_Y = 1024, 768
MAX_X, MAX_Y = 1920, 1024



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
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.vel = vel
        self.angle = 0
        self.drag = 0.9

    def __str__(self):
        return f"(x={self.pos[0]:.1f}, y={self.pos[1]:.1f}, angle={self.angle:.1f})"

    def update(self, *args):
        x = self.pos[0] + self.vel[0]
        y = self.pos[1] + self.vel[1]
        self.pos = (x,y)

    def load_sprite(self, width, pts=None, color=WHITE):
        if pts == None:
            pts = ( (width-1, width-1), (0, width-1), (0, 0), (width-1, 0) )
        img = pygame.Surface((width, width))
        img.fill(VIOLET)
        img.set_colorkey(VIOLET)
        pygame.draw.polygon(img, color, pts, 4)
        self.image_orig = img
        self.image = img

    def prep_for_draw(self, offset=None):
        self.image = pygame.transform.rotate(self.image_orig, -self.angle)
        self.rect = self.image.get_rect()
        x = MAX_X/2 + self.pos[0] - offset[0]
        y = MAX_Y/2 + self.pos[1] - offset[1]
        self.rect.center = (x, y)


#---- class: Player --------------------------------------------------------
class Player(GameObject):

    def __init__(self, pos=(0,0)):
        super().__init__(self)
        self.load_sprite()
        self.pos = pos
        self.angle = 270

        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect.center = [ MAX_X/2, MAX_Y/2 ]

    def load_sprite(self):
        pts = ( (32, 16), (0, 28), (0, 4) )
        super().load_sprite(32, pts, GRAY)


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
        super().load_sprite(32, None, RED)

    def update(self, coords):
        super().update(self)
        self.prep_for_draw(coords)


#---- class: Station --------------------------------------------------------
class Station(GameObject):

    def __init__(self, pos=(0,0)):
        super().__init__(pos)
        self.load_sprite()

    def load_sprite(self):
        super().load_sprite(128, None, BLUE)

    def update(self, coords):
        super().update(self, coords)
        self.prep_for_draw(coords)


#-------------------------------------------------------------------------
class PolarObject(GameObject):
    """Extension of the base GameObject to use polar coordinates."""

    def __init__(self, angle=0, radius=100, vel=1):
        super().__init__(self)
        self.angle = angle
        self.radius = radius
        self.vel = vel

    def __str__(self):
        return f"(angle={self.angle:.1f}, rad={self.radius:.1f}, vel={self.vel:.1f})"

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
        super().load_sprite(32, None, YELLOW)

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
    commands = {'quit': False, 'left': 0, 'right': 0, 'thrust': 0, 'fire': 0}

    DISPLAY, CLOCK = init(MAX_X, MAX_Y)
    FONT1 = pygame.font.SysFont('arial', 20)
    FONT2 = pygame.font.SysFont('courier', 15)

    player = Player()
    allsprites = pygame.sprite.Group(player)

    station = Station()
    allsprites.add(station)

    asteroids = pygame.sprite.Group()
    asteroids.add( Asteroid(vel=(-1,0.5), pos=(300,-250)) )
    asteroids.add( Asteroid(vel=(1,0.5)) )
    allsprites.add(asteroids)

    asteroids2 = pygame.sprite.Group()
    for n in range(1,8):
        a = random.randint(0, 360)
        r = random.randint(200, 500)
        v = random.randint(25, 150) / 100.0
        p = PolarAsteroid(angle=a, radius=r, vel=v)
        asteroids2.add(p)

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
        for s in allsprites.sprites():
            msg_disp = FONT1.render(f"{i}: {s}", True, GRAY, BLACK)
            DISPLAY.blit(msg_disp, (10, 10+i*30))
            i += 1

        # advance game frame
        pygame.display.update()
        CLOCK.tick(FPS)


    terminate()

####
if __name__ == '__main__':
    main()



