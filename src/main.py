from population import Population
from analysis import compare_crossovers

"""
population = Population(population_size=30, 
                        map_size=100, 
                        num_cities=15, 
                        polish=False)
population.evolution(num_generations=30, 
                     selection_mode="roulette",
                     crossover_mode="gx", 
                     mutation_mode="swap")

population.plot_route_lenghts()
"""
compare_crossovers(population_size=50,
                    map_size=100, 
                    num_cities=15, polish=False, 
                    num_generations=100, 
                    selection_mode="roulette", 
                    mutation_mode="swap")
