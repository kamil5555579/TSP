from analysis import compare_crossovers, single_run

single_run(population_size=100,
           map_size=200, 
           num_cities=20, polish=False, 
           num_generations=300, 
           selection_mode="roulette", 
           crossover_mode="ox", 
           mutation_mode="swap",
           elitism=0.2)

# compare_crossovers(population_size=50,
#                     map_size=100, 
#                     num_cities=15, polish=False, 
#                     num_generations=500, 
#                     selection_mode="roulette", 
#                     mutation_mode="swap",
#                     elitism=0.2)
