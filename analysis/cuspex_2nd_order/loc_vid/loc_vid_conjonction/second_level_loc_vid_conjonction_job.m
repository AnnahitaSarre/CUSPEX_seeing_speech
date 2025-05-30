%%% One-way ANOVA for conjonction of two or three groups %%%

function matlabbatch = second_level_loc_vid_conjonction_job(subjects_list, group, smoothing_level, contrast, covariates)

    if ~isempty(covariates)
        covariates_name = covariates{1}(1);
        for i_covariate=2:numel(covariates{1})
            covariates_name = strcat(covariates_name, '+', covariates{1}{i_covariate});
        end
        contrast_dir_name = char(strcat(contrast{1}, " (", covariates_name,')'));
    else
        contrast_dir_name = contrast{1};
    end
   matlabbatch{1}.spm.stats.factorial_design.dir = {strcat('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_2nd_order/loc_vid/loc_vid_conjonction/results_s', smoothing_level, '/', contrast_dir_name, '/', group)};

    contrast_file_num = contrast{2};

    scans1 = {};
    for subject=1:numel(subjects_list{1})
       scans1{subject} = sprintf('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images/CUSPEX_s%02d/func/loc_vid/stats/smoothed_%s/con_00%02d.nii,1', subjects_list{1}(subject), smoothing_level, contrast_file_num);
    end
    scans1 = scans1.';
    matlabbatch{1}.spm.stats.factorial_design.des.anova.icell(1).scans = scans1;

    scans2 = {};
    for subject=1:numel(subjects_list{2})
       scans2{subject} = sprintf('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images/CUSPEX_s%02d/func/loc_vid/stats/smoothed_%s/con_00%02d.nii,1', subjects_list{2}(subject), smoothing_level, contrast_file_num);
    end
    scans2 = scans2.';
    matlabbatch{1}.spm.stats.factorial_design.des.anova.icell(2).scans = scans2;

    if numel(subjects_list) == 3
        scans3 = {};
        for subject=1:numel(subjects_list{3})
           scans3{subject} = sprintf('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images/CUSPEX_s%02d/func/loc_vid/stats/smoothed_%s/con_00%02d.nii,1', subjects_list{3}(subject), smoothing_level, contrast_file_num);
        end
        scans3 = scans3.';
        matlabbatch{1}.spm.stats.factorial_design.des.anova.icell(3).scans = scans3;
    end


    matlabbatch{1}.spm.stats.factorial_design.des.anova.dept = 0;
    matlabbatch{1}.spm.stats.factorial_design.des.anova.variance = 1;
    matlabbatch{1}.spm.stats.factorial_design.des.anova.gmsca = 0;
    matlabbatch{1}.spm.stats.factorial_design.des.anova.ancova = 0;


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
    matlabbatch{3}.spm.stats.con.consess{3}.tcon.name = strcat(contrast_name, ' G1');
    matlabbatch{3}.spm.stats.con.consess{3}.tcon.weights = [1 0];
    matlabbatch{3}.spm.stats.con.consess{4}.tcon.name = strcat(contrast_name, ' G2');
    matlabbatch{3}.spm.stats.con.consess{4}.tcon.weights = [0 1];
    if numel(subjects_list) > 2
        matlabbatch{3}.spm.stats.con.consess{5}.tcon.name = strcat(contrast_name, ' G3');
        matlabbatch{3}.spm.stats.con.consess{5}.tcon.weights = [0 0 1];
        matlabbatch{3}.spm.stats.con.consess{6}.tcon.name = strcat(contrast_name, ' G1-G3');
        matlabbatch{3}.spm.stats.con.consess{6}.tcon.weights = [1 0 -1];
        matlabbatch{3}.spm.stats.con.consess{7}.tcon.name = strcat(contrast_name, ' G3-G1');
        matlabbatch{3}.spm.stats.con.consess{7}.tcon.weights = [-1 0 1];
        matlabbatch{3}.spm.stats.con.consess{8}.tcon.name = strcat(contrast_name, ' G2-G3');
        matlabbatch{3}.spm.stats.con.consess{8}.tcon.weights = [0 1 -1];
        matlabbatch{3}.spm.stats.con.consess{9}.tcon.name = strcat(contrast_name, ' G3-G2');
        matlabbatch{3}.spm.stats.con.consess{9}.tcon.weights = [0 -1 1];
    end

    if ~isempty(covariates)
        for i_covariate=1:numel(covariates{1})
            matlabbatch{3}.spm.stats.con.consess{2+i_covariate}.tcon.name = char(strcat(contrast_name, " ", covariates{1}{i_covariate}));
            matlabbatch{3}.spm.stats.con.consess{2+i_covariate}.tcon.weights = [zeros(1,1+i_covariate), 1]; % The +1 is because there are two groups
        end
    end

end
