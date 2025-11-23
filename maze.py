import pygame
import sys

pygame.init()
TILE_SIZE = 40
MAZE_WIDTH = 15
MAZE_HEIGHT = 15
SCREEN_WIDTH = MAZE_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * TILE_SIZE + 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (60, 60, 60)

MAZE = [
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,1,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,0,1,0,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
]

class Maze:
    def __init__(self):
        self.grid = [row[:] for row in MAZE]
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        
    def is_wall(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.grid[y][x] == 1
    
    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, DARK_GRAY, rect)
                    pygame.draw.rect(screen, GRAY, rect, 2)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                    pygame.draw.rect(screen, LIGHT_GRAY, rect, 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game2")
        self.clock = pygame.time.Clock()
        self.maze = Maze()
        self.running = True
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill(WHITE)
        self.maze.draw(self.screen)
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
