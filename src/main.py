from population import Population

population = Population(population_size=10, map_size=100, num_cities=10, polish=False)
population.evolution(num_generations=10, selection_mode="roulette", crossover_mode="order", mutation_mode="swap")
