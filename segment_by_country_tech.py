import pandas as pd
import math

df = pd.read_csv('/gpfs/home/schiu4/PatentsInventorsTimed.csv')
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
        # df of the first unique patents
        unique_patent_df = sub_sub_df.drop_duplicates(subset='patent_id', keep='first', inplace=False).reset_index(drop=True)
        unique_patent_df = unique_patent_df.sort_values(by=['time'], ignore_index=True)
        # drop if the number of unique patents is less than 10
        if len(unique_patent_df) < 10:
            continue
        # if the df of only GMIs is empty
        if len(sub_sub_df[sub_sub_df.GMI1yr_prevexpabroad == 1]) == 0:
            country_list.append(country)
            tech_list.append(tech)
            continue
        # first patent with GMI
        first_GMI_patent = sub_sub_df[sub_sub_df.GMI1yr_prevexpabroad == 1].iloc[0]['patent_id']
        # index of first_GMI_patent in unique_patent_df
        index = int(unique_patent_df.index[unique_patent_df.patent_id == first_GMI_patent][0])
        # calculating the decile
        decile = math.ceil((index/len(unique_patent_df)) * 10)
        if decile == 0:
            decile = 1
        # rewrite to separate df to do sanity check
        unique_patent_df['first_GMI_patent'] = first_GMI_patent
        unique_patent_df['decile'] = decile
        unique_patent_df.to_csv('/gpfs/home/schiu4/decile_check/' + country + '-' + tech + '.csv')
        # patents in the decile
        patents_to_consider = unique_patent_df.head(math.ceil(decile/10 * len(unique_patent_df))).patent_id.unique()
        cut_df = sub_sub_df[~sub_sub_df.patent_id.isin(patents_to_consider)].reset_index()
        cut_df['decile'] = decile
        if len(cut_df.index) == 0:
            continue
        cut_df.to_csv('/gpfs/home/schiu4/segmented_data_tech/' + country + '-' + tech + '.csv')

no_GMI_df['country'] = country_list
no_GMI_df['tech'] = tech_list
no_GMI_df.to_csv('/gpfs/home/schiu4/no_GMI_tech.csv')