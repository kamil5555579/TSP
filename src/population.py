from cityMap import CityMap
from city import City, initialize_cities
import random
from poland import generate_polish_cities

class Population:

    def __init__(self, population_size, map_size, num_cities, polish = False) -> None:
        self.population_size = population_size
        self.polish = polish

        if polish:
            self.cityMap = CityMap(generate_polish_cities(num_cities, map_size))
        else:
            self.cityMap = CityMap(initialize_cities(num_cities, map_size))

        self.map_size = map_size
        self.cityMap.calculate_adjacency_matrix()
        self.population = [self.cityMap.random_route() for _ in range(population_size)]
        print(self.population)

    def calculate_fitness(self):
        self.fitness = [1 / self.cityMap.calculate_route_length(genome) for genome in self.population]
        self.fitness_sum = sum(self.fitness)
        print(self.fitness)

    def plot_best_route(self, filename = "fig.png", show = False, title = "", save = True):
        fig = self.cityMap.plot(self.population[self.fitness.index(max(self.fitness))], self.map_size, filename, show, title, polish = self.polish, save = save)
        return fig
    
    def selection(self, mode = "roulette"):
        
        if mode == "roulette":

            fitness_percentages = [fitness / self.fitness_sum for fitness in self.fitness]
            new_population = []

            for _ in range(self.population_size):
                random_number = random.random()
                for i in range(self.population_size):
                    if random_number < sum(fitness_percentages[:i+1]):
                        new_population.append(self.population[i])
                        break
            
            self.population = new_population

        elif mode == "tournament":
            pass
        else:
            raise Exception("Wrong selection mode")
        
    def crossover(self, mode = "order"):
        if mode == "order":
            pass
        elif mode == "pmx":
            pass
        else:
            raise Exception("Wrong crossover mode")
        
    def mutation(self, mode = "swap"):
        if mode == "swap":
            pass
        elif mode == "insert":
            pass
        elif mode == "inversion":
            pass
        else:
            raise Exception("Wrong mutation mode")
    
    def evolution(self, selection_mode = "roulette", crossover_mode = "order", mutation_mode = "swap", num_generations = 10):

        self.figures = []
        self.calculate_fitness()

        for i in range(num_generations):
            self.selection(selection_mode)
            self.crossover(crossover_mode)
            self.mutation(mutation_mode)
            self.calculate_fitness()
            self.figures.append(self.plot_best_route(filename="fig" + str(i) + ".png", show=False, title=i, save=True))

    def plot_evolution(self, filename = "evolution.gif"):
        pass




