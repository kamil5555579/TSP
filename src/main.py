from population import Population

population = Population(population_size=100, 
                        map_size=100, 
                        num_cities=15, 
                        polish=False)
population.evolution(num_generations=500, 
                     selection_mode="roulette", 
                     crossover_mode="ox", 
                     mutation_mode="swap")

population.plot_route_lenghts()
