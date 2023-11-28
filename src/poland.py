import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import os
from city import City
import random

class Poland:
    #path = os.getcwd()
    path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    ''' u mnie to nie działa
    borders = gpd.read_file(os.path.join(
        path, 
        'maps', 
        'PRG_jednostki_administracyjne_2022'))
    '''
    borders = gpd.read_file('maps/PRG_jednostki_administracyjne_2022')
    borders = borders['geometry']

    """
    cities = pd.read_html(os.path.join(
        path, 
        'maps', 
        'wspolrzedne_polskich_miast.html'))[3]
    """
    cities = pd.read_html('maps/wspolrzedne_polskich_miast.html')[3]
    cities.columns = cities.iloc[0]
    cities = cities.iloc[1:]
    cities['Szerokość'] = cities['Szerokość'].str.replace('°N', '').astype(float)
    cities['Długość'] = cities['Długość'].str.replace('°E', '').astype(float)
    list_of_cities = ['Białystok', 'Warszawa', 'Gdynia',
                    'Wrocław', 'Kraków', 'Poznań',
                        'Szczecin', 'Gdańsk', 'Katowice',
                        'Lublin', 'Łódź', 'Olsztyn',
                        'Rzeszów', 'Bydgoszcz', 'Zielona Góra',
                        'Opole', 'Toruń', 'Kielce',]

    def generate_polish_cities(num_cities, size):
        list_of_cities = sorted(Poland.list_of_cities, key=lambda x: random.random())
        list_of_cities = list_of_cities[:num_cities]
        few_cities = Poland.cities[Poland.cities['Miasto'].isin(list_of_cities)]
        Poland.few_cities = few_cities
        polish_cities = [City(city[1]['Długość'], city[1]['Szerokość'], i) for i, city in enumerate(few_cities.iterrows())]
        return polish_cities

    def generate_poland_map():
        fig, ax = plt.subplots(figsize=(10,10))
        Poland.borders.plot(color='white', edgecolor='black', ax=ax)
        Poland.few_cities.plot.scatter(y='Szerokość', x='Długość', ax=ax, color='black', s=5)
        # Plot city labels
        for i, city in Poland.few_cities.iterrows():
            ax.annotate(city['Miasto'], (city['Długość'], city['Szerokość']), fontsize=8)

        return fig, ax