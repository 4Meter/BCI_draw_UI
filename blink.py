import pygame
import sys

# --- constants ---

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)

# --- classes ---

class Rectangle():

    def __init__(self, color, rect, time, delay):
        self.color = color
        self.rect = rect
        self.time = time
        self.delay = delay
        self.show = False
        self.show_portion = 0.8
        self.times = []
        imp = pygame.image.load(".\\icons\\arrow-left-44.svg").convert_alpha()
        self.imp = pygame.transform.scale(imp, (50,50))

    def draw(self, screen):
        if self.show:
            pygame.draw.rect(screen, self.color, self.rect)
            screen.blit(self.imp, (self.rect[0], self.rect[1]))
    

    def update(self, current_time):
        if current_time >= self.time:
            if self.show:
                # show
                self.time = current_time + self.delay*self.show_portion
            else:
                # no-show
                self.time = current_time + self.delay*(1-self.show_portion)
            self.show = not self.show
    

# --- main ---

def main():
    pygame.init()

    fenetre = pygame.display.set_mode((500, 400), 0, 32)

    current_time = pygame.time.get_ticks()

    # time of show or hide
    delay = 500 # 5000ms = 0.5s

    # objects    
    #rect_white = Rectangle(WHITE, (200,150,100,50), current_time+1000/9, 1000/9)
    rect_red = Rectangle(RED, (100,150,100,50), current_time+1000/8*0.05, 1000/8)
    #rect_green = Rectangle(GREEN, (300, 150, 100, 50), current_time+1000/7, 1000/7)

    while True:
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- updates ---

        current_time = pygame.time.get_ticks()

        #rect_white.update(current_time)
        rect_red.update(current_time)
        #rect_green.update(current_time)

        # --- draws ---

        fenetre.fill(BLACK)

        #rect_green.draw(fenetre)
        #rect_white.draw(fenetre)
        rect_red.draw(fenetre)
        
        pygame.display.update()

main()