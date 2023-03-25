import pandas as pd
import math

df = pd.read_csv('/gpfs/home/schiu4/PatentsInventorsTimed.csv')
no_GMI_df = pd.DataFrame()
country_list = []
firm_list = []

for country in df.inventor_iso2.unique():
    sub_df = df[df.inventor_iso2 == country]
    for firm in sub_df.assigneeid.unique():
        sub_sub_df = sub_df[sub_df.assigneeid == firm]
        sub_sub_df = sub_sub_df.sort_values(by=['time'])
        cut_length = sub_sub_df.shape[0] / 10
        decile = 0
        for i in range(10):
            cut_df = sub_sub_df.head(int(math.floor(cut_length * (i + 1))))
            if 1 in cut_df['GMI1yr_prevexpabroad'].values:
                decile = i + 1
                break
        cut_df['decile'] = decile
        if len(cut_df.index) == 0:
            continue
        if decile == 0:
            country_list.append(country)
            firm_list.append(firm)
            continue
        cut_df.to_csv('/gpfs/home/schiu4/segmented_data_firm/' + country + '-' + str(int(firm)) + '.csv')

no_GMI_df['country'] = country_list
no_GMI_df['firm'] = firm_list
no_GMI_df.to_csv('/gpfs/home/schiu4/no_GMI_firm.csv')