#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

CUSPEX script for plotting correlations between mean individual fMRI activation withinn a region and a behavioral covariate
OUTPUT: Activation x covariate plots

"""
    
    
#%% Import modules

import os
import subprocess
import pandas as pd
import numpy as np
from mat4py import loadmat
import matplotlib.pyplot as plt
from matplotlib import colors


#%% Parameters to modify

task = 'loc_vid'
main_path = '/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis'
smoothing_level = '4'

# All lines in a given plot use the same covariate. Then loops are zipped and each position represents a line so the order matters!
# Masks were thresholded and saved directly in spm before running this script
plots_list = [
    {'cov_value': 'lpc_age', 'cov_name': 'age of cs learning', 'mask_files': ['sent_negcov_lpc_age_g2_mask.nii','lipreading_negcov_lpc_age_g2_mask.nii'],
                'mask_names': ['negative correlation between\nSentences > baseline activations in Hearing and age of cs learning',
                               'negative correlation between\nLip-reading > baseline activations in Hearing and age of cs learning'],
                'con_names': ['Sentences > baseline', 'Sentences > baseline'], 'con_nums': [2, 2], 'colors':['#6ce6e6', '#feff55']},
               {'cov_value': 'sentences_all_scores', 'cov_name': 'sentence comprehension score', 'mask_files': 2*['sent-pseudo_negcov_sentences_all_scores_g2_mask.nii'],
                              'mask_names': ['negative correlation between\nSentences > baseline activations in Hearing and sentence comprehension score',
                                             'negative correlation between\npseudo-Sentences > baseline activations in Hearing and sentence comprehension score'],
                              'con_names': ['Sentences > baseline', 'pseudo-Sentences > baseline'], 'con_nums': [2, 5], 'colors':['#606060', '#b5b5b5'], 'diff_color': '#6ce6e6'},
              
               {'cov_value': 'sentences_all_scores', 'cov_name': 'sentence comprehension score', 'mask_files': 2*['sent-pseudo_poscov_sentences_all_scores_g2_mask.nii'],
                              'mask_names': ['positive correlation between\nSentences > baseline activations in Hearing and sentence comprehension score',
                                             'positive correlation between\npseudo-Sentences > baseline activations in Hearing and sentence comprehension score'],
                              'con_names': ['Sentences > baseline', 'pseudo-Sentences > baseline'], 'con_nums': [2, 5], 'colors':['#606060', '#b5b5b5'], 'diff_color': '#e27169'},
                {'cov_value': 'sentences_all_scores', 'cov_name': 'sentence comprehension score', 'mask_files': ['sent_negcov_sent_all_scores_g2_mask.nii'],
                               'mask_names': ['negative correlation between\nSentences > baseline activations in Hearing and sentence comprehension score'],
                               'con_names': ['Sentences > baseline'], 'con_nums': [2], 'colors':['#6ce6e6']},
                {'cov_value': 'sentences_all_scores', 'cov_name': 'sentence comprehension score', 'mask_files': ['gestures_negcov_sentences_all_scores_g2_mask.nii'],
                                'mask_names': ['negative correlation between\nGestures > baseline activations in Hearing and sentence comprehension score'],
                                'con_names': ['Gestures > baseline'], 'con_nums': [3], 'colors':['#d02cdc']},
                {'cov_value': 'sentences_all_scores', 'cov_name': 'sentence comprehension score', 'mask_files': ['gestures_poscov_sentences_all_scores_g2_mask.nii'],
                                'mask_names': ['positive correlation between\nGestures > baseline activations in Hearing and sentence comprehension score'],
                                'con_names': ['Gestures > baseline'], 'con_nums': [3], 'colors':['#c83026']}
               ]

subjects = [
            # '11', '12', '13', '14', '15', '16', '17', '18', '19', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119',
            '21', '22', '23', '24', '25', '26', '27', '28', '29', '210', '211', '212', '213', '214', '215', '216', '217', '218', '219', '220', '221',
            # '01', '31', '32', '33', '34', '35', '36', '37', '38', '39', '310', '311', '312', '313', '314', '315', '316', '317', '318', '319'
            ]
groups_list = []
for subject in subjects:
    if subject.startswith('0'):
        groups_list.append(3)
    else:
        groups_list.append(int(subject[0]))
groups_array = np.asarray(groups_list)


#%% Import covariates

# Import mat file as df
mat_file = loadmat(os.path.join(main_path,'cuspex_analysis_scripts/behavior/cuspex_covariates.mat'))
df_cov = pd.DataFrame(mat_file.get('all_R'), columns=mat_file.get('all_names'))
df_cov['subject'] = df_cov[['subject']].astype(int).astype(str)
df_cov['group'] = df_cov[['group']].astype(int).astype(str)
df_cov.index = ['01' if sub == '1' else sub for sub in df_cov.index]
df_cov.set_index('subject', inplace=True)
df_cov = df_cov.loc[subjects]


#%% Mask and average all voxels in each participant

for plot_dict in plots_list:
    activation_diff = []
    cmap = colors.ListedColormap(plot_dict['colors'])
    for i_line in range(len(plot_dict['mask_files'])):
        mask_file = plot_dict['mask_files'][i_line]
        mask_path = os.path.join(main_path,'cuspex_2nd_order/masks/contrast_masks', mask_file)
        means_in_mask = {}
        for subject in subjects:
            subject_con = os.path.join(main_path,f"cuspex_final_images/CUSPEX_s{subject}/func/{task}/stats/smoothed_{smoothing_level}/con_{plot_dict['con_nums'][i_line]:04d}.nii")
            list_time_series = subprocess.check_output(f'fslmeants -i {subject_con} -m {mask_path} --showall', shell=True, encoding='UTF-8').split()
            if '-nan' in list_time_series:
                subject_glm_mask = '-k ' + os.path.join(main_path,f'cuspex_final_images/CUSPEX_s{subject}/func/{task}/stats/smoothed_{smoothing_level}/mask.nii')
                print('Nan present in time series: averaging in the participant mask')
            else:
                subject_glm_mask = ''
            mask_and_average = float(subprocess.check_output(f'fslstats {subject_con} -k {mask_path} {subject_glm_mask} -m', shell=True, encoding='UTF-8').split()[0])
            means_in_mask[subject] = mask_and_average
        df_cov['means_in_mask'] = pd.Series(means_in_mask)
        df_cov = df_cov.sort_values(by=plot_dict['cov_value'])
        if 'diff_color' in list(plot_dict.keys()):
            activation_diff.append(df_cov['means_in_mask'].to_list())
        
        
        #%% Plot result
        
        label = f"{plot_dict['con_names'][i_line]} in regions showing {plot_dict['mask_names'][i_line]}"
        plt.plot(df_cov[plot_dict['cov_value']], df_cov['means_in_mask'], marker='o', color=plot_dict['colors'][i_line], linestyle='none', markeredgecolor='black', label=label)
        slope, intercept = np.polyfit(df_cov[plot_dict['cov_value']], df_cov['means_in_mask'], 1)
        regression_line = slope * df_cov[plot_dict['cov_value']] + intercept
        plt.plot(df_cov[plot_dict['cov_value']], regression_line, linewidth=2, color=plot_dict['colors'][i_line])
        plt.plot(df_cov[plot_dict['cov_value']], regression_line, linewidth=0.5, color='black')
        plt.xlabel(f"{plot_dict['cov_name']}", fontsize=15)
        plt.ylabel('mean activation', fontsize=15)
        plt.legend(bbox_to_anchor=(0.5, -0.15), fontsize=15, title_fontsize=15, loc='upper center', borderaxespad=1.5)
    if 'diff_color' in list(plot_dict.keys()):
        activation_diff = [a - b for a, b in zip(activation_diff[0], activation_diff[1])]
        plt.plot(df_cov[plot_dict['cov_value']], activation_diff, marker='o', color=plot_dict['diff_color'], linestyle='none', markeredgecolor='black',
                 label=f"Individual activation difference between {plot_dict['con_names'][0]} and {plot_dict['con_names'][1]}")
        slope, intercept = np.polyfit(df_cov[plot_dict['cov_value']], activation_diff, 1)
        regression_line = slope * df_cov[plot_dict['cov_value']] + intercept
        plt.plot(df_cov[plot_dict['cov_value']], regression_line, linewidth=2, color=plot_dict['diff_color'])
        plt.plot(df_cov[plot_dict['cov_value']], regression_line, linewidth=0.5, color='black')
        plt.legend(bbox_to_anchor=(0.5, -0.15), fontsize=15, title_fontsize=15, loc='upper center', borderaxespad=1.5) 
    plt.show()