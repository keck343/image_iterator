import pandas as pd
import os
import glob
import random
from PIL import Image, ImageOps
import sys

csv_file = sys.argv[1]
responces_df = pd.read_csv(csv_file)
opactiy_level = 87

for row_num in range(responces_df.shape[0] -19, responces_df.shape[0]):
    file_name = responces_df.iloc[row_num, 1]
    print(file_name)
    image_layers = []
    image_folder = "exciting_labels/"
    color_folder = "color_palettes/"
    for i in range(2, 5):
        print(responces_df.iloc[row_num, i].split(" ")[0])
        matches = glob.glob(image_folder + responces_df.iloc[row_num, i].split(" ")[0] + "*.jpg")
        match = matches[random.randint(0, len(matches)-1)]
        image_layers.append(match)

    color_image = glob.glob(color_folder + responces_df.iloc[row_num, 5].split(" ")[0] + "*.jpg")[0]
    image_layers.append(color_image)

    print(image_layers)
    
    if os.path.isdir(file_name + "_layers_" + str(opactiy_level)) == False:
        print("make dir")
        os.mkdir(file_name + "_layers_" + str(opactiy_level))

    #resize to match
    widths = []
    heights = []


    for i in range(len(image_layers)):
        im = Image.open(image_layers[i])
        widths.append(im.size[0])
        heights.append(im.size[1])
    
    w = min(widths)
    h = min(heights)

    # iterate through other layers
    for i in range(len(image_layers)):
        im = Image.open(image_layers[i])
        alpha = Image.new("L", im.size, opactiy_level)
        im_copy = im.copy() 
        im_copy.putalpha(alpha)
        crop = im_copy.crop((0, 0, w, h))
        crop.save(file_name + "_layers_" + str(opactiy_level) + "/layer_" + str(i) + ".png")
        
    # combine images 

    layer_files = glob.glob(file_name + "_layers_" + str(opactiy_level) + "/*.png")
    random.shuffle(layer_files)
    print(layer_files)

    background = Image.open(layer_files[0])
    foreground = Image.open(layer_files[1])
    composite = Image.alpha_composite(background, foreground)
    composite.save(file_name + "_composite_1" +  ".png")

    for i in range(2, len(layer_files)):
        print(layer_files[i])
        background = Image.open(file_name + "_composite_" + str(i-1) +  ".png")
        foreground = Image.open(layer_files[i])
        composite = Image.alpha_composite(background, foreground)
        if i < len(layer_files) -1:
            composite.save(file_name + "_composite_" + str(i) +  ".png")
        else:
            composite.save(file_name + "_composite_final_" + str(opactiy_level)  +  ".png")
    
