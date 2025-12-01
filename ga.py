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
            pass #Populaiton for maze genom = [1,2,1,3,4] 1= left, 2 = right, 3 = go up, 4 = go down
        elif self.game == "Bird":
            pass #Population for bird genom = [y_weight,x_weight,velocity_weight,bias]
