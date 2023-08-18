import pygame
from pygame import Surface, time
import numpy as np
from datetime import datetime

# --- constants ---

BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
YELLOW = (255, 255,   0)

# --- classes ---
        
class Button():

    def __init__(self, name, color, rect, time, target_f, img = None, text = None):
        self.name = name
        self.color = color
        self.rect = rect
        self.target_f = target_f
        self.delay = 1000/target_f
        self.time = time + self.delay
        self.show = False
        self.show_portion = 0.5
        self.time_buffer = []
        self.maxBuffer = 16
        self.font_size = 40
        self.font_color = BLACK
        if img: self.img = pygame.transform.scale(img, (40,40))
        else: self.img = None
        if text: 
            font = pygame.font.SysFont("simhei", self.font_size)
            t = font.render(text, True, self.font_color)
            self.text = t
        else: self.text = None

    def draw(self, screen):
        if self.show:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen,BLACK,self.rect,5)
            if self.img:
                screen.blit(
                    self.img, (self.rect[0]+self.rect[2]/2-20, self.rect[1]+self.rect[3]/2-20))
            elif self.text:
                text_width = self.text.get_width()
                text_height = self.text.get_height()
                screen.blit(self.text, (self.rect[0]+self.rect[2]/2-text_width/2, self.rect[1]+self.rect[3]/2-text_height/2))
    def update(self, current_time):
        if current_time >= self.time:
            if self.show:
                # show
                self.time = current_time + self.delay*self.show_portion
            else:
                # no-show
                self.time = current_time + self.delay*(1-self.show_portion)
            self.show = not self.show
            if self.show:
                self.time_buffer.append(current_time)
                if(len(self.time_buffer) > self.maxBuffer):
                    dif = np.diff(self.time_buffer)
                    actual_f = 1000/np.mean(dif)
                    if actual_f - self.target_f > 0.05:
                        self.delay += 0.5
                    elif actual_f - self.target_f < 0.05:
                        self.delay -= 0.5
                    self.time_buffer.clear()
    
    # print the average time interval per blink of the button
    def observe(self):
        if(len(self.time_buffer) > 1):
            dif = np.diff(self.time_buffer)
            actual_f = 1000/np.mean(dif)
            print(f" {self.name} | Sample: {len(self.time_buffer):2d} | Actual Frequency: {actual_f:.5f} Hz | Delay: {self.delay:.5f} ms    \r",end = "\b")

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.rect)

class Canvas():

    def __init__(self, color, rect):
        self.color = color
        self.rect = rect
        self.canvas = Surface((rect[2],rect[3])).convert()
        self.canvas.fill(color)

    def draw(self, screen):
        screen.blit(self.canvas,(self.rect[0], self.rect[1]))
        pygame.draw.rect(screen,BLACK,self.rect,5)
        
    def add_brush(self, color, position, size):
        pygame.draw.circle(self.canvas, color, (position[0]-self.rect[0], position[1]-self.rect[1]), size, 0)
    
    def reset(self):
        self.canvas.fill(self.color)

    def save(self, path):
        current_time = datetime.now()
        time_string = current_time.strftime(f"%Y%m%d_%H%M%S")
        name = "drawing_"+time_string+".png"
        pygame.image.save(self.canvas, path/'drawings'/name)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.rect)