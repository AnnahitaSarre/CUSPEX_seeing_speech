#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CUSPEX video localizer debriefing analysis

"""

#%%Import modules

import pandas as pd
import numpy as np
import pingouin as pg
import seaborn as sns
import matplotlib.pyplot as plt


#%% Import and arrange df

df = pd.read_csv('../questionnaires/RedCap_data_processed/cuspex_tableau_final_demography_comm.csv', sep=',')
study_columns = ['group','subject','concentration_localizer','comprehension_lpc_son','comprehension_lpc_sans_son',
                 'comprehension_lpc_pseudo','comprehension_labial','comprehension_indices']
df = df.loc[:,study_columns]
df = df.astype('int')


#%% Defrief responses analysis

plt.figure(figsize=(8,6))
sns.histplot(x=df['group'], hue=df['concentration_localizer'], stat='count',
             multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported focus difficulty during the task by group (min 0 max 4)')
plt.show()
print(df[['group', 'concentration_localizer']].groupby('group').describe())
print(pg.anova(data=df, dv='concentration_localizer', between='group'))


df_plot = df.iloc[:,:2]
df_plot = pd.DataFrame(np.repeat(df_plot.values, 5, axis=0),columns=df_plot.columns)
df_plot['stim_category'] = ['comprehension_lpc_son','comprehension_lpc_sans_son',
                            'comprehension_lpc_pseudo','comprehension_labial','comprehension_indices']*60
comprehension_series = []
for index in df.index:
    subject_comprehension = df.loc[index].values[3:].tolist()
    comprehension_series = comprehension_series + subject_comprehension
df_plot['score'] = comprehension_series
# df_plot['group'] = pd.Categorical(df_plot['group'], ['1', '2','3']) # to arrange the order when plotting

plt.figure(figsize=(25,20))
sns.violinplot(x=df_plot['stim_category'], y=df_plot['score'], hue=df_plot['group'], data=df_plot, inner='quartile', density_norm='count', palette='pastel').set(title='Self-reported stimuli comprehension by group (min 1 max 5)')
sns.stripplot(x=df_plot['stim_category'], y=df_plot['score'], hue=df_plot['group'], dodge=True, jitter=1, data=df_plot, palette='dark')