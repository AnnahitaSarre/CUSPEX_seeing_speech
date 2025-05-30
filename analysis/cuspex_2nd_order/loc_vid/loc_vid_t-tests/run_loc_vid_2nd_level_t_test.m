%%%%% Runs all 2nd order video localizer univariate analysis, with or without covariates %%%%%

clear
clc

% addpath(genpath('/home/laurent.cohen/spm12/'));

%% Parameters to modify

% Participants to analyse
subjects_g1 = [11 12 13 14 15 16 17 18 19 110 111 112 113 114 115 116 117 118 119];
subjects_g2 = [21 22 23 24 25 26 27 28 29 210 211 212 213 214 215 216 217 218 219 220 221];
subjects_g3 = [01 31 32 33 34 35 36 37 38 39 310 311 312 313 314 315 316 317 318 319];

% Group to analyse
groups = {'g1vg3'}; % 'g1+g2+g3', 'g1', 'g3', 'g1+g2', 'g2+g3', 'g1+g3', 'g1vg2', 'g2vg3', 'g1vg3', 'g1vg2+g3', 'g3vg1+g2'

% Smoothing level
smoothing_level = '4';

% Contrast to compute and corresponding con file numbers according to
% individual pipeline (comment uneeded contrasts)
contrasts_list = {...
%     {'Sound_LPC', 1}...
%     {'Silent_LPC', 2}...
%     {'Manual_cues', 3}...
%     {'Labial', 4}...
%     {'Pseudo', 5}...
%     {'Sound_LPC - Silent_LPC', 6}...
%     {'Silent_LPC - Sound_LPC', 7}...
%     {'Silent_LPC - Manual_cues', 8}...
%     {'Manual_cues - Silent_LPC', 9}...
%     {'Silent_LPC - Labial', 10}...
%     {'Labial - Silent_LPC', 11}...
%     {'Silent_LPC - Pseudo', 12}...
%     {'Pseudo - Silent_LPC', 13}...
%     {'Manual_cues - Labial', 14}...
%     {'Labial - Manual_cues', 15}...
    {'Pseudo - Labial', 17}...
    {'Pseudo - Manual cues', 18}...
    };

% Covariates to include (comment uneeded covariates)
covariates_list = [...
%                 {'sentences_all_scores'}...
%                 {'sentences_easy_scores'}...
%                 {'sentences_medium_scores'}...
%                 {'sentences_hard_scores'}...
%                 {'syllables_scores'}...
%                 {'age'}...
%                 {'sex'}...
%                 {'diplome'}...
%                 {'gr1_nb_appareils'}...
%                 {'gr1_lpc_niv_lecture'}...
%                 {'gr1_lpc_lecture_age'}...
%                 {'gr1_lpc_lecture_difficultes_yn'}...
%                 {'lpc_age'}...
%                 {'lpc_freq'}...
%                 {'lpc_niv_coder'}...
%                 {'lpc_niv_comprendre'}...
%                 {'lpc_niv_labial'}...
%                 {'lsf_yn'}...
%                 {'lsf_age'}...
%                 {'lsf_freq'}...
%                 {'lsf_niv_exprimer'}...
%                 {'lsf_niv_comprendre'}...
%                 {'lateralityscore'}...
%                 {'concentration_localizer'}...
%                 {'comprehension_lpc_son'}...
%                 {'comprehension_lpc_sans_son'}...
%                 {'comprehension_lpc_pseudo'}...
%                 {'comprehension_labial'}...
%                 {'comprehension_indices'}...
                ];


%% Define subject list

for i_group=1:numel(groups)
    
    group = groups{i_group};
    if strcmp(group,'g1+g2+g3')
        subjects_list = [subjects_g1, subjects_g2, subjects_g3];
    elseif strcmp(group,'g1')
        subjects_list = subjects_g1;
    elseif strcmp(group,'g2')
        subjects_list = subjects_g2;
    elseif strcmp(group,'g3')
        subjects_list = subjects_g3;
    elseif strcmp(group,'g1+g2')
        subjects_list = [subjects_g1, subjects_g2];
    elseif strcmp(group,'g1+g3')
        subjects_list = [subjects_g1, subjects_g3];
    elseif strcmp(group,'g2+g3')
        subjects_list = [subjects_g2, subjects_g3];
    elseif strcmp(group,'g1vg2')
        subjects_list = [{subjects_g1}, {subjects_g2}];
    elseif strcmp(group,'g2vg3')
        subjects_list = [{subjects_g2}, {subjects_g3}];
    elseif strcmp(group,'g1vg3')
        subjects_list = [{subjects_g1}, {subjects_g3}];
    elseif strcmp(group,'g1vg2+g3')
        subjects_list = [{subjects_g1}, {[subjects_g2, subjects_g3]}];
    elseif strcmp(group,'g3vg1+g2')
        subjects_list = [{subjects_g3}, {[subjects_g1, subjects_g2]}];
    end


    %% Select data of interest to create covariates' table
    % See how to create this mat file (indications in create_covariates.m)

    load('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_analysis_scripts/behavior/cuspex_covariates.mat');

    if ~isempty(covariates_list)
        % Retrieve the index of the column where 'subject' is stored
        for i_name=1:size(all_names, 2)
            if strcmp(all_names{i_name}, 'subject')
                id_col_index = i_name;
            end
        end
        % Flatten the list of particpants to handle cases with two groups
        if numel(subjects_list) == 2
            subjects_list_flat = cat(2,subjects_list{:});
        else
            subjects_list_flat = subjects_list;
        end
        % Select the considered participants
        group_R = [];
        for i_subject=1:numel(subjects_list_flat)
            for i_R_row=1:size(all_R,1)
                if all_R(i_R_row,id_col_index) == subjects_list_flat(i_subject)
                    group_R = [group_R ; all_R(i_R_row,:)];
                end
            end
        end
        % Select the considered covariate(s)
        R = [];
        names = {};
        for i_name = 1:length(all_names)
            if ismember(all_names{i_name}, covariates_list)
                names{end+1} = all_names{i_name};
                R = [R, group_R(:,i_name)];
            end
        end
        covariates = {names, R};
    else
        covariates = {};
    end


    %% Compute one model per contrast + group combination + covariates combination

    for i_contrast=1:numel(contrasts_list)
        contrast = contrasts_list{i_contrast};
        if contains(group,'v')
            matlabbatch_second_level_loc_vid_2g_t_test_job = second_level_loc_vid_2g_t_test_job(subjects_list, group, smoothing_level, contrast, covariates);
            spm_jobman('run', matlabbatch_second_level_loc_vid_2g_t_test_job);
        else
            matlabbatch_second_level_loc_vid_1g_t_test_job = second_level_loc_vid_1g_t_test_job(subjects_list, group, smoothing_level, contrast, covariates);
            spm_jobman('run', matlabbatch_second_level_loc_vid_1g_t_test_job);
        end
    end
end