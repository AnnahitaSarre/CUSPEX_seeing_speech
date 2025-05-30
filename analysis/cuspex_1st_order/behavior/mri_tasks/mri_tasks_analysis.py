#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CUSPEX static localizer behavioral analysis

"""

#%%Import modules

import pandas as pd
import pingouin as pg
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro


#%% Study parameter to change

study = 'loc_stat'


#%% Import and arrange df

df_task = pd.read_csv(f'behavior_{study}.csv', sep=',')
rt_columns = [col for col in df_task.columns if col.startswith('list_rt')]
df_task['list_rt'] = df_task[rt_columns].values.tolist()
df_task = df_task.drop(rt_columns, axis=1)
if study == 'decod':
    df_task = df_task.loc[df_task['run']=='all_runs']

df_debrief = pd.read_csv('../questionnaires/RedCap_data_processed/cuspex_tableau_final_demography_comm.csv', sep=',')
study_suffix = {'decod':'decoding','loc_stat':'static'}
study_columns = ['group','subject'] + [col for col in df_debrief.columns if col.endswith(study_suffix[study])]
df_debrief = df_debrief.loc[:,study_columns]
df_debrief = df_debrief.astype('int')

df = pd.merge(df_task, df_debrief, on=['subject','group'])


#%%% Hit and fa rates

plt.figure(figsize=(8,6))
sns.boxplot(x=df['group'], y=df['hit_rate'], data=df, palette='pastel').set(title='Hit rate by group')
sns.stripplot(x=df['group'], y=df['hit_rate'], palette='dark')
plt.show()
# plt.figure(figsize=(8,6))
# sns.histplot(x=df['group'], y=df['nb_hits'],
#              stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Number of hits by group')
# plt.show()
print(df[['group', 'hit_rate']].groupby('group').describe())
print(df['hit_rate'].describe())
print(df['fa_rate'].describe())

plt.figure(figsize=(8,6))
sns.boxplot(x=df['group'], y=df['fa_rate'], data=df, palette='pastel').set(title='FA rate by group')
sns.stripplot(x=df['group'], y=df['fa_rate'], palette='dark')
plt.show()
print(df[['group', 'fa_rate']].groupby('group').describe())


#%% Dprime

plt.figure(figsize=(8,6))
sns.boxplot(x=df['group'], y=df['dprime'], data=df, palette='pastel', legend=False).set(title='Dprime by group')
sns.stripplot(x=df['group'], y=df['dprime'], palette='dark', legend=False)
plt.show()


#%% Response times analysis

plt.figure(figsize=(8,6))
sns.boxplot(x=df['group'], y=df['mean_rt'], data=df, palette='pastel').set(title='Mean RT by group')
sns.stripplot(x=df['group'], y=df['mean_rt'], palette='dark')
plt.show()
print(df[['group', 'mean_rt']].groupby('group').describe())
print(df['mean_rt'].describe())

# Do non-parametric Mann–Whitney U test (= Wilcoxon rank-sum test)
print(f"Mann–Whitney U test between mean RTs of groups 1 and 2:\n{pg.mwu(df.loc[df['group']==1]['mean_rt'],df.loc[df['group']==2]['mean_rt'])}\n")
print(f"Mann–Whitney U test between mean RTs of groups 2 and 3:\n{pg.mwu(df.loc[df['group']==2]['mean_rt'],df.loc[df['group']==3]['mean_rt'])}\n")
print(f"Mann–Whitney U test between mean RTs of groups 1 and 3:\n{pg.mwu(df.loc[df['group']==1]['mean_rt'],df.loc[df['group']==3]['mean_rt'])}")

print(['g1 and g2: equal mean RT variance' if pg.homoscedasticity(df.loc[df['group']==1]['mean_rt'], df.loc[df['group']==2]['mean_rt'])[1]> 0.05 else 'g1 and g2: unnequal mean RT variance'][0])
print(['g2 and g3: equal mean RT variance' if pg.homoscedasticity(df.loc[df['group']==2]['mean_rt'], df.loc[df['group']==3]['mean_rt'])[1]> 0.05 else 'g1 and g2: unnequal mean RT variance'][0])
print(['g1 and g3: equal mean RT variance' if pg.homoscedasticity(df.loc[df['group']==1]['mean_rt'], df.loc[df['group']==3]['mean_rt'])[1]> 0.05 else 'g1 and g2: unnequal mean RT variance'][0])


plt.figure(figsize=(8,6))
sns.boxplot(x=df['group'], y=df['median_rt'], data=df, palette='pastel').set(title='Median RT by group')
sns.stripplot(x=df['group'], y=df['median_rt'], palette='dark')
plt.show()
print(df[['group', 'median_rt']].groupby('group').describe())

plt.figure(figsize=(8,6))
sns.boxplot(x=df['group'], y=df['std_rt'], data=df, palette='pastel').set(title='STD of RT by group')
sns.stripplot(x=df['group'], y=df['std_rt'], palette='dark')
plt.show()
print(df[['group', 'std_rt']].groupby('group').describe())


#%% SDT analyses

plt.figure(figsize=(8,6))
sns.boxplot(x=df['group'], y=df['dprime'], data=df, palette='pastel').set(title='Sensitivity (dprime) by group')
sns.stripplot(x=df['group'], y=df['dprime'], palette='dark')
plt.show()
print(df[['group', 'dprime']].groupby('group').describe())
print(df['dprime'].describe())

plt.figure(figsize=(8,6))
sns.histplot(x=df['dprime'], hue=df['group'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Visualisation of dprime in each group')
plt.show()

# Check if it's possible to perform an ANOVA: normality in all groups + equal variance
for group_num in range(1,4):
    print([f'g{group_num}: normal' if shapiro(df.loc[df['group']==group_num]['dprime']).pvalue > 0.05 else f'g{group_num}: not normal'][0])
print(['g1 and g2: equal dprime variance' if pg.homoscedasticity(df.loc[df['group']==1]['dprime'], df.loc[df['group']==2]['dprime'])[1]> 0.05 else 'g1 and g2: unnequal dprime variance'][0])
print(['g2 and g3: equal dprime variance' if pg.homoscedasticity(df.loc[df['group']==2]['dprime'], df.loc[df['group']==3]['dprime'])[1]> 0.05 else 'g1 and g2: unnequal dprime variance'][0])
print(['g1 and g3: equal dprime variance' if pg.homoscedasticity(df.loc[df['group']==1]['dprime'], df.loc[df['group']==3]['dprime'])[1]> 0.05 else 'g1 and g2: unnequal dprime variance'][0])
if study == 'decod': # The study passed the two tests above
    print(pg.anova(dv='dprime', between='group', data=df, detailed=False))
    # There's a main effect so we proceed to post-hoc Tukey test
    print(pg.pairwise_tukey(dv='dprime', between='group', data=df))
if study == 'loc_stat': # The study did not pass the two tests: use of non-parametric equivalent Kruskal-Wallis test
    pg.kruskal(dv='dprime', between='group', data=df)
    # No main effect so we stop here

# Alternative: Do non-parametric Mann–Whitney U test (= Wilcoxon rank-sum test) in all cases
print(f"Mann–Whitney U test between dprimes of groups 1 and 2:\n{pg.mwu(df.loc[df['group']==1]['dprime'],df.loc[df['group']==2]['dprime'])}\n")
print(f"Mann–Whitney U test between dprimes of groups 2 and 3:\n{pg.mwu(df.loc[df['group']==2]['dprime'],df.loc[df['group']==3]['dprime'])}\n")
print(f"Mann–Whitney U test between dprimes of groups 1 and 3:\n{pg.mwu(df.loc[df['group']==1]['dprime'],df.loc[df['group']==3]['dprime'])}")
    
plt.figure(figsize=(8,6))
sns.boxplot(x=df['group'], y=df['criterion'], data=df, palette='pastel').set(title='Criterion by group')
sns.stripplot(x=df['group'], y=df['criterion'], palette='dark')
plt.show()
print(df[['group', 'criterion']].groupby('group').describe())


#%% Defrief responses analysis

plt.figure(figsize=(8,6))
sns.histplot(x=df['group'], hue=df[f'concentration_{study_suffix[study]}'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported focus difficulty during the task by group (min 0 max 4)')
plt.show()
print(df[['group', f'concentration_{study_suffix[study]}']].groupby('group').describe())

plt.figure(figsize=(8,6))
sns.histplot(x=df['group'], hue=df[f'difficulte_{study_suffix[study]}'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported task difficulty by group (min 0 max 4)')
plt.show()
print(df[['group', f'difficulte_{study_suffix[study]}']].groupby('group').describe())

plt.figure(figsize=(8,6))
sns.histplot(x=df['group'], hue=df[f'confiance_{study_suffix[study]}'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported level of confidence by group (min 0 max 4)')
plt.show()
print(df[['group', f'confiance_{study_suffix[study]}']].groupby('group').describe())

if study == 'decod':
    plt.figure(figsize=(8,6))
    sns.histplot(x=df['group'], hue=df['comprehension_decoding'],
                 stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported syllables understanding by group (min 0 max 4)')
    plt.show()
    print(df[['group', 'comprehension_decoding']].groupby('group').describe())
