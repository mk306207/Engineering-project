from maze_config import *
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