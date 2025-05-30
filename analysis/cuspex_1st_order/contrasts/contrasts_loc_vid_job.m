%%%%% Contrasts of the video localizer experiment %%%%%

function matlabbatch = contrasts_loc_vid_job(subject, smoothing_dir)

    subject=num2str(subject,'%02.f');

    matlabbatch{1}.spm.stats.con.spmmat = {strcat('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images/CUSPEX_s', subject, '/func/loc_vid/stats/', smoothing_dir,'/SPM.mat')};

    matlabbatch{1}.spm.stats.con.consess{1}.tcon.name = 'Sound LPC';
    matlabbatch{1}.spm.stats.con.consess{1}.tcon.weights = 1;
    matlabbatch{1}.spm.stats.con.consess{1}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{2}.tcon.name = 'Silent LPC';
    matlabbatch{1}.spm.stats.con.consess{2}.tcon.weights = [0 1];
    matlabbatch{1}.spm.stats.con.consess{2}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{3}.tcon.name = 'Manual cues';
    matlabbatch{1}.spm.stats.con.consess{3}.tcon.weights = [0 0 1];
    matlabbatch{1}.spm.stats.con.consess{3}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{4}.tcon.name = 'Labial';
    matlabbatch{1}.spm.stats.con.consess{4}.tcon.weights = [0 0 0 1];
    matlabbatch{1}.spm.stats.con.consess{4}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{5}.tcon.name = 'Pseudo';
    matlabbatch{1}.spm.stats.con.consess{5}.tcon.weights = [0 0 0 0 1];
    matlabbatch{1}.spm.stats.con.consess{5}.tcon.sessrep = 'repl';

    matlabbatch{1}.spm.stats.con.consess{6}.tcon.name = 'Sound LPC - Silent LPC';
    matlabbatch{1}.spm.stats.con.consess{6}.tcon.weights = [1 -1];
    matlabbatch{1}.spm.stats.con.consess{6}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{7}.tcon.name = 'Silent LPC - Sound LPC';
    matlabbatch{1}.spm.stats.con.consess{7}.tcon.weights = [-1 1];
    matlabbatch{1}.spm.stats.con.consess{7}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{8}.tcon.name = 'Silent LPC - Manual cues';
    matlabbatch{1}.spm.stats.con.consess{8}.tcon.weights = [0 1 -1];
    matlabbatch{1}.spm.stats.con.consess{8}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{9}.tcon.name = 'Manual cues - Silent LPC';
    matlabbatch{1}.spm.stats.con.consess{9}.tcon.weights = [0 -1 1];
    matlabbatch{1}.spm.stats.con.consess{9}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{10}.tcon.name = 'Silent LPC - Labial';
    matlabbatch{1}.spm.stats.con.consess{10}.tcon.weights = [0 1 0 -1];
    matlabbatch{1}.spm.stats.con.consess{10}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{11}.tcon.name = 'Labial - Silent LPC';
    matlabbatch{1}.spm.stats.con.consess{11}.tcon.weights = [0 -1 0 1];
    matlabbatch{1}.spm.stats.con.consess{11}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{12}.tcon.name = 'Silent LPC - Pseudo';
    matlabbatch{1}.spm.stats.con.consess{12}.tcon.weights = [0 1 0 0 -1];
    matlabbatch{1}.spm.stats.con.consess{12}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{13}.tcon.name = 'Pseudo - Silent LPC';
    matlabbatch{1}.spm.stats.con.consess{13}.tcon.weights = [0 -1 0 0 1];
    matlabbatch{1}.spm.stats.con.consess{13}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{14}.tcon.name = 'Manual cues - Labial';
    matlabbatch{1}.spm.stats.con.consess{14}.tcon.weights = [0 0 1 -1 0];
    matlabbatch{1}.spm.stats.con.consess{14}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{15}.tcon.name = 'Labial - Manual cues';
    matlabbatch{1}.spm.stats.con.consess{15}.tcon.weights = [0 0 -1 1 0];
    matlabbatch{1}.spm.stats.con.consess{15}.tcon.sessrep = 'repl';

    matlabbatch{1}.spm.stats.con.consess{16}.tcon.name = 'Silent_LPC - (Manual cues + Labial)';
    matlabbatch{1}.spm.stats.con.consess{16}.tcon.weights = [0 1 -1 -1];
    matlabbatch{1}.spm.stats.con.consess{16}.tcon.sessrep = 'repl';

    matlabbatch{1}.spm.stats.con.consess{17}.tcon.name = 'Pseudo - Labial';
    matlabbatch{1}.spm.stats.con.consess{17}.tcon.weights = [0 0 0 -1 1];
    matlabbatch{1}.spm.stats.con.consess{17}.tcon.sessrep = 'repl';
    matlabbatch{1}.spm.stats.con.consess{18}.tcon.name = 'Pseudo - Manual cues';
    matlabbatch{1}.spm.stats.con.consess{18}.tcon.weights = [0 0 -1 0 1];
    matlabbatch{1}.spm.stats.con.consess{18}.tcon.sessrep = 'repl';

    matlabbatch{1}.spm.stats.con.delete = 1;

end % function
