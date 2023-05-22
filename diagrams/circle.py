# this script uses pycirclize to make circle_50.png

import pandas as pd
from pycirclize import Circos
from pycirclize.parser import Matrix
import math

data_df = pd.read_csv('data/CircularPlotTop5020152019.csv')
matrix_df = pd.DataFrame()

source_target_value_list = []
source_list = []
target_list = []
value_list = []

# create lists of tuples from the source to the target
for _, row in data_df.iterrows():
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

# create separate lists of the sources, targets, and values (how many immigrants)
for i, source_target_value in enumerate(source_target_value_list):
    source_list.append(source_target_value[0])
    target_list.append(source_target_value[1])
    value_list.append(source_target_value[2])

# make a df of the lists
matrix_df['source'] = source_list
matrix_df['target'] = target_list
matrix_df['value'] = value_list

# https://moshi4.github.io/pyCirclize/chord_diagram/
matrix = Matrix.parse_fromto_table(matrix_df)

circos = Circos.initialize_from_matrix(
    matrix,
    space=3,
    cmap='tab20',
    ticks_interval=250,
    label_kws=dict(size=12, r=110),
    link_kws=dict(direction=1, ec='black', lw=0.5),
)
fig = circos.plotfig()
fig.savefig('diagrams/circle_50.png')