from colorthief import ColorThief
import numpy as np
import glob
import pandas as pd
import matplotlib.pyplot as plt
import sys

image_folder = sys.argv[1]
image_files = glob.glob(image_folder+"*.jpg")

for image_filename in image_files:
    color_thief = ColorThief(image_filename)
    palette = color_thief.get_palette(quality=1)
    palette = np.array(palette)[np.newaxis, :, :]

    plt.imshow(palette)
    plt.axis('off')
    print(image_filename)
    plt.savefig(image_filename.split("/")[1].split(".")[0] + "_perc" + "_color_palette.jpg", pad_inches=0)







