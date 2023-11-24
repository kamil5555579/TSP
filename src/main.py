from population import Population

population = Population(
    population_size=10, 
    map_size=100, 
    num_cities=10, 
    polish=False)
population.calculate_fitness()
population.plot_best_route(filename="fig.png", show=True, title="0")
