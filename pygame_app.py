#! /usr/bin/env python3

# *** NOT IMPORTABLE!!!
if __name__ != '__main__':
    import os
    raise Exception('This python script "%s" is not an import module!' % os.path.basename(__file__))

# *** IMPORTS

import math
import numpy
import os
import pygame
import sys

# *** FROM

from pygame.locals import *

# *** CLASSES

class TObject:
    def __init__(self, xy=(0, 0)):
        self._x, self._y = xy[0], xy[1]

    def __str__(self):
        return 'TObject: x = %d, y = %d' % (self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def xy(self):
        return self._x, self._y

    def assign(self, xy=(0, 0)):
        self._x, self._y = xy[0], xy[1]

class TMovingObject(TObject):
    def __init__(self, xy=(0, 0), direction=0):
        super().__init__(xy)
        self._direction = direction

    def __str__(self):
        return 'TMovingObject: x = %d, y = %d, direction = %0.2f' % (self._x, self._y, self._direction)

    @property
    def direction(self):
        return self._direction

    def assign(self, xy=(0, 0), direction=0):
        super().assign(xy)
        self._direction = direction

    def rotate(self, step=math.pi/100., increment=True):
        if increment:
            self._direction += step
        else:
            self._direction = step

    def move(self, step=1):
        self._x += step * math.cos(self._direction)
        self._y += step * math.sin(self._direction)

class TPygameApplication:
    def __init__(self, size=(800, 600)):
        if not pygame.get_init():
            pygame.init()

        self._clock = pygame.time.Clock()
        self._display = pygame.display.set_mode(size, HWSURFACE|DOUBLEBUF, 32)
        self._running = True

    def on_initialize(self):
        pass

    def on_loop(self):
        self._display.fill('black')

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self._running = False

    def on_display(self, display):
        pass

    def execute(self):
        self.on_initialize()

        while self._running:
            self.on_loop()

            for event in pygame.event.get():
                self.on_event(event)

            self.on_display(self._display)

            pygame.display.flip()
            self._clock.tick(60)

class TestApplication(TPygameApplication):
    def __init__(self):
        super().__init__()

    def on_initialize(self):
        self._arrow = TMovingObject((200, 150))
    
    def on_loop(self):
        self._display.fill('green')
    
    def on_event(self, event):
        super().on_event(event)

    def on_display(self, display):
        keys = pygame.key.get_pressed()

        if keys[K_UP]:
            self._arrow.move(-1)
        if keys[K_DOWN]:
            self._arrow.move()
        if keys[K_LEFT]:
            self._arrow.rotate(-math.pi/100.)
        if keys[K_RIGHT]:
            self._arrow.rotate()

        pygame.draw.circle(self._display, 'red', self._arrow.xy, 20, 1)

# *** BODY
TestApplication().execute()
