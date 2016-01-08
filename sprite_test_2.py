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
    """
    Helper class to manage loading sprite sheet image files, slicing
    them up into frames.  Ensures only one copy exists in memory.
    """

    sprites = { }
    sheet1 = None
    sheet2 = None

    def __init__(self):
        self.load_asteroid_sprites()
        self.load_explosion_sprites()
        self.load_ship_sprite()

    def load_asteroid_sprites(self):
        self.sheet1 = pygame.image.load('assets/asteroid2.png')
        images = self._extract_sprites(self.sheet1, 64, 6, 5)
        self.sprites['asteroid'] = images

    def load_explosion_sprites(self):
        self.sheet2 = pygame.image.load('assets/explosion1_64x64.png')
        images = self._extract_sprites(self.sheet2, 64, 5, 5)
        self.sprites['explosion'] = images

    def load_ship_sprite(self):
        img = pygame.Surface((32, 32))
        img.fill(WHITE)
        img.set_colorkey(WHITE)
        pts = ( (32, 16), (0, 28), (0, 4) )
        #pts = ( (32, 16), (4, 28), (4, 4) )
        pygame.draw.polygon(img, GRAY, pts, 3)
        self.sprites['ship'] = img


    @staticmethod
    def _extract_sprites(sheet, size, rows, columns):
        images = []
        for y in range(0, rows):
            for x in range (0, columns):
                rect = (x*size, y*size, size, size)
                img = sheet.subsurface(rect)
                images.append(img)
        return images


    def get_sprites(self, name):
        return self.sprites[name]



#---- class: AnimatedSprite ----------------------------------------------
class AnimatedSprite(pygame.sprite.Sprite):

    frames = None  #list of ordered images used for animation
    repeat = True  #loop through frames or stop at the last one?

    @classmethod
    def set_frames(cls, frame_images):
        cls.frames = frame_images

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()

    def advance_frame(self, increment = 1):
        self.index += increment
        max_index = len(self.frames)-1
        if self.index > max_index:
            if self.repeat:
                self.index = 0
            else:
                self.index = max_index

    def is_done(self):
        return not self.repeat and self.index >= len(self.frames)-1

    def update(self, frames = 1):
        self.advance_frame(frames)
        self.image = self.frames[self.index]
        if self.is_done():
            self.kill()


#---- class: GameObject --------------------------------------------------
class GameObject():
    """
    Base class containing logic for objects in the game. Implements the physics
    of position and velocity.
    """
    def __init__(self, pos=[0,0], vel=[0,0]):
        self.pos = pos
        self.vel = vel
        self.angle = 0

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
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



#---- class: Asteroid ----------------------------------------------------
class Asteroid(AnimatedSprite, GameObject):

    def __init__(self, pos=[0,0], vel=[0,0]):
        AnimatedSprite.__init__(self)
        GameObject.__init__(self, pos, vel)

    def update(self, commands):
        AnimatedSprite.update(self)
        GameObject.update(self)
        self.rect.center = self.pos


#---- class: Explosion ---------------------------------------------------
class Explosion(AnimatedSprite):

    def __init__(self, pos):
        AnimatedSprite.__init__(self)
        self.repeat = False
        self.rect.center = pos

#---- class: Ship --------------------------------------------------------
class Ship(pygame.sprite.Sprite, GameObject):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        GameObject.__init__(self)
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.pos = [MAX_X/2, MAX_Y/2]
        self.angle = 270

    def update(self, cmd):
        self.angle += 10 * (cmd['right'] + cmd['left'])
        if cmd['thrust']:
            self.vel[0] += math.cos(math.radians(self.angle))*0.5
            self.vel[1] += math.sin(math.radians(self.angle))*0.5

        GameObject.update(self)

        self.image = pygame.transform.rotate(self.image_orig, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    @classmethod
    def set_image(cls, img):
        cls.image_orig = img


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

    sheet = Spritesheet()
    Asteroid.set_frames( sheet.sprites['asteroid'] )
    Explosion.set_frames( sheet.get_sprites('explosion') )
    Ship.set_image( sheet.sprites['ship'] )

    grp = pygame.sprite.RenderPlain()
    grp.add( Asteroid([140, 0], [3, 4]))
    #grp.add( Asteroid([MAX_X/2.0, MAX_Y/2.0]))
    #grp.add(Explosion([MAX_X/2.0, MAX_Y/2.0]))
    ship = Ship()
    grp.add(ship)


    #main game loop
    while True:

        handle_events(commands)

        if commands['quit']:
            terminate()

        grp.update(commands)

        # draw main screen
        DISPLAY.fill(BGCOLOR)
        grp.draw(DISPLAY)

        # advance game frame
        pygame.display.update()
        CLOCK.tick(FPS)


    terminate()

####
if __name__ == '__main__':
    main()



#---- class: Game --------------------------------------------------------
class Game():

    max_x = 0
    max_y = 0
    display = None
    clock = None
    gameover = False
    level = 1
    score = 0
    lives = 2
    highscore = 0

    def __init__(self, display, clock):
        self.display = display
        self.clock = clock
        self.max_x = self.display.get_width()
        self.max_y = self.display.get_height()

        self.asteroids = pygame.sprite.RenderPlain()
        self.create_level()

    def create_level(self):
        for i in range(0, self.level):
            pos_x = random.randint(0, self.max_x)
            a = Asteroid([pos_x, 0], [3,4])
            self.asteroids.add(a)


    def main_loop(self):
        while not self.gameover:
            self.handle_events()
            self.update()
            self.detect_collisions()
            self.draw()
            self.clock.tick(FPS)

    def update(self):
        self.asteroids.update()

    def detect_collisions(self):
        pass

    def draw(self):
        self.display.fill(BGCOLOR)
        self.asteroids.draw(self.display)
        pygame.display.update()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_q:
                    self.gameover = True



