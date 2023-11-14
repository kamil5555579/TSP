from cityMap import CityMap
from city import City, initialize_cities
import random

class Population:

    def __init__(self, population_size, map_size, num_cities) -> None:
        self.population_size = population_size
        self.map_size = map_size
        self.cityMap = CityMap(initialize_cities(num_cities, map_size))
        self.cityMap.calculate_adjacency_matrix()
        self.population = [self.cityMap.random_route() for _ in range(population_size)]

    def calculate_fitness(self):
        self.fitness = [1 / self.cityMap.calculate_route_length(genome) for genome in self.population]
        self.fitness_sum = sum(self.fitness)

    def plot_best_route(self, filename = "fig.png", show = False, title = ""):
        self.cityMap.plot(self.population[self.fitness.index(max(self.fitness))], self.map_size, filename, show, title)

    def mutate():
        pass

    def crossover():
        pass
    
    def selection():
        pass