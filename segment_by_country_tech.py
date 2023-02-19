# import pandas as pd
# import sys
# from datetime import datetime

# reload(sys)
# sys.setdefaultencoding('utf8')

# df = pd.read_csv('/users/schiu4/data/schiu4/PatentsInventorsTimed.csv')

# for country in df.inventor_iso2.unique():
#     sub_df = df[df.inventor_iso2 == country]
#     for technology in sub_df.cpc_id.unique():
#         sub_sub_df = sub_df[sub_df.cpc_id == technology]
#         cut_length = sub_sub_df.shape[0]/10
#         sub_sub_df = sub_sub_df.sort_values(by=['pri_time'])
#         sub_sub_df = sub_sub_df.head(cut_length)
#         sub_sub_df.to_csv('/users/schiu4/data/schiu4/segmented_data/' + country + '-' + technology + '.csv')