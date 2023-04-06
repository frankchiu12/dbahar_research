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
        sub_sub_df['time'] = pd.to_datetime(sub_sub_df['time'])
        sub_sub_df = sub_sub_df.sort_values(by=['time'], ignore_index=True)
        unique_firm_df = sub_sub_df.drop_duplicates(subset='assigneeid', keep='first', inplace=False).reset_index(drop=True)
        unique_firm_df = unique_firm_df.sort_values(by=['time'], ignore_index=True)
        if len(unique_firm_df) < 10:
            continue
        if len(sub_sub_df[sub_sub_df.GMI1yr_prevexpabroad == 1]) == 0:
            country_list.append(country)
            tech_list.append(tech)
            continue
        first_GMI_firm = sub_sub_df[sub_sub_df.GMI1yr_prevexpabroad == 1].iloc[0]['assigneeid']
        index = int(unique_firm_df.index[unique_firm_df.assigneeid == first_GMI_firm][0])
        decile = math.ceil((index/len(unique_firm_df)) * 10)
        if decile == 0:
            decile = 1
        firms_to_consider = unique_firm_df.head(math.ceil(decile/10 * len(unique_firm_df))).assigneeid.unique()
        cut_df = sub_sub_df[~sub_sub_df.assigneeid.isin(firms_to_consider)].reset_index()
        cut_df['decile'] = decile
        if len(cut_df.index) == 0:
            continue
        cut_df.to_csv('/gpfs/home/schiu4/segmented_data_firm/' + country + '-' + tech + '.csv')

no_GMI_df['country'] = country_list
no_GMI_df['tech'] = tech_list
no_GMI_df.to_csv('/gpfs/home/schiu4/no_GMI_firm.csv')