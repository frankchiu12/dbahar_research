# this scripts converts a stata data file into a csv

import pandas as pd

reader = pd.read_stata('/users/schiu4/data/schiu4/PatentsInventors.dta',chunksize=1000000, columns=['patent_id', 'inventor_id', 'GMI1yr_prevexpabroad', 'year', 'month', 'day', 'inventor_iso2', 'cpc_id', 'location_id', 'assigneeid'])

df = pd.DataFrame()

counter = 1
for item in reader:
	df = df.append(item)
	print(counter)
	counter += 1

df.to_csv('/gpfs/home/schiu4/PatentsInventors.csv')