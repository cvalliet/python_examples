#!/usr/bin/env python3 -O

# IMPORTs ---------------------------------------------------------------------

import math
import re
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
STEP = 1
ROTATION = PI_DIV_100

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

def main(init, loop, term):
    # INITIALIZATION
    pygame.init()

    # VARIABLES
    _clock = pygame.time.Clock()
    _font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    _screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | DOUBLEBUF)
    _display = pygame.Surface(DISPLAY_SIZE, HWSURFACE | DOUBLEBUF)
    _running = True

    init()

    # MAIN LOOP
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

        loop(_display)

        _screen.blit(pygame.transform.scale(_display, SCREEN_SIZE), ORIGIN)
        pygame.display.update()

        _clock.tick(FPS)

    # TERMINATION

    term()
    pygame.quit()

# CLASSEs ---------------------------------------------------------------------

class Arrow:
    def __init__(self, origin, length, angle):
        self._position = list(origin)
        self._length = length
        self._angle = angle
        self._font = pygame.font.SysFont(None, 16)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self._angle += 0.01
        elif keys[K_RIGHT]:
            self._angle -= 0.01

        if keys[K_UP]:
            return 1
        if keys[K_DOWN]:
            return -1

        return 0

    def display(self, surface):
        end = [self._position[0] + math.sin(self._angle) * self._length, self._position[1] + math.cos(self._angle) * self._length]

        pygame.draw.line(surface, 'yellow', self._position, end, 1)
        pygame.draw.circle(surface, 'red', self._position, self._length + 3, 1)

        x = self.move()
        """
                if x > 0:
                    self._position[0] += math.sin(self._angle)
                    self._position[1] += math.cos(self._angle)
                elif x < 0:
                    self._position[0] -= math.sin(self._angle)
                    self._position[1] -= math.cos(self._angle)
        """
        img = self._font.render('[%d, %d], %.2f' % (self._position[0], self._position[1], self._angle), True, 'blue')
        surface.blit(img, (10, 10))


# INITIALIZATION --------------------------------------------------------------

pygame.init()

# VARIABLES -------------------------------------------------------------------

_clock = pygame.time.Clock()
_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
_screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | DOUBLEBUF)
_display = pygame.Surface(DISPLAY_SIZE, HWSURFACE | DOUBLEBUF)
_running = True
_arrow = Arrow(DISPLAY_MIDDLE, 16, 0)

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

    _arrow.display(_display)

    _screen.blit(pygame.transform.scale(_display, SCREEN_SIZE), ORIGIN)
    pygame.display.update()

    _clock.tick(FPS)

# TERMINATION -----------------------------------------------------------------

pygame.quit()

# END OF FILE -----------------------------------------------------------------

class Coordinates:
    def __init__(self, ab, kind='polar'):
        if kind == 'polar':
            self._radius, self._theta = ab[0], ab[1]
            self._x, self._y = pol2cart(ab[0], ab[1])
        elif t == 'cartesian':
            self._radius, self._theta = cart2pol(ab[0], ab[1])
            self._x, self._y = ab[0], ab[1]
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

    def rect_at(self, width=1, height=1):
        return pygame.Rect(self._x, self._y, width, height)

    def draw_at(self, a, b):
        a.blit(b, self.position)

    def rect_around(self, width=1, height=1):
        return pygame.Rect(self._x - width / 2, self._y - height / 2, width, height)

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

    def draw_at(self, a, b):
        a.blit(b, self.position)

    def rect_around(self, width=1, height=1):
        return pygame.Rect(self._x - width / 2, self._y - height / 2, width, height)
