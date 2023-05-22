# this scripts segements the data by firms in the decile we want into files of country-tech

import pandas as pd

df = pd.read_csv('/gpfs/home/schiu4/PatentInventorsDecilesTimed.csv')
no_GMI_df = pd.DataFrame()
country_list = []
tech_list = []

# loop through each country
for country in df.inventor_iso2.unique():
    sub_df = df[df.inventor_iso2 == country]
    # loop through each technology
    for tech in sub_df.cpc_id.unique():
        # make a df called sub_sub_df that has data for a given technology for a given country
        sub_sub_df = sub_df[sub_df.cpc_id == tech]
        # convert the time into datetime objects
        sub_sub_df['time'] = pd.to_datetime(sub_sub_df['time'])
        # sort sub_sub_df by time
        sub_sub_df = sub_sub_df.sort_values(by=['time'], ignore_index=True)
        # if sub_sub_df doesn't contain a GMI, we add them to lists to indicate that there is no GMI
        if len(sub_sub_df[sub_sub_df.GMI1yr_prevexpabroad == 1]) == 0:
            country_list.append(country)
            tech_list.append(tech)
            continue
        # find the decile of the first GMI appearance
        decile = sub_sub_df[sub_sub_df.GMI1yr_prevexpabroad == 1].iloc[0]['pt_patents_10']
        # find all of the firms in that decile
        firms_to_consider = sub_sub_df[sub_sub_df.pt_patents_10 == decile].assigneeid.unique()
        # make a df called cut_df that has data for firms in the decile
        cut_df = sub_sub_df[(sub_sub_df.assigneeid.isin(firms_to_consider)) & (sub_sub_df.pt_patents_10 == decile)].reset_index()
        # set the decile variable
        cut_df['decile'] = decile
        # if it is empty ignore
        if len(cut_df.index) == 0:
            continue
        cut_df = cut_df.dropna()
        cut_df = cut_df.drop(['index'], axis=1)
        cut_df.to_csv('/gpfs/home/schiu4/segmented_data_firm_decile/' + country + '-' + tech + '.csv')

# make a df called no_GMI_df that has data for countries and technologies without GMIs
no_GMI_df['country'] = country_list
no_GMI_df['tech'] = tech_list
no_GMI_df.to_csv('/gpfs/home/schiu4/no_GMI_firm_decile.csv')