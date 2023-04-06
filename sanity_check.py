import pandas as pd

df = pd.read_csv('data/sanity_check.csv')
print(df.index[df['patent_id'] == 5448317].tolist())
print(df['patent_id'].nunique())
print(len(df))