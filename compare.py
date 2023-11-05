import pandas as pd

df_1 = pd.read_stata('CEO Profile_Personality.dta', columns=['agree_m5u', 'consc_m5u', 'extra_m5u', 'neuro_m5u', 'openn_m5u', 'DirectorName'])
df_2 = pd.read_csv('personality_step_48.csv')

df_1.dropna(inplace=True)
df_1['DirectorName'] = df_1['DirectorName'].str.lower()
df_1['DirectorName'] = df_1['DirectorName'].str.replace(' ', '_')
df_1.rename(columns={'DirectorName': 'CEO'}, inplace=True)

df_3 = pd.merge(df_1, df_2, on='CEO')
df_3.drop('Unnamed: 0', axis=1, inplace=True)
desired_order = ['CEO', 'openn_m5u', 'consc_m5u', 'extra_m5u', 'agree_m5u', 'neuro_m5u', 'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'emotional_stability']
df_3 = df_3[desired_order]

df_3.to_csv('comparison.csv')