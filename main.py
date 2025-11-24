import pygame
import sys
import pygame_widgets as pw
from pygame_widgets.button import Button
from colors import *

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#Set-ExecutionPolicy Unrestricted -Scope Process

button = Button(
    win,  # Surface to place button on
    100,  # X-coordinate of top left corner
    100,  # Y-coordinate of top left corner
    30,  # Width
    15,  # Height
    text='Test',
    fontSize=12,
    margin=5,
    inactiveColour=YELLOW,
    hoverColour=(150, 0, 0),
    pressedColour=(0, 200, 20),
    radius=50,
    onClick=lambda: print('Click')
)

class GUI:
    def __init__(self):
        self.screen = win
        pygame.display.set_caption("GUI")
        self.clock = pygame.time.Clock()
        self.button = button

    def update(self):
        return
    
    def draw(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(overlay, (0, 0))
        self.button.draw()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
            pw.update(event)
        return True

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gui = GUI()
    gui.run()