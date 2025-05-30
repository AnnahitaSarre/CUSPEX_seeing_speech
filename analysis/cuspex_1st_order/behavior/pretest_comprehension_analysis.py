#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CUSPEX comprehension pretest analysis

"""


#%% Import modules

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
from scipy.stats import shapiro, levene


#%% Import csv

csv_file = 'cuspex_pretest_comprehension_results.csv'
df = pd.read_csv(csv_file, delimiter=';', encoding='latin-1')
df = df[:-1] # erase 'notes' row


#%% Retrieve total of points in each category

total_syllables = 0
total_sentences = 0
total_sentences_easy = 0
total_sentences_medium = 0
total_sentences_hard = 0

for index in df.index:
    if df['stim'].loc[index].startswith('S'):
        total_syllables = total_syllables + df['total_points'].loc[index]
    else:
        total_sentences = total_sentences + df['total_points'].loc[index]
        if df['stim'].loc[index].startswith('F'):
            total_sentences_easy = total_sentences_easy + df['total_points'].loc[index]
        elif df['stim'].loc[index].startswith('M'):
            total_sentences_medium = total_sentences_medium + df['total_points'].loc[index]
        else:
            total_sentences_hard = total_sentences_hard + df['total_points'].loc[index]


#%% Create a dataframe that will serve as basis in various cases (see below)

subject_array = pd.Series(df.columns.values[3:], name='subject')
df_base = subject_array.to_frame()
df_base['group'] = np.nan
for index in df_base.index:
    df_base['group'].loc[index] = df_base['subject'].loc[index][0]
    

#%% Create a df to be used for further stats (LC request + used to separate the two attemps)

df_stats = df_base.copy()
df_stats = pd.DataFrame(np.repeat(df_stats.values, 24, axis=0),columns=df_base.columns) # 1 col/sub/sentence
df_stats['sentence'] = (df.loc[~df['stim'].str.startswith('S')].iloc[:,0].tolist())*40
df_stats['total'] = (df.loc[~df['stim'].str.startswith('S')].iloc[:,2].tolist())*40
df_stats['difficulty'] = df_stats['sentence'].str[0]
df_stats['num_try'] = df_stats['sentence'].str[3]
df_stats['sentence'] = df_stats['sentence'].str[:2]
scores_list = [df.loc[~df['stim'].str.startswith('S')][col].tolist() for col in df.columns[3:]]
df_stats['correct_syll'] = [item for row in scores_list for item in row]
df_stats['wrong_syll'] = df_stats['total'].astype('float') - df_stats['correct_syll'].astype('float')
# df_stats['score'] = df_stats['score'].astype('float')/df_stats['total'].astype('float')*100
df_stats = df_stats.drop('total', axis=1)

df_stats.to_csv('pretest_comprehension_stats.csv')


#%% Compute and save global individual results for covariates

## Copy the begining of df to create the 'scores' dfs
df_subject_scores_all = df_base.copy()
df_subject_scores_try1 = df_base.copy()
df_subject_scores_try2 = df_base.copy()

## Compute sentences scores for the two groups mixing the two attemps
df_sentences_all = df.loc[~df['stim'].str.startswith('S')].iloc[:,3:].astype('float')
df_subject_scores_all['sentences_all_scores'] = df_sentences_all.sum().reset_index(drop=True)
df_subject_scores_all['sentences_all_scores'] = df_subject_scores_all['sentences_all_scores']/total_sentences*100

df_sentences_easy_all = df.loc[df['stim'].str.startswith('F')].iloc[:,3:].astype('float')
df_subject_scores_all['sentences_easy_scores'] = df_sentences_easy_all.sum().reset_index(drop=True)
df_subject_scores_all['sentences_easy_scores'] = df_subject_scores_all['sentences_easy_scores']/total_sentences_easy*100

df_sentences_medium_all = df.loc[df['stim'].str.startswith('M')].iloc[:,3:].astype('float')
df_subject_scores_all['sentences_medium_scores'] = df_sentences_medium_all.sum().reset_index(drop=True)
df_subject_scores_all['sentences_medium_scores'] = df_subject_scores_all['sentences_medium_scores']/total_sentences_medium*100

df_sentences_hard_all = df.loc[df['stim'].str.startswith('D')].iloc[:,3:].astype('float')
df_subject_scores_all['sentences_hard_scores'] = df_sentences_hard_all.sum().reset_index(drop=True)
df_subject_scores_all['sentences_hard_scores'] = df_subject_scores_all['sentences_hard_scores']/total_sentences_hard*100

df_syllables_all = df.loc[df['stim'].str.startswith('S')].iloc[:,3:].astype('float')
df_subject_scores_all['syllables_scores'] = df_syllables_all.sum(min_count=1).reset_index(drop=True)
df_subject_scores_all['syllables_scores'] = df_subject_scores_all['syllables_scores']/total_syllables*100

df_subject_scores_all.to_csv('pretest_comprehension_results.csv') # Use it to create covariates

## Compute sentences scores for the two groups for the two attemps separately
# Try 1
df_sentences_try1 = df.loc[~df['stim'].str.startswith('S') & df['stim'].str.endswith('1')].iloc[:,3:].astype('float')
df_subject_scores_try1['sentences_all_scores'] = df_sentences_try1.sum().reset_index(drop=True)
df_subject_scores_try1['sentences_all_scores'] = df_subject_scores_try1['sentences_all_scores']/(total_sentences/2)*100

df_sentences_easy_try1 = df.loc[df['stim'].str.startswith('F') & df['stim'].str.endswith('1')].iloc[:,3:].astype('float')
df_subject_scores_try1['sentences_easy_scores'] = df_sentences_easy_try1.sum().reset_index(drop=True)
df_subject_scores_try1['sentences_easy_scores'] = df_subject_scores_try1['sentences_easy_scores']/(total_sentences_easy/2)*100

df_sentences_medium_try1 = df.loc[df['stim'].str.startswith('M') & df['stim'].str.endswith('1')].iloc[:,3:].astype('float')
df_subject_scores_try1['sentences_medium_scores'] = df_sentences_medium_try1.sum().reset_index(drop=True)
df_subject_scores_try1['sentences_medium_scores'] = df_subject_scores_try1['sentences_medium_scores']/(total_sentences_medium/2)*100

df_sentences_hard_try1 = df.loc[df['stim'].str.startswith('D') & df['stim'].str.endswith('1')].iloc[:,3:].astype('float')
df_subject_scores_try1['sentences_hard_scores'] = df_sentences_hard_try1.sum().reset_index(drop=True)
df_subject_scores_try1['sentences_hard_scores'] = df_subject_scores_try1['sentences_hard_scores']/(total_sentences_hard/2)*100

df_syllables_try1 = df.loc[df['stim'].str.startswith('S') & df['stim'].str.endswith('1')].iloc[:,3:].astype('float')
df_subject_scores_try1['syllables_scores'] = df_syllables_try1.sum(min_count=1).reset_index(drop=True)
df_subject_scores_try1['syllables_scores'] = df_subject_scores_try1['syllables_scores']/(total_syllables/2)*100

# Try 2
df_sentences_try2 = df.loc[~df['stim'].str.startswith('S') & df['stim'].str.endswith('2')].iloc[:,3:].astype('float')
df_subject_scores_try2['sentences_all_scores'] = df_sentences_try2.sum().reset_index(drop=True)
df_subject_scores_try2['sentences_all_scores'] = df_subject_scores_try2['sentences_all_scores']/(total_sentences/2)*100

df_sentences_easy_try2 = df.loc[df['stim'].str.startswith('F') & df['stim'].str.endswith('2')].iloc[:,3:].astype('float')
df_subject_scores_try2['sentences_easy_scores'] = df_sentences_easy_try2.sum().reset_index(drop=True)
df_subject_scores_try2['sentences_easy_scores'] = df_subject_scores_try2['sentences_easy_scores']/(total_sentences_easy/2)*100

df_sentences_medium_try2 = df.loc[df['stim'].str.startswith('M') & df['stim'].str.endswith('2')].iloc[:,3:].astype('float')
df_subject_scores_try2['sentences_medium_scores'] = df_sentences_medium_try2.sum().reset_index(drop=True)
df_subject_scores_try2['sentences_medium_scores'] = df_subject_scores_try2['sentences_medium_scores']/(total_sentences_medium/2)*100

df_sentences_hard_try2 = df.loc[df['stim'].str.startswith('D') & df['stim'].str.endswith('2')].iloc[:,3:].astype('float')
df_subject_scores_try2['sentences_hard_scores'] = df_sentences_hard_try2.sum().reset_index(drop=True)
df_subject_scores_try2['sentences_hard_scores'] = df_subject_scores_try2['sentences_hard_scores']/(total_sentences_hard/2)*100

df_syllables_try2 = df.loc[df['stim'].str.startswith('S') & df['stim'].str.endswith('2')].iloc[:,3:].astype('float')
df_subject_scores_try2['syllables_scores'] = df_syllables_try2.sum(min_count=1).reset_index(drop=True)
df_subject_scores_try2['syllables_scores'] = df_subject_scores_try2['syllables_scores']/(total_syllables/2)*100


#%% Plot participants' results mixing the two attemps

## Create an extended scores df to permit easier plotting
df_subject_scores_all_plot = df_subject_scores_all.iloc[:,:2]
col = df_subject_scores_all_plot.columns
df_subject_scores_all_plot = pd.DataFrame(np.repeat(df_subject_scores_all_plot.values, 5, axis=0),columns=col)
df_subject_scores_all_plot['stim_category'] = ['sentences_all','sentences_easy','sentences_medium','sentences_hard','syllables']*40
scores_series = []
for index in df_subject_scores_all.index:
    subject_score = df_subject_scores_all.loc[index].values[2:].tolist()
    scores_series = scores_series + subject_score
df_subject_scores_all_plot['score'] = scores_series
df_subject_scores_all_plot['group'] = pd.Categorical(df_subject_scores_all_plot['group'], ['1', '2']) # to arrange the order when plotting

## Scores for all categories displayed by group
plt.figure(figsize=(12,10))
# df_subject_scores_all_plot = df_subject_scores_all_plot.drop(df_subject_scores_all_plot[df_subject_scores_all_plot['stim_category'] == 'syllables'].index)
sns.boxplot(x='stim_category', y='score', hue='group', data=df_subject_scores_all_plot,  palette='pastel', legend=False)
sns.stripplot(x='stim_category', y='score', hue='group', dodge=True, data=df_subject_scores_all_plot, palette='dark', legend=False)
plt.xlabel('Level of difficulty', fontsize=15, labelpad=11)
plt.ylabel('Proportion of correctly transcribed phonemes (%)', fontsize=15, labelpad=10)
# plt.title('CS sentences comprehension scores', fontsize= 20, y=1.025)
new_labels = ['All Sentences', 'Easy', 'Intermediate', 'Difficult', 'Syllables']
plt.xticks(ticks=plt.gca().get_xticks(), labels=new_labels, fontsize=14)
plt.yticks(range(0, 101, 10), fontsize=14)
plt.show()


#%% Plot participants' results for the two attemps separately

## Create extended scores dfs to permit easier plotting (try 1)
df_subject_scores_try1_plot = df_subject_scores_try1.iloc[:,:2]
col = df_subject_scores_try1_plot.columns
df_subject_scores_try1_plot = pd.DataFrame(np.repeat(df_subject_scores_try1_plot.values, 5, axis=0),columns=col)
df_subject_scores_try1_plot['stim_category'] = ['sentences_all','sentences_easy','sentences_medium','sentences_hard','syllables']*40
scores_series = []
for index in df_subject_scores_try1.index:
    subject_score = df_subject_scores_try1.loc[index].values[2:].tolist()
    scores_series = scores_series + subject_score
df_subject_scores_try1_plot['score'] = scores_series
df_subject_scores_try1_plot['group'] = pd.Categorical(df_subject_scores_try1_plot['group'], ['1', '2']) # to arrange the order when plotting

## Create extended scores dfs to permit easier plotting (try 2)
df_subject_scores_try2_plot = df_subject_scores_try2.iloc[:,:2]
col = df_subject_scores_try2_plot.columns
df_subject_scores_try2_plot = pd.DataFrame(np.repeat(df_subject_scores_try2_plot.values, 5, axis=0),columns=col)
df_subject_scores_try2_plot['stim_category'] = ['sentences_all','sentences_easy','sentences_medium','sentences_hard','syllables']*40
scores_series = []
for index in df_subject_scores_try1.index:
    subject_score = df_subject_scores_try2.loc[index].values[2:].tolist()
    scores_series = scores_series + subject_score
df_subject_scores_try2_plot['score'] = scores_series
df_subject_scores_try2_plot['group'] = pd.Categorical(df_subject_scores_try2_plot['group'], ['1', '2']) # to arrange the order when plotting

## Scores for all categories displayed by group (one plot per attempt)
fig, axs = plt.subplots(1,2, figsize=(24,15), sharey=True)
sns.violinplot(x='stim_category', y='score', hue='group', data=df_subject_scores_try1_plot, inner='quartile', scale='count', palette='pastel', legend=False, ax=axs[0]).set(title='Pretest scores by stim category and group (1st attempt)')
sns.stripplot(x='stim_category', y='score', hue='group', dodge=True, data=df_subject_scores_try1_plot, palette='dark', ax=axs[0])
sns.violinplot(x='stim_category', y='score', hue='group', data=df_subject_scores_try2_plot, inner='quartile', scale='count', palette='pastel', ax=axs[1]).set(title='Pretest scores by stim category and group (2nd attempt)')
sns.stripplot(x='stim_category', y='score', hue='group', dodge=True, data=df_subject_scores_try2_plot, palette='dark', ax=axs[1])


#%% Compute statistics mixing the two attemps

## Create a df for each group, only keeping the scores
df_g1_scores_all = df_subject_scores_all[df_subject_scores_all['group']=='1'].iloc[:, 2:-1] # Drop syllable column
df_g2_scores_all = df_subject_scores_all[df_subject_scores_all['group']=='2'].iloc[:, 2:]

## Compute basic stats on each group's scores
df_g1_description = df_g1_scores_all.describe()
df_g2_description = df_g2_scores_all.describe()

## Testing normality with the Shapiro-Wilk test
df_shapiro_all = pd.DataFrame(columns = df_g2_scores_all.columns, index = ['group 1','group 2'])
for col in df_g1_scores_all.columns: # Group 1
    shapiro_result = shapiro(df_g1_scores_all[col])
    normality = ['normal' if shapiro_result.pvalue > 0.05 else 'not normal'][0] # if p>0.05 the data is normally distributed
    df_shapiro_all[col].iloc[0] = [shapiro_result.statistic, shapiro_result.pvalue, normality]
for col in df_g2_scores_all.columns: # Group 2
    shapiro_result = shapiro(df_g2_scores_all[col])
    normality = ['normal' if shapiro_result.pvalue > 0.05 else 'not normal'][0] # if p>0.05 the data is normally distributed
    df_shapiro_all[col].iloc[1] = [shapiro_result.statistic, shapiro_result.pvalue, normality]

## Assess differences between the two groups
# Means with Mann–Whitney U test (= Wilcoxon rank-sum test)
df_2g_mwu = pd.DataFrame(columns = df_g1_scores_all.columns, index = ['U-val','p-val','RBC','CLES'])
for col in df_g1_scores_all.columns:
    df_2g_mwu[col] = pg.mwu(df_g1_scores_all[col],df_g2_scores_all[col]).values.tolist()[0]
    
for col in df_g1_scores_all.columns:
    print(f'Results for {col}: {pg.mwu(df_g1_scores_all[col],df_g2_scores_all[col])}')
    
# Compare variance
pg.homoscedasticity(df_g1_scores_all['sentences_all_scores'], df_g2_scores_all['sentences_all_scores'])
levene(df_g1_scores_all['sentences_all_scores'], df_g2_scores_all['sentences_all_scores'])

## Assess differences between sentences' level of difficulty
df_g1_difficulty = pd.DataFrame(index = ['U-val','p-val','RBC','CLES']) # Group 1
df_g1_difficulty['easy vs medium'] = pg.mwu(df_g1_scores_all.iloc[:,1],df_g1_scores_all.iloc[:,2]).values.tolist()[0]
df_g1_difficulty['medium vs hard'] = pg.mwu(df_g1_scores_all.iloc[:,2],df_g1_scores_all.iloc[:,3]).values.tolist()[0]
df_g1_difficulty['easy vs hard'] = pg.mwu(df_g1_scores_all.iloc[:,1],df_g1_scores_all.iloc[:,3]).values.tolist()[0]
df_g2_difficulty = pd.DataFrame(index = ['U-val','p-val','RBC','CLES']) # Group 2
df_g2_difficulty['easy vs medium'] = pg.mwu(df_g2_scores_all.iloc[:,1],df_g2_scores_all.iloc[:,2]).values.tolist()[0]
df_g2_difficulty['medium vs hard'] = pg.mwu(df_g2_scores_all.iloc[:,2],df_g2_scores_all.iloc[:,3]).values.tolist()[0]
df_g2_difficulty['easy vs hard'] = pg.mwu(df_g2_scores_all.iloc[:,1],df_g2_scores_all.iloc[:,3]).values.tolist()[0]
df_g2_difficulty['sentences vs syllables'] = pg.mwu(df_g2_scores_all.iloc[:,0],df_g2_scores_all.iloc[:,4]).values.tolist()[0]


#%% Compute statistics on the two attempts separately

## Try 1

# Create a df for each group, only keeping the scores
df_g1_scores_try1 = df_subject_scores_try1[df_subject_scores_try1['group']=='1'].iloc[:, 2:-1] # Drop syllable column
df_g2_scores_try1 = df_subject_scores_try1[df_subject_scores_try1['group']=='2'].iloc[:, 2:]

# Compute basic stats on each group's scores
df_g1_description = df_g1_scores_try1.describe()
df_g2_description = df_g2_scores_try1.describe()

# Testing normality with the Shapiro-Wilk test
df_shapiro_try1 = pd.DataFrame(columns = df_g2_scores_try1.columns, index = ['group 1','group 2'])
for col in df_g1_scores_try1.columns: # Group 1
    shapiro_result = shapiro(df_g1_scores_try1[col])
    normality = ['normal' if shapiro_result.pvalue > 0.05 else 'not normal'][0] # if p>0.05 the data is normally distributed
    df_shapiro_try1[col].iloc[0] = [shapiro_result.statistic, shapiro_result.pvalue, normality]
for col in df_g2_scores_try1.columns: # Group 2
    shapiro_result = shapiro(df_g2_scores_try1[col])
    normality = ['normal' if shapiro_result.pvalue > 0.05 else 'not normal'][0] # if p>0.05 the data is normally distributed
    df_shapiro_try1[col].iloc[1] = [shapiro_result.statistic, shapiro_result.pvalue, normality]

## Try 2

# Create a df for each group, only keeping the scores
df_g1_scores_try2 = df_subject_scores_try2[df_subject_scores_try2['group']=='1'].iloc[:, 2:-1] # Drop syllable column
df_g2_scores_try2 = df_subject_scores_try2[df_subject_scores_try2['group']=='2'].iloc[:, 2:]

# Compute basic stats on each group's scores
df_g1_description = df_g1_scores_try2.describe()
df_g2_description = df_g2_scores_try2.describe()

# Testing normality with the Shapiro-Wilk test
df_shapiro_try2 = pd.DataFrame(columns = df_g2_scores_try2.columns, index = ['group 1','group 2'])
for col in df_g1_scores_try2.columns: # Group 1
    shapiro_result = shapiro(df_g1_scores_try2[col])
    normality = ['normal' if shapiro_result.pvalue > 0.05 else 'not normal'][0] # if p>0.05 the data is normally distributed
    df_shapiro_try2[col].iloc[0] = [shapiro_result.statistic, shapiro_result.pvalue, normality]
for col in df_g2_scores_try2.columns: # Group 2
    shapiro_result = shapiro(df_g2_scores_try2[col])
    normality = ['normal' if shapiro_result.pvalue > 0.05 else 'not normal'][0] # if p>0.05 the data is normally distributed
    df_shapiro_try2[col].iloc[1] = [shapiro_result.statistic, shapiro_result.pvalue, normality]

# Non normal distributions so Wilcoxon signed-rank test to compare tries 1 and 2 within each participant
df_tries_diff = pd.DataFrame(columns = df_g2_scores_try1.columns, index = ['group 1','group 2'])
for col in df_g1_scores_try1.columns: # Group 1
    df_tries_diff[col].iloc[0] = pg.wilcoxon(df_g1_scores_try1[col], df_g1_scores_try2[col])
for col in df_g2_scores_try1.columns: # Group 1
    df_tries_diff[col].iloc[1] = pg.wilcoxon(df_g2_scores_try1[col], df_g2_scores_try2[col])
print('Signiticant differences between attemps in all cases except for easy sentences in group 1.')
print('Small sample so carefull with these results!')


#%% Compare the two attempts

for col in df_g1_scores_try1.columns: # Sentences Group 1
    print(f'Group 1 {col}:')
    print(pg.mwu(df_g1_scores_try1[col],df_g1_scores_try2[col])) # => difference between all sentenpces and hard sentences
    print(levene(df_g1_scores_try1[col],df_g1_scores_try2[col])) # => difference between all sentences

for col in df_g2_scores_try1.columns: # Sentences Group 2
    print(f'Group 2 {col}:')
    print(pg.mwu(df_g2_scores_try1[col],df_g2_scores_try2[col])) # => No significant difference
    print(levene(df_g2_scores_try1[col],df_g2_scores_try2[col])) # => No significant difference

# Syllables Group 2
df_syllables_try1, df_syllables_try2 = df_syllables_try1.dropna(axis=1, how='all'), df_syllables_try2.dropna(axis=1, how='all')
print('Within participants')
print(pg.wilcoxon(df_syllables_try1.mean(),df_syllables_try2.mean())) # Within participants => significant difference
print('For each syllable')
for syll in range(0,16):
    if (df_syllables_try1.iloc[syll] - df_syllables_try2.iloc[syll] != 0).any():
        print(pg.wilcoxon(df_syllables_try1.iloc[syll],df_syllables_try2.iloc[syll])) # Sample sizes too small


#%% Assess scores on syllables

syll_dict = {'da': ['unrounded', 'coronal',], 'de': ['unrounded',], 'do': ['rounded',], 'du': ['rounded',],
             'ma': ['unrounded',], 'me': ['unrounded',], 'mo': ['rounded',], 'mu': ['rounded',],
             'pa': ['unrounded',], 'pe': ['unrounded',], 'po': ['rounded',], 'pu': ['rounded',],
             'ta': ['unrounded',], 'te': ['unrounded',], 'to': ['rounded',], 'tu': ['rounded',]}

# Individual stimuli
df_syllables_all = df_syllables_all
df_assess_syllables = pd.concat([df.iloc[24:,1], df_syllables_all.sum(axis=1)/len([col for col in df_syllables_all.columns if col.startswith('2')])*100], axis=1)
df_assess_syllables = df_assess_syllables.rename(columns={0: 'score'})
df_assess_syllables = df_assess_syllables.groupby(df['valeur']).aggregate('mean').reset_index()
plt.figure(figsize=(8,6))
sns.stripplot(x='valeur', y='score', dodge=True, data=df_assess_syllables.sort_values(by=['score']), palette='dark').set(title='Mean score for each syllable')
df_assess_syllables.describe()

# Assess further du po te tu
df_assess_ind_syll = pd.concat([df.iloc[24:,1], df_syllables_all], axis=1)
df_assess_du = df_assess_ind_syll[df_assess_ind_syll['valeur']=='du'].T
df_assess_du.columns = ['first_try', 'second_try']
df_assess_du = df_assess_du[1:]
plt.figure(figsize=(8,6))
sns.histplot(x=df_assess_du['first_try'],
             stat='count', multiple='dodge', palette='dark', shrink=.7).set(title='Scores for syllable du')
sns.histplot(x=df_assess_du['second_try'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Scores for syllable du')

# Individual phonemes
list_all_scores = []
for phoneme in ['d', 'm', 'p', 't', 'a', 'e', 'o', 'u']:
    list_phoneme_scores = []
    for i_syll in df_assess_syllables.index:
        if phoneme in df_assess_syllables['valeur'].iloc[i_syll]:
            list_phoneme_scores.append(df_assess_syllables['score'].iloc[i_syll])
    list_all_scores.append(np.average(list_phoneme_scores))
df_assess_phonemes = pd.DataFrame({'phoneme':['d', 'm', 'p', 't', 'a', 'e', 'o', 'u'],'score':list_all_scores})
plt.figure(figsize=(8,6))
sns.stripplot(x='phoneme', y='score', dodge=True, data=df_assess_phonemes.sort_values(by=['score']), palette='dark').set(title='Mean score for each phoneme')
df_assess_phonemes.describe()