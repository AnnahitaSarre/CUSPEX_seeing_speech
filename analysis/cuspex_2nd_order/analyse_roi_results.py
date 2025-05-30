#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CUSPEX script computing the ROI statistical group results using the output of compute_roi_results.py
OUTPUT: Txt file containing statistical results for the Bayesian version and related boxplots
"""


#%% Import modules

import os
import sys
import numpy as np
import pingouin as pg
import pandas as pd
import seaborn as sns
from itertools import product, combinations
import matplotlib.pyplot as plt
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr


#%% Parameters to modify

task = 'loc_vid'
main_path = '/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis'
smoothing_level = '4'
subjects = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119',
            '21', '22', '23', '24', '25', '26', '27', '28', '29', '210', '211', '212', '213', '214', '215', '216', '217', '218', '219', '220', '221',
            '01', '31', '32', '33', '34', '35', '36', '37', '38', '39', '310', '311', '312', '313', '314', '315', '316', '317', '318', '319']
roi_list = ['VWFA_l','VWFA_r','EBA_l','EBA_r','FFA_l','FFA_r']
con_dict_loc_vid = {
    # 'Sound_LPC': 1,
    'Silent_LPC': 2,
    'Manual_cues': 3, 'Labial': 4,
    # 'Pseudo': 5,
    # 'Sound_LPC - Silent_LPC': 6, 'Silent_LPC - Sound_LPC': 7, 'Silent_LPC - Manual_cues': 8,
    # 'Manual_cues - Silent_LPC': 9, 'Silent_LPC - Labial': 10, 'Labial - Silent_LPC': 11, 'Silent_LPC - Pseudo': 12,
    # 'Pseudo - Silent_LPC': 13, 'Manual_cues - Labial': 14, 'Labial - Manual_cues': 15
    }
con_dict_loc_stat = {
    # 'Faces': 1, 'Bodies': 2, 'Words': 3,
    # 'Houses': 4, 'Tools': 5,
    # 'Targets': 6,'Keypress': 7,
    # 'Faces-all': 8, 'Bodies-all': 9, 'Words-all': 10,
    # 'Houses-all': 11, 'Tools-all': 12,
    # 'Faces-Bodies': 13, 'Bodies-Faces': 14,
    # 'Faces-Words': 15, 'Words-Faces': 16,
    # 'Bodies-Words': 17,'Words-Bodies': 18
    }

pd.set_option('display.max_columns', None)


#%% Retrieve mean voxel value

con_dict = con_dict_loc_vid if task == 'loc_vid' else con_dict_loc_stat
df_con_list = []
for con in con_dict:
    df_con = pd.read_csv(os.path.join(main_path,f'cuspex_2nd_order/{task}/{task}_roi_analysis/results_s{smoothing_level}/roi_analysis_results_con_{con_dict[con]:04d}.csv'))
    df_con = df_con.rename(columns={'Unnamed: 0': 'subject'})
    df_con.insert(0, 'contrast', con)
    df_con_list.append(df_con)
df = pd.concat(df_con_list, ignore_index=True)
df['subject'] = df['subject'].astype(str)
df['group'] = df['group'].astype(str)

# Melt ROIs into one column
df = pd.melt(df, id_vars=['contrast', 'subject', 'group'], var_name='roi', value_name='mean_value')

# Only keep ROIs to consider for analysis
df = df[df['roi'].isin(roi_list)]

# Indicate ROI laterality in a separate column
df['laterality'] = df['roi'].apply(lambda x: 'l' if x.endswith('_l') else ('r' if x.endswith('_r') else None))
df['roi'] = df['roi'].str.replace('(_l$|_r$)', '', regex=True)

pivot_df = df.pivot_table(index=['subject','group'], columns=['contrast', 'roi', 'laterality'], values='mean_value', aggfunc='mean')
pivot_df.columns = ['{}_{}_{}'.format(col[1], col[0], col[2]) for col in pivot_df.columns]
pivot_df = pivot_df.reindex(sorted(pivot_df.columns), axis=1)
pivot_df.reset_index(inplace=True)


#%% Statistical analysis - Bayesian version

file = open('bayesian_results.txt', 'w')
sys.stdout = file

for group, cond in product(df['group'].unique(), pivot_df.columns[2:]):
    group_cond_col = pivot_df[pivot_df['group']==group][cond]
    print(f'\n### Results for {cond} in group {group}: \n{pg.ttest(group_cond_col, np.zeros(len(group_cond_col)))}')
    
for cond in pivot_df.columns[2:]:
    for group_1, group_2 in combinations(df['group'].unique(), 2):
        df_1 = pivot_df[pivot_df['group'] == group_1][cond]
        df_2 = pivot_df[pivot_df['group'] == group_2][cond]
        print(f'\n### Independent t-test for {cond} between {group_1} and {group_2}:')
        print(pg.ttest(df_1, df_2))

sys.stdout = sys.__stdout__
file.close()



#%% Statistical analysis - ANOVA version

pandas2ri.activate()

## For each ROI, perform ANOVA to study the interaction between 'group', 'contrast' and 'laterality'
base = importr('base')
lme4 = importr('lme4')
stats = importr('stats')
emmeans = importr('emmeans')
lmerTest = importr('lmerTest')
roi_anova_results = {}
for roi in df['roi'].unique():
    df_roi = pandas2ri.py2rpy(df[df['roi'] == roi])
    model = lmerTest.lmer('mean_value ~ group * contrast * laterality + (1|subject)', data=df_roi)
    roi_anova_results[roi] = stats.anova(model)
## Display results
for key in roi_anova_results.keys():
    print(f'## {key}\n')
    print(roi_anova_results[key])

pandas2ri.deactivate()


#%% Box plots

# Set up the dimensions of the grid containing the plots
n_rows = 3 if task == 'loc_vid' else 3
n_cols = 2 if task == 'loc_vid' else 2
fig, axs = plt.subplots(n_rows, n_cols, figsize=(8*n_cols, 8*n_rows))
plot_index = 0

# Plot each ROI with the determined y-axis limits
axs = axs.flatten() if n_rows * n_cols > 1 else [axs] # Ensure axs is 1D or 2D based on the number of rows and columns
roi_list_plot = set([roi[:-2] for roi in roi_list])
for roi in roi_list_plot:
    for laterality in ['l', 'r']:
        if plot_index < n_rows * n_cols:
            ax = axs[plot_index]
            df_plot = df[(df['roi'] == roi) & (df['laterality'] == laterality)]
            sns.boxplot(x='group', y='mean_value', hue='contrast', data=df_plot, palette='pastel', ax=ax)
            sns.stripplot(x='group', y='mean_value', hue='contrast', dodge=True, data=df_plot, palette='dark', ax=ax)
            ax.set_title(f'{roi} ({laterality.capitalize()})')
            handles, labels = ax.get_legend_handles_labels()
            ax.set_ylim(-1.2, 4.4)
            ax.axhline(y=0, color='black', linestyle=':') 
            ax.legend(handles[:3], labels[:3], title='Group')
            plot_index += 1
plt.show()