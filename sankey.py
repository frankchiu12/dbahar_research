import pandas as pd

df = pd.read_csv('data/Rank_data.csv')
dictionary = {}
to_print_list = []

for i, row in df.iterrows():
    pair = row['pair']
    source = pair.partition('-')[0]
    destination = pair.partition('-')[2]
    tot_GMIs = row['totGMIs']
    if source not in dictionary:
        dictionary[source] = {}
    if destination not in dictionary[source]:
        dictionary[source][destination] = tot_GMIs
    else:
        dictionary[source][destination] += tot_GMIs

for key, value in dictionary.items():
    for sub_key, sub_value in dictionary[key].items():
        to_print_list.append([key, sub_key, sub_value])

print(to_print_list)