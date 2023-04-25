import pandas as pd

df = pd.read_csv('/users/schiu4/data/schiu4/PatentsInventors.csv').dropna()
df.to_csv('/gpfs/home/schiu4/PatentsInventorsDroppedNAN.csv')