import os

path = '/gpfs/home/schiu4/segmented_data/'

r = []
for root, dirs, files in os.walk(path):
    for name in files:
        r.append(os.path.join(root, name))