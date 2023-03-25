import pandas as pd
import holoviews as hv
from holoviews import opts, dim
import math
from bokeh.plotting import show

hv.extension('bokeh')

df = pd.read_csv('data/CircularPlotTop5020152019.csv')
new_df = pd.DataFrame()

source_target_value_list = []
source_list = []
target_list = []
value_list = []

for _, row in df.iterrows():
    if not math.isnan(row['movedAT']):
        source_target_value_list.append((row['prev_iso2'], 'AT', row['movedAT']))
    if not math.isnan(row['movedAU']):
        source_target_value_list.append((row['prev_iso2'], 'AU', row['movedAU']))
    if not math.isnan(row['movedCA']):
        source_target_value_list.append((row['prev_iso2'], 'CA', row['movedCA']))
    if not math.isnan(row['movedCH']):
        source_target_value_list.append((row['prev_iso2'], 'CH', row['movedCH']))
    if not math.isnan(row['movedCN']):
        source_target_value_list.append((row['prev_iso2'], 'CN', row['movedCN']))
    if not math.isnan(row['movedDE']):
        source_target_value_list.append((row['prev_iso2'], 'DE', row['movedDE']))
    if not math.isnan(row['movedFR']):
        source_target_value_list.append((row['prev_iso2'], 'FR', row['movedFR']))
    if not math.isnan(row['movedGB']):
        source_target_value_list.append((row['prev_iso2'], 'GB', row['movedGB']))
    if not math.isnan(row['movedHK']):
        source_target_value_list.append((row['prev_iso2'], 'HK', row['movedHK']))
    if not math.isnan(row['movedIE']):
        source_target_value_list.append((row['prev_iso2'], 'IE', row['movedIE']))
    if not math.isnan(row['movedIL']):
        source_target_value_list.append((row['prev_iso2'], 'IL', row['movedIL']))
    if not math.isnan(row['movedIN']):
        source_target_value_list.append((row['prev_iso2'], 'IN', row['movedIN']))
    if not math.isnan(row['movedJP']):
        source_target_value_list.append((row['prev_iso2'], 'JP', row['movedJP']))
    if not math.isnan(row['movedKR']):
        source_target_value_list.append((row['prev_iso2'], 'KR', row['movedKR']))
    if not math.isnan(row['movedNL']):
        source_target_value_list.append((row['prev_iso2'], 'AT', row['movedAT']))
    if not math.isnan(row['movedSE']):
        source_target_value_list.append((row['prev_iso2'], 'SE', row['movedSE']))
    if not math.isnan(row['movedSG']):
        source_target_value_list.append((row['prev_iso2'], 'SG', row['movedSG']))
    if not math.isnan(row['movedTW']):
        source_target_value_list.append((row['prev_iso2'], 'TW', row['movedTW']))
    if not math.isnan(row['movedUS']):
        source_target_value_list.append((row['prev_iso2'], 'US', row['movedUS']))

for i, source_target_value in enumerate(source_target_value_list):
    source_list.append(source_target_value[0])
    target_list.append(source_target_value[1])
    value_list.append(source_target_value[2])

new_df['source'] = source_list
new_df['target'] = target_list
new_df['value'] = value_list

node = pd.DataFrame()
for i, value in enumerate(new_df.source.unique()):
    _list = list(new_df[new_df['source'] == value].source.unique())
    node = pd.concat([node, pd.DataFrame({'name':_list})], ignore_index=True)

values = list(new_df.source.unique())
d = {value: i for i, value in enumerate(values)}

def str2num(s):
    return d[s]

new_df.source = new_df.source.apply(str2num)
new_df.target = new_df.target.apply(str2num)

hv.Chord(new_df)
nodes = hv.Dataset(pd.DataFrame(node), 'index')

chord = hv.Chord((new_df, nodes)).select(value=(5, None))
chord.opts(opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('target').str(), labels='name', node_color=dim('index').str()))
chord.opts(label_text_font_size='7pt', width=1000, height=1000, tools=['save', 'pan', 'wheel_zoom', 'box_zoom', 'reset'])

show(hv.render(chord))