%%%%% GLM estimation and specification of the static localizer experiment %%%%%

function matlabbatch = model_loc_stat_job(subject, loc_stat_nb_scans_list, smoothing_level)

    if strcmp(smoothing_level, 'unsmoothed')
        smoothing_dir = smoothing_level;
        smoothing_prefix = '';
    else
        smoothing_dir = strcat('smoothed', smoothing_level);
        smoothing_prefix = strcat('s', smoothing_level);
    end

    matlabbatch{1}.spm.stats.fmri_spec.dir = {strcat('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images/CUSPEX_s', subject, '/func/loc_stat/stats/%s', smoothing_dir)};
    matlabbatch{1}.spm.stats.fmri_spec.timing.units = 'secs';
    matlabbatch{1}.spm.stats.fmri_spec.timing.RT = 1.66;
    matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t = 16;
    matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t0 = 8;

    num_run=1;
    scans = {};

    for volumes=1:loc_stat_nb_scans_list(num_run)
        scans{volumes} = sprintf('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images/CUSPEX_s%s/func/loc_stat/%sstatic.nii,%d',subject,smoothing_prefix,volumes);
    end

    scans = scans.';

    matlabbatch{1}.spm.stats.fmri_spec.sess(1).scans = scans;

    matlabbatch{1}.spm.stats.fmri_spec.sess(1).cond = struct('name', {}, 'onset', {}, 'duration', {}, 'tmod', {}, 'pmod', {}, 'orth', {});
    matlabbatch{1}.spm.stats.fmri_spec.sess(1).multi = {strcat('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images/CUSPEX_s', subject, '/func/loc_stat/LPC_res_loc_static_s', subject, '.mat')};
    matlabbatch{1}.spm.stats.fmri_spec.sess(1).regress = struct('name', {}, 'val', {});
    matlabbatch{1}.spm.stats.fmri_spec.sess(1).multi_reg = {strcat('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images/CUSPEX_s', subject, '/func/loc_stat/regressors_static.txt')};
    matlabbatch{1}.spm.stats.fmri_spec.sess(1).hpf = 128;


    matlabbatch{1}.spm.stats.fmri_spec.fact = struct('name', {}, 'levels', {});
    matlabbatch{1}.spm.stats.fmri_spec.bases.hrf.derivs = [0 0];
    matlabbatch{1}.spm.stats.fmri_spec.volt = 1;
    matlabbatch{1}.spm.stats.fmri_spec.global = 'None';
    matlabbatch{1}.spm.stats.fmri_spec.mthresh = 0.8;
    matlabbatch{1}.spm.stats.fmri_spec.mask = {''};
    matlabbatch{1}.spm.stats.fmri_spec.cvi = 'FAST';
    matlabbatch{2}.spm.stats.fmri_est.spmmat(1) = cfg_dep('fMRI model specification: SPM.mat File', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','spmmat'));
    matlabbatch{2}.spm.stats.fmri_est.write_residuals = 0;
    matlabbatch{2}.spm.stats.fmri_est.method.Classical = 1;

end
