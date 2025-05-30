%%% Two samples t-test for comparing two groups %%%

function matlabbatch = second_level_loc_stat_2g_t_test_job(subjects_list, group, smoothing_level, contrast, covariates)

    if strcmp(smoothing_level, 'unsmoothed')
        smoothing_dir = smoothing_level;
        smoothing_prefix = 'unsmoothed';
    else
        smoothing_dir = strcat('smoothed_', smoothing_level);
        smoothing_prefix = strcat('s', smoothing_level);
    end
    
    if ~isempty(covariates)
        covariates_name = covariates{1}(1);
        for i_covariate=2:numel(covariates{1})
            covariates_name = strcat(covariates_name, '+', covariates{1}{i_covariate});
        end
        contrast_dir_name = char(strcat(contrast{1}, " (", covariates_name,')'));
    else
        contrast_dir_name = contrast{1};
    end
    matlabbatch{1}.spm.stats.factorial_design.dir = {strcat('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_2nd_order/loc_stat/loc_stat_t-tests/results_', smoothing_prefix, '/', contrast_dir_name, '/', group)};
    
    contrast_file_num = contrast{2};
    
    scans1 = {};
    for subject=1:numel(subjects_list{1})
       scans1{subject} = sprintf('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images/CUSPEX_s%02d/func/loc_stat/stats/%s/con_00%02d.nii,1', subjects_list{1}(subject), smoothing_dir, contrast_file_num);
    end
    scans1 = scans1.';
    matlabbatch{1}.spm.stats.factorial_design.des.t2.scans1 = scans1;

    scans2 = {};
    for subject=1:numel(subjects_list{2})
       scans2{subject} = sprintf('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images/CUSPEX_s%02d/func/loc_stat/stats/%s/con_00%02d.nii,1', subjects_list{2}(subject), smoothing_dir, contrast_file_num);
    end
    scans2 = scans2.';
    matlabbatch{1}.spm.stats.factorial_design.des.t2.scans2 = scans2;                                                       
                                                           
                                                           
    matlabbatch{1}.spm.stats.factorial_design.des.t2.dept = 0;
    matlabbatch{1}.spm.stats.factorial_design.des.t2.variance = 1;
    matlabbatch{1}.spm.stats.factorial_design.des.t2.gmsca = 0;
    matlabbatch{1}.spm.stats.factorial_design.des.t2.ancova = 0;
    
    
    if ~isempty(covariates)
        for i_covariate=1:numel(covariates{1})
            matlabbatch{1}.spm.stats.factorial_design.cov(i_covariate).c = covariates{2}(:,i_covariate);
            matlabbatch{1}.spm.stats.factorial_design.cov(i_covariate).cname = covariates{1}{i_covariate};
            matlabbatch{1}.spm.stats.factorial_design.cov(i_covariate).iCFI = 1;
            matlabbatch{1}.spm.stats.factorial_design.cov(i_covariate).iCC = 1;
        end
    else
        matlabbatch{1}.spm.stats.factorial_design.cov = struct('c', {}, 'cname', {}, 'iCFI', {}, 'iCC', {});
    end
    
    
    matlabbatch{1}.spm.stats.factorial_design.masking.tm.tm_none = 1;
    matlabbatch{1}.spm.stats.factorial_design.masking.im = 1;
    matlabbatch{1}.spm.stats.factorial_design.masking.em = {''};
    matlabbatch{1}.spm.stats.factorial_design.globalc.g_omit = 1;
    matlabbatch{1}.spm.stats.factorial_design.globalm.gmsca.gmsca_no = 1;
    matlabbatch{1}.spm.stats.factorial_design.globalm.glonorm = 1;
    
    matlabbatch{2}.spm.stats.fmri_est.spmmat(1) = cfg_dep('Factorial design specification: SPM.mat File', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','spmmat'));
    matlabbatch{2}.spm.stats.fmri_est.write_residuals = 0;
    matlabbatch{2}.spm.stats.fmri_est.method.Classical = 1;
    
    contrast_name = char(strcat(group, " ", contrast{1}));
    
    matlabbatch{3}.spm.stats.con.spmmat(1) = cfg_dep('Model estimation: SPM.mat File', substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','spmmat'));
    matlabbatch{3}.spm.stats.con.consess{1}.tcon.name = strcat(contrast_name, ' G1-G2');
    matlabbatch{3}.spm.stats.con.consess{1}.tcon.weights = [1 -1];
    matlabbatch{3}.spm.stats.con.consess{2}.tcon.name = strcat(contrast_name, ' G2-G1');
    matlabbatch{3}.spm.stats.con.consess{2}.tcon.weights = [-1 1];
    
    if ~isempty(covariates)
        for i_covariate=1:numel(covariates{1})
            matlabbatch{3}.spm.stats.con.consess{2+i_covariate}.tcon.name = char(strcat(contrast_name, " pos ", covariates{1}{i_covariate}));
            matlabbatch{3}.spm.stats.con.consess{2+i_covariate}.tcon.weights = [zeros(1,1+i_covariate), 1]; % The +1 is because there are two groups
            matlabbatch{3}.spm.stats.con.consess{3+i_covariate}.tcon.name = char(strcat(contrast_name, " neg ", covariates{1}{i_covariate}));
            matlabbatch{3}.spm.stats.con.consess{3+i_covariate}.tcon.weights = [zeros(1,1+i_covariate), -1];
        end
    end

end