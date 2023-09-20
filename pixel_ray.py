#!/usr/bin/env python3

# IMPORTs -------------------------------------------------------------------------------------------------------------

import numpy
import pygame
import os
import sys
import time


# FROMs ---------------------------------------------------------------------------------------------------------------

from pygame.locals import *


# VARIABLEs   ---------------------------------------------------------------------------------------------------------

Map = [
    '##########',
    '#        #',
    '# ###### #',
    '#      # #',
    '# #### # #',
    '# #  # # #',
    '# #    # #',
    '# ###### #',
    '#        #',
    '##########',
]


# FUNCTIONs -----------------------------------------------------------------------------------------------------------


def vector2_length(v):
    return numpy.sqrt(v[0]*v[0] + v[1]*v[1])


def vector2_convert_as_int(v):
    return int(v[0]), int(v[1])

def vector2_add(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def vector2_substract(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


def vector2_multiply(v, scalar):
    return v[0] * scalar, v[1] * scalar


def vector2_rotate(v, angle):
    return v[0] * numpy.cos(angle) - v[1] * numpy.sin(angle), v[0] * numpy.sin(angle) + v[1] * numpy.cos(angle)


def map_draw(map, map_size, block_size):
    surface = pygame.Surface((block_size*map_size, block_size*map_size))
    for row in range(map_size):
        for col in range(map_size):
            color = (192, 192, 192) if map[row][col] == '#' else (96, 96, 96)
            pygame.draw.rect(surface, color, (col * block_size, row * block_size, block_size-1, block_size-1))

    return surface


def map_is_empty(map, map_size, block_size, position):
    x, y = int(position[0] // block_size), int(position[1] // block_size)
    return map[y][x] == ' '


def map_special(map, map_size, block_size, position, direction):
    factor = 1 / block_size
    a = vector2_multiply(position, factor)
    mp = vector2_convert_as_int(a)

    # direction x positive
    if direction[0] > 0:
        next_x = mp[0] + 1
    else:
        next_x = mp[0]
    if direction[1] > 0:
        next_y = mp[1] + 1
    else:
        next_y = mp[1]

    #mp = int(position[0] // block_size), int(position[1] // block_size)
    #a = position[0] / block_size, position[1] / block_size
    #b = a[0] - mp[0], a[1] - mp[1]
    #c = 1 - b[0], 1 - b[1]
    #d = vector2_add(c, direction)

    return mp, a, direction, (next_x, next_y)


def text_draw(surface, text, position, font):
    text_surface = font.render(text, True, 'white', 'black')
    surface.blit(text_surface, position)


# CLASSEs -------------------------------------------------------------------------------------------------------------

class PygameApplication:
    def __init__(self):
        self._clock = pygame.time.Clock()
        self._frame = 0
        self._running = False

        self._font = None
        self._window = None
        self._screen = None

    def Run(self, fps, window_size, screen_size, font_name, font_size):
        self._font = pygame.font.SysFont(font_name, font_size)
        self._window = pygame.display.set_mode(window_size, HWSURFACE | DOUBLEBUF)
        self._screen = pygame.Surface(screen_size, HWSURFACE | DOUBLEBUF)
        self._running = True

        ROTATION_SPEED = 0.1
        MOVE_SPEED = 0.6

        # origin vector
        origin = 0, 0
        # middle vector
        middle = screen_size[0] // 2, screen_size[1] // 2
        # position vector
        position = 21., 24.
        # direction vector
        direction = -1., 0.
        # plane vector
        ratio = 1.
        plane = 0., ratio

        map_surface = map_draw(Map, 10, 16)
        #pygame.image.save(map_surface, "map.png")

        map_show = True
        while (self._running):
            self._screen.fill('black')
            if map_show:
                self._screen.blit(map_surface, origin)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self._running = False
                    break

            # Write your keyboard, mouse and display management code here...
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                self._running = False
                break

            if keys[K_n]:
                direction = 0, -1
                plane = -ratio, 0

            if keys[K_s]:
                direction = 0, 1
                plane = ratio, 0

            if keys[K_e]:
                direction = 1, 0
                plane = 0, -ratio

            if keys[K_w]:
                direction = -1, 0
                plane = 0, ratio

            if keys[K_m]:
                map_show = not map_show

            if keys[K_RIGHT]:
                direction = vector2_rotate(direction, ROTATION_SPEED)
                plane = vector2_rotate(plane, ROTATION_SPEED)

            if keys[K_LEFT]:
                direction = vector2_rotate(direction, -ROTATION_SPEED)
                plane = vector2_rotate(plane, -ROTATION_SPEED)

            if keys[K_UP]:
                expected_position = vector2_add(position, vector2_multiply(direction, MOVE_SPEED))
                if map_is_empty(Map, 10, 16, expected_position):
                    position = expected_position
                    mp = map_special(Map, 10, 16, position, direction)
                    print(mp)

            if keys[K_DOWN]:
                expected_position = vector2_add(position, vector2_multiply(direction, -MOVE_SPEED))
                if map_is_empty(Map, 10, 16, expected_position):
                    position = expected_position
                    mp = map_special(Map, 10, 16, position, direction)
                    print(mp)

            pygame.draw.circle(self._screen, 'red', position, 5.)
            end = vector2_add(vector2_multiply(direction, 4.), position)
            pygame.draw.line(self._screen, 'yellow', position, end)

            for column in range(0, 160):
                height = 160
                line_start = 0
                line_end = 160
                pygame.draw.line(self._screen, 'lightblue' if column % 2 else 'blue', (column + 160, line_start), (column + 160, line_end))

            pygame.transform.scale2x(self._screen, self._window)
            pygame.display.flip()

            if keys[K_SPACE]:
                pygame.image.save(self._screen, f"{time.strftime('%Y%m%d%H%M%S')}_screen.png")

            self._clock.tick(fps)
            self._frame += 1

            pygame.display.set_caption(f'PIXEL ART - Frame : #{self._frame % 1000:04d}')


# VARIABLEs -----------------------------------------------------------------------------------------------------------

PROGRAM_NAME = os.path.basename(sys.argv[0])
FONT_NAME = 'Monospace'
FONT_SIZE = 14
WINDOW_SIZE = 640, 640
SCREEN_SIZE = 320, 320
FPS = 30


# FUNCTIONs -----------------------------------------------------------------------------------------------------------

def Main():
    pygame.init()

    PygameApplication().Run(FPS, WINDOW_SIZE, SCREEN_SIZE, FONT_NAME, FONT_SIZE)

    pygame.quit()


# ENTRYPOINT ----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    Main()


# DEPRECATED

"""
            # Field Of View
            #rays = []
            WIDTH = 160
            for column in range(0, WIDTH, 1):
                x = 1 - 2 * column / WIDTH
                ray = vector2_add(direction, vector2_multiply(plane, x))
                start = position
                for length in range(0, 256, 1):
                    next = vector2_multiply(ray, length)
                    end = vector2_add(next, position)
                    if not map_is_empty(Map, 10, 16, end):
                        height = round(1024 / length if length != 0 else 80)
                        #print(column, height)
                        wall_start = 160 + column, 160 // 2 - height
                        wall_end = 160 + column, 160 // 2 + height
                        component = 128 + (height / 4) % 128
                        if column % 2:
                            pygame.draw.line(self._screen, (component,0,0), wall_start, wall_end)
                        else:
                            pygame.draw.line(self._screen, (0,component,0), wall_start, wall_end)

                        color = 'magenta'
                        if column < 10:
                            color = 'blue'
                        elif column > WIDTH - 11:
                            color = 'lightblue'
                        pygame.draw.line(self._screen, color, start, end)
                        break

            # position + direction * 10 => display direction vector with a length or 10 pixels
            end = vector2_add(vector2_multiply(direction, 10), position)
            pygame.draw.line(self._screen, 'yellow', position, end)
"""

# END OF FILE ---------------------------------------------------------------------------------------------------------
