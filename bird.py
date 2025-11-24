import pygame
import random
import sys
from colors import *

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GRAVITY = 0.8
JUMP_FORCE = -12
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_SPEED = 4

class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 20
        
    def jump(self):
        self.velocity = JUMP_FORCE
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
    def draw(self, screen):
        rect = pygame.Rect(self.x - 25, self.y - 15, 50, 30)
        pygame.draw.ellipse(screen, YELLOW, rect)
        pygame.draw.circle(screen, BLACK, (int(self.x + 8), int(self.y - 5)), 3)
        beak_points = [
            (self.x + 20, self.y),
            (self.x + 30, self.y + 3),
            (self.x + 20, self.y + 6)
        ]
        pygame.draw.polygon(screen, (255, 165, 0), beak_points)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(150, SCREEN_HEIGHT - 250)
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self, screen):
        top_rect = (self.x, 0, PIPE_WIDTH, self.gap_y)
        pygame.draw.rect(screen, GREEN, top_rect)
        pygame.draw.rect(screen, BLACK, top_rect, 3)
        bottom_rect = (self.x, self.gap_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (self.gap_y + PIPE_GAP))
        pygame.draw.rect(screen, GREEN, bottom_rect)
        pygame.draw.rect(screen, BLACK, bottom_rect, 3)
        cap_height = 30
        cap_width = PIPE_WIDTH + 10
        top_cap = (self.x - 5, self.gap_y - cap_height, cap_width, cap_height)
        pygame.draw.rect(screen, (0, 150, 0), top_cap)
        pygame.draw.rect(screen, BLACK, top_cap, 2)
        bottom_cap = (self.x - 5, self.gap_y + PIPE_GAP, cap_width, cap_height)
        pygame.draw.rect(screen, (0, 150, 0), bottom_cap)
        pygame.draw.rect(screen, BLACK, bottom_cap, 2)
    
    def collides_with_bird(self, bird):
        bird_rect = bird.get_rect()
        top_pipe_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y)
        bottom_pipe_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (self.gap_y + PIPE_GAP))
        
        return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)
    
    def is_passed(self, bird):
        return self.x + PIPE_WIDTH < bird.x

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game1")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.reset_game()
        
    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.game_started = False
        for i in range(3):
            self.pipes.append(Pipe(SCREEN_WIDTH + i * 300))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_over:
                        self.bird.jump()
                        self.game_started = True
                    else:
                        self.reset_game()
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def update(self):
        if not self.game_started or self.game_over:
            return
            
        self.bird.update()
        if self.bird.y + self.bird.radius >= SCREEN_HEIGHT or self.bird.y - self.bird.radius <= 0:
            self.game_over = True

        for pipe in self.pipes[:]:
            pipe.update()
            if pipe.collides_with_bird(self.bird):
                self.game_over = True
            if not pipe.passed and pipe.is_passed(self.bird):
                pipe.passed = True
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score
            if pipe.x + PIPE_WIDTH < 0:
                self.pipes.remove(pipe)

        if len(self.pipes) < 3:
            last_pipe_x = max(pipe.x for pipe in self.pipes)
            self.pipes.append(Pipe(last_pipe_x + 300))
    
    def draw_gradient_background(self):
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(135 + (255 - 135) * color_ratio)
            g = int(206 + (255 - 206) * color_ratio)
            b = int(235 + (255 - 235) * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    def draw(self):
        self.draw_gradient_background()
        
        for pipe in self.pipes:
            pipe.draw(self.screen)
            
        self.bird.draw(self.screen)
        
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        score_shadow = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_shadow, (12, 12))
        self.screen.blit(score_text, (10, 10))
        
        if not self.game_started and not self.game_over:
            subtitle = self.small_font.render("Press 'SPACE' to play", True, BLACK)
            controls = self.small_font.render("SPACE - jump, ESC - exit", True, BLACK)
            self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(controls, (SCREEN_WIDTH//2 - controls.get_width()//2, SCREEN_HEIGHT//2 + 20))
        
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER!", True, RED)
            final_score = self.small_font.render(f"Score: {self.score}", True, WHITE)
            high_score = self.small_font.render(f"Best score: {self.high_score}", True, WHITE)
            restart_text = self.small_font.render("SPACE - restart, ESC - exit", True, WHITE)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 80))
            self.screen.blit(final_score, (SCREEN_WIDTH//2 - final_score.get_width()//2, SCREEN_HEIGHT//2 - 30))
            self.screen.blit(high_score, (SCREEN_WIDTH//2 - high_score.get_width()//2, SCREEN_HEIGHT//2))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()