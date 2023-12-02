from analysis import compare_crossovers, single_run, compare_mutation_rates

# single_run(population_size=200,
#            map_size=200, 
#            num_cities=25, polish=False, 
#            num_generations=100, 
#            selection_mode="roulette", 
#            crossover_mode="gx", 
#            mutation_mode="swap",
#            num_elites=2)

# compare_crossovers(population_size=200,
#                     map_size=200, 
#                     num_cities=25, polish=False, 
#                     num_generations=150, 
#                     selection_mode="roulette", 
#                     mutation_mode="swap",
#                     num_elites=2)

compare_mutation_rates(population_size=200,
                    map_size=200, 
                    num_cities=25, polish=False, 
                    num_generations=50, 
                    selection_mode="roulette", 
                    crossover_mode="uhx",
                    num_elites=2)