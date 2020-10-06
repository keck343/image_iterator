# https://www.learnopencv.com/pytorch-for-beginners-image-classification-using-pre-trained-models/

from torchvision import models
from torchvision import transforms
import torch
import os
from PIL import Image
import sys
import glob
import pandas as pd


print(dir(models))

# image transform
transform = transforms.Compose([            #[1]
 transforms.Resize(256),                    #[2]
 transforms.CenterCrop(224),                #[3]
 transforms.ToTensor(),                     #[4]
 transforms.Normalize(                      #[5]
 mean=[0.485, 0.456, 0.406],                #[6]
 std=[0.229, 0.224, 0.225]                  #[7]
 )])

# Load resnet152 model
resnet152 = models.resnet152(pretrained=True)
print(resnet152)
resnet152.eval()

# Load labels
# https://raw.githubusercontent.com/Lasagne/Recipes/master/examples/resnet50/imagenet_classes.txt
with open('imagenet_classes.txt') as f:
    classes = [line.strip() for line in f.readlines()]


img_folder = sys.argv[1]
labels_matrix = []

# convert any .png to ,jpg
png_files = glob.glob(img_folder + '*.png')
for png in png_files:
    try:
        im = Image.open(png)
        im = im.convert("RGB")
        im.save(png.replace('.png', '.jpg'))
    except:
        print(png)
        continue



for img in glob.glob(img_folder + '*.jpg'):
    img_name = img
    try: 
        img = Image.open(img)
    except:
        print(img)
        continue
    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)
    # inference
    out = resnet152(batch_t)
    print(out.shape)
    _, indices = torch.sort(out, descending=True)
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
    idx = indices[0][:1]
    labels_matrix.append([img_name, classes[idx], percentage[idx].item()])

print(labels_matrix)

# create csv
labels_df = pd.DataFrame(labels_matrix)
labels_df.columns = ['image', 'label','percentage']
print(labels_df.head())
labels_df.to_csv(img_folder + "labels.csv")