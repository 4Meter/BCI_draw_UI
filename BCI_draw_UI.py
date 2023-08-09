import sys
import pygame
from pygame.locals import *
from pathlib import Path 

from model import *

"""
Keyboard Shortcuts:
S: save canvas
R: reset canvas
F: open/close button blinking
"""

def main(path):
    # pygame initialize
    pygame.init()

    # UI Settings
    WIDTH, HEIGHT = 1000, 600
    W1 = 200
    H1 = 80
    BACKGROUND_COLOR = 255,255,225  
    CANVAS_COLOR = 255,255,255        
    CAPTION = "BCI Drawing"
    MARGIN1 = 10
    MARGIN2 = 10
    BRUSH_COLOR = BLACK

    pygame.display.set_caption(CAPTION)   
    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    # build objects
    canvas = Canvas(
        color = CANVAS_COLOR,
        rect = (
            MARGIN1*2 + W1,     # x coordinate
            MARGIN1,            # y coordinate
            WIDTH-MARGIN1*3-W1, # width
            HEIGHT-MARGIN1*2    # height
        )
    )

    current_time = pygame.time.get_ticks()
    button_back = Button(
        name = "Back Button", 
        color = RED,
        rect = (
            MARGIN1,            # x coordinate
            MARGIN1,            # y coordinate
            (W1-MARGIN2)/2,     # width
            H1                  # height
            ),
        time = current_time,
        target_f = 6,           # target frequency
        img = pygame.image.load(path/'icons'/'back.png'), 
        )
    button_next = Button(
        name = "Next Button",
        color = GREEN,
        rect = (
            MARGIN1+MARGIN2+(W1-MARGIN2)/2,     # x coordinate
            MARGIN1,                            # y coordinate
            (W1-MARGIN2)/2,                     # width
            H1                                  # height
            ),
        time = current_time,
        target_f = 7,                           # target frequency
        img = pygame.image.load(path/'icons'/'next.png'), 
        )
    button_comfirm = Button(
        name = "Confirm Button",
        color = YELLOW,
        rect = (
            MARGIN1,               # x coordinate
            HEIGHT-MARGIN1-H1,     # y coordinate
            W1,                    # width
            H1                     # height
            ),
        time = current_time,
        target_f = 10,             # target frequency
        text = "Confirm", 
        )
    button_list = [button_back, button_next, button_comfirm]

    # --- Clock, fps ---
    """
    fps = 60
    clock = pygame.time.Clock()
    """
    # --- events --- 
    running = True
    is_flashing = True

    while running:
        #clock.tick(fps)

        # --- events ---  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                print("The Pygame window is now " + str ( event.w ) + " pixels wide and " + str ( event.h ) + " pixels high")
                WIDTH, HEIGHT = event.size
                if WIDTH < min_width:
                    WIDTH = min_width
                if HEIGHT < min_height:
                    HEIGHT = min_height
                screen = pygame.display.set_mode((WIDTH,HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
                CANVAS_SIZE = (WIDTH-MARGIN1*2)/2, HEIGHT-MARGIN1*2
                screen.fill(BACKGROUND_COLOR) 
                canvas = pygame.transform.scale(canvas, CANVAS_SIZE)
            elif event.type == pygame.KEYDOWN:
                # Save canvas when "S" is pressed
                if event.key == pygame.K_s:
                    canvas.save()
                # Reset canvas when "R" is pressed
                if event.key == pygame.K_r:
                    canvas.reset()
                # Open/Close button blinking when "F" is pressed
                if event.key == pygame.K_f:
                    is_flashing = not is_flashing
            if event.type == MOUSEBUTTONDOWN: 
                mouse_pos = pygame.mouse.get_pos()
                for button in button_list:
                    if button.get_rect().collidepoint(mouse_pos):
                        print(f"--- {button.name} got pressed ---    \r",end='\b')
        
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if canvas.get_rect().collidepoint(mouse_pos):
                canvas.add_brush(
                    color = BRUSH_COLOR,
                    position = mouse_pos,
                    size = 10
                )

        # --- updates ---
        if is_flashing:
            current_time = pygame.time.get_ticks()
            for button in button_list:
                button.update(current_time)
        else:
            for button in button_list:
                button.show = True

        # --- draws ---
        screen.fill(BACKGROUND_COLOR)
        for button in button_list:
            button.draw(screen)      
        canvas.draw(screen)
        #button_back.observe()     # Uncomment to observe actual frequency of button
        pygame.display.update()

    print("Ended"+ " "*100)
    pygame.quit()

if __name__ == '__main__':
    path = Path()
    main(path)

