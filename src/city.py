import random
class City:
    def __init__(self, x, y, index) -> None:
        self.x = x
        self.y = y
        self.index = index

    def distance(self, city):
        return ((self.x - city.x)**2 + (self.y - city.y)**2)**0.5
    
def initialize_cities(num_cities, size):
    cities = []
    for i in range(num_cities):
        cities.append(City(random.randint(0, size), random.randint(0, size), i))
    return cities
