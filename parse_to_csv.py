# import pandas as pd
# import sys

# reload(sys)
# sys.setdefaultencoding('utf8')

# reader = pd.read_stata('/users/schiu4/data/schiu4/PatentsInventors.dta',chunksize=100000)

# df = pd.DataFrame()

# counter = 1
# for item in reader:
# 	df = df.append(item)
# 	if counter == 1:
# 		break

# df.to_csv("PatentsInventors.csv")