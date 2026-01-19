import random

class genetic_algorithm:
    def __init__(self,game):
        if game=="Bird" or game=="Maze":
            self.game = game
        else:
            raise AttributeError(f"Wrong game type: '{game}'.")
        self.population = []
        self.kids = []
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
                #print(self.population)
            #Populaiton for maze genom = [1,2,1,3,4] 1= left, 2 = right, 3 = go up, 4 = go down
        elif self.game == "Bird":
            for chromosome in range(0,self.population_size):
                genom = []
                w_y   = random.uniform(-2.0, 2.0)
                w_x   = random.uniform(-1.0, 1.0)
                w_v   = random.uniform(-2.0, 2.0)
                bias  = random.uniform(-1.0, 1.0)
                genom.append(w_y)
                genom.append(w_x)
                genom.append(w_v)
                genom.append(bias)
                self.population.append(genom)
            #Population for bird genom = [y_weight,x_weight,velocity_weight,bias]

    def fitness(self, player, finish_line=None):
        if self.game == 'Maze':
            distance = abs(player.x - finish_line[0]) + abs(player.y - finish_line[1])
            fitness_score = 1000 - distance
            if (player.x, player.y) == finish_line:
                fitness_score = 2000 - player.moves 
            wasted_moves = player.moves - player.successful_moves
            fitness_score -= wasted_moves * 5
            return max(0, fitness_score)
        
        elif self.game == 'Bird':
            fitness_score = 0
            #fitness_score += player.frames_alive
            fitness_score += player.score * 1000
            fitness_score += player.distance_traveled * 0.1 
            return max(0, fitness_score)
        
    def live_longer(self,survivor):
        self.kids.append(survivor)

    def swap_generations(self):
        self.population = self.kids

    def crossover(self, parent1, parent2):
        point1 = random.randint(1, len(parent1) - 2)
        point2 = random.randint(point1 + 1, len(parent1) - 1)
        kid = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        return kid

    def mutate(self, chromosome, mutation_rate=0.05):
        mutated = chromosome.copy()
        mutations_count = 0
        
        if self.game == "Maze":
            for i in range(len(mutated)):
                if random.random() < mutation_rate:
                    mutated[i] = random.randint(1, 4)
                    mutations_count += 1
        
        elif self.game == "Bird":
            for i in range(len(mutated)):
                if random.random() < mutation_rate:
                    mutated[i] += random.uniform(-1.0, 1.0)
                    mutations_count += 1
        
        return mutated

    def select_parent(self, players, tournament_size=5):
        tournament = random.sample(players, tournament_size)
        best = max(tournament, key=lambda p: p.fitness)
        return best.genom
    
    def evolve(self, players, elite_count=2):
        self.kids.clear()
        self.elite_genomes = []
        self.elite_genome_ids = []
        
        for i in range(elite_count):
            #print(f"{players[i].fitness}")
            self.live_longer(players[i].genom) #players are sorted, so they are for sure here in the first and second slot
            self.elite_genomes.append(players[i].genom)
            self.elite_genome_ids.append(id(players[i].genom))

        while len(self.kids) < self.population_size:
            parent1 = self.select_parent(players)
            parent2 = self.select_parent(players)
            kid = self.crossover(parent1, parent2)
            kid = self.mutate(kid)
            self.kids.append(kid)
        self.swap_generations()