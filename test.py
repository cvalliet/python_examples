#!/usr/bin/env python3 -O

# IMPORTs ---------------------------------------------------------------------

import math
import numpy
import os
import pygame
from pygame.locals import *
import sys

# CONSTANTs -------------------------------------------------------------------

FPS = 60
ORIGIN = 0, 0
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT
SCREEN_MIDDLE = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
DISPLAY_WIDTH, DISPLAY_HEIGHT = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT
DISPLAY_MIDDLE = DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2
FONT_NAME = 'Monospace'
FONT_SIZE = 14
PI_DIV_100 = math.pi * 0.01
IMAGE_NAME = 'target.png'
MAP_NAME = 'map256.png'

# FUNCTIONs -------------------------------------------------------------------

def get_program_name():
    return os.path.basename(sys.argv[0])

def get_module_path(name = '__main__'):
    module = sys.modules[name]
    if module:
        path, name = os.path.split(module.__file__)
        return path, name

def is_module_main():
    return __name__ == '__main__'

def draw_text(display, font, text, color, position):
    surface = font.render(text, True, color)
    display.blit(surface, position)

def cart2pol(x, y):
    rho = numpy.sqrt(x**2 + y**2)
    phi = numpy.arctan2(y, x)
    return rho, phi

def pol2cart(rho, phi):
    x = rho * numpy.cos(phi)
    y = rho * numpy.sin(phi)
    return x, y

def draw_robot(surface, xy, radius, next_xy):
    pygame.draw.circle(surface, 'red', (self._x, self._y), self._radius)
    start_pos = self._x, self._y
    end_pos = start_pos[0] + 4 * self._vx, start_pos[1] + 4 * self._vy
    pg.draw.line(surface, 'yellow', start_pos, end_pos , 1)

# CLASSEs ---------------------------------------------------------------------

class Coordinates:
    def __init__(self, a, b, kind='polar'):
        if kind == 'polar':
            self._radius, self._theta = a, b
            self._x, self._y = pol2cart(a, b)
        elif t == 'cartesian':
            self._radius, self._theta = cart2pol(a, b)
            self._x, self._y = a, b
        else:
            raise Exception('bad type "%s"' % kind)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def radius(self):
        return self._radius

    @property
    def theta(self):
        return self._theta

    def as_cartesian(self):
        return self._x, self._y
    
    def as_polar(self):
        return self._r, self._theta

    def rotate(self, step=PI_DIV_100):
        self._theta += step
        self._x, self._y = pol2cart(self._radius, self._theta)

    def move_to(self, x, y):
        self._x, self._y = x, y
        self._radius, self._theta = cart2pol(x, y)

class MoveVector:
    def __init__(self, xy, alpha):
        self._x, self._y = xy
        self._alpha = alpha

    def __str__(self):
        return 'MoveVector: x=%0.2f, y=%0.2f, alpha=%0.2f' % (self._x, self._y, self._alpha)

    def x(self):
        return self._x

    def y(self):
        return self._y

    def xy(self):
        return self._x, self._y

    def alpha(self):
        return self._alpha

    def position(self):
        return self._x, self._y

    def rotate(self, step=PI_DIV_100):
        self._alpha += step

    def move(self, step=1):
        self._x += step * math.sin(self._alpha)
        self._y += step * math.cos(self._alpha)

    def move_to(self, x, y, alpha):
        self._x, self._y, self._alpha = x, y, alpha

    def rect_at(self, width=1, height=1):
        return pygame.Rect(self._x, self._y, width, height)
    
    def rect_around(self, width=1, height=1):
        return pygame.Rect(self._x - width / 2, self._y - height / 2, width, height)

class MoveImage(MoveVector):
    def __init__(self, filename, xy, alpha=0, colorkey=0):
        super().__init__(xy, alpha)
        self._image = pygame.image.load(filename).convert()
        if colorkey == 0:
            colorkey = self._image.get_at(ORIGIN)
        self._image.set_colorkey(colorkey)

    def draw(self, display):
        surface = pygame.transform.rotate(self._image, math.degrees(self._alpha))
        rect = surface.get_rect()
        rect.center = self._x + self._image.get_width() // 2, self._y + self._image.get_height() // 2
        display.blit(surface, rect)

# INITIALIZATION --------------------------------------------------------------

pygame.init()

# VARIABLES -------------------------------------------------------------------

_clock = pygame.time.Clock()
_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
_screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | DOUBLEBUF)
_display = pygame.Surface(DISPLAY_SIZE, HWSURFACE | DOUBLEBUF)
_running = True
_direction = 0
_protagonist = MoveVector(DISPLAY_MIDDLE, 0.0)
_rose = MoveImage(IMAGE_NAME, (8, 24))
_map = MoveImage(MAP_NAME, (72, 32), 0, 1)

# MAIN LOOP -------------------------------------------------------------------

while _running:
    _display.fill('black')

    for event in pygame.event.get():
        if event.type == QUIT:
            _running = False
            break
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                _running = False
                break

    mods = pygame.key.get_mods()
    keys = pygame.key.get_pressed()

    _direction = 0
    if keys[K_UP]:
        _direction += 1
    if keys[K_DOWN]:
        _direction -= 1
    if keys[K_LEFT]:
        _protagonist.rotate()
        _rose.rotate()
    if keys[K_RIGHT]:
        _protagonist.rotate(-PI_DIV_100)
        _rose.rotate(-PI_DIV_100)

    _map.draw(_display)
    _protagonist.move(_direction)
    _rose.draw(_display)

    draw_text(_display, _font, str(_protagonist), 'green', (8, 8))
    _screen.blit(pygame.transform.scale(_display, SCREEN_SIZE), ORIGIN)
    pygame.display.update()

    _clock.tick(FPS)

# TERMINATION -----------------------------------------------------------------

pygame.quit()

# END OF FILE -----------------------------------------------------------------
