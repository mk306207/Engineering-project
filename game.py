import pygame
import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GRAVITY = 0.5
JUMP_FORCE = -10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 15
        
    def jump(self):
        self.velocity = JUMP_FORCE
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
        if self.y <= 0:
            self.y = 0
            self.velocity = 0
        if self.y >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT
            self.velocity = 0
        
    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game1")
    clock = pygame.time.Clock()
    
    bird = Bird()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        bird.update()       
        screen.fill(WHITE)
        bird.draw(screen)
        font = pygame.font.Font(None, 36)
        velocity_text = font.render(f"Velocity: {bird.velocity:.1f}", True, BLACK)
        screen.blit(velocity_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()