import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

csv_url = 'US-G06F.csv'
country_tech_url = csv_url.partition('.')[0]
df = pd.read_csv(csv_url)
new_df = pd.DataFrame()
join_df = pd.read_csv(csv_url, usecols=['inventor_id', 'GMI1yr_prevexpabroad'])

patent_to_inventor = {}
inventor_to_patent = {}
inventor_to_partner = {}

inventor_id_list = []
global_partner_list = []
partner_id_count_list = []
deg_centrality_list = []
close_centrality_list = []
bet_centrality_list = []
pr_list = []

for index, row in df.iterrows():
    patent_id = row['patent_id']
    inventor_id = row['inventor_id']

    if patent_id not in patent_to_inventor:
        patent_to_inventor[patent_id] = [inventor_id]
    else:
        patent_to_inventor[patent_id].append(inventor_id)
    
    if inventor_id not in inventor_to_patent:
        inventor_to_patent[inventor_id] = [patent_id]
    else:
        inventor_to_patent[inventor_id].append(patent_id)

for inventor, patent in inventor_to_patent.items():
    inventor_id_list.append(inventor)
    if inventor not in inventor_to_partner:
        inventor_to_partner[inventor] = []
        for pat in patent:
            partner_list = patent_to_inventor[pat]
            partner_list = [x for x in partner_list if x != inventor]
            inventor_to_partner[inventor] += partner_list
        global_partner_list.append(inventor_to_partner[inventor])
        partner_id_count_list.append(len(inventor_to_partner[inventor]))

new_df['inventor_id'] = inventor_id_list
new_df['partner_list'] = global_partner_list
new_df['partner_count'] = partner_id_count_list

g = nx.DiGraph()

for inventor, partner in inventor_to_partner.items():
    g.add_node(inventor)
    for part in partner:
        g.add_node(part)
        g.add_edge(inventor, part)

plt.figure(figsize=(30,25))
nx.draw(g, pos=nx.spiral_layout(g), node_size=100, edge_color=['red', 'green'], linewidths=10)
plt.savefig('graph.png')

# random or spiral

deg_centrality = nx.degree_centrality(g)
close_centrality = nx.closeness_centrality(g)
bet_centrality = nx.betweenness_centrality(g, normalized = True, endpoints = False)
pr = nx.pagerank(g, alpha = 0.8)

for inventor_id in new_df['inventor_id']:
    deg_centrality_list.append(deg_centrality[inventor_id])
    close_centrality_list.append(close_centrality[inventor_id])
    bet_centrality_list.append(bet_centrality[inventor_id])
    pr_list.append(pr[inventor_id])

new_df['deg_centrality'] = deg_centrality_list
new_df['close_centrality'] = close_centrality_list
new_df['bet_centrality'] = bet_centrality_list
new_df['page_rank'] = pr_list
new_df = new_df.join(join_df.set_index('inventor_id'), on = 'inventor_id')

new_df.to_csv(country_tech_url + '_network.csv', index=False)