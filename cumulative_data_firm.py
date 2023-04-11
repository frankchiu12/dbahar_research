import os
import pandas as pd
import networkx as nx

cumulative_df = pd.DataFrame()

path_list = []
for root, dirs, files in os.walk('/gpfs/home/schiu4/segmented_data_firm_decile/'):
    for name in files:
        path_list.append(os.path.join(root, name))

def network_centrality_calculation(csv_url, local):
    read_df = pd.read_csv(csv_url)
    data_df = pd.DataFrame()

    firm_to_inventor = {}
    inventor_to_firm = {}
    inventor_to_partner = {}
    inventor_to_indicator = {}

    global_partner_list = []
    partner_count_list = []
    GMI_indicator_list = []
    deg_centrality_list = []
    close_centrality_list = []
    bet_centrality_list = []
    pr_list = []
    decile = 0

    for i, row in read_df.iterrows():
        firm = row['assigneeid']
        inventor = row['inventor_id']
        GMI_indicator = row['GMI1yr_prevexpabroad']

        if firm not in firm_to_inventor:
            firm_to_inventor[firm] = [inventor]
        else:
            firm_to_inventor[firm].append(inventor)

        if inventor not in inventor_to_firm:
            inventor_to_firm[inventor] = [firm]
        else:
            inventor_to_firm[inventor].append(firm)

        if inventor not in inventor_to_indicator:
            inventor_to_indicator[inventor] = GMI_indicator

        if i == 0:
            decile = row['decile']

    for inventor, firm in inventor_to_firm.items():
        if inventor not in inventor_to_partner:
            inventor_to_partner[inventor] = []
            for f in firm:
                partner_list = firm_to_inventor[f]
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

    data_df['inventor_id'] = inventor_to_firm.keys()
    data_df['partner_list'] = global_partner_list
    data_df['partner_count'] = partner_count_list

    g = nx.Graph()

    for inventor, partner in inventor_to_partner.items():
        g.add_node(inventor)
        for part in partner:
            g.add_node(part)
            g.add_edge(inventor, part)

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

    only_GMI_df = data_df.copy()
    only_GMI_df = only_GMI_df[only_GMI_df.GMI1yr_prevexpabroad == 1]
    if len(only_GMI_df) > 0:
        partner_count_avg = only_GMI_df['partner_count'].sum() / len(only_GMI_df)
        deg_centrality_avg = only_GMI_df['deg_centrality'].sum() / len(only_GMI_df)
        close_centrality_avg = only_GMI_df['close_centrality'].sum() / len(only_GMI_df)
        bet_centrality_avg = only_GMI_df['bet_centrality'].sum() / len(only_GMI_df)
        page_rank_avg = only_GMI_df['page_rank'].sum() / len(only_GMI_df)
    else:
        partner_count_avg = 0
        deg_centrality_avg = 0
        close_centrality_avg = 0
        bet_centrality_avg = 0
        page_rank_avg = 0

    return [partner_count_avg, deg_centrality_avg, close_centrality_avg, bet_centrality_avg, page_rank_avg, len(only_GMI_df), len(data_df), decile]

for i, path in enumerate(path_list):
    csv_url = path
    country_firm_url = csv_url.partition('/gpfs/home/schiu4/segmented_data_firm_decile/')[2].partition('/')[2].partition('.')[0]
    country = csv_url.partition('/gpfs/home/schiu4/segmented_data_firm_decile/')[2].partition('/')[2].partition('-')[0]
    tech = csv_url.partition('/gpfs/home/schiu4/segmented_data_firm_decile/')[2].partition('/')[2].partition('-')[2].partition('.')[0]

    local_list = network_centrality_calculation(csv_url, True)
    non_local_list = network_centrality_calculation(csv_url, False)

    avg_data_df = pd.DataFrame()
    avg_data_df['country'] = [country]
    avg_data_df['tech'] = [tech]
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
    avg_data_df['decile'] = [non_local_list[7]]

    cumulative_df = cumulative_df.append(avg_data_df, ignore_index=True)

    print(i)

cumulative_df.to_csv('/gpfs/home/schiu4/CumulativeDataFirm.csv')