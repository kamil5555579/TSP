import matplotlib.pyplot as plt
import numpy as np
import imageio.v2 as imageio


def visualise_Map(
    city_coordinates, 
    size, 
    filename = "fig.png", 
    show = False,
    title = ""):

    fig, ax = plt.subplots()
    ax.plot(np.append(city_coordinates[0, :], city_coordinates[0, 0]),
     np.append(city_coordinates[1, :], city_coordinates[1, 0]), '-o')
    ax.set_xlim(0,size)
    ax.set_ylim(0,size)
    if title != "":
        ax.set_title('Generation: ' + str(title) )
    
    fig.savefig(filename)
    if show is True:
        plt.show()


def make_gif(
    list_of_cisty_coordinates_to_plot, 
    size, 
    img_path, 
    gif_name = 'nextGeneration.gif',
    list_of_generation_number = None):

    i = 0
    filenames = []

    for coordinates in list_of_cisty_coordinates_to_plot:
        file_name = img_path + f"/figure_{i}.png"
        filenames.append(file_name)
        # Optional use of generation number
        if list_of_generation_number == None:
            visualise_Map(
                coordinates, 
                size, 
                filename = file_name)
        else:
            visualise_Map(
                coordinates, 
                size, 
                filename = file_name, 
                title = list_of_generation_number[i])
        i += 1

    print(filenames)
    with imageio.get_writer(gif_name, fps = 0.5, loop = 10) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)


# Example of make_gif() usage:
'''
size = 10
list_of_cisty_coordinates_to_plot = []
img_path = r"/home/tymon/Desktop/Tutorials/GeneticAlgorithm's/images"

testArray = np.array([[1, 3, 5, 5, 7, 9, 9, 1], [6, 6, 4, 6, 6, 6, 2, 2]])
# Using np.copy instead of reference (later changes doesn't influence this list)
list_of_cisty_coordinates_to_plot.append( np.copy(testArray) )

# Swaping columns
testArray[:, [2, 3]] = testArray[:, [3, 2]]
list_of_cisty_coordinates_to_plot.append( np.copy(testArray) )

make_gif(
    list_of_cisty_coordinates_to_plot, 
    size, 
    img_path,
    list_of_generation_number = [1, 100])
'''