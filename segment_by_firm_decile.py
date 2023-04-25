import pandas as pd

df = pd.read_csv('/gpfs/home/schiu4/PatentInventorsDecilesTimed.csv')
no_GMI_df = pd.DataFrame()
country_list = []
tech_list = []

for country in df.inventor_iso2.unique():
    sub_df = df[df.inventor_iso2 == country]
    for tech in sub_df.cpc_id.unique():
        sub_sub_df = sub_df[sub_df.cpc_id == tech]
        sub_sub_df['time'] = pd.to_datetime(sub_sub_df['time'])
        sub_sub_df = sub_sub_df.sort_values(by=['time'], ignore_index=True)
        if len(sub_sub_df[sub_sub_df.GMI1yr_prevexpabroad == 1]) == 0:
            country_list.append(country)
            tech_list.append(tech)
            continue
        decile = sub_sub_df[sub_sub_df.GMI1yr_prevexpabroad == 1].iloc[0]['pt_patents_10']
        firms_to_consider = sub_sub_df[sub_sub_df.pt_patents_10 == decile].assigneeid.unique()
        cut_df = sub_sub_df[(sub_sub_df.assigneeid.isin(firms_to_consider)) & (sub_sub_df.pt_patents_10 == decile)].reset_index()
        cut_df['decile'] = decile
        if len(cut_df.index) == 0:
            continue
        cut_df = cut_df.dropna()
        cut_df = cut_df.drop(['index'], axis=1)
        cut_df.to_csv('/gpfs/home/schiu4/segmented_data_firm_decile/' + country + '-' + tech + '.csv')

no_GMI_df['country'] = country_list
no_GMI_df['tech'] = tech_list
no_GMI_df.to_csv('/gpfs/home/schiu4/no_GMI_firm_decile.csv')