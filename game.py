import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GRAVITY = 0.6
JUMP_FORCE = -11
PIPE_WIDTH = 80
PIPE_GAP = 180
PIPE_SPEED = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (100, 150, 255)

class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 18
        
    def jump(self):
        self.velocity = JUMP_FORCE
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x + 6), int(self.y - 4)), 2)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(120, SCREEN_HEIGHT - 200)
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, 
                        (self.x, 0, PIPE_WIDTH, self.gap_y))
        pygame.draw.rect(screen, GREEN, 
                        (self.x, self.gap_y + PIPE_GAP, PIPE_WIDTH, 
                         SCREEN_HEIGHT - (self.gap_y + PIPE_GAP)))
    
    def collides_with_bird(self, bird):
        bird_rect = bird.get_rect()
        top_pipe_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y)
        bottom_pipe_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP, PIPE_WIDTH, 
                                     SCREEN_HEIGHT - (self.gap_y + PIPE_GAP))
        
        return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game1")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 48)
    
    bird = Bird()
    pipes = []
    score = 0
    game_over = False
    
    for i in range(2):
        pipes.append(Pipe(SCREEN_WIDTH + i * 400))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()
                elif event.key == pygame.K_r and game_over:
                    bird = Bird()
                    pipes = []
                    for i in range(2):
                        pipes.append(Pipe(SCREEN_WIDTH + i * 400))
                    score = 0
                    game_over = False
        
        if not game_over:
            bird.update()
            if bird.y <= 0 or bird.y >= SCREEN_HEIGHT:
                game_over = True

            for pipe in pipes[:]:
                pipe.update()
                if pipe.collides_with_bird(bird):
                    game_over = True
                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)
                    score += 1

            if len(pipes) < 2:
                last_pipe_x = max(pipe.x for pipe in pipes) if pipes else SCREEN_WIDTH
                pipes.append(Pipe(last_pipe_x + 400))

        screen.fill(BLUE)
        for pipe in pipes:
            pipe.draw(screen)
        bird.draw(screen)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("GAME OVER!", True, WHITE)
            restart_text = font.render("Press R to reset", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 + 50))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()