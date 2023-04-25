import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data/Rank_data.csv')
pair_list = ['TW-CN', 'US-TW', 'US-JP', 'US-DE', 'US-IN', 'US-GB', 'US-KR', 'US-CA', 'US-CN']
year_list = [1990, 1995, 2000, 2005, 2010, 2015]
res = {}
data_list = []

df = df[df.pair.isin(pair_list)].reset_index()
df = df.sort_values(by=['fiveyear'], ignore_index=True)

for index, row in df.iterrows():
    pair = row['pair']
    year = row['fiveyear']
    rank = row['rank']
    if pair not in res:
        res[pair] = {}
        res[pair]['Name'] = [pair for i in range(5)]
        res[pair]['Year'] = year_list
        if rank >= 10:
            rank = 10
        res[pair]['Rank'] = [rank]
    else:
        if rank >= 10:
            rank = 10
        res[pair]['Rank'] += [rank]

for key, value in res.items():
    data_list.append(value)

fig, ax = plt.subplots()
plt.rcParams["figure.figsize"] = (12,6)

for element in data_list:
    ax.plot(element['Year'], element['Rank'], 'o-', markerfacecolor='white', linewidth=2)
    ax.annotate(element["Name"][0], xy=(2015, element["Rank"][5]), xytext=(2016, element["Rank"][5]), va="center")

plt.gca().invert_yaxis()
plt.yticks(np.arange(1, 10, 1))
plt.ylim(9.5)

counter = 0
for spine in ax.spines.values():
    if counter == 1:
        spine.set_visible(False)
    counter += 1

plt.show()