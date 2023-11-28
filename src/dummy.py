from cityMap import CityMap

def dummy_algorithm(cityMap):
    adjacency_matrix = cityMap.adjacency_matrix
    cities = cityMap.cities
    number_of_cities = len(cities)
    route_lengths = []

    for k in range(number_of_cities):

        first_city = cities[k].index
        route = [first_city]

        for i in range(number_of_cities - 1):
            current_city = route[-1]
            min_distance = float('inf')
            for j in range(number_of_cities):
                if j not in route:
                    if adjacency_matrix[current_city][j] < min_distance:
                        min_distance = adjacency_matrix[current_city][j]
                        next_city = j
            route.append(next_city)

        route_length = cityMap.calculate_route_length(route)
        route_lengths.append(route_length)

    best_route = min(route_lengths)

    return best_route

