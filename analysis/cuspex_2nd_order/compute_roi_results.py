#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

CUSPEX script for averaging voxel values in all ROIs for a given contrast
OUTPUT: One csv file per contrast with ROIs as columns and subjects as lines,
to be used in analyse_roi_results.py

"""
    
    
#%% Import modules

import os
from pathlib import PurePath
import subprocess
from glob import glob
from tqdm import tqdm
import pandas as pd
import numpy as np


#%% Parameters to modify

task = 'loc_vid'
main_path = '/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images'
smoothing_level = '4'
subjects = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119',
            '21', '22', '23', '24', '25', '26', '27', '28', '29', '210', '211', '212', '213', '214', '215', '216', '217', '218', '219', '220', '221',
            '01', '31', '32', '33', '34', '35', '36', '37', '38', '39', '310', '311', '312', '313', '314', '315', '316', '317', '318', '319']
groups_list = []
for subject in subjects:
    if subject.startswith('0'):
        groups_list.append(3)
    else:
        groups_list.append(int(subject[0]))
groups_array = np.asarray(groups_list)
col_order = ['group','occ_pole_l', 'occ_pole_r', 'occ_inf_l', 'occ_inf_r', 'occ_lat_l', 'occ_lat_r',
             'fusiform_l', 'fusiform_r',
             'IFGop_l', 'IFGop_r', 'IFGorb_l', 'IFGorb_r',
             'STSpost_l', 'STSpost_r', 'STGpost_l', 'STGpost_r',
             'STSmid_l', 'STSmid_r',
             'STSant_l', 'STSant_r', 'STGant_l', 'STGant_r', 'STGant++_l', 'STGant++_r',
             'IPS_l', 'IPS_r', 'FEF_l', 'FEF_r',
             'precentral_l', 'precentral_r', 'SMA_l', 'SMA_r',
             'cerebellum_inf_l', 'cerebellum_inf_r', 'cerebellum_sup_l', 'cerebellum_sup_r',
             'EBA_l', 'EBA_r', 'FFA_l', 'FFA_r', 'VWFA_l', 'VWFA_r']


#%% Retrieve ROI masks

masks_path = os.path.join(main_path,f'CUSPEX_s214/func/*/stats/smoothed_{smoothing_level}/voi/*')
mask_cons = [full_path.partition('func/')[2] for full_path in glob(os.path.join(masks_path,'*_mask.nii'))]
col_names = [os.path.basename(mask_col)[os.path.basename(mask_col).index('VOI_') + 4 : os.path.basename(mask_col).index('_mask.nii')] for mask_col in mask_cons]


#%% Mask and average all voxels in each participant

nb_cons = 16 if task == 'loc_vid' else 18
for con_num in tqdm(range(1,nb_cons+1)):
    con_list = []
    for mask_con in tqdm(mask_cons):
        mean_in_roi = []
        for subject in subjects:
            subject_roi_mask = os.path.join(main_path,f'CUSPEX_s{subject}/func',mask_con)
            subject_con = os.path.join(main_path,f'CUSPEX_s{subject}/func/{task}/stats/smoothed_{smoothing_level}/con_{con_num:04d}.nii')
            list_time_series = subprocess.check_output(f'fslmeants -i {subject_con} -m {subject_roi_mask} --showall', shell=True, encoding='UTF-8').split()
            if '-nan' in list_time_series:
                subject_glm_mask = '-k ' + os.path.join(main_path,f'CUSPEX_s{subject}/func/{task}/stats/smoothed_{smoothing_level}/mask.nii')
            else:
                subject_glm_mask = ''
            mask_and_average = float(subprocess.check_output(f'fslstats {subject_con} -k {subject_roi_mask} {subject_glm_mask} -m', shell=True, encoding='UTF-8').split()[0])
            mean_in_roi.append(mask_and_average)
        con_list.append(mean_in_roi)
    df_con = pd.DataFrame(np.asarray(con_list).T, columns=col_names, index=subjects)
    df_con.insert(0, 'group', groups_array)
    df_con = df_con[col_order]
    df_con.to_csv(f'{task}/{task}_roi_analysis/results_s{smoothing_level}/roi_analysis_results_con_{con_num:04d}.csv')