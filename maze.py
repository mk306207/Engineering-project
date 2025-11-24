import pygame
import sys
from colors import *

pygame.init()
TILE_SIZE = 40
MAZE_WIDTH = 15
MAZE_HEIGHT = 15
SCREEN_WIDTH = MAZE_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * TILE_SIZE + 60

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

START_POSITION = (1,0)
FINISH_LINE = (13,14)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = TILE_SIZE // 3
        
    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        if not maze.is_wall(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        return False
    
    def draw(self, screen):
        center_x = self.x * TILE_SIZE + TILE_SIZE // 2
        center_y = self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, BLUE, (center_x, center_y), self.radius)

    def get_position(self):
        return(self.x,self.y)

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
        self.player = Player(START_POSITION[0],START_POSITION[1])
        self.score = 0
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.game_over = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    temp = self.player.move(0, -1, self.maze)
                    if not temp:
                        self.game_over = True
                    self.score+=1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    temp = self.player.move(0, 1, self.maze)
                    if not temp:
                        self.game_over = True
                    self.score+=1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    temp = self.player.move(-1, 0, self.maze)
                    if not temp:
                        self.game_over = True
                    self.score+=1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    temp = self.player.move(1, 0, self.maze)
                    if not temp:
                        self.game_over = True
                    self.score+=1
    
    def update(self):
        print(self.player.get_position())
        if self.player.get_position() == FINISH_LINE:
            self.running = False
    
    def draw(self):
        self.screen.fill(WHITE)
        self.maze.draw(self.screen)
        self.player.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (0, 625))
        pygame.display.flip()
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER!", True, RED)
            final_score = self.small_font.render(f"Score: {self.score}", True, WHITE)
            restart_text = self.small_font.render("SPACE - restart, ESC - exit", True, WHITE)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 80))
            self.screen.blit(final_score, (SCREEN_WIDTH//2 - final_score.get_width()//2, SCREEN_HEIGHT//2 - 30))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
    
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
