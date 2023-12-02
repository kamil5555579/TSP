from population import Population
import matplotlib.pyplot as plt
from dummy import dummy_algorithm
from cityMap import CityMap, create_city_map

def single_run(population_size=30,
               map_size=100,
               num_cities=15,
               polish=False, 
               num_generations=30, 
               selection_mode="roulette",
               crossover_mode="ox", 
               mutation_mode="swap",
               elitism=0.2):

    population = Population(population_size=population_size, 
                            cityMap=create_city_map(num_cities, map_size, polish))
    population.evolution(num_generations=num_generations, 
                         selection_mode=selection_mode,
                         crossover_mode=crossover_mode, 
                         mutation_mode=mutation_mode,
                         elitism=elitism)
    population.plot_route_lenghts()

def compare_crossovers(population_size=30,
                     map_size=100,
                     num_cities=15,
                     polish=False, 
                     num_generations=30, 
                     selection_mode="roulette",
                     mutation_mode="swap",
                     elitism=0.2):

    crossovers = ["ox", "cx", "gx"]
    route_lengths = []
    cityMap = create_city_map(num_cities, map_size, polish)

    for crossover in crossovers:

        population = Population(population_size=population_size, 
                                cityMap=cityMap)
        population.evolution(num_generations=num_generations, 
                        selection_mode=selection_mode,
                        crossover_mode=crossover, 
                        mutation_mode=mutation_mode,
                        elitism=elitism)
        route_lengths.append(population.route_lengths)

    dummy_route_length = dummy_algorithm(cityMap)

    fig, ax = plt.subplots()
    for i in range(len(crossovers)):
        ax.plot(route_lengths[i], label=crossovers[i])

    ax.plot([dummy_route_length for i in range(num_generations)], label="dummy")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Route length")
    ax.set_title("Route length over generations")
    ax.legend()
    fig.savefig("figures/compare_crossovers.png")
    plt.show()

