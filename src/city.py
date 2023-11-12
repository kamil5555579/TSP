import random
import matplotlib.pyplot as plt
import numpy as np

class City:
    def __init__(self, x, y, index) -> None:
        self.x = x
        self.y = y
        self.index = index

    def distance(self, city):
        return ((self.x - city.x)**2 + (self.y - city.y)**2)**0.5
    
class Route:
    def __init__(self, cities) -> None:
        self.cities = cities

    def random_route(self):
        random.shuffle(self.cities)
        self.route = [city.index for city in self.cities]

    def calculate_adjacency_matrix(self):
        self.adjacency_matrix = np.zeros((len(self.cities), len(self.cities)))
        for i in range(len(self.cities)):
            for j in range(len(self.cities)):
                self.adjacency_matrix[i][j] = self.cities[i].distance(self.cities[j])

    def calculate_route_length(self):
        self.route_length = 0
        for i in range(len(self.cities) - 1):
            self.route_length += self.adjacency_matrix[self.route[i]][self.route[i+1]]
        self.route_length += self.adjacency_matrix[self.route[-1]][self.route[0]]

    def plot(self):
        x = [city.x for city in self.cities]
        y = [city.y for city in self.cities]
        plt.plot(x, y, 'o-')
        plt.show()
        
class Population:

    def __init__(self, routes, population_size) -> None:
        self.routes = routes
        self.population_size = population_size