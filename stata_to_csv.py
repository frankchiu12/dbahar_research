# import pandas as pd
# import sys

# reload(sys)
# sys.setdefaultencoding('utf8')

# reader = pd.read_stata('/users/schiu4/data/schiu4/PatentsInventors.dta',chunksize=100000, columns=['patent_id', 'inventor_id', 'GMI1yr_prevexpabroad', 'pri_year', 'pri_month', 'pri_day', 'inventor_iso2', 'cpc_id'])

# df = pd.DataFrame()

# counter = 1
# for item in reader:
# 	df = df.append(item)
# 	print(counter)
# 	counter += 1

# df.to_csv('PatentsInventors.csv')