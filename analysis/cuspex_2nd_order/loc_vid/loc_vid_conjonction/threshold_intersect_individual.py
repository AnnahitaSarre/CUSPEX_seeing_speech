#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CUSPEX script to threshold and binarize individual contrasts, then compute their intersection

Only works with two contrasts (at the intersection level)!
"""

#%% Import modules

import os
import subprocess


#%% Parameters to modify

task = 'loc_vid'
main_path = '/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis'
smoothing_level = '4'
subjects = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119',
            '21', '22', '23', '24', '25', '26', '27', '28', '29', '210', '211', '212', '213', '214', '215', '216', '217', '218', '219', '220', '221',
            '01', '31', '32', '33', '34', '35', '36', '37', '38', '39', '310', '311', '312', '313', '314', '315', '316', '317', '318', '319']
con_dict_loc_vid = {
    # 'Sound_LPC': 1,
    # 'Silent_LPC': 2,
    # 'Manual_cues': 3, 'Labial': 4,
    # 'Pseudo': 5,
    # 'Sound_LPC - Silent_LPC': 6, 'Silent_LPC - Sound_LPC': 7,
    'Silent_LPC - Manual_cues': 8,
    # 'Manual_cues - Silent_LPC': 9,
    'Silent_LPC - Labial': 10,
    # 'Labial - Silent_LPC': 11, 'Silent_LPC - Pseudo': 12,
    # 'Pseudo - Silent_LPC': 13, 'Manual_cues - Labial': 14, 'Labial - Manual_cues': 15
    }
threshold = 2 # Because the df is very high, we consider that 10-3: 3, 10-2: 2 and 5*10-2: 1


#%% Threshold and binarize contrasts, then compute the intersection of the two

for subject in subjects:
    maps_to_conj = []
    for con in con_dict_loc_vid:
        subject_con = os.path.join(main_path,f"cuspex_final_images/CUSPEX_s{subject}/func/{task}/stats/smoothed_{smoothing_level}/spmT_{con_dict_loc_vid[con]:04d}.nii")
        thr_bin_file = os.path.join(main_path,f"cuspex_final_images/CUSPEX_s{subject}/func/{task}/stats/smoothed_{smoothing_level}/spmT_{con_dict_loc_vid[con]:04d}_thr{threshold}_bin.nii")
        subprocess.check_output(f'FSLOUTPUTTYPE=NIFTI fslmaths {subject_con} -thr {threshold} -bin {thr_bin_file}', shell=True, encoding='UTF-8')
        maps_to_conj.append(thr_bin_file)
    conj_file = os.path.join(main_path,f"cuspex_final_images/CUSPEX_s{subject}/func/{task}/stats/smoothed_{smoothing_level}/spmT_conj_thr{threshold}.nii")
    subprocess.check_output(f'FSLOUTPUTTYPE=NIFTI fslmaths {maps_to_conj[0]} -mul {maps_to_conj[1]} {conj_file}', shell=True, encoding='UTF-8')


#%% Statistical analysis

# See group_comparisons_int_job.m