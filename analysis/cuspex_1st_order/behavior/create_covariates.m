%%%%% Create covariate table to be used in the CUSPEX fMRI experiments %%%%%

clear
clc

all_names = {'subject','group'};
all_R = [[11 12 13 14 15 16 17 18 19 110 111 112 113 114 115 116 117 118 119 ...
    21 22 23 24 25 26 27 28 29 210 211 212 213 214 215 216 217 218 219 220 221 ...
    01 31 32 33 34 35 36 37 38 39 310 311 312 313 314 315 316 317 318 319]', ...
    [repelem(1,19,1); repelem(2,21,1); repelem(3,20,1)]];


%% Append decod mri task results

load('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_analysis_scripts/behavior/mri_tasks/behavior_decod_struct.mat');

% Only keep rows corresponding to all the runs
behavior_decod_struct = behavior_decod_struct(strcmp({behavior_decod_struct.run},'all_runs'));

% Append relevant column names to 'all_names'
decod_names = {'decod_hit_rate','decod_fa_rate','decod_dprime','decod_criterion','decod_mean_rt'};
all_names = [all_names, decod_names];

% Append corresponding data to 'all.R'
all_R = [all_R, cell2mat({behavior_decod_struct(:).hit_rate}'), cell2mat({behavior_decod_struct(:).fa_rate}'), ...
    cell2mat({behavior_decod_struct(:).dprime}'), cell2mat({behavior_decod_struct(:).criterion}'), cell2mat({behavior_decod_struct(:).mean_rt}')];


%% Append static localizer mri task results

load('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_analysis_scripts/behavior/mri_tasks/behavior_loc_stat_struct.mat');

% Append relevant column names to 'all_names'
loc_stat_names = {'loc_stat_hit_rate','loc_stat_fa_rate','loc_stat_dprime','loc_stat_criterion','loc_stat_mean_rt'};
all_names = [all_names, loc_stat_names];

% Append corresponding data to 'all.R'
all_R = [all_R, cell2mat({behavior_loc_stat_struct(:).hit_rate}'), cell2mat({behavior_loc_stat_struct(:).fa_rate}'), ...
    cell2mat({behavior_loc_stat_struct(:).dprime}'), cell2mat({behavior_loc_stat_struct(:).criterion}'), cell2mat({behavior_loc_stat_struct(:).mean_rt}')];


%% Append pretest results

% To regenerate the pretest results table from the csv, manually import it
% as table with text option = 'cell array of character vectors', not
% selecting the first line containing the column names and the first column
% containing the dataframe's indexes

load('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_analysis_scripts/behavior/pretest/pretest_comprehension_results.mat');

% Append relevant column names to 'all_names'
pretest_names = pretest_comprehension_results.Properties.VariableNames(3:end);
all_names = [all_names, pretest_names];

% Append corresponding data to 'all.R'
all_R = [all_R, NaN(size(all_R,1),length(pretest_names))];
for row_R=1:size(all_R,1) % Loop dans la matrice à remplir puis loop dans les résultats pour sélectionner le participant correspondant
    for row_pretest=1:size(pretest_comprehension_results,1)
        if all_R(row_R) == pretest_comprehension_results.('subject')(row_pretest)
            all_R(row_R,:) = [all_R(row_R,1:end-length(pretest_names)), pretest_comprehension_results{row_pretest,3:end}];
        end
    end
end


%% Append questionnaire results

% To regenerate the questionaire results table from the csv, manually import it
% as table with text option = 'cell array of character vectors', not
% selecting the first line containing the column names and the first column
% containing the dataframe's indexes

load('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_analysis_scripts/behavior/questionnaires/RedCap_data_processed/cuspex_tableau_final_covariates.mat');

% Append relevant column names to 'all_names'
questionnaire_names = cuspex_tableau_final_covariates.Properties.VariableNames(2:end);
all_names = [all_names, questionnaire_names];

% Append corresponding data to 'all.R'
all_R = [all_R, NaN(size(all_R,1),length(questionnaire_names))];
for row_R=1:size(all_R,1) % Loop dans la matrice à remplir puis loop dans les résultats pour sélectionner le participant correspondant
    for row_questionnaire=1:size(cuspex_tableau_final_covariates,1)
        if all_R(row_R) == cuspex_tableau_final_covariates.('subject')(row_questionnaire)
            all_R(row_R,:) = [all_R(row_R,1:end-length(questionnaire_names)), cuspex_tableau_final_covariates{row_questionnaire,2:end}];
        end
    end
end


%% Save final covariates table

save('cuspex_covariates.mat','all_names','all_R');
