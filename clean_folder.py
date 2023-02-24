import os
import shutil

path = '/gpfs/home/schiu4/segmented_data/'

for x in os.listdir(path):
    file = os.path.join(path, x)
    if not os.path.isdir(file):
        folder_name = os.path.join(path, x.partition('-')[0])
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        shutil.move(file, folder_name)