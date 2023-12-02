import numpy as np
import matplotlib.pyplot as plt
import random
from poland import Poland
from city import initialize_cities

class CityMap:
    def __init__(self, cities, map_size, polish) -> None:
        self.cities = cities
        self.map_size = map_size
        self.polish = polish

    def random_route(self):
        cities_copy = self.cities.copy()
        random.shuffle(cities_copy)
        route = np.array([city.index for city in cities_copy])
        return route

    def calculate_adjacency_matrix(self):
        self.adjacency_matrix = np.zeros((len(self.cities), len(self.cities)))
        for i in range(len(self.cities)):
            for j in range(len(self.cities)):
                self.adjacency_matrix[i][j] = self.cities[i].distance(self.cities[j])

    def calculate_route_length(self, genome):
        length = 0
        for i in range(len(genome) - 1):
            length += self.adjacency_matrix[genome[i]][genome[i+1]]
        length += self.adjacency_matrix[genome[-1]][genome[0]]
        return length

    def plot(self, genome, size, filename = "fig.png", show = False, title = "", polish = False, save = True):

        if polish:
            fig, ax = Poland.generate_poland_map()
        else:
            fig, ax = plt.subplots()
            ax.set_xlim(0,size)
            ax.set_ylim(0,size)

        ax.plot(np.append([self.cities[city_index].x for city_index in genome], self.cities[genome[0]].x),
                 np.append([self.cities[city_index].y for city_index in genome], self.cities[genome[0]].y), '-o')

        if title != "":
            ax.set_title('Generation: ' + str(title) )
    
        if save:
            fig.savefig(filename)
            
        if show is True:
            plt.show()

        plt.close(fig)

        return fig
        

def create_city_map(num_cities, map_size, polish=False):
    if polish:
        cities = Poland.generate_polish_cities(num_cities, map_size)
    else:
        cities = initialize_cities(num_cities, map_size)
    cityMap = CityMap(cities, map_size, polish)
    cityMap.calculate_adjacency_matrix()
    return cityMap