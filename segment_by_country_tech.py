import pandas as pd
import math

df = pd.read_csv('/gpfs/home/schiu4/PatentsInventorsTimed.csv')
no_GMI_df = pd.DataFrame()
country_list = []
tech_list = []

for country in df.inventor_iso2.unique():
    sub_df = df[df.inventor_iso2 == country]
    for tech in sub_df.cpc_id.unique():
        sub_sub_df = sub_df[sub_df.cpc_id == tech]
        sub_sub_df = sub_sub_df.sort_values(by=['time'], ignore_index=True)
        unique_patent_df = sub_sub_df.drop_duplicates(subset='patent_id', keep='first', inplace=False)
        if len(unique_patent_df) < 10:
            continue
        if len(sub_sub_df[sub_sub_df.GMI1yr_prevexpabroad == 1]) == 0:
            country_list.append(country)
            tech_list.append(tech)
            continue
        first_patent = sub_sub_df[sub_sub_df.GMI1yr_prevexpabroad == 1].iloc[0]['patent_id']
        index = int(df.index[df.patent_id == first_patent][0])
        decile = math.ceil((index/len(unique_patent_df)) * 10)
        patents_to_consider = df.head(math.ceil(decile/10 * len(unique_patent_df))).patent_id.unique()
        patent_list = sub_sub_df.patent_id.to_list()
        index = 0
        for i, patent in enumerate(patent_list):
            if patent in patents_to_consider:
                index = i
        cut_df = sub_sub_df.head(index + 1)
        if len(cut_df.index) == 0:
            continue
        cut_df.to_csv('/gpfs/home/schiu4/segmented_data_tech/' + country + '-' + tech + '.csv')

no_GMI_df['country'] = country_list
no_GMI_df['tech'] = tech_list
no_GMI_df.to_csv('/gpfs/home/schiu4/no_GMI_tech.csv')