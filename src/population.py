from cityMap import CityMap
from city import City, initialize_cities
import random
from poland import generate_polish_cities
import numpy as np
import matplotlib.pyplot as plt

class Population:

    def __init__(self, population_size, map_size, num_cities, polish = False) -> None:
        self.population_size = population_size
        self.polish = polish

        if polish:
            self.cityMap = CityMap(generate_polish_cities(num_cities, map_size)) 
            # jeszcze ogarne lepiej to generowanie miast bo na razie zawsze są te same i ta sama ilość
        else:
            self.cityMap = CityMap(initialize_cities(num_cities, map_size))

        self.map_size = map_size
        self.cityMap.calculate_adjacency_matrix()
        self.population = \
            [self.cityMap.random_route() for o in range(population_size)]
        #print(self.population)


    def calculate_fitness(self):
        self.fitness = np.array([1 / self.cityMap.calculate_route_length(genome) for genome in self.population])
        self.fitness_sum = np.sum(self.fitness)
        #print(self.fitness)

    def plot_best_route(self, filename = "fig.png", show = False, title = "", save = True):
        fig = self.cityMap.plot(self.population[np.argmax(self.fitness)], self.map_size, filename, show, title, polish = self.polish, save = save)
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

        elif mode == "tournament": # drugi rodzaj selekcji też możesz zrobić
            pass
        else:
            raise Exception("Wrong selection mode")
        
    def crossover(self, mode = "ox"):
        if mode == "ox": # To ja zrobię
            new_population = []
            self.population = sorted(self.population, key = lambda x: random.random())

            for i in range(0, self.population_size, 2):
                genome_length = len(self.population[i])
                parent1 = self.population[i]
                parent2 = self.population[i+1]
                child1 = np.ones(genome_length, dtype=int) * -1 # -1 means that there is no city with such index
                child2 = np.ones(genome_length, dtype=int) * -1 # -1 means that there is no city with such index
                start_point = random.randint(0, genome_length - 1)
                end_point = random.randint(start_point, genome_length - 1)
                child1[start_point:end_point] = parent1[start_point:end_point]
                child2[start_point:end_point] = parent2[start_point:end_point]
                for j in range(genome_length):
                    if parent2[j] not in child1:
                        for k in range(genome_length):
                            if child1[k] == -1:
                                child1[k] = parent2[j]
                                break
                    if parent1[j] not in child2:
                        for k in range(genome_length):
                            if child2[k] == -1:
                                child2[k] = parent1[j]
                                break
                new_population.append(child1)
                new_population.append(child2)

            self.population = new_population

        elif mode == "pmx": # to dla Ciebie
            pass

        elif mode == "cx": # dla mnie
            new_population = []
            self.population = sorted(self.population, key = lambda x: random.random())

            for i in range(0, self.population_size, 2):
                genome_length = len(self.population[i])
                parent1 = self.population[i]
                parent2 = self.population[i+1]
                child1 = np.ones(genome_length, dtype=int) * -1
                child2 = np.ones(genome_length, dtype=int) * -1

                city = parent1[0]
                child1[0] = city
                while True:
                    city_index = np.where(parent2 == city)[0][0]
                    city = parent1[city_index]
                    child1[city_index] = city
                    if city == parent2[0]:
                        break

                city = parent2[0]
                child2[0] = city
                while True:
                    city_index = np.where(parent1 == city)[0][0]
                    city = parent2[city_index]
                    child2[city_index] = city
                    if city == parent1[0]:
                        break

                for j in range(genome_length):
                    if child1[j] == -1:
                        child1[j] = parent2[j]
                    if child2[j] == -1:
                        child2[j] = parent1[j]

                new_population.append(child1)
                new_population.append(child2)

            self.population = new_population

        elif mode == "gx": # dla mnie 
            new_population = []

            for _ in range(2): # 2 parents only produce 1 child so we need to do it twice
                self.population = sorted(self.population, key = lambda x: random.random())

                for i in range(0, self.population_size, 2):
                    genome_length = len(self.population[i])
                    parent1 = self.population[i]
                    parent2 = self.population[i+1]
                    child = np.ones(genome_length, dtype=int) * -1 # -1 means that there is no city with such index
                    city = 0
                    for i in range(genome_length-1):
                        parent1_city_index = np.where(parent1 == city)[0][0]
                        parent2_city_index = np.where(parent2 == city)[0][0]
                        child[i] = city
                        adjacent_cities = [parent1[(parent1_city_index - 1) % genome_length],
                                            parent1[(parent1_city_index + 1) % genome_length],
                                            parent2[(parent2_city_index - 1) % genome_length],
                                            parent2[(parent2_city_index + 1) % genome_length]]
                        distances = [self.cityMap.adjacency_matrix[city][adjacent_city] for adjacent_city in adjacent_cities]

                        while True:
                            nearest_city = adjacent_cities[distances.index(min(distances))]
                            if nearest_city not in child:
                                break
                            elif len(distances) > 1:
                                distances.remove(min(distances))
                                adjacent_cities.remove(nearest_city)
                            else:
                                nearest_city = random.randint(0, genome_length - 1)
                                while nearest_city in child:
                                    nearest_city = random.randint(0, genome_length - 1)
                                break
                                
                        city = nearest_city
                    
                    child[-1] = city

                    new_population.append(child)

            self.population = new_population

        elif mode == "MSCX": # dla ciebie
            pass
        else:
            raise Exception("Wrong crossover mode")
        
    def mutation(self, mode = "swap", chance = 0.001):
        if mode == "swap":
            for person in self.population:
                if random.random() <= chance: 
                    random_index_1 = random.randint(0, len(person)-1)
                    while True:
                        random_index_2 = random.randint(0, len(person)-1)
                        if random_index_2 != random_index_1:
                            break

                    person[random_index_1], person[random_index_2] = \
                        person[random_index_2], person[random_index_1] 
        else:
            raise Exception("Wrong mutation mode")
    
    def evolution(self, selection_mode = "roulette", crossover_mode = "ox", mutation_mode = "swap", num_generations = 10):

        self.figures = []
        self.fitnesses = []
        self.calculate_fitness()

        for i in range(num_generations):
            self.figures.append(self.plot_best_route(filename="fig" + str(i) + ".png", show=False, title=i, save=False))
            self.fitnesses.append(max(self.fitness))
            self.selection(selection_mode)
            self.crossover(crossover_mode)
            self.mutation(mutation_mode)
            self.calculate_fitness()

        self.figures.append(self.plot_best_route(filename="fig" + str(num_generations) + ".png",
                                                show=False,
                                                title=num_generations,
                                                save=True))
        self.fitnesses.append(max(self.fitness))

        self.route_lengths = [1/fitness for fitness in self.fitnesses]

        # tu po tym można zrobić animację, albo w nowej metodzie - dla ciebie

        # i wykres dlugosci od generacji - dla mnie

    def plot_route_lenghts(self):
        fig, ax = plt.subplots()
        ax.plot(self.route_lengths)
        ax.set_xlabel("Generation")
        ax.set_ylabel("Route length")
        ax.set_title("Route length over generations")
        fig.savefig("route_length.png")






