import sys
import pygame
from pygame.locals import *

import time

def main():
    # pygame initialize
    pygame.init()

    # UI Settings
    width, height = 1000, 600
    min_width, min_height = 600, 400
    BACKGROUND_COLOR = 255,255,255          
    CAPTION = "BCI Drawing"
    MARGIN = 10
    CANVAS_SIZE = (width-MARGIN*2)/2, height-MARGIN*2

    pygame.display.set_caption(CAPTION)   
    screen = pygame.display.set_mode((width,height), HWSURFACE|DOUBLEBUF|RESIZABLE)
    screen.fill(BACKGROUND_COLOR) 
    # build canvas
    canvas = draw_canvas(CANVAS_SIZE)

    # create a surface object, image is drawn on it.
    imp = pygame.image.load(".\\icons\\arrow-left-44.svg").convert_alpha()
    imp = pygame.transform.scale(imp, (50,50))
    # Using blit to copy content from one surface to other
    screen.blit(imp, (50, 50))


    # Clock, fps
    fps = 60
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                print("The Pygame window is now " + str ( event.w ) + " pixels wide and " + str ( event.h ) + " pixels high")
                width, height = event.size
                if width < min_width:
                    width = min_width
                if height < min_height:
                    height = min_height
                screen = pygame.display.set_mode((width,height), HWSURFACE|DOUBLEBUF|RESIZABLE)
                CANVAS_SIZE = (width-MARGIN*2)/2, height-MARGIN*2
                screen.fill(BACKGROUND_COLOR) 
                canvas = draw_canvas(CANVAS_SIZE)
                


        screen.blit(canvas,(MARGIN+CANVAS_SIZE[0], MARGIN))

        pygame.display.update()

    pygame.quit()

def draw_canvas(size):
    color = 200,200,200
    canvas = pygame.Surface(size).convert()
    canvas.fill(color)
    return canvas



if __name__ == '__main__':
    main()

