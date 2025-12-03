import random

class genetic_algorithm:
    def __init__(self,game):
        if game=="Bird" or game=="Maze":
            self.game = game
        else:
            raise AttributeError(f"Wrong game type: '{game}'.")
        self.population = []
        self.generation = 0
        self.population_size = 50
        
    def create_population(self):
        if self.game == "Maze":
            for chromosome in range(0,self.population_size):
                genom = []
                for i in range(0,200):
                    move = random.randint(1, 4)
                    genom.append(move)
                self.population.append(genom)
                print(self.population)
            #Populaiton for maze genom = [1,2,1,3,4] 1= left, 2 = right, 3 = go up, 4 = go down
        elif self.game == "Bird":
            for chromosome in range(0,self.population_size):
                genom = []
                for i in range(0,200):
                    w_y   = random.uniform(-2.0, 2.0)
                    w_x   = random.uniform(-1.0, 1.0)
                    w_v   = random.uniform(-2.0, 2.0)
                    bias  = random.uniform(-1.0, 1.0)
                    genom.append(w_y)
                    genom.append(w_x)
                    genom.append(w_v)
                    genom.append(bias)
                self.population.append(genom)
                print(self.population)
            #Population for bird genom = [y_weight,x_weight,velocity_weight,bias]

    def fitness(self, maze_player, finish_line):
        if self.game == 'Maze':
            distance = abs(maze_player.x - finish_line[0]) + abs(maze_player.y - finish_line[1])
            fitness_score = 1000 - distance
            if (maze_player.x, maze_player.y) == finish_line:
                fitness_score = 10000 - maze_player.moves 
            wasted_moves = maze_player.moves - maze_player.successful_moves
            fitness_score -= wasted_moves * 5
            return max(0, fitness_score)
        
        elif self.game == 'Bird':
            # TODO: fitness for Bird
            return 0
        
genetic_algorithm("Bird").create_population()