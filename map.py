#!/usr/bin/env python3

# IMPORTs ---------------------------------------------------------------------

import math
import pygame
import os
import sys


# FROMs ---------------------------------------------------------------------------------------------------------------

from pygame.locals import *


# VARIABLEs -----------------------------------------------------------------------------------------------------------

FONT_NAME = 'Monospace'
MAP_NAME = 'map2.png'
FONT_SIZE = 14
ORIGIN = 0, 0
SCREEN_SIZE = 640, 480
SCALE = 2
DISPLAY_SIZE = SCREEN_SIZE[0] // SCALE, SCREEN_SIZE[1] // SCALE
MIDDLE = DISPLAY_SIZE[0] // 2, DISPLAY_SIZE[1] // 2
FPS = 60


# FUNCTIONs -----------------------------------------------------------------------------------------------------------

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


def blit_rotate(surf, image, pos, originPos, angle):
    # calculate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

    # draw rectangle around the image
    pygame.draw.rect (surf, (255, 0, 0), (*origin, *rotated_image.get_size()),2)



# CLASSEs -------------------------------------------------------------------------------------------------------------

class Map:
    def __init__(self, filename):
        self._image = pygame.image.load(filename).convert()

    def display(self, surface, angle, position):
        # surface.blit(self._image, ORIGIN)
        angle *= 120 / math.pi
        surface.blit(pygame.transform.rotate(self._image, angle), position)


class Protagonist:
    def __init__(self, origin, length, angle):
        self._position = list(origin)
        self._length = length
        self._angle = angle
        self._font = pygame.font.SysFont(None, 16)
        self._move = 0

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self._angle += 0.01
        elif keys[K_RIGHT]:
            self._angle -= 0.01

        self._move = 0
        if keys[K_UP]:
            self._move = 1
        if keys[K_DOWN]:
            self._move = -1

        return self._move

    def draw(self, surface):
        end = [self._position[0] + math.sin(self._angle) * self._length, self._position[1] + math.cos(self._angle) * self._length]

        color = 'red'
        if self._move > 0:
            color = 'green'
        elif self._move < 0:
            color = 'yellow'

        pygame.draw.line(surface, color, self._position, end, 1)
        pygame.draw.circle(surface, 'red', self._position, self._length + 3, 1)

        if self._move > 0:
            self._position[0] += math.sin(self._angle)
            self._position[1] += math.cos(self._angle)
        elif self._move < 0:
            self._position[0] -= math.sin(self._angle)
            self._position[1] -= math.cos(self._angle)


# ENTRYPOINT ----------------------------------------------------------------------------------------------------------

if is_module_main():
    pygame.init()

    frame = 0
    running = True

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | DOUBLEBUF)
    display = pygame.Surface(DISPLAY_SIZE, HWSURFACE | DOUBLEBUF)
    protagonist = Protagonist(ORIGIN, 20, 0)
    map = Map(MAP_NAME)

    while running:
        display.fill('black')

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    break

        # Draw on display surface...
        map.display(display, protagonist._angle, protagonist._position)
        protagonist.move()
        protagonist.draw(display)

        screen.blit(pygame.transform.scale(display, SCREEN_SIZE), ORIGIN)

        # Draw on screen surface...
        draw_text(screen, font, 'frame %d' % frame, 'yellow', (8, 8))
        draw_text(screen, font, '[%d, %d], %.2f' % (protagonist._position[0], protagonist._position[1], protagonist._angle), 'yellow', (8,24))

        pygame.display.flip()

        clock.tick(FPS)
        frame += 1

    pygame.quit()

# END OF FILE ---------------------------------------------------------------------------------------------------------
