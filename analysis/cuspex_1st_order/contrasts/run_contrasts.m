%%%%% Runs all contrast analysis %%%%%

clear
clc


%% Parameter to modify

subjects_list = [11 12 13 14 15 16 17 18 19 110 111 112 113 114 115 116 117 118 119 ...
    21 22 23 24 25 26 27 28 29 210 211 212 213 214 215 216 217 218 219 220 221 ...
    01 31 32 33 34 35 36 37 38 39 310 311 312 313 314 315 316 317 318 319];

smoothing_dir = 'smoothed_4'; % 'smoothed_n' or 'unsmoothed'


%% Subjects loop

for subject=subjects_list

    subject=num2str(subject,'%02.f');

    fprintf('\n####### Subject %s contrasts starting... #######\n\n', subject);

    %% Video localizer

    fprintf('\n##### Video localizer contrasts starting...\n');
    matlabbatch_contrasts_loc_vid = contrasts_loc_vid_job(subject, smoothing_dir);
    spm_jobman('run', matlabbatch_contrasts_loc_vid);
    fprintf('\n##### Video localizer contrasts completed.\n');


    %% Static localizer

     fprintf('\n##### Static localizer contrasts starting...\n');
     matlabbatch_contrasts_loc_stat = contrasts_loc_stat_job(subject, smoothing_dir);
     spm_jobman('run', matlabbatch_contrasts_loc_stat);
     fprintf('\n##### Static localizer contrasts completed.\n');

     fprintf('\n####### Subject %s contrasts done. #######\n\n', subject);


end
