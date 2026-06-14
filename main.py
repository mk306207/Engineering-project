import pygame
import sys
import pygame_widgets as pw
from pygame_widgets.button import Button
from colors import *
import maze
import bird
import maze_config
from ga import genetic_algorithm
from maze import simulate_maze_players, Maze
from bird import simulate_bird_players, Bird
from ai_players import Maze_player, Bird_player
import matplotlib.pyplot as plt
from io import BytesIO
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#Set-ExecutionPolicy Unrestricted -Scope Process

class MazeSettingsMenu:
    def __init__(self, ai_mode=True):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.ai_mode = ai_mode
        pygame.display.set_caption("Maze AI settings" if self.ai_mode else "Maze settings")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 34)
        self.small_font = pygame.font.Font(None, 26)
        self.selected = 0
        self.settings = maze_config.MAZE_SETTINGS.copy()
        self.settings["generated_seed"] = None
        self.fields = self._build_fields()

    def _build_fields(self):
        maze_fields = [
            ("maze_type", "Maze type"),
            ("maze_size", "Maze size"),
        ]
        if not self.ai_mode:
            return maze_fields
        return [
            ("mutation_rate", "Mutation probability"),
            ("satisfactory_fitness", "Expected fitness"),
            *maze_fields,
            ("population_size", "Population size"),
            ("chromosome_length", "Chromosome length"),
        ]

    def _change_value(self, field, direction):
        if field == "mutation_rate":
            value = self.settings[field] + direction * 0.01
            self.settings[field] = round(max(0.0, min(1.0, value)), 2)
        elif field == "satisfactory_fitness":
            self.settings[field] = max(100, self.settings[field] + direction * 100)
        elif field == "maze_type":
            options = maze_config.MAZE_TYPE_OPTIONS
            index = options.index(self.settings[field])
            self.settings[field] = options[(index + direction) % len(options)]
        elif field == "maze_size":
            options = maze_config.MAZE_SIZE_OPTIONS
            index = options.index(self.settings[field])
            self.settings[field] = options[(index + direction) % len(options)]
        elif field == "population_size":
            self.settings[field] = max(10, self.settings[field] + direction * 10)
        elif field == "chromosome_length":
            self.settings[field] = max(20, self.settings[field] + direction * 10)

    def draw(self):
        self.screen.fill((24, 28, 35))
        title_text = "Maze AI configuration" if self.ai_mode else "Maze configuration"
        title = self.font.render(title_text, True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))

        y = 150
        for index, (field, label) in enumerate(self.fields):
            is_selected = index == self.selected
            text_color = BLACK if is_selected else WHITE
            row_color = (210, 230, 255) if is_selected else (45, 52, 64)
            rect = pygame.Rect(120, y - 8, 560, 44)
            pygame.draw.rect(self.screen, row_color, rect, border_radius=6)
            pygame.draw.rect(self.screen, (105, 120, 140), rect, 1, border_radius=6)

            value = self.settings[field]
            value_text = f"{value:.2f}" if isinstance(value, float) else str(value)
            label_surface = self.small_font.render(label, True, text_color)
            value_surface = self.small_font.render(value_text, True, text_color)
            self.screen.blit(label_surface, (140, y))
            self.screen.blit(value_surface, (660 - value_surface.get_width(), y))
            y += 58

        info_lines = [
            "UP/DOWN: select   LEFT/RIGHT: change",
            f"ENTER: start {'maze AI' if self.ai_mode else 'maze'}   ESC: back to menu",
        ]
        y = 690
        for line in info_lines:
            info = self.small_font.render(line, True, LIGHT_GRAY)
            self.screen.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, y))
            y += 28

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    if event.key == pygame.K_RETURN:
                        self.settings["generated_seed"] = None
                        return maze_config.apply_maze_settings(self.settings).copy()
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.fields)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.fields)
                    elif event.key == pygame.K_LEFT:
                        self._change_value(self.fields[self.selected][0], -1)
                    elif event.key == pygame.K_RIGHT:
                        self._change_value(self.fields[self.selected][0], 1)

            self.draw()
            self.clock.tick(60)

def start_maze():
    selected_settings = MazeSettingsMenu(ai_mode=False).run()
    if selected_settings is None:
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("GUI")
        return

    maze_game = maze.Game()
    maze_game.run()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("GUI")

