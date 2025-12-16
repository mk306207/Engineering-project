from maze_config import *
from bird_config import *
from colors import BLACK
import pygame

pygame.init()

class Maze_player():
    def __init__(self,x,y,genom,color):
        self.x = x
        self.y = y
        self.genom = genom
        self.moves = 0
        self.successful_moves = 0
        self.unsuccessful_moves = 0
        self.is_alive = True
        self.color = color
        self.radius = TILE_SIZE // 4
        self.fitness = 0

    def move_mp(self, maze):
        if self.is_alive and self.moves >= len(self.genom):
            self.is_alive = False
            return
        move = self.genom[self.moves]
        self.moves += 1
        new_x, new_y = self.x, self.y
        if move == 1:
            new_x -= 1
        elif move == 2:
            new_x += 1
        elif move == 3:
            new_y -= 1
        elif move == 4:
            new_y += 1
        if not maze.is_wall(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.successful_moves += 1
        else:
            self.unsuccessful_moves += 1

    def draw(self,screen):
        if self.is_alive:
            center_x = self.x * TILE_SIZE + TILE_SIZE // 2
            center_y = self.y * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.circle(screen, self.color, (center_x, center_y), self.radius)
            if hasattr(self, 'is_elite') and self.is_elite:
                pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), self.radius + 2, 2)

    def draw_copy(self, screen, offset_x=0):
        if self.is_alive:
            center_x = self.x * TILE_SIZE + TILE_SIZE // 2 + offset_x
            center_y = self.y * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.circle(screen, self.color, (center_x, center_y), self.radius)
            if hasattr(self, 'is_elite') and self.is_elite:
                pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), self.radius + 2, 2)

    def get_position(self):
        return (self.x, self.y)
    
    def get_genom(self):
        return self.genom
    
class Bird_player():
    def __init__(self, genom, color):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.score = 0
        self.is_alive = True
        self.color = color
        self.velocity = 0
        self.radius = 20
        self.genom = genom  # [y_w, x_w, v_w, bias]
        self.fitness = 0
        self.frames_alive = 0
        self.distance_traveled = 0
    
    def decide(self, pipes):
        if not pipes:
            return False

        nearest_pipe = None
        for pipe in pipes:
            if pipe.x + PIPE_WIDTH > self.x:
                nearest_pipe = pipe
                break
        if nearest_pipe is None:
            return False
        
        y_diff = (self.y - nearest_pipe.gap_y) / SCREEN_HEIGHT
        x_diff = (nearest_pipe.x - self.x) / SCREEN_WIDTH
        velocity_normalized = self.velocity / 20.0   
        w_y = self.genom[0]
        w_x = self.genom[1]
        w_v = self.genom[2]
        bias = self.genom[3]
        activation = y_diff * w_y + x_diff * w_x + velocity_normalized * w_v + bias
        return activation > 0
    
    def jump(self):
        self.velocity = JUMP_FORCE
    
    def update(self, pipes):
        if not self.is_alive:
            return
        if self.decide(pipes):
            self.jump()
        self.velocity += GRAVITY
        self.y += self.velocity
        self.frames_alive += 1
        self.distance_traveled += PIPE_SPEED
        if self.y + self.radius >= SCREEN_HEIGHT or self.y - self.radius <= 0:
            self.is_alive = False
    
    def draw(self, screen):
        if self.is_alive:
            rect = pygame.Rect(self.x - 25, self.y - 15, 50, 30)
            pygame.draw.ellipse(screen, self.color, rect)
            pygame.draw.circle(screen, BLACK, (int(self.x + 8), int(self.y - 5)), 3)
            beak_points = [
                (self.x + 20, self.y),
                (self.x + 30, self.y + 3),
                (self.x + 20, self.y + 6)
            ]
            pygame.draw.polygon(screen, (255, 165, 0), beak_points)
            if hasattr(self, 'is_elite') and self.is_elite:
                pygame.draw.circle(screen, (255, 215, 0), (int(self.x), int(self.y)), self.radius + 5, 3)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
    
    def get_position(self):
        return (self.x, self.y)
    
    def get_genom(self):
        return self.genom