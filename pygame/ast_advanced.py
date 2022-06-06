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
    def __init__(self, pos=[0,0], vel=[0,0]):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.vel = vel
        self.angle = 0
        self.drag = 0.9

    def update(self, *args):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]



#---- class: Player --------------------------------------------------------
class Player(GameObject):

    def __init__(self):
        GameObject.__init__(self)
        self.load_sprite()
        self.pos = [0, 0]
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
        pygame.draw.polygon(img, GRAY, pts, 4)
        self.image_orig = img


    def update(self, cmd):
        self.angle += 10 * (cmd['right'] + cmd['left'])
        if cmd['thrust']:
            self.vel[0] += math.cos(math.radians(self.angle))*0.5
            self.vel[1] += math.sin(math.radians(self.angle))*0.5

        GameObject.update(self)

        # prep for draw
        self.image = pygame.transform.rotate(self.image_orig, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = [ MAX_X/2, MAX_Y/2 ]


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

    player = Player()
    allsprites = pygame.sprite.Group(player)

    #main game loop
    while True:

        handle_events(commands)

        if commands['quit']:
            terminate()

        allsprites.update(commands)

        # draw main screen
        DISPLAY.fill(BGCOLOR)
        allsprites.draw(DISPLAY)


        msg = f"pos: ({player.pos[0]:.1f}, {player.pos[1]:.1f}, {player.angle:.1f})"
        msg_disp = FONT1.render(msg, True, WHITE, BLACK)
        DISPLAY.blit(msg_disp, (10, 10))



        # advance game frame
        pygame.display.update()
        CLOCK.tick(FPS)


    terminate()

####
if __name__ == '__main__':
    main()



