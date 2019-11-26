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


#### Class: GameObject ######################################################
class GameObject(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos = (0, 0)
        self.vel = (0, 0)
        self.angle = None
        self.is_animated = False

    def update(self):
        x = (self.pos[0] + self.vel[0]) % MAX_X
        y = (self.pos[1] + self.vel[1]) % MAX_Y
        self.pos = (x, y)

        if self.angle is not None:
            self.angle %= 360
            self.image = pygame.transform.rotate(self.image_orig, self.angle)
            self.rect = self.image.get_rect()

        self.set_position((x, y))
        if self.is_animated:
            self.advance_frame()

    def set_position(self, new_pos):
        self.pos = new_pos
        try:
            self.rect.center = self.pos
        except AttributeError:
            pass

    def load_image(self, filename):
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect( center=self.pos )

    def load_animation(self, filename, size, width, height, loop=True):
        self.spritesheet = pygame.image.load(filename).convert_alpha()
        self.frames = []
        for y in range(0, height):
            for x in range (0, width):
                sub_img = self.spritesheet.subsurface( (x*size, y*size, size, size) )
                self.frames.append(sub_img)
        self.is_animated = True
        self.animation_loops = loop
        self.reset_animation()

    def reset_animation(self, frame=0):
        self.image = self.frames[frame]
        self.rect = self.image.get_rect( center=self.pos )
        self.next_frame_idx = frame + 1

    def advance_frame(self):
        self.image = self.frames[self.next_frame_idx]
        self.next_frame_idx += 1
        if self.animation_loops:
            self.next_frame_idx %= len(self.frames)

    def is_animation_done(self):
        return self.next_frame_idx >= len(self.frames)

    def set_velocity(self, angle, speed):
        vel_x = math.cos(math.radians(self.angle)) * speed
        vel_y = -1 * math.sin(math.radians(self.angle)) * speed
        self.vel = (vel_x, vel_y)


#### Class: Asteroid ########################################################
class Asteroid(GameObject):

    def __init__(self):
        GameObject.__init__(self)

        side = random.randint(1, 4)
        if side == 1:    self.pos = (random.randint(0, MAX_X), 0)
        elif side == 2:  self.pos = (0, random.randint(0, MAX_Y))
        elif side == 3:  self.pos = (random.randint(0, MAX_X), MAX_Y)
        elif side == 4:  self.pos = (MAX_X, random.randint(0, MAX_Y))

        s = random.randint(3, 6)
        self.vel = (random.randint(-s, s), random.randint(-s, s))

        self.load_animation('assets/asteroid2.png', 64, 5, 6)


#### Class: Explosion ######################################################
class Explosion(GameObject):

    def __init__(self, pos):
        GameObject.__init__(self)
        self.load_animation('assets/explosion1_64x64.png', 64, 5, 5, False)
        self.set_position(pos)

    def is_done(self):
        return self.is_animation_done()

#### class: Shot ############################################################
class Shot(GameObject):
    def __init__(self, pos, angle, speed=20):
        GameObject.__init__(self)
        self.create_sprite()
        self.set_position(pos)
        self.angle = angle
        self.set_velocity(self.angle, speed)
        self.time_to_live = FPS//2

    def create_sprite(self):
        size = 8
        self.image = pygame.Surface((size, size))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, (192,  10,  10), (size//2, size//2), size//2)
        pygame.draw.circle(self.image, (192, 128, 128), (size//2, size//2), size//4)
        self.image_orig = self.image
        self.rect = self.image.get_rect()

    def update(self):
        GameObject.update(self)
        self.time_to_live -= 1

    def is_done(self):
        return self.time_to_live <= 0

#### class: Ship ##########################################################
class Ship(GameObject):

    def __init__(self):
        GameObject.__init__(self)
        self.load_image('assets/ship1_32x32.png')
        self.image_orig = self.image
        self.reset()

    def reset(self):
        self.set_position( (MAX_X//2, MAX_Y//2) )
        self.angle = 90
        self.vel = (0, 0)

    def update(self, thrust, left, right):
        if left:
            self.angle += 10
        if right:
            self.angle -= 10
        if thrust:
            vel_x = self.vel[0] + math.cos(math.radians(self.angle))*0.25
            vel_y = self.vel[1] - math.sin(math.radians(self.angle))*0.25
            self.vel = (vel_x, vel_y)

        GameObject.update(self)


#### helper functions #####################################################
def terminate():
    pygame.quit()
    sys.exit()



#### main ################################################################
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((MAX_X, MAX_Y))
BASICFONT = pygame.font.SysFont('arial', 12, True)
pygame.display.set_caption('pyGame Template')
random.seed()

background = pygame.image.load(f"assets/space_background.jpg").convert()

asteroids = pygame.sprite.RenderPlain( Asteroid() )
explosions = pygame.sprite.RenderPlain()
shots = pygame.sprite.RenderPlain()
ship = Ship()
ships = pygame.sprite.RenderPlain(ship)

score = 0
level = 1
lives = 2
cmd_thrust = False
cmd_left = False
cmd_right = False
delay_game = 0

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
            if event.key == K_LCTRL:
                if ship.alive():
                    sh = Shot(ship.pos, ship.angle)
                    shots.add(sh)

        elif event.type == KEYUP:
            if event.key == K_UP:    cmd_thrust = False
            if event.key == K_LEFT:  cmd_left = False
            if event.key == K_RIGHT: cmd_right = False

            if event.key == K_n:
                asteroids.add( Asteroid() )
            if event.key == K_ESCAPE:
                terminate()

    #update game objects
    asteroids.update()
    explosions.update()
    shots.update()
    if ship.alive():
        ships.update(cmd_thrust, cmd_left, cmd_right)

    for exp in explosions.sprites():
        if exp.is_done():
            exp.kill()

    for sh in shots.sprites():
        if sh.is_done():
            sh.kill()

    # detect collisions
    for a in pygame.sprite.spritecollide(ship, asteroids, False):
        if ship.alive():
            explosions.add(Explosion(ship.pos))
            ship.kill()

    for a in pygame.sprite.groupcollide(asteroids, shots, True, True).keys():
        explosions.add(Explosion(a.pos))
        score += 10


    # draw frame
    #DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(background, (0, 0))
    shots.draw(DISPLAYSURF)
    ships.draw(DISPLAYSURF)
    asteroids.draw(DISPLAYSURF)
    explosions.draw(DISPLAYSURF)

    msg = f"LEVEL: {level}   SCORE: {score}    LIVES: {lives}"
    msg_disp = BASICFONT.render(msg, True, WHITE, BLACK)
    DISPLAYSURF.blit(msg_disp, (10, 10))

    # show some debuging info
    real_fps = FPSCLOCK.get_fps()
    sprite_count = len(asteroids) + len(explosions) + len (shots) + len(ships)
    debug_msg = f"FPS: {real_fps:.2f}   SPRITES: {sprite_count}"
    debug_msg_surf = BASICFONT.render(debug_msg, True, WHITE, BLACK)
    DISPLAYSURF.blit(debug_msg_surf, (10, 28))


    if len(asteroids) == 0 and len(explosions) == 0:
        level += 1
        ship.reset()
        for i in range (0, level):
            asteroids.add( Asteroid() )
        delay_game = FPS*2

    if len(ships) == 0 and len(explosions) == 0 and lives > 0:
        lives -= 1
        ship = Ship()
        ships.add(ship)
        delay_game = FPS*2

    if delay_game > 0:
        delay_game -= 1

    #advance frame
    #pygame.display.update()
    pygame.display.flip()
    FPSCLOCK.tick(FPS)


terminate()   # won't actually get called
