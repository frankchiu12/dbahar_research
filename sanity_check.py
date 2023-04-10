import pandas as pd

df_1 = pd.read_csv('data/CumulativeDataPatent.csv')
df_2 = pd.read_csv('data/Tech_class_decile 1st GMI.csv', usecols=['country', 'technology', 'decile_1stGMI_Sara'])

merged_df = pd.merge(df_1, df_2, on=['country', 'technology'])
merged_df = merged_df.drop(['Unnamed: 0'], axis=1)
merged_df.to_csv('data/sanity_check.csv')