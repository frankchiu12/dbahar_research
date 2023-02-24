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
inventor_to_indicator = {}

inventor_list = []
global_partner_list = []
partner_count_list = []
color_list = []
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
    
    if inventor_id not in inventor_to_indicator:
        inventor_to_indicator[inventor_id] = row['GMI1yr_prevexpabroad']

for inventor, patent in inventor_to_patent.items():
    if inventor not in inventor_to_partner:
        inventor_to_partner[inventor] = []
        for pat in patent:
            partner_list = patent_to_inventor[pat]
            partner_list = [x for x in partner_list if x != inventor]
            inventor_to_partner[inventor] += partner_list

for inventor, partner in inventor_to_partner.items():
    inventor_to_partner[inventor] = list(set(partner))
    global_partner_list.append(inventor_to_partner[inventor])
    partner_count_list.append(len(inventor_to_partner[inventor]))

inventor_list = inventor_to_patent.keys()

new_df['inventor_id'] = inventor_list
new_df['partner_list'] = global_partner_list
new_df['partner_count'] = partner_count_list

g = nx.Graph()

for inventor, partner in inventor_to_partner.items():
    g.add_node(inventor)
    for part in partner:
        g.add_node(part)
        g.add_edge(inventor, part)

for node in g:
    if inventor_to_indicator[node] == 1:
        color_list.append('red')
    else:
        color_list.append('blue')

plt.figure(figsize=(30,25))
nx.draw(g, pos=nx.spiral_layout(g), node_size=100, node_color=color_list, edge_color=['green'], linewidths=10)
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
join_df = join_df.drop_duplicates()
new_df = new_df.join(join_df.set_index('inventor_id'), on = 'inventor_id')

new_df.to_csv(country_tech_url + '_network.csv', index=False)

# no GMIs in partner list, centrality only for GMIs, with non-GMIs as 0
# one big csv of by country and by tech centrality