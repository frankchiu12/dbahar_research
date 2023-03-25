import pandas as pd

def check(step):
    if step == 1:
        df = pd.read_csv('/gpfs/home/schiu4/PatentsInventorsTimed.csv')
        df = df[df.inventor_iso2 == 'IN']
        df = df[df.cpc_id == 'G06N']
        df.to_csv('/gpfs/home/schiu4/sanity_check.csv')
    else:
        df = pd.read_csv('data/sanity_check.csv')
        df = df.sort_values(by=['time'])
        df.reindex(list(range(0, len(df))))
        df.to_csv('data/sanity_check.csv')
        print(df.index[df['GMI1yr_prevexpabroad'] == 1].tolist())
        print(len(df))

check(2)