# this script organizes the folder by creating folders for each country and moving relevant files into these folders

import os
import shutil

path = '/gpfs/home/schiu4/segmented_data_firm_decile/'

for x in os.listdir(path):
    file = os.path.join(path, x)
    if not os.path.isdir(file):
        folder_name = os.path.join(path, x.partition('-')[0])
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        shutil.move(file, folder_name)