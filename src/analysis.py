from population import Population
import matplotlib.pyplot as plt

def compare_crossovers():

    crossovers = ["ox", "cx", "gx"]
    route_lengths = []
    for crossover in crossovers:

        population = Population(population_size=30, 
                            map_size=100, 
                            num_cities=15, 
                            polish=False)
        population.evolution(num_generations=30, 
                        selection_mode="roulette",
                        crossover_mode=crossover, 
                        mutation_mode="swap")
        route_lengths.append(population.route_lengths)

    fig, ax = plt.subplots()
    for i in range(len(crossovers)):
        ax.plot(route_lengths[i], label=crossovers[i])
    ax.set_xlabel("Generation")
    ax.set_ylabel("Route length")
    ax.set_title("Route length over generations")
    ax.legend()
    plt.show()

