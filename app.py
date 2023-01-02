#!/usr/bin/env python3

# Imports ---
import pygame as pg


# Variables ---
initialization_entrypoint = None
render_entrypoint = None
process_entrypoint = None


# Decorators ---
def initialization(func):
    global initialization_entrypoint
    initialization_entrypoint = func

def render(func):
    global render_entrypoint
    render_entrypoint = func

def process(func):
    global process_entrypoint
    process_entrypoint = func


# Main function ---
def main():
    if render_entrypoint is None:
        raise RuntimeError('function "render" not defined')

    if process_entrypoint is None :
        raise RuntimeError('function "process" not defined')

    # Setup pygame/window ---
    pg.init()

    # Initialize variables ---
    clock = pg.time.Clock()
    running = True
    caption = 'not defined'
    size = 640, 480
    tick = 30

    if initialization_entrypoint:
        caption, size, tick = initialization_entrypoint()

    pg.display.set_caption(caption)
    screen = pg.display.set_mode(size, 0, 32)

    # Loop --
    while running:
        # Render ---
        render_entrypoint(screen)

        # Event ---
        for event in pg.event.get():
            # Quit ---
            if event.type == pg.QUIT:
                running = False

            # Key down ---
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

            process_entrypoint(event)

        # Update ---
        pg.display.update()
        clock.tick(tick)

    pg.quit()
