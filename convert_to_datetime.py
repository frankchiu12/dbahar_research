import pandas as pd

df = pd.read_csv('/gpfs/home/schiu4/PatentsInventorsDroppedNAN.csv', dtype={'year': str, 'month': str, 'day': str, 'GMI1yr_prevexpabroad': str})

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

pd.to_datetime(df['time'], format='%Y/%m/%d')

df = df.drop(['year', 'month', 'day', 'Unnamed: 0.1', 'Unnamed: 0'], axis=1)

df.to_csv('/gpfs/home/schiu4/PatentsInventorsTimed.csv', index=False)