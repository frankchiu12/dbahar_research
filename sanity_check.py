import pandas as pd

df = pd.read_csv('test.csv')
print(df.index[df['GMI1yr_prevexpabroad'] == 1].tolist())
print(len(df))