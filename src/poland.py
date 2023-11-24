import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import os
from city import City

#path = os.getcwd()
path = os.path.normpath(os.getcwd() + os.sep + os.pardir)

borders = gpd.read_file(os.path.join(
    path, 
    'maps', 
    'PRG_jednostki_administracyjne_2022'))
borders = borders['geometry']

cities = pd.read_html(os.path.join(
    path, 
    'maps', 
    'wspolrzedne_polskich_miast.html'))[3]
cities.columns = cities.iloc[0]
cities = cities.iloc[1:]
cities['Szerokość'] = cities['Szerokość'].str.replace('°N', '').astype(float)
cities['Długość'] = cities['Długość'].str.replace('°E', '').astype(float)
list_of_cities = ['Białystok', 'Warszawa', 'Gdynia', 'Wrocław']
few_cities = cities[cities['Miasto'].isin(list_of_cities)]

def generate_polish_cities(num_cities, size):
    polish_cities = [City(city[1]['Długość'], city[1]['Szerokość'], i) for i, city in enumerate(few_cities.iterrows())]
    return polish_cities

def generate_poland_map():
    fig, ax = plt.subplots(figsize=(10,10))
    borders.plot(color='white', edgecolor='black', ax=ax)
    few_cities.plot.scatter(y='Szerokość', x='Długość', ax=ax, color='black', s=5)
    # Plot city labels
    for i, city in few_cities.iterrows():
        ax.annotate(city['Miasto'], (city['Długość'], city['Szerokość']), fontsize=8)

    return fig, ax