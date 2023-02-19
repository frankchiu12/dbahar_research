import pandas as pd
import sys
from datetime import datetime

# reload(sys)
sys.setdefaultencoding('utf8')

df = pd.read_csv('/users/schiu4/data/schiu4/PatentsInventorsDroppedNAN.csv', dtype={'pri_year': str, 'pri_month': str, 'pri_day': str, 'GMI1yr_prevexpabroad': str})

def drop_decimal(string_to_drop):
	return string_to_drop.partition('.0')[0]

df['pri_year'] = df['pri_year'].apply(drop_decimal)
df['pri_month'] = df['pri_month'].apply(drop_decimal)
df['pri_day'] = df['pri_day'].apply(drop_decimal)
df['GMI1yr_prevexpabroad'] = df['GMI1yr_prevexpabroad'].apply(drop_decimal)

df = df[(df.pri_year != '0') & (df.pri_year != '2973') & (df.pri_year != '9174') & (df.pri_year != '2979') & (df.pri_year != '2981') & (df.pri_year != '9180')]
df = df[df.pri_month != '0']
df = df[df.pri_day != '0']

df['pri_time'] = df['pri_year'] + '/' + df['pri_month'] + '/' + df['pri_day']

pd.to_datetime(df['pri_time'], format='%Y/%m/%d')

df = df.drop(['pri_year', 'pri_month', 'pri_day', 'Unnamed: 0.1', 'Unnamed: 0'], axis=1)

df.to_csv('PatentsInventorsTimed.csv', index=False)