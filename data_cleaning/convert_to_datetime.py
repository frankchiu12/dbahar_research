import pandas as pd

df = pd.read_csv('/gpfs/home/schiu4/PatentInventorsDeciles.csv', dtype={'year': str, 'month': str, 'day': str, 'GMI1yr_prevexpabroad': str})

def drop_decimal(string_to_drop):
	return string_to_drop.partition('.0')[0]

df['year'] = df['year'].apply(drop_decimal)
df['month'] = df['month'].apply(drop_decimal)
df['day'] = df['day'].apply(drop_decimal)
df['GMI1yr_prevexpabroad'] = df['GMI1yr_prevexpabroad'].apply(drop_decimal)

df = df[(df.year != '0') & (df.year <= '2015')]
df = df[df.month != '0']
df = df[df.day != '0']
df['time'] = df['year'] + '/' + df['month'] + '/' + df['day']

df = df.drop(['year', 'month', 'day', 'GMI', 'GMI1yr', 'GMIalways','GMI_prevexp', 'GMI1yr_prevexp', 'GMIalways_prevexp', 'GMI_prevexpabroad', 'GMIalways_prevexpabroad', 'pt1', 'pt2', 'pt3', 'pt4', 'pt5', 'pt6', 'pt7', 'pt8', 'pt9', 'pt10', 'class', 'tot_patents', 'patentcount', 'pt_patents'], axis=1)

df.to_csv('/gpfs/home/schiu4/PatentInventorsDecilesTimed.csv', index=False)