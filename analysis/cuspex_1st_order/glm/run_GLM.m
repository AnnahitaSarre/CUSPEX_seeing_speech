%%%%% Runs all GLM %%%%%

clear
clc

% addpath('/home/laurent.cohen/spm12');
% spm_jobman('initcfg')


%% Parameters to modify

% Participants and scans to analyse
subjects_list = [113 114]; % Note: When you rerun a GLM, the corresponding contrasts are erased.

% Smoothing level
smoothing_level = 'unsmoothed'; % 'number' or 'unsmoothed'

% Number of volumes in each run
loc_vid_nb_scans_list = [400];
loc_stat_nb_scans_list = [400];

%% Subjects loop

for subject=subjects_list

    if mod(subject,2)==0  % Determine the number of the video the subject has seen during loc vid; Inverted for s31, s11 and s12!
        num_timetable='2'; % default = 2
    else
        num_timetable='1'; % default = 1
    end

    subject=num2str(subject,'%02.f');

    fprintf('\n####### Subject %s GLMs starting... #######\n\n', subject);

    %% Video localizer

%     fprintf('\n##### Video localizer GLM starting...\n');
%     matlabbatch_model_loc_vid = model_loc_vid_job(subject, loc_vid_nb_scans_list, smoothing_level, num_timetable);
%     spm_jobman('run', matlabbatch_model_loc_vid);
%     fprintf('\n##### Video localizer GLM completed.\n');


    %% Static localizer

%      fprintf('\n##### Static localizer GLM starting...\n');
%      matlabbatch_model_loc_stat = model_loc_stat_job(subject, loc_stat_nb_scans_list, smoothing_level);
%      spm_jobman('run', matlabbatch_model_loc_stat);
%      fprintf('\n##### Static localizer GLM completed.\n');

    fprintf('\n####### Subject %s GLMs done. #######\n\n', subject);

end
