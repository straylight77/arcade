#!/usr/bin/env python

import pygame, sys, math, random
from pygame.locals import *

FPS = 30
#MAX_X, MAX_Y = 1024, 768   # XGA
#MAX_X, MAX_Y = 1280, 720   # HD (720p)
MAX_X, MAX_Y = 1920, 1024   # Full HD

WHITE     = (255, 255, 255)
GRAY      = (128, 128, 128)
DARKGRAY  = ( 30,  30,  30)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
ORANGE    = (255, 128,   0)
YELLOW    = (255, 255,   0)
GREEN     = (40,  255,   0)
BLUE      = (64,   64, 255)
VIOLET    = (255,   0, 255)
BGCOLOR = BLACK


#-----------------------------------------------------------------------------
class GameObject(pygame.sprite.Sprite):
    """Base class containing logic for objects in the game. Implements the physics
    of position (pos) and velocity (vel) within the game world."""

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

    def get_relative_pos(self, origin):
        x = self.pos[0] - origin[0]
        y = self.pos[1] - origin[1]
        return (x, y)

    def get_distance_from(self, point):
        dx = point[0] - self.pos[0]
        dy = point[1] - self.pos[1]
        return math.sqrt(dx**2 + dy**2)


#-----------------------------------------------------------------------------
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


#-----------------------------------------------------------------------------
class Asteroid(GameObject):

    def __init__(self, pos=(0,0), vel=(0,0)):
        super().__init__(pos, vel)
        self.load_sprite()

    def load_sprite(self):
        super().load_sprite(32, None, RED)

    def update(self, coords):
        super().update(self)
        self.prep_for_draw(coords)


#-----------------------------------------------------------------------------
class Station(GameObject):

    def __init__(self, pos=(0,0)):
        super().__init__(pos)
        self.load_sprite()

    def load_sprite(self):
        super().load_sprite(128, None, BLUE)

    def update(self, coords):
        super().update(self, coords)
        self.prep_for_draw(coords)


#-----------------------------------------------------------------------------
class PolarObject(GameObject):
    """Extension of the base GameObject to use polar coordinates."""
    #TODO add a center position (pos) and refactor into GameObject.
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


#-----------------------------------------------------------------------------
class PolarAsteroid(PolarObject):

    def __init__(self, angle=0, radius=100, vel=1):
        super().__init__(angle, radius, vel)
        self.load_sprite()

    def load_sprite(self):
        super().load_sprite(32, None, YELLOW)

    def update(self, coords):
        super().update()
        self.pos = self.get_xy()

        # prep for draw
        #self.image = pygame.transform.rotate(self.image_orig, -self.angle)
        self.rect = self.image.get_rect()
        x = MAX_X/2 + self.pos[0] - coords[0]
        y = MAX_Y/2 + self.pos[1] - coords[1]
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


def draw_hud(disp, player):
    #pygame.draw.circle(disp, DARKGRAY, (MAX_X/2, MAX_Y/2), 500, width=1)
    FONT = pygame.font.SysFont('arial', 20)
    msg_disp = FONT.render(f"({player.pos[0]:.0f}, {player.pos[1]:.0f})", True, GRAY, BLACK)
    w = msg_disp.get_width()
    disp.blit(msg_disp, (210-w/2, 420))


def draw_radar_hud(disp):
    r = 200
    s = pygame.Surface((r*2, r*2))
    s.set_alpha(192)
    s.fill(VIOLET)
    s.set_colorkey(VIOLET)
    pygame.draw.circle(s, DARKGRAY, (r,r), r)               # background
    pygame.draw.circle(s, GRAY, (r,r), r, width=2)      # outer circle
    #pygame.draw.circle(s, GRAY, (r,r), 50, width=1)     # inner circle
    pts =[
        (r-MAX_X/2/20, r-MAX_Y/2/20),
        (r+MAX_X/2/20, r-MAX_Y/2/20),
        (r+MAX_X/2/20, r+MAX_Y/2/20),
        (r-MAX_X/2/20, r+MAX_Y/2/20)
    ]
    pygame.draw.polygon(s, GRAY, pts, 2)  # rectangle to show the viewport
    pygame.draw.line(s, GRAY, (r-10,r), (r+10,r), width=1)  # crosshairs
    pygame.draw.line(s, GRAY, (r,r-10), (r,r+10), width=1)
    disp.blit(s, (10, 10))


def draw_radar_objects(disp, player, objects, color, r):
    #TODO show arrow towards station when it goes off the radar (?)
    scale = 10
    for obj in objects:
        if obj.get_distance_from(player.pos) < 4000:
            x = 210 + (obj.pos[0] - player.pos[0]) / 20
            y = 210 + (obj.pos[1] - player.pos[1]) / 20
            pygame.draw.circle(disp, color, (x, y), r, width=2)



#---- main() -------------------------------------------------------------
def main():
    commands = {'quit': False, 'left': 0, 'right': 0, 'thrust': 0, 'fire': 0}

    DISPLAY, CLOCK = init(MAX_X, MAX_Y)
    FONT = pygame.font.SysFont('arial', 20)

    player = Player()
    allsprites = pygame.sprite.Group(player)

    station = Station()
    allsprites.add(station)

    asteroids = pygame.sprite.Group()
    asteroids.add( Asteroid(vel=(-1,0.5), pos=(300,-250)) )
    asteroids.add( Asteroid(vel=(1,0.5)) )

    for n in range(8):
        a = random.randint(0, 360)
        r = random.randint(600, 1000)
        v = random.randint(25, 150) / 100.0
        p = PolarAsteroid(angle=a, radius=r, vel=v)
        asteroids.add(p)

    allsprites.add(asteroids)

    #main game loop
    while True:

        handle_events(commands)

        if commands['quit']:
            terminate()

        player.update(commands)
        asteroids.update(player.pos)
        station.update(player.pos)

        # draw main screen
        DISPLAY.fill(BGCOLOR)
        allsprites.draw(DISPLAY)

        draw_hud(DISPLAY, player)
        draw_radar_hud(DISPLAY)
        draw_radar_objects(DISPLAY, player, asteroids.sprites(), RED, 2)
        draw_radar_objects(DISPLAY, player, [station], BLUE, 6)
        #draw_radar_objects(DISPLAY, player, [player], WHITE, 3)

        i = 0
        for s in allsprites.sprites():
            msg_disp = FONT.render(f"{i}: {s}", True, GRAY, BLACK)
            #DISPLAY.blit(msg_disp, (10, 10+i*30))
            i += 1

        # advance game frame
        pygame.display.update()
        CLOCK.tick(FPS)


    terminate()

####
if __name__ == '__main__':
    main()



