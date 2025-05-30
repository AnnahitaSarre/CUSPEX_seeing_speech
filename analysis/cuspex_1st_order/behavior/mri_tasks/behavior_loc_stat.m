%%%%% Single subject behavioral analysis of the static experiment: writes a csv with all the results (one row = one subject) %%%%%


clear
clc


%% Modifiable variables

list_subjects = [11 12 13 14 15 16 17 18 19 110 111 112 113 114 115 116 117 118 119 ...
    21 22 23 24 25 26 27 28 29 210 211 212 213 214 215 216 217 218 219 220 221 ...
    01 31 32 33 34 35 36 37 38 39 310 311 312 313 314 315 316 317 318 319];
files_main_path = '/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images';


%% Initialize the structure log

nb_subjects = length(list_subjects);

log_structure(nb_subjects) = struct('group', [], 'subject', [], 'nb_trials', [], ...
    'nb_hits', [], 'nb_misses', [], 'nb_fa', [], ...
    'hit_rate', [], 'fa_rate', [], 'dprime', [], 'criterion', [], ...
    'mean_rt', [], 'std_rt', [], 'median_rt', [], 'list_rt', []);


%% For each subject...

for subject=1:nb_subjects

        % (Re)initialize subject counters
        nb_hits = 0;
        nb_miss = 0;
        nb_fa = 0;
        subject_list_rt = [];

        % Load the run's file
        subject_file = fullfile(files_main_path, sprintf('CUSPEX_s%02d/func/loc_stat/LPC_res_loc_static_s%02d.mat', list_subjects(subject), list_subjects(subject)));
        load(sprintf(subject_file));

        % Append basic info to the struct log
        log_structure(subject).subject = subjid;
        if startsWith(subjid,'1')
            log_structure(subject).group = '1';
        elseif startsWith(subjid,'2')
            log_structure(subject).group = '2';
        else
            log_structure(subject).group = '3';
        end

        % Analyse the subject's responses, with 0.3 < resp < 1.3
        for row=1:size(result.log, 2)
            if result.log(row).SDT == 1
                nb_hits = nb_hits + 1;
                subject_list_rt = [subject_list_rt, result.log(row).resp];
            elseif result.log(row).SDT == 2
                nb_miss = nb_miss + 1;
            end
            if (result.log(row).odd == 0) && ~isempty(result.log(row).key)
                nb_fa = nb_fa + 1;
            end
        end

        % Compute d' and criterion
        nb_trials = size(result.log, 2);
        hit_rate = nb_hits/(nb_trials/2); % Same nb of target and non-target blocks hence the /2
        fa_rate = nb_fa/(nb_trials/2);
        if hit_rate == 1 % See https://fr.mathworks.com/matlabcentral/answers/1566863-how-do-i-get-matlab-to-display-the-d-when-my-hit-rate-1-using-the-norminv-function
            hit_rate = 1-1/(2*nb_trials/2);
        elseif hit_rate == 0
            hit_rate = 1/(2*nb_trials/2);
        end
        if fa_rate == 1
            fa_rate = 1-1/(2*nb_trials/2);
        elseif fa_rate == 0
            fa_rate = 1/(2*nb_trials/2);
        end
        dprime = norminv(hit_rate)-norminv(fa_rate);
        criterion = -0.5*(norminv(hit_rate)+ norminv(fa_rate));

        % Log in the responses information for the subject
        log_structure(subject).nb_trials = nb_trials;
        log_structure(subject).nb_hits = nb_hits;
        log_structure(subject).nb_misses = nb_miss;
        log_structure(subject).nb_fa = nb_fa;
        log_structure(subject).hit_rate = hit_rate;
        log_structure(subject).fa_rate = fa_rate;
        log_structure(subject).dprime = dprime;
        log_structure(subject).criterion = criterion;
        log_structure(subject).mean_rt = mean(subject_list_rt);
        log_structure(subject).std_rt = std(subject_list_rt);
        log_structure(subject).median_rt = median(subject_list_rt);
        log_structure(subject).list_rt = subject_list_rt;

end

% Rename and save structure
behavior_loc_stat_struct = log_structure;
save('behavior_loc_stat_struct', 'behavior_loc_stat_struct')

writetable(struct2table(behavior_loc_stat_struct), 'behavior_loc_stat.csv');
