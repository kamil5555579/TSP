from cityMap import CityMap
from city import City, initialize_cities
import random
from poland import Poland
import numpy as np
import matplotlib.pyplot as plt
from Visualisation import  make_gif
import os
import shutil
from progressbar import progressbar


class Population:

    def __init__(self, population_size, cityMap) -> None:
        self.population_size = population_size
        self.cityMap = cityMap
        self.map_size = cityMap.map_size
        self.polish = cityMap.polish
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
    
    def find_elites(self, num_elites = 2):
        sorted_population = [x for _, x in sorted(zip(self.fitness, self.population), key=lambda pair: pair[0], reverse=True)]
        mating_size = self.population_size - num_elites
        elites = sorted_population[0:num_elites]
        return elites, mating_size

    def selection(self, mode = "roulette", mating_size = 0):
        
        if mode == "roulette":

            fitness_percentages = [fitness / self.fitness_sum for fitness in self.fitness]
            mating_pool = []

            for _ in range(mating_size):
                random_number = random.random()
                for i in range(self.population_size):
                    if random_number < sum(fitness_percentages[:i+1]):
                        mating_pool.append(self.population[i])
                        break
            
            return mating_pool

        elif mode == "tournament": # drugi rodzaj selekcji też możesz zrobić
            pass
        else:
            raise Exception("Wrong selection mode")
        
    def crossover(self, mode = "ox", mating_pool = []):
        if mode == "ox": # To ja zrobię
            children = []

            for i in range(0, len(mating_pool), 2):
                genome_length = len(self.population[i])
                parent1 = mating_pool[i]
                parent2 = mating_pool[i+1]
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
                children.append(child1)
                children.append(child2)

            return children

        elif mode == "pmx": # to dla Ciebie
            # Parameters
            min_procentage_size = 0.25
            max_procentage_size = 0.75

            new_population = []

            for _ in range(2):
                # Creating two pools of parents
                # P - stands for parent
                rng = np.random.default_rng()
                ref_indexes = np.arange(0, len(mating_pool), 1)
                group_of_P0 = rng.choice(
                    ref_indexes, 
                    size=int(len(ref_indexes)/2), 
                    replace=False)
                group_of_P1 = ref_indexes[np.logical_not(np.isin(
                    ref_indexes,
                    group_of_P0))]
                
                for j in range(0, len(group_of_P0)):
                    P0 = np.array(mating_pool[group_of_P0[j]])
                    P1 = np.array(mating_pool[group_of_P1[j]])
                    child = np.zeros_like(P0)

                    min_size = np.rint(min_procentage_size * len(P0)) 
                    max_size = np.rint(max_procentage_size * len(P0))

                    length_of_copied_gene = random.randint(min_size, max_size)
                    starting_index = random.randint(0,len(P0)-length_of_copied_gene)

                    selected = np.arange(
                        starting_index, 
                        starting_index+length_of_copied_gene,
                        1)
                    used_indexes = []

                    # Copying firs chunk (it has to be in separated loop)
                    for index in selected:
                        child[index] = P0[index]
                        used_indexes.append(index)

                    for index in selected:
                        # Checking if value is already copied
                        value_indexP1 = P1[index]
                        if np.isin(value_indexP1, P0[selected]):
                            pass
                        else:
                            # Retrying to fit P1's replaced number into spot where  
                            # new number was moved from until spot is free
                            value_indexP0 = P0[index]
                            while True:
                                index_to_place = np.where(P1 == value_indexP0)[0][0]
                                if not np.isin(index_to_place, used_indexes):
                                    break
                                else:
                                    value_indexP0 = P0[index_to_place]

                            child[ index_to_place ] = value_indexP1
                            used_indexes.append(index_to_place)

                    # Copying rest of P1
                    for i in range(len(child)):
                        if not (i in used_indexes):
                            child[i] = P1[i]

                    new_population.append(child.tolist())
            return new_population

        elif mode == "cx": # dla mnie
            children = []

            for i in range(0, len(mating_pool), 2):
                genome_length = len(self.population[i])
                parent1 = mating_pool[i]
                parent2 = mating_pool[i+1]
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

                children.append(child1)
                children.append(child2)

            return children

        elif mode == "gx": # dla mnie 
            children = []

            for _ in range(2): # 2 parents only produce 1 child so we need to do it twice
                self.population = sorted(self.population, key = lambda x: random.random())

                for i in range(0, len(mating_pool), 2):
                    genome_length = len(self.population[i])
                    parent1 = mating_pool[i]
                    parent2 = mating_pool[i+1]
                    child = np.ones(genome_length, dtype=int) * -1 # -1 means that there is no city with such index
                    city = random.randint(0, genome_length - 1)
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

                    children.append(child)

            return children

        elif mode == "uhx":
            children = []

            for _ in range(2): # 2 parents only produce 1 child so we need to do it twice
                self.population = sorted(self.population, key = lambda x: random.random())

                for i in range(0, len(mating_pool), 2):
                    genome_length = len(self.population[i])
                    parent1 = mating_pool[i]
                    parent2 = mating_pool[i+1]
                    child = np.ones(genome_length, dtype=int) * -1 # -1 means that there is no city with such index
                    city = random.randint(0, genome_length - 1)
                    parent1_city_index = np.where(parent1 == city)[0][0]
                    parent2_city_index = np.where(parent2 == city)[0][0]
                    pointers = [parent1_city_index-1, parent1_city_index+1, parent2_city_index-1, parent2_city_index+1]
                    for i in range(genome_length-1):
                        child[i] = city
                        adjacent_cities = [parent1[pointers[0] % genome_length],
                                            parent1[pointers[1] % genome_length],
                                            parent2[pointers[2] % genome_length],
                                            parent2[pointers[3] % genome_length]]
                        distances = [self.cityMap.adjacency_matrix[city][adjacent_city] for adjacent_city in adjacent_cities]

                        while True:
                            nearest_city = adjacent_cities[distances.index(min(distances))]
                            if nearest_city not in child:
                                if distances.index(min(distances)) == 0 or distances.index(min(distances)) == 2:
                                    pointers[distances.index(min(distances))] -= 1
                                else:
                                    pointers[distances.index(min(distances))] += 1
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

                    children.append(child)

            return children

        elif mode == "MSCX": # dla ciebie
            pass
        else:
            raise Exception("Wrong crossover mode")
        
    def mutation(self, mode = "swap", chance = 0.001, children = []):
        if mode == "swap":
            for person in children:
                if random.random() <= chance: 
                    random_index_1 = random.randint(0, len(person)-1)
                    while True:
                        random_index_2 = random.randint(0, len(person)-1)
                        if random_index_2 != random_index_1:
                            break

                    person[random_index_1], person[random_index_2] = \
                        person[random_index_2], person[random_index_1] 
            return children
        else:
            raise Exception("Wrong mutation mode")
    
    def evolution(self, selection_mode = "roulette", crossover_mode = "ox", mutation_mode = "swap", mutation_rate=0.001, num_generations = 10, num_elites = 2):

        self.fitnesses = []
        self.calculate_fitness()

        # Making and clearing temporary folder for png's to create GIF
        if os.path.exists('tmp_figures'):
            shutil.rmtree('tmp_figures')
        os.makedirs('tmp_figures')

        print("Progres in simulating generations:")
        for i in progressbar(range(num_generations), redirect_stdout=True):
            self.plot_best_route(
                filename = "tmp_figures/" + "fig" + str(i) + ".png", 
                show=False, 
                title=i, 
                save=True)
            self.fitnesses.append(max(self.fitness))
            elites, mating_size = self.find_elites(num_elites)
            mating_pool = self.selection(selection_mode, mating_size)
            children = self.crossover(crossover_mode, mating_pool)
            children = self.mutation(mutation_mode, chance=mutation_rate, children=children)
            self.population = elites + children
            self.calculate_fitness()

        make_gif("tmp_figures/", num_generations, gif_path="../figures/generations.gif")
        self.fitnesses.append(max(self.fitness))

        self.route_lengths = [1/fitness for fitness in self.fitnesses]

        # tu po tym można zrobić animację, albo w nowej metodzie - dla ciebie

        # i wykres dlugosci od generacji - dla mnie

    def plot_route_lenghts(self, filename = "route_length.png", show = False, save = True):
        fig, ax = plt.subplots()
        ax.plot(self.route_lengths)
        ax.set_xlabel("Generation")
        ax.set_ylabel("Route length")
        ax.set_title("Route length over generations")
        if save:
            fig.savefig('figures/'+ filename)
        if show:
            plt.show()






