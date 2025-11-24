import pygame
import sys
import pygame_widgets as pw
from pygame_widgets.button import Button
from colors import *
import maze
import bird

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#Set-ExecutionPolicy Unrestricted -Scope Process

def start_maze():
    maze_game = maze.Game()
    maze_game.run()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def start_bird():
    bird_game = bird.Game()
    bird_game.run()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

maze_button = Button(
    win,  # Surface to place button on
    150,  # X-coordinate of top left corner
    350,  # Y-coordinate of top left corner
    80,  # Width
    50,  # Height
    text='Maze',
    fontSize=20,
    margin=5,
    inactiveColour=GREEN,
    hoverColour=WHITE,
    pressedColour=WHITE,
    radius=50,
    onClick=start_maze
)

bird_button = Button(
    win,  # Surface to place button on
    580,  # X-coordinate of top left corner
    350,  # Y-coordinate of top left corner
    80,  # Width
    50,  # Height
    text='Bird',
    fontSize=20,
    margin=5,
    inactiveColour=YELLOW,
    hoverColour=WHITE,
    pressedColour=WHITE,
    radius=50,
    onClick=start_bird
)

class GUI:
    def __init__(self,win):
        self.screen = win
        pygame.display.set_caption("GUI")
        self.clock = pygame.time.Clock()
        self.maze_button = maze_button
        self.bird_button = bird_button

    def update(self):
        return
    
    def draw(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(overlay, (0, 0))
        self.maze_button.draw()
        self.bird_button.draw()
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
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    gui = GUI(win)
    gui.run()