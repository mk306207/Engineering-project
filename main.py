import pygame
import sys
import pygame_widgets as pw
from pygame_widgets.button import Button
from colors import *
import maze
import bird
from ga import genetic_algorithm
from maze import simulate_players, Maze
from ai_players import Maze_player
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

def start_maze_ai():
    import random
    from maze_config import START_POSITION, FINISH_LINE, SCREEN_WIDTH as MAZE_SCREEN_WIDTH, SCREEN_HEIGHT as MAZE_SCREEN_HEIGHT

    screen = pygame.display.set_mode((MAZE_SCREEN_WIDTH, MAZE_SCREEN_HEIGHT))
    pygame.display.set_caption("AI Game2")
    clock = pygame.time.Clock()
    maze_obj = Maze()
    ga = genetic_algorithm("Maze")
    ga.create_population()
    #print(f"{len(ga.population)}")
    players = []
    for i, genom in enumerate(ga.population):
        color = (
            random.randint(50, 255), 
            random.randint(50, 255), 
            random.randint(50, 255)
        )
        player = Maze_player(
            START_POSITION[0],
            START_POSITION[1], 
            genom,
            color
        )
        players.append(player)
    
    #print(f"Created {len(players)} players")
    sorted_players = []
    expected_fitness = 900
    current_fitness = 0
    generation_id = 0
    while(expected_fitness>current_fitness):
        ga.generation = generation_id
        if not generation_id == 0:
            ga.evolve(sorted_players, elite_count=2)
            players.clear()
            #print(len(ga.population))
            for i, genom in enumerate(ga.population):
                is_elite = any(genom == elite_genom for elite_genom in ga.elite_genomes)
                
                if is_elite:
                    color = (0, 255, 0)
                else:
                    color = (
                        random.randint(50, 255), 
                        random.randint(50, 255), 
                        random.randint(50, 255)
                    )
                
                player = Maze_player(
                    START_POSITION[0],
                    START_POSITION[1], 
                    genom,
                    color
                )
                player.is_elite = is_elite 
                players.append(player)

        simulate_players(screen, maze_obj, players, clock, ga.generation)
        print(f"\n=== Generation {generation_id} ===")
        for player in players:
            player.fitness = ga.fitness(player, FINISH_LINE)
        sorted_players = sorted(players, key=lambda player: player.fitness, reverse=True)
        
        for i, player in enumerate(sorted_players):
            if i < 5:
                elite_marker = "(E)" if hasattr(player, 'is_elite') and player.is_elite else "   "
                print(f"{elite_marker} Player {i+1}: position {player.get_position()}, fitness = {player.fitness:.2f}, moves = {player.successful_moves}")

        best_player = sorted_players[0]
        print(f"\nBest player = {best_player.fitness:.2f}, his position = {best_player.get_position()}, his color = {best_player.color}")
        current_fitness = best_player.fitness
        generation_id += 1
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

maze_ai_button = Button(
    win,  # Surface to place button on
    150,  # X-coordinate of top left corner
    450,  # Y-coordinate of top left corner
    80,  # Width
    50,  # Height
    text='Maze AI',
    fontSize=20,
    margin=5,
    inactiveColour=GREEN,
    hoverColour=WHITE,
    pressedColour=WHITE,
    radius=50,
    onClick=start_maze_ai
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
        self.maze_ai_button = maze_ai_button

    def update(self):
        return
    
    def draw(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(overlay, (0, 0))
        self.maze_button.draw()
        self.bird_button.draw()
        self.maze_ai_button.draw()
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