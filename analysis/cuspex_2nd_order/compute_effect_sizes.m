%%% Compute activation effect sizes %%%

function activation_effect_sizes(varargin)

    addpath(genpath('/home/laurent.cohen/spm12/'));
    addpath(genpath('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_2nd_order/loc_vid'));
    addpath(genpath('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_2nd_order/loc_stat'));

    pause(100); % wait until all batches have added the paths
    
    if isempty(varargin)
		error('No inputs provided.');
    end
    con_path = varargin{1};
    con_name = varargin{2};

    groups = {'g1+g2+g3', 'g1', 'g2', 'g3', 'g1+g2', 'g2+g3', 'g1+g3', 'g1vg2', 'g2vg3', 'g1vg3', 'g1vg2+g3', 'g3vg1+g2'};

    fprintf('\n##### Processing %s \n', con_name);
    con_path = fullfile(con_path,con_name);

    for group=1:length(groups)
        group_name = groups{group};
        fprintf('\n## Processing %s \n', group_name);
        group_con_path = fullfile(con_path,group_name);
        output_name = fullfile(group_con_path,'effect_size');
        mask = spm_vol(fullfile(group_con_path,'mask.nii'));
        if exist(strcat(output_name, '_g.nii'), 'file') == 2
            disp('Output found, skipping analysis.');
        else
            t_map = spm_vol(fullfile(group_con_path,'spmT_0001.nii'));
            SPM = load(fullfile(group_con_path,'SPM.mat'));
            con = SPM.SPM.xCon.c;
            X = SPM.SPM.xX.xKXs.X;
            confLevel = 0.95;
            es_ci_spm(t_map, con, X, mask, confLevel, output_name)
        end
    end
    fprintf('\n##### %s done\n', con_name);
end
