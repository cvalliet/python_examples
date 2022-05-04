#!/usr/bin/env python3

"""Rotate, scale and flip an image."""

# import modules
import pygame
import math, sys, os
from pygame.locals import *

# define constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)

# initialize pygame
pygame.init()
# set window size to 640x240
w, h = 640, 240
# create pygame application
screen = pygame.display.set_mode((w, h))
# set running flag 
running = True

# get module class instance of __main__
module = sys.modules['__main__']
# get path and name from module path
path, name = os.path.split(module.__file__)
# create 'bird.png' file path from module path
path = os.path.join(path, 'bird.png')

# load 'bird.png' image to surface
img0 = pygame.image.load(path)
# optimize surface
img0.convert()

# draw a green border around img0
rect0 = img0.get_rect()
pygame.draw.rect(img0, GREEN, rect0, 1)

# set center of the screen
center = w//2, h//2
img = img0
rect = img.get_rect()
rect.center = center

angle = 0
scale = 1

clock = pygame.time.Clock()
mouse = pygame.mouse.get_pos()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_r:
                if event.mod & KMOD_SHIFT:
                    angle -= 10
                else:
                    angle += 10
                img = pygame.transform.rotozoom(img0, angle, scale)

            elif event.key == K_s:
                if event.mod & KMOD_SHIFT:
                    scale /= 1.1
                else:
                    scale *= 1.1
                img = pygame.transform.rotozoom(img0, angle, scale)

            elif event.key == K_o:
                img = img0
                angle = 0
                scale = 1

            elif event.key == K_h:
                img = pygame.transform.flip(img, True, False)
            
            elif event.key == K_v:
                img = pygame.transform.flip(img, False, True)

            elif event.key == K_l:
                img = pygame.transform.laplacian(img)

            elif event.key == K_2:
                img = pygame.transform.scale2x(img)

            rect = img.get_rect()
            rect.center = center

        elif event.type == MOUSEMOTION:
            mouse = event.pos
            x = mouse[0] - center[0]
            y = mouse[1] - center[1]
            d = math.sqrt(x ** 2 + y ** 2)

            angle = math.degrees(-math.atan2(y, x))
            scale = abs(5 * d / w)
            img = pygame.transform.rotozoom(img0, angle, scale)
            rect = img.get_rect()
            rect.center = center
    
    screen.fill(GRAY)
    screen.blit(img, rect)
    pygame.draw.rect(screen, RED, rect, 1)
    pygame.draw.line(screen, GREEN, center, mouse, 1)
    pygame.draw.circle(screen, RED, center, 6, 1)
    pygame.draw.circle(screen, RED, mouse, 6, 1)
    pygame.display.update()
    clock.tick(60)

pygame.quit()