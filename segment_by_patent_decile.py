import pandas as pd
import math

df = pd.read_csv('/gpfs/home/schiu4/PatentInventorsDecilesTimed.csv')
no_GMI_df = pd.DataFrame()
country_list = []
tech_list = []

# looping through country and technology
for country in df.inventor_iso2.unique():
    sub_df = df[df.inventor_iso2 == country]
    for tech in sub_df.cpc_id.unique():
        sub_sub_df = sub_df[sub_df.cpc_id == tech]
        # sort
        sub_sub_df['time'] = pd.to_datetime(sub_sub_df['time'])
        sub_sub_df = sub_sub_df.sort_values(by=['time'], ignore_index=True)
        # if the df of only GMIs is empty
        if len(sub_sub_df[sub_sub_df.GMI1yr_prevexpabroad == 1]) == 0:
            country_list.append(country)
            tech_list.append(tech)
            continue
        # first patent with GMI
        decile = sub_sub_df[sub_sub_df.GMI1yr_prevexpabroad == 1].iloc[0]['pt_patents_10']
        patents_to_consider = sub_sub_df[sub_sub_df.pt_patents_10 == decile].patent_id.unique()
        cut_df = sub_sub_df[sub_sub_df.patent_id.isin(patents_to_consider)].reset_index()
        cut_df['decile'] = decile
        if len(cut_df.index) == 0:
            continue
        cut_df = cut_df.drop(['index'], axis=1)
        cut_df.to_csv('/gpfs/home/schiu4/segmented_data_patent_decile/' + country + '-' + tech + '.csv')

no_GMI_df['country'] = country_list
no_GMI_df['tech'] = tech_list
no_GMI_df.to_csv('/gpfs/home/schiu4/no_GMI_patent_decile.csv')