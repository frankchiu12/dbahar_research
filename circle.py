import math
import pandas as pd
import networkx as nx
import nxviz as nv
import matplotlib.pyplot as plt

df = pd.read_csv('data/CircularPlotTop5020152019.csv')

g = nx.DiGraph()

for _, row in df.iterrows():
    g.add_node(row['prev_iso2'], group=_)
    if not math.isnan(row['movedAT']):
        g.add_edge(row['prev_iso2'], 'AT', weight=row['movedAT'])
    if not math.isnan(row['movedAU']):
        g.add_edge(row['prev_iso2'], 'AU', weight=row['movedAU'])
    if not math.isnan(row['movedCA']):
        g.add_edge(row['prev_iso2'], 'CA', weight=row['movedCA'])
    if not math.isnan(row['movedCH']):
        g.add_edge(row['prev_iso2'], 'CH', weight=row['movedCH'])
    if not math.isnan(row['movedCN']):
        g.add_edge(row['prev_iso2'], 'CN', weight=row['movedCN'])
    if not math.isnan(row['movedDE']):
        g.add_edge(row['prev_iso2'], 'DE', weight=row['movedDE'])
    if not math.isnan(row['movedFR']):
        g.add_edge(row['prev_iso2'], 'FR', weight=row['movedFR'])
    if not math.isnan(row['movedGB']):
        g.add_edge(row['prev_iso2'], 'GB', weight=row['movedGB'])
    if not math.isnan(row['movedHK']):
        g.add_edge(row['prev_iso2'], 'HK', weight=row['movedHK'])
    if not math.isnan(row['movedIE']):
        g.add_edge(row['prev_iso2'], 'IE', weight=row['movedIE'])
    if not math.isnan(row['movedIL']):
        g.add_edge(row['prev_iso2'], 'IL', weight=row['movedIL'])
    if not math.isnan(row['movedIN']):
        g.add_edge(row['prev_iso2'], 'IN', weight=row['movedIN'])
    if not math.isnan(row['movedJP']):
        g.add_edge(row['prev_iso2'], 'JP', weight=row['movedJP'])
    if not math.isnan(row['movedKR']):
        g.add_edge(row['prev_iso2'], 'KR', weight=row['movedKR'])
    if not math.isnan(row['movedNL']):
        g.add_edge(row['prev_iso2'], 'AT', weight=row['movedAT'])
    if not math.isnan(row['movedSE']):
        g.add_edge(row['prev_iso2'], 'SE', weight=row['movedSE'])
    if not math.isnan(row['movedSG']):
        g.add_edge(row['prev_iso2'], 'SG', weight=row['movedSG'])
    if not math.isnan(row['movedTW']):
        g.add_edge(row['prev_iso2'], 'TW', weight=row['movedTW'])
    if not math.isnan(row['movedUS']):
        g.add_edge(row['prev_iso2'], 'US', weight=row['movedUS'])

fig = nv.circos(
    g,
    node_color_by="group",
    edge_color_by="source_node_color",
    edge_alpha_by="weight"
)
plt.show()