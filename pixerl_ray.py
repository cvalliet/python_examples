#!/usr/bin/env python3

# IMPORTs -------------------------------------------------------------------------------------------------------------

import math
import numpy
import pygame
import os
import sys


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
    return math.sqrt(v[0]*v[0] + v[1]*v[1])


def vector2_add(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def vector2_substract(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


def vector2_multiply(v, scalar):
    return v[0] * scalar, v[1] * scalar


def vector2_rotate(v, angle):
    return v[0] * math.cos(angle) - v[1] * math.sin(angle), v[0] * math.sin(angle) + v[1] * math.cos(angle)


def map_draw(map, map_size, block_size):
    surface = pygame.Surface((block_size*map_size, block_size*map_size))
    for row in range(map_size):
        for col in range(map_size):
            color = (192, 192, 192) if map[row][col] == '#' else (96, 96, 96)
            pygame.draw.rect(surface, color, (col * block_size, row * block_size, block_size - 2, block_size - 2))

    return surface


def map_is_empty(map, map_size, block_size, position):
    x, y = int(position[0] // block_size), int(position[1] // block_size)
    return map[y][x] == ' '


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

        ROTATION_SPEED = 0.05
        MOVE_SPEED = 0.3

        # origin vector
        origin = 0, 0
        # middle vector
        middle = screen_size[0] // 2, screen_size[1] // 2
        # position vector
        position = 21, 24
        # direction vector
        direction = -1, 0
        # plane vector
        plane = 0, 0.66

        map_surface = map_draw(Map, 10, 16)
        #pygame.image.save(map_surface, "map.png")

        dir = ''
        map_show = False
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
                plane = -0.66, 0

            if keys[K_s]:
                direction = 0, 1
                plane = 0.66, 0

            if keys[K_e]:
                direction = 1, 0
                plane = 0, -0.66

            if keys[K_w]:
                direction = -1, 0
                plane = 0, 0.66

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

            if keys[K_DOWN]:
                expected_position = vector2_add(position, vector2_multiply(direction, -MOVE_SPEED))
                if map_is_empty(Map, 10, 16, expected_position):
                    position = expected_position

            pygame.draw.circle(self._screen, 'red', position, 5.)

            # Field Of View
            rays = []
            WIDTH = 20
            for column in range(1, WIDTH, 1):
                x = 2 * column / WIDTH - 1
                ray = vector2_add(direction, vector2_multiply(plane, x))
                for length in range(0, 256, 1):
                    next = vector2_multiply(ray, length)

                    end = vector2_add(next, position)
                    if not map_is_empty(Map, 10, 16, end):
                        rays.append((end, length))
                        break

                pygame.draw.line(self._screen, 'magenta', position, end)

            # position + direction * 10 => display direction vector with a length or 10 pixels
            end = vector2_add(vector2_multiply(direction, 10), position)
            pygame.draw.line(self._screen, 'yellow', position, end)
            pygame.transform.scale2x(self._screen, self._window)

            pygame.display.flip()

            if keys[K_SPACE]:
                pygame.image.save(self._screen, "screen.png")

            self._clock.tick(fps)
            self._frame += 1

            pygame.display.set_caption(f'PIXEL ART - Frame : #{self._frame % 1000:04d}')


# VARIABLEs -----------------------------------------------------------------------------------------------------------

PROGRAM_NAME = os.path.basename(sys.argv[0])
FONT_NAME = 'Monospace'
FONT_SIZE = 14
WINDOW_SIZE = 640, 640
SCREEN_SIZE = 320, 320
FPS = 60


# FUNCTIONs -----------------------------------------------------------------------------------------------------------

def Main():
    pygame.init()

    PygameApplication().Run(FPS, WINDOW_SIZE, SCREEN_SIZE, FONT_NAME, FONT_SIZE)

    pygame.quit()


# ENTRYPOINT ----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    Main()


# END OF FILE ---------------------------------------------------------------------------------------------------------


"""
#!/usr/bin/env python3

import math
import pygame

from pygame.locals import *
from typing import overload

BOARD = (
    '################'
    '#              #'
    '# ########## # #'
    '# #        # # #'
    '# # # #### # # #'
    '# # # #  # # # #'
    '# # # ## # # # #'
    '# # #  # # # # #'
    '# # ## # # # # #'
    '# ###  #   # # #'
    '# #   ###### # #'
    '# # ######   # #'
    '# #        # # #'
    '# ########## # #'
    '#              #'
    '################'
)

ORIGIN = 60, 60
TILE_SIZE = 32
MOVE_SPEED = 0.03
ROTATION_STEP = 0.03

class Drawing:
    @staticmethod
    def Vector2Add(a, b):
        return a[0] + b[0], a[1] + b[1]

    @staticmethod
    def Vector2Substract(a, b):
        return a[0] - b[0], a[1] - b[1]

    @staticmethod
    def Vector2Multiply(a, b):
        return a[0] * b, a[1] * b

    @staticmethod
    def Vector2Rotate(a, b):
        return a[0] * math.cos(b) - a[1] * math.sin(b), a[0] * math.sin(b) + a[1] * math.cos(b)

    @staticmethod
    def Vector2Length(a):
        return math.sqrt(a[0]**2 + a[1]**2)

    @staticmethod
    def Vector2AsInt(a):
        return int(a[0]), int(a[1])

    @staticmethod
    def CreateSurface(self, size):
        return pygame.Surface(size)

    def __init__(self, surface, font, origin=ORIGIN, factor=1):
        self.origin_ = origin
        self.factor_ = factor
        self.surface_ = surface
        self.font_ = font

    @property
    def surface(self):
        return self.surface_

    def __GetPosition(self, point):
        return Drawing.Vector2Add(Drawing.Vector2Multiply(point, self.factor_), self.origin_)

    def Circle(self, color, point, radius):
        pygame.draw.circle(self.surface_, color, self.__GetPosition(point), self.factor_ * radius)

    def Line(self, color, start, end):
        pygame.draw.line(self.surface_, color, self.__GetPosition(start), self.__GetPosition(end))

    def Rectangle(self, color, point, size):
        p = self.__GetPosition(point)
        w, h = size[0] * self.factor_, size[1] * self.factor_
        pygame.draw.rect(self.surface_, color, (p[0], p[1], w, h))

    def Text(self, colors, point, text):
        text_surface = self.font_.render(text, True, colors[0], colors[1])
        self.surface_.blit(text_surface, self.__GetPosition(point))

    def Clear(self, color='black'):
        self.surface_.fill(color)

    def Image(self, image, position=(0,0)):
        self.surface_.blit(image, position)

    def Update(self):
        pygame.display.flip()


class Map:
    def __init__(self, board, width, height):
        self.board_ = board
        self.width_ = width
        self.height_ = height

    @property
    def board(self):
        return self.board_

    @property
    def width(self):
        return self.width_

    @property
    def height(self):
        return self.height_

    def IsEmpty(self, x, y):
        return '#' != self.board_[int(x) + int(y) * self.width_]

    def IsEmpty2(self, xy):
        return '#' != self.board_[int(xy[0]) + int(xy[1]) * self.width_]

    def CreateSurface(self, factor=1, border=0):
        surface = pygame.Surface((self.width_*factor, self.height_*factor))
        for col in range(self.width_):
            for row in range(self.height_):
                color = (192, 192, 192) if self.board_[col + row * self.width] == '#' else (96, 96, 96)
                pygame.draw.rect(surface, color, (col * factor, row * factor, factor - border, factor - border))

        return surface

    def Draw(self, drawing):
        for col in range(self.width_):
            for row in range(self.height_):
                color = (192, 192, 192) if self.board_[col + row * self.width] == '#' else (96, 96, 96)
                drawing.Rectangle(color, (col, row), (1, 1))


class LineEquation:
    def __init__(self, position, angle):
        self.m_ = math.tan(angle)
        self.p_ = position[1] - self.m_ * position[0]

    def PointFromX(self, x):
        return x, self.m_ * x + self.p_

    def PointFromY(self, y):
        if self.m_ == 0:
            return math.inf, y

        return (y - self.p_) / self.m_, y

    def __str__(self):
        return str(f'y = {self.m_} * x + {self.p_}')


class Player:
    def __init__(self, position, direction):
        self.x_, self.y_ = position
        self.direction_ = direction

    @property
    def position(self):
        return self.x_, self.y_

    @property
    def x(self):
        return self.x_

    @property
    def y(self):
        return self.y_

    @property
    def direction(self):
        return self.direction_

    def Direction(self, length = 1.):
        return self.x_ + math.cos(self.direction_) * length, self.y_ + math.sin(self.direction_) * length

    def Move(self, speed):
        self.x_ += math.cos(self.direction_) * speed
        self.y_ += math.sin(self.direction_) * speed

    def MoveIf(self, speed, pred):
        x = self.x_ + math.cos(self.direction_) * speed
        y = self.y_ + math.sin(self.direction_) * speed

        if pred((x, y)):
            self.x_, self.y_ = x, y
            return True

        return False

    def Rotate(self, step):
        self.direction_ = (self.direction_ + step) % math.tau

    def Draw(self, drawing):
        drawing.Circle('white', self.position, .25)
        drawing.Line('white', self.position, self.Direction(1.))


class Raycasting:
    def __init__(self, map, player):
        self.map_ = map
        self.player_ = player

    @property
    def map(self):
        return self.map_

    @property
    def player(self):
        return self.player_

    def Draw(self, drawing):
        self.map_.Draw(drawing)
        self.player.Draw(drawing)
        equation = LineEquation(self.player_.position, self.player_.direction)

        x, y = self.player_.position


        stepX = stepY = 1

        if math.pi / 2 < self.player_.direction < math.pi:
            stepX = -1
        if math.pi < self.player_.direction < 3 * math.pi / 2:
            stepX = stepY = -1
        if 3 * math.pi / 2 < self.player_.direction < math.tau:
            stepY = -1

        p1 = equation.PointFromX(int(x) + stepX)
        drawing.Circle('red', p1, .1)
        p2 = equation.PointFromY(int(y) + stepY)
        drawing.Circle('blue', p2, .1)

        print(p1, p2)

def Main(window_size, fps):
    pygame.init()
    window = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()
    verdana_14 = pygame.font.SysFont('Verdana', 14)
    frame = 0
    running = True
    tile_size = TILE_SIZE
    drawing = Drawing(window, verdana_14, (0, 0), tile_size)
    map = Map(BOARD, 16, 16)
    map_image = map.CreateSurface(tile_size)
    player = Player((1., 1.), 0)
    raycasting = Raycasting(map, player)

    command_keys = {
        'left': K_LEFT,
        'right': K_RIGHT,
        'up': K_UP,
        'down': K_DOWN,
        'fire': K_SPACE
    }

    while running:
        for event in pygame.event.get():
            if QUIT == event.type:
                running = False
                continue

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            running = False
            continue

        if keys[command_keys['fire']]:
            pass
        if keys[command_keys['up']]:
            player.MoveIf(MOVE_SPEED, map.IsEmpty2)
        if keys[command_keys['down']]:
            player.MoveIf(-MOVE_SPEED, map.IsEmpty2)
        if keys[command_keys['right']]:
            player.Rotate(ROTATION_STEP)
        if keys[command_keys['left']]:
            player.Rotate(-ROTATION_STEP)

        drawing.Clear()

        raycasting.Draw(drawing)

        drawing.Update()

        clock.tick(fps)
        frame += 1

    pygame.quit()


if __name__ == '__main__':
    Main((800, 800), 60)


"""
class Player:
    def __init__(self, position, direction):
        self.x, self.y = position
        self.direction = direction

    @property
    def position(self):
        return self.x, self. y

    @property
    def positioni(self):
        return int(self.x), int(self.y)

    @property
    def slope(self):
        return math.tan(self.direction)

    def __str__(self):
        return f'pos:{self.x:0.1f},{self.y:0.1f};dir:{self.direction:0.1f};slope:{self.slope:0.1f}'

    def multiply(self, factor):
        return self.position[0] * factor, self.position[1] * factor

    def next_from_x(self, y):
        return self.x + y / math.tan(self.direction), y

    def next_from_y(self, x):
        return x, self.y + x * math.tan(self.direction)

    def rotate_if(self, pred, step):
        direction = (self.direction + step) % math.tau

        if pred(direction):
            self.direction += direction
            return True

        return False

    def rotate(self, step):
        self.direction += step
        self.direction %= math.tau

    def move_if(self, pred, step):
        x = self.x + math.cos(self.direction) * step
        y = self.y + math.sin(self.direction) * step

        if pred(x, y):
            self.x, self.y = x, y
            return True

        return False

    def move(self, step):
        self.x += math.cos(self.direction) * step
        self.y += math.sin(self.direction) * step

    def display(self, surface, factor=1, length=6):
        end = factor * self.x + math.cos(self.direction) * length, factor * self.y + math.sin(self.direction) * length
        pygame.draw.circle(surface, 'red', self.multiply(factor), 3.)
        pygame.draw.line(surface, 'yellow', self.multiply(factor), end)


class Map:
    def __init__(self, board, width, height):
        self._board = board
        self._width = width
        self._height = height
        self._image = None

    def __build(self, tile_size):
        if self._image:
            del self._image

        self._image = pygame.Surface((tile_size*self._width, tile_size*self._height))

        x = 1
        for col in range(self._width):
            for row in range(self._height):
                color = (192, 192, 192) if self._board[col + row * self._width] == '#' else (96, 96, 96)
                pygame.draw.rect(self._image, color, (col * tile_size, row * tile_size, tile_size - x, tile_size - x))

        return self._image

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def image(self, tile_size=16):
        if self._image:
            return self._image

        return self.__build(tile_size)

    def is_empty(self, x, y):
        return '#' != self._board[int(x) + int(y) * self._width]

    def is_empty2(self, xy):
        return '#' != self._board[int(xy[0]) + int(xy[1]) * self._width]

    def display(self, surface, dest=(0, 0), tile_size=16):
        surface.blit(self.image(tile_size), dest)

    def cast_rays(self, position, direction, fov, nb_rays=120, tile_size=16):
        start = direction - fov / 2
        step = fov / nb_rays

        rays = []
        for r in range(nb_rays):
            for depth in range(max(self._width, self._height)):
                target = position[0] - math.sin(start) * depth, position[1] + math.cos(start) * depth

                col, row = int(target[0]), int(target[1])
                print(col, row)
                #if not self.is_empty2(target):
                    # fix fish eye effect
                #    depth *= math.cos(direction - start)
                    # calculate wall height
                #    wall_height = 21000 / (depth + 0.0001)
                    # end point
                #    rays.append(((target[0] * tile_size, target[1] * tile_size), depth * tile_size, wall_height))

            start += step

def eval_step(r):
    if r > 0:
        return 1

    if r < 0:
        return -1

    return 0

def projections(surface, position, direction, tile_size):
    x, y = int(position[0]), int(position[1])
    dx, dy = position[0] - x, position[1] - y
    m = math.tan(direction)

    nx, ny = int(dx + position[0]), int(position[1] + dx * m)

    pygame.draw.rect(surface, 'white', (nx * tile_size, ny * tile_size, tile_size // 2, tile_size // 2))




def _projections(surface, position, direction, tile_size):
    x, y = int(position[0]), int(position[1])
    rx, ry = math.cos(direction), math.sin(direction)

    point = position[0] + rx, position[1] + ry

    point = point[0] * tile_size, point[1] * tile_size
    pygame.draw.circle(surface, 'white', point, 4.)

    point = x, y

    point = point[0] * tile_size, point[1] * tile_size
    pygame.draw.circle(surface, 'violet', point, 2.)

    if rx > 0:
        point = x + 1, position[1]
        color = 'lightblue'
    else:
        point = x - 1, position[1]
        color = 'blue'

    point = point[0] * tile_size, point[1] * tile_size
    pygame.draw.circle(surface, color, point, 2.)

    if ry > 0:
        point = position[0], y + 1
        color = 'magenta'
    else:
        point = position[0], y - 1
        color = 'red'

    point = point[0] * tile_size, point[1] * tile_size
    pygame.draw.circle(surface, color, point, 2.)

    if rx > 0:
        point = x + 1, y
    else:
        point = x, y + 1

    point = point[0] * tile_size, point[1] * tile_size
    pygame.draw.circle(surface, 'red', point, 5.)


def Main(window_size, fps):
    pygame.init()

    board = (
        '################'
        '#              #'
        '# ########## # #'
        '# #        # # #'
        '# # # #### # # #'
        '# # # #  # # # #'
        '# # # ## # # # #'
        '# # #  # # # # #'
        '# # ## # # # # #'
        '# ###  #   # # #'
        '# #   ###### # #'
        '# # ######   # #'
        '# #        # # #'
        '# ########## # #'
        '#              #'
        '################'
    )

    window = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()
    verdana_14 = pygame.font.SysFont('Verdana', 14)
    running = True
    player = Player((1., 1.), 0)
    map = Map(board, 16, 16)
    frame = 0

    while running:
        for event in pygame.event.get():
            if QUIT == event.type:
                running = False
                continue

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            running = False
            continue

        if keys[K_n]:
            player.direction = -math.pi / 2
        if keys[K_s]:
            player.direction = math.pi / 2
        if keys[K_e]:
            player.direction = 0
        if keys[K_w]:
            player.direction = math.pi
        if keys[K_RIGHT]:
            player.rotate(0.1)
        if keys[K_LEFT]:
            player.rotate(-0.1)
        if keys[K_UP]:
            player.move_if(map.is_empty, 0.1)
        if keys[K_DOWN]:
            player.move_if(map.is_empty, -0.1)

        window.fill('lightblue')

        pygame.display.set_caption(f'Frame#{frame:04d}/ Fps:{fps:02d}')
        info_player = verdana_14.render(str(player), True, 'red', 'lightblue')
        map.display(window, (0, 0), TILE_SIZE)
        player.display(window, TILE_SIZE)
        window.blit(info_player, (4, 500))

        projections(window, player.position, player.direction, TILE_SIZE)

        pygame.display.flip()

        clock.tick(fps)
        frame += 1

    pygame.quit()


"""
"""
