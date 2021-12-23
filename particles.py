# ======================================================================================================================
# DESCRIPTION
# ======================================================================================================================


# Pygame base example

# ======================================================================================================================
# IMPORTS
# ======================================================================================================================


from pygame import *

import pygame
import random
import sys

# ======================================================================================================================
# CONSTANTS
# ======================================================================================================================


ORIGIN = (0, 0)
DISPLAY_WIDTH = 400
DISPLAY_HEIGHT = 300
DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
DISPLAY_CENTER = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
SCALE = 2
COLOR_PARTICLE = (0, 128, 0)
COLOR_SKY = (0, 0, 0) #(31, 24, 48)
COLOR_DEPTH = 32
CAPTION = 'Pygame base example'
TICKS = 40

# ======================================================================================================================
# VARIABLES
# ======================================================================================================================


# None

# ======================================================================================================================
# CLASSES
# ======================================================================================================================


class Particle:
    def __init__(self, color, location, velocity, duration):
        self._color = [0, 0, 0]
        self._color[0], self._color[1], self._color[2] = color[0], color[1], color[2]
        self._location = location
        self._velocity = velocity
        self._duration = duration

    def __init__(self, color):
        self._color = [0, 0, 0]
        self._color[0], self._color[1], self._color[2] = color[0], color[1], color[2]
        self._location = [DISPLAY_CENTER[0], DISPLAY_CENTER[1]]
        self._velocity = [random.randint(0, 40) / 20 - 1, random.randint(0, 40) / 20 - 1]
        self._duration = random.randint(4, 8)

    def __fade(self):
        # fade to black
        if self._color[0] > 0:
            self._color[0] -= 1
        if self._color[1] > 0:
            self._color[1] -= 1
        if self._color[2] > 0:
            self._color[2] -= 1

    def expired(self):
        return self._duration <= 0

    def move(self):
        if self._duration > 0:
            self._location[0] += self._velocity[0]
            self._location[1] += self._velocity[1]
            self._duration -= 0.05
            #self._velocity[1] += 0.03 # some kind of gravity
            self.__fade()

    def draw(self, screen):
        if self._duration > 0:
            pygame.draw.circle(screen , self._color, self._location, self._duration)


class Particles:
    def __init__(self, max=500):
        self._particles = []
        self._max = max

    def __len__(self):
        return len(self._particles)

    def __getitem__(self, item):
        return self._particles[item]

    def __add_new(self):
        self._particles.append(Particle(COLOR_PARTICLE))

    def draw(self, screen, pause=False):
        if not pause:
            if len(self._particles) < self._max:
                self.__add_new()

        for particle in self._particles:
            if not pause:
                particle.move()
            if particle.expired():
                self._particles.remove(particle)
                self.__add_new()
            else:
                particle.draw(screen)


# ======================================================================================================================
# FUNCTIONS
# ======================================================================================================================


def scale_set(s, scale):
    return s[0] * scale, s[1] * scale


def int_div_set(s, denum):
    return int(s[0] / denum), int(s[1] / denum)


def main():
    # *** Pygame initialization
    pygame.init()

    # *** Set window caption
    pygame.display.set_caption(CAPTION)

    # *** Set window size. using pixel mode (*2)
    screen_size = scale_set(DISPLAY_SIZE, SCALE)
    screen = pygame.display.set_mode(screen_size, 0, COLOR_DEPTH)
    display = pygame.Surface(DISPLAY_SIZE)

    # Particles
    particles = Particles()

    # *** Create clock
    clock = pygame.time.Clock()

    # *** Running loop
    running = True
    pause = False
    while running:
        # *** Background update #
        display.fill(COLOR_SKY)

        # *** Get mouse position
        mx, my = int_div_set(pygame.mouse.get_pos(), SCALE)

        # *** Manage particles
        particles.draw(display, pause)
        pygame.display.set_caption(CAPTION + ' %d' % (len(particles)))

        # *** Manage events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    pause = not pause

        # *** Update display
        screen.blit(pygame.transform.scale(display, screen_size), ORIGIN)
        pygame.display.update()
        clock.tick(TICKS)

# ======================================================================================================================
# ENTRY POINT
# ======================================================================================================================


if __name__ == '__main__':
    main()

# ======================================================================================================================
# END OF FILE
# ======================================================================================================================
