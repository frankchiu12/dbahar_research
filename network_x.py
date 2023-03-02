import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

csv_url = 'CN-B23K.csv'
country_tech_url = csv_url.partition('.')[0]
country = csv_url.partition('-')[0]
tech = csv_url.partition('-')[2].partition('.')[0]

def network_centrality_calculation(local):
    read_df = pd.read_csv(csv_url)
    data_df = pd.DataFrame()

    patent_to_inventor = {}
    inventor_to_patent = {}
    inventor_to_partner = {}
    inventor_to_indicator = {}

    global_partner_list = []
    partner_count_list = []
    GMI_indicator_list = []
    color_list = []
    deg_centrality_list = []
    close_centrality_list = []
    bet_centrality_list = []
    pr_list = []

    for _, row in read_df.iterrows():
        patent = row['patent_id']
        inventor = row['inventor_id']
        GMI_indicator = row['GMI1yr_prevexpabroad']

        if patent not in patent_to_inventor:
            patent_to_inventor[patent] = [inventor]
        else:
            patent_to_inventor[patent].append(inventor)

        if inventor not in inventor_to_patent:
            inventor_to_patent[inventor] = [patent]
        else:
            inventor_to_patent[inventor].append(patent)

        if inventor not in inventor_to_indicator:
            inventor_to_indicator[inventor] = GMI_indicator

    for inventor, patent in inventor_to_patent.items():
        if inventor not in inventor_to_partner:
            inventor_to_partner[inventor] = []
            for pat in patent:
                partner_list = patent_to_inventor[pat]
                partner_list = [x for x in partner_list if x != inventor]
                inventor_to_partner[inventor] += partner_list

    for inventor, partner in inventor_to_partner.items():
        unique_partner_list = list(set(partner))
        if local:
            inventor_to_partner[inventor] = [x for x in unique_partner_list if inventor_to_indicator[x] != 1]
        else:
            inventor_to_partner[inventor] = unique_partner_list

        global_partner_list.append(inventor_to_partner[inventor])
        partner_count_list.append(len(inventor_to_partner[inventor]))
        GMI_indicator_list.append(inventor_to_indicator[inventor])

    data_df['inventor_id'] = inventor_to_patent.keys()
    data_df['partner_list'] = global_partner_list
    data_df['partner_count'] = partner_count_list

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
    nx.draw(g, pos=nx.spiral_layout(g), node_size=100, node_color=color_list, edge_color='green', linewidths=10)
    if local:
        plt.savefig('graph_local.png')
    else:
        plt.savefig('graph.png')

    deg_centrality = nx.degree_centrality(g)
    close_centrality = nx.closeness_centrality(g)
    bet_centrality = nx.betweenness_centrality(g, normalized=True, endpoints=False)
    pr = nx.pagerank(g, alpha=0.8)

    for inventor in data_df['inventor_id']:
        deg_centrality_list.append(deg_centrality[inventor])
        close_centrality_list.append(close_centrality[inventor])
        bet_centrality_list.append(bet_centrality[inventor])
        pr_list.append(pr[inventor])

    data_df['deg_centrality'] = deg_centrality_list
    data_df['close_centrality'] = close_centrality_list
    data_df['bet_centrality'] = bet_centrality_list
    data_df['page_rank'] = pr_list
    data_df['GMI1yr_prevexpabroad'] = GMI_indicator_list

    if local:
        data_df.to_csv(country_tech_url + '_network_local.csv', index=False)
    else:
        data_df.to_csv(country_tech_url + '_network.csv', index=False)

    only_GMI_df = data_df.copy()
    only_GMI_df = only_GMI_df[only_GMI_df.GMI1yr_prevexpabroad == 1]
    partner_count_avg = only_GMI_df['partner_count'].sum() / len(only_GMI_df)
    deg_centrality_avg = only_GMI_df['deg_centrality'].sum() / len(only_GMI_df)
    close_centrality_avg = only_GMI_df['close_centrality'].sum() / len(only_GMI_df)
    bet_centrality_avg = only_GMI_df['bet_centrality'].sum() / len(only_GMI_df)
    page_rank_avg = only_GMI_df['page_rank'].sum() / len(only_GMI_df)

    return [partner_count_avg, deg_centrality_avg, close_centrality_avg, bet_centrality_avg, page_rank_avg, len(only_GMI_df), len(data_df)]

local_list = network_centrality_calculation(True)
non_local_list = network_centrality_calculation(False)

avg_data_df = pd.DataFrame()
avg_data_df['country'] = [country]
avg_data_df['technology'] = [tech]
avg_data_df['partner_count_avg'] = [non_local_list[0]]
avg_data_df['deg_centrality_avg'] =[non_local_list[1]]
avg_data_df['close_centrality_avg'] = [non_local_list[2]]
avg_data_df['bet_centrality_avg'] = [non_local_list[3]]
avg_data_df['page_rank_avg'] = [non_local_list[4]]
avg_data_df['local_partner_count_avg'] = [local_list[0]]
avg_data_df['local_deg_centrality_avg'] = [local_list[1]]
avg_data_df['local_close_centrality_avg'] = [local_list[2]]
avg_data_df['local_bet_centrality_avg'] = [local_list[3]]
avg_data_df['local_page_rank_avg'] = [local_list[4]]
avg_data_df['GMI_count'] = [non_local_list[5]]
avg_data_df['count'] = [non_local_list[6]]

avg_data_df.to_csv(country_tech_url + '_network_average.csv', index=False)