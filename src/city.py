import random
import matplotlib.pyplot as plt
import numpy as np

class City:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def distance(self, city):
        return ((self.x - city.x)**2 + (self.y - city.y)**2)**0.5
    
class Route:
    def __init__(self, cities) -> None:
        self.cities = cities

    def random_route(self):
        random.shuffle(self.cities)

    def distance(self):
        distance = 0
        for i in range(len(self.cities)):
            distance += self.cities[i].distance(self.cities[i-1])
        return distance

    def plot(self):
        x = [city.x for city in self.cities]
        y = [city.y for city in self.cities]
        plt.plot(x, y, 'o-')
        plt.show()
        
class Population:

    def __init__(self, routes, population_size) -> None:
        self.routes = routes
        self.population_size = population_size