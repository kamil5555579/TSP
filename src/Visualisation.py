import matplotlib.pyplot as plt
import numpy as np
import imageio.v2 as imageio
import os


def make_gif(img_path, num_generations, gif_path="generations.gif"):#os.getcwd()+"/generations.gif"):
    # Parameters
    # display_time time after gif will loop in seconds
    display_time = 30

    filenames = []
    for j in range(num_generations):
        filenames.append('fig'+str(j)+'.png')

    os.chdir(img_path)
    with imageio.get_writer(gif_path, fps = num_generations/display_time, loop = 10) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    os.chdir("..")