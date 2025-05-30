%%%%% Contrasts of the static localizer experiment %%%%%

function matlabbatch = contrasts_loc_stat_job(subject, smoothing_dir)

    subject=num2str(subject,'%02.f');

    matlabbatch{1}.spm.stats.con.spmmat = {strcat('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images/CUSPEX_s', subject, '/func/loc_stat/stats/', smoothing_dir, '/SPM.mat')};

    matlabbatch{1}.spm.stats.con.consess{1}.tcon.name = 'Faces';
    matlabbatch{1}.spm.stats.con.consess{1}.tcon.weights = 1;
    matlabbatch{1}.spm.stats.con.consess{1}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{2}.tcon.name = 'Bodies';
    matlabbatch{1}.spm.stats.con.consess{2}.tcon.weights = [0 1];
    matlabbatch{1}.spm.stats.con.consess{2}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{3}.tcon.name = 'Words';
    matlabbatch{1}.spm.stats.con.consess{3}.tcon.weights = [0 0 1];
    matlabbatch{1}.spm.stats.con.consess{3}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{4}.tcon.name = 'Houses';
    matlabbatch{1}.spm.stats.con.consess{4}.tcon.weights = [0 0 0 1];
    matlabbatch{1}.spm.stats.con.consess{4}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{5}.tcon.name = 'Tools';
    matlabbatch{1}.spm.stats.con.consess{5}.tcon.weights = [0 0 0 0 1];
    matlabbatch{1}.spm.stats.con.consess{5}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{6}.tcon.name = 'Targets';
    matlabbatch{1}.spm.stats.con.consess{6}.tcon.weights = [0 0 0 0 0 1];
    matlabbatch{1}.spm.stats.con.consess{6}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{7}.tcon.name = 'Keypress';
    matlabbatch{1}.spm.stats.con.consess{7}.tcon.weights = [0 0 0 0 0 0 1];
    matlabbatch{1}.spm.stats.con.consess{7}.tcon.sessrep = 'repl';

    matlabbatch{1}.spm.stats.con.consess{8}.tcon.name = 'Faces-all';
    matlabbatch{1}.spm.stats.con.consess{8}.tcon.weights = [4 -1 -1 -1 -1];
    matlabbatch{1}.spm.stats.con.consess{8}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{9}.tcon.name = 'Bodies-all';
    matlabbatch{1}.spm.stats.con.consess{9}.tcon.weights = [-1 4 -1 -1 -1];
    matlabbatch{1}.spm.stats.con.consess{9}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{10}.tcon.name = 'Words-all';
    matlabbatch{1}.spm.stats.con.consess{10}.tcon.weights = [-1 -1 4 -1 -1];
    matlabbatch{1}.spm.stats.con.consess{10}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{11}.tcon.name = 'Houses-all';
    matlabbatch{1}.spm.stats.con.consess{11}.tcon.weights = [-1 -1 -1 4 -1];
    matlabbatch{1}.spm.stats.con.consess{11}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{12}.tcon.name = 'Tools-all';
    matlabbatch{1}.spm.stats.con.consess{12}.tcon.weights = [-1 -1 -1 -1 4];
    matlabbatch{1}.spm.stats.con.consess{12}.tcon.sessrep = 'repl';

    matlabbatch{1}.spm.stats.con.consess{13}.tcon.name = 'Faces-Bodies';
    matlabbatch{1}.spm.stats.con.consess{13}.tcon.weights = [1 -1];
    matlabbatch{1}.spm.stats.con.consess{13}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{14}.tcon.name = 'Bodies-Faces';
    matlabbatch{1}.spm.stats.con.consess{14}.tcon.weights = [-1 1];
    matlabbatch{1}.spm.stats.con.consess{14}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{15}.tcon.name = 'Faces-Words';
    matlabbatch{1}.spm.stats.con.consess{15}.tcon.weights = [1 0 -1];
    matlabbatch{1}.spm.stats.con.consess{15}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{16}.tcon.name = 'Words-Faces';
    matlabbatch{1}.spm.stats.con.consess{16}.tcon.weights = [-1 0 1];
    matlabbatch{1}.spm.stats.con.consess{16}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{17}.tcon.name = 'Bodies-Words';
    matlabbatch{1}.spm.stats.con.consess{17}.tcon.weights = [0 1 -1];
    matlabbatch{1}.spm.stats.con.consess{17}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{18}.tcon.name = 'Words-Bodies';
    matlabbatch{1}.spm.stats.con.consess{18}.tcon.weights = [0 -1 1];
    matlabbatch{1}.spm.stats.con.consess{18}.tcon.sessrep = 'repl';

    matlabbatch{1}.spm.stats.con.delete = 1;

end % function
