import pandas as pd

def check(step):
    if step == 1:
        df = pd.read_csv('/gpfs/home/schiu4/PatentsInventorsTimed.csv')
        df = df[df.inventor_iso2 == 'US']
        df = df[df.cpc_id == 'F41A']
        df.to_csv('/gpfs/home/schiu4/sanity_check.csv')
    if step == 2:
        df = pd.read_csv('data/sanity_check.csv')
        df = df.sort_values(by=['time'], ignore_index=True)
        df.to_csv('data/sanity_check.csv', columns=['patent_id', 'inventor_id', 'GMI1yr_prevexpabroad','inventor_iso2', 'cpc_id', 'location_id', 'assigneeid', 'time'])
        print(df.index[df['GMI1yr_prevexpabroad'] == 1].tolist())
        print(len(df))

check(2)