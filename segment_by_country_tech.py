import pandas as pd
import sys

# reload(sys)
sys.setdefaultencoding('utf8')

df = pd.read_csv('/gpfs/home/schiu4/PatentsInventorsTimed.csv')

for country in df.inventor_iso2.unique():
    sub_df = df[df.inventor_iso2 == country]
    for technology in sub_df.cpc_id.unique():
        sub_sub_df = sub_df[sub_df.cpc_id == technology]
        cut_length = sub_sub_df.shape[0]/10
        decile = 0
        for i in range(10):
            cut_df = sub_sub_df.head(cut_length * (i + 1))
            if 1 in cut_df['GMI1yr_prevexpabroad'].values:
                decile = i + 1
                break
        sub_sub_df = sub_sub_df.sort_values(by=['time'])
        sub_sub_df = sub_sub_df.head(cut_length)
        sub_sub_df['decile'] = decile
        sub_sub_df.to_csv('/gpfs/home/schiu4/segmented_data/' + country + '-' + technology + '.csv')
        # sub_sub_df.to_csv('/gpfs/home/schiu4/segmented_data_test/' + country + '-' + technology + '.csv')