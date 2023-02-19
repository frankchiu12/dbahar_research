import pandas as pd
import sys

# reload(sys)
sys.setdefaultencoding('utf8')

df = pd.read_csv('/users/schiu4/data/schiu4/PatentsInventors.csv').dropna()

df.to_csv('PatentsInventorsDroppedNAN.csv')