def start_bird():
    bird_game = bird.Game()
    bird_game.run()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def start_maze_ai():
    import random

    selected_settings = MazeSettingsMenu(ai_mode=True).run()
    if selected_settings is None:
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("GUI")
        return

    screen = pygame.display.set_mode((maze_config.SCREEN_WIDTH*2, maze_config.SCREEN_HEIGHT))
    pygame.display.set_caption("AI Game2")
    clock = pygame.time.Clock()
    maze_obj = Maze()
    ga = genetic_algorithm("Maze", selected_settings)
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
            maze_config.START_POSITION[0],
            maze_config.START_POSITION[1], 
            genom,
            color
        )
        players.append(player)
    
    #print(f"Created {len(players)} players")
    user_interrupt = False
    sorted_players = []
    expected_fitness = selected_settings["satisfactory_fitness"]
    current_fitness = 0
    generation_id = 0
    best_player_object = None
    best_fitness = []
    while(expected_fitness>current_fitness and not user_interrupt):
        ga.generation = generation_id
        if not generation_id == 0:
            ga.evolve(sorted_players, elite_count=2)
            players.clear()
            #print(len(ga.population))
            for i, genom in enumerate(ga.population):
                is_elite = id(genom) in ga.elite_genome_ids
                
                if is_elite:
                    color = (0, 255, 0)
                else:
                    color = (
                        random.randint(50, 255), 
                        random.randint(50, 255), 
                        random.randint(50, 255)
                    )
                
                player = Maze_player(
                    maze_config.START_POSITION[0],
                    maze_config.START_POSITION[1], 
                    genom,
                    color
                )
                player.is_elite = is_elite 
                players.append(player)

        user_interrupt = simulate_maze_players(screen, maze_obj, players, clock, ga.generation,best_player_object)
        total_fitness = 0
        print(f"\n=== Generation {generation_id} ===")
        for player in players:
            player.fitness = ga.fitness(player, maze_config.FINISH_LINE)
            total_fitness += player.fitness
        sorted_players = sorted(players, key=lambda player: player.fitness, reverse=True)
        
        for i, player in enumerate(sorted_players):
            if i < 5:
                elite_marker = "(E)" if hasattr(player, 'is_elite') and player.is_elite else "   "
                print(f"{elite_marker} Player {i+1}: position {player.get_position()}, fitness = {player.fitness:.2f}, successful moves = {player.successful_moves}, unsuccessful moves = {player.unsuccessful_moves}")

        best_player = sorted_players[0]
        best_player_genom = best_player.get_genom()
        best_fitness.append(best_player.fitness)
        print(best_player_genom)
        best_player_object = Maze_player(
            maze_config.WINNER_START_POSITION[0],
            maze_config.WINNER_START_POSITION[1], 
            best_player_genom,
            BLACK
        )
        print(f"\nBest player = {best_player.fitness:.2f}, his position = {best_player.get_position()}, his color = {best_player.color}")
        current_fitness = best_player.fitness
        generation_id += 1
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(best_fitness)), best_fitness, linewidth=2, color='blue', marker='o', markersize=4)
    plt.xlabel('Generation ID', fontsize=12)
    plt.ylabel('Best Fitness', fontsize=12)
    plt.title('Best Fitness per Generation', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=80)
    buf.seek(0)
    plt.close()
    graph_image = pygame.image.load(buf)
    buf.close()
    graph_screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("AI Game2 - Results")
    showing_graph = True
    while showing_graph:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                showing_graph = False
                pygame.display.set_caption("GUI")
        
        graph_screen.fill(WHITE)
        graph_screen.blit(graph_image, (0, 0))
        pygame.display.flip()
        clock.tick(30)
    
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def start_bird_ai():
    import random
    from bird_config import SCREEN_WIDTH as BIRD_SCREEN_WIDTH, SCREEN_HEIGHT as BIRD_SCREEN_HEIGHT, SATISFACTORY_FITNESS

    screen = pygame.display.set_mode((BIRD_SCREEN_WIDTH*2, BIRD_SCREEN_HEIGHT))
    pygame.display.set_caption("AI Game1")
    clock = pygame.time.Clock()
    ga = genetic_algorithm("Bird")
    ga.create_population()
    
    players = []
    for i,genom in enumerate(ga.population): #i is just to delete genom id, its useless so you can assume that "i" variable is just a placeholder i guess
        color = (
            random.randint(50, 255), 
            random.randint(50, 255), 
            random.randint(50, 255)
        )
        player = Bird_player(genom, color)
        players.append(player)
    
    expected_fitness = SATISFACTORY_FITNESS;current_fitness = 0;user_interrupt = False;sorted_players = [];generation_id = 0;best_fitness = [];best_player_object = None;best_seed = None
    
    # Stały seed dla całej ewolucji - wszystkie generacje mają te same rury
    evolution_seed = random.randint(0, 1000000)
    
    while(expected_fitness>current_fitness and not user_interrupt):
        ga.generation = generation_id

        current_seed = evolution_seed  # Ten sam seed dla każdej generacji
        if not generation_id == 0:
            ga.evolve(sorted_players, elite_count=2)
            players.clear()
            for i, genom in enumerate(ga.population):
                is_elite = id(genom) in ga.elite_genome_ids
                
                if is_elite:
                    color = (0, 255, 0)
                else:
                    color = (
                        random.randint(50, 255), 
                        random.randint(50, 255), 
                        random.randint(50, 255)
                    )
                
                player = Bird_player(genom, color)
                player.is_elite = is_elite 
                players.append(player)
        
        user_interrupt = simulate_bird_players(screen, players, clock, ga.generation, best_player_object, current_seed, best_seed)
        
        # Calculate fitness
        total_fitness = 0
        print(f"\n=== Generation {generation_id} ===")
        for player in players:
            player.fitness = ga.fitness(player)
            total_fitness += player.fitness
        sorted_players = sorted(players, key=lambda player: player.fitness, reverse=True)
        
        # Print top 5
        for i, player in enumerate(sorted_players):
            if i < 5:
                elite_marker = "(E)" if hasattr(player, 'is_elite') and player.is_elite else "   "
                print(f"{elite_marker} Player {i+1}: fitness = {player.fitness:.2f}, score = {player.score}, frames = {player.frames_alive}")
        
        best_player = sorted_players[0]
        best_player_genom = best_player.get_genom()
        best_fitness.append(best_player.fitness)
        best_player_object = Bird_player(best_player_genom, BLACK)
        best_seed = current_seed  # Save seed from this generation
        print(f"\nBest player = {best_player.fitness:.2f}, score = {best_player.score}, frames alive = {best_player.frames_alive}")
        current_fitness = best_player.fitness
        generation_id += 1
    
    # Display graph
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(best_fitness)), best_fitness, linewidth=2, color='blue', marker='o', markersize=4)
    plt.xlabel('Generation ID', fontsize=12)
    plt.ylabel('Best Fitness', fontsize=12)
    plt.title('Best Fitness per Generation - Bird', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=80)
    buf.seek(0)
    plt.close()
    
    graph_image = pygame.image.load(buf)
    buf.close()
    
    graph_screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("AI Game1 - Results")
    
    showing_graph = True
    while showing_graph:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                showing_graph = False
        
        graph_screen.fill(WHITE)
        graph_screen.blit(graph_image, (0, 0))
        pygame.display.flip()
        clock.tick(30)
    
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

bird_ai_button = Button(
    win,  # Surface to place button on
    580,  # X-coordinate of top left corner
    450,  # Y-coordinate of top left corner
    80,  # Width
    50,  # Height
    text='Bird AI',
    fontSize=20,
    margin=5,
    inactiveColour=YELLOW,
    hoverColour=WHITE,
    pressedColour=WHITE,
    radius=50,
    onClick=start_bird_ai
)

class GUI:
    def __init__(self,win):
        self.screen = win
        pygame.display.set_caption("GUI")
        self.clock = pygame.time.Clock()
        self.maze_button = maze_button
        self.bird_button = bird_button
        self.maze_ai_button = maze_ai_button
        self.bird_ai_button = bird_ai_button

    def update(self):
        return
    
    def draw(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(overlay, (0, 0))
        self.maze_button.draw()
        self.bird_button.draw()
        self.maze_ai_button.draw()
        self.bird_ai_button.draw()
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
