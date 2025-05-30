%% plot mean and SEM of contrasts, across subjects,
% for any number of experiments, groups of subjects, conditions, in or around a voxel
% 2 possible uses:
% 1/  with no argument plots at the current SPM coordinates
% 2/ with argument ([x y z]) plots at the xyz MNI coordinates
%
% LC april 2014, july 2018, modified by AS 2022
%
function [] = plot_voxel_profil(MNIcoords)

% addpath(genpath('/home/laurent.cohen/spm12/'));
% addpath(genpath('/home/laurent.cohen/MATLAB/R2018a/toolbox/mathworks_functions/barwitherr'));

%% parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% where to find 1st level contrast files

group_labels={'Deaf','Hearing','Controls'}; % labels for the plots (may be different from dir names)

smoothing_level = num2str(4);
subjects_g1 = [11 12 13 14 15 16 17 18 19 110 111 112 113 114 115 116 117 118 119];
subjects_g2 = [21 22 23 24 25 26 27 28 29 210 211 212 213 214 215 216 217 218 219 220 221];
subjects_g3 = [01 31 32 33 34 35 36 37 38 39 310 311 312 313 314 315 316 317 318 319];
subjects = {subjects_g1;subjects_g2;subjects_g3};

% 1st level stats dirs within subjects, for each experiment
axe_des_x={'Sound         Sentences         Gestures         Lipreading         Pseudo         Faces         Bodies         Words         Houses         Tools'};


%% which contrasts to plot

contrasts_list = {...
    {'Sound_LPC', 1, 'loc_vid'}...
    {'Silent_LPC', 2, 'loc_vid'}...
    {'Manual_cues', 3, 'loc_vid'}...
    {'Labial', 4, 'loc_vid'}...
    {'Pseudo', 5, 'loc_vid'}...
    {'Faces', 1, 'loc_stat'}...
    {'Bodies', 2, 'loc_stat'}...
    {'Words', 3, 'loc_stat'}...
    {'Houses', 4, 'loc_stat'}...
    {'Tools', 5, 'loc_stat'}...
    };

% their number in the 1st level model, for each experiment
% contrasts_num={[189 195 190 196 191 197], [ 95 101 96 102],[192 198 193 199 194 200],[ 98 104 99 105]};
% contrasts_weights=[1 1 1 1 1 1 2 2 2 2 1 1 1 1 1 1 2 2 2 2 ]; % in case the 1st level contrasts differ in their sum.

% their names (will only serve as labels in the plots)
% contrasts_labels= {...
% {'Sent Att','Sent UnAtt','List Att','List UnAtt','Cont Att','Cont UnAtt'},{'Sent2h Att','Sent2h UnAtt','List2h Att','List2h UnAtt'},...
% {'Sent Att','Sent UnAtt','List Att','List UnAtt','Cont Att','Cont UnAtt'},{'Sent2h Att','Sent2h UnAtt','List2h Att','List2h UnAtt'},...
%     };


%% other parameters

% odd number of voxels defining the edge of the cube, centered on the chosen voxel, in which data will be averaged
cubesize=1;


%% display of experiments as subplots

% grid of subplots
plot_cols=1; % 2
plot_rows=1; % 2
 %%% position of subplots
a={1}; % ,2,3,4
%%% plot position and dimensions
x0=10;
y0=10;
width=900;
height=600;

% save plots as image files
% save_plots=1;
plot_filename='cuspex_loc_vid_barchart'; % generic file name

% equate means across groups (within experiment)
equate_means=0; % leave at 0 or debug the plotting part below


%% end params %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

nbcon=length(contrasts_list);

nbsubj=0;
for i=1:length(subjects)
    nbsubj=nbsubj+length(subjects{i});
end

cs=(cubesize-1)/2 ;

% get coordinates
load( 'SPM.mat' ) ;
if nargin==0
    xyzmm=spm_mip_ui('GetCoords');
end
if nargin==1
    xyzmm=MNIcoords';
end

% iM = SPM.xVol.iM ;
matrice=[   -0.4000         0         0   37.0000
         0    0.4000         0   51.4000
         0         0    0.4000   29.8000];
% xyzvox = iM( 1:3, : ) * [ xyzmm ; 1 ] ;
xyzvox = matrice * [ xyzmm ; 1 ] ; % Makes the transition from the given MNI coordinates to the corresponding voxels in mm

% read data and fill a matrix of nbcon lines x nbsubj columns
matcon=zeros(nbcon,nbsubj);
sx=0;
for gr=1:length(subjects)
    for ss=1:length(subjects{gr})
        sx=sx+1;
        cx=0;
        for cc=1:length(contrasts_list)
            cx=cx+1;
            subject = subjects{gr}(ss);
            contrast_num = contrasts_list{cc}{2};
            contrast_dir = contrasts_list{cc}{3};
            confile=sprintf('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_final_images/CUSPEX_s%02d/func/%s/stats/smoothed_%s/con_00%02d.nii,1', subject, contrast_dir, smoothing_level, contrast_num);
            header = spm_vol(confile);
%             confile
%             display([sx cx])
            for u = (xyzvox(1)-cs):(xyzvox(1)+cs)
                for v = (xyzvox(2)-cs):(xyzvox(2)+cs)
                    for w = (xyzvox(3)-cs):(xyzvox(3)+cs)
                        matcon(cx,sx)=matcon(cx,sx)+spm_sample_vol(header, u, v, w, 0 ) ; % returns the voxel values at coordinates x,y,z
                    end
                end
            end
        end
    end
end

matcon=matcon/cubesize^3;
% matcon=contrasts_weights' .* matcon;

% subtract from matcon each subject's mean (for each experiment separately)
% (used to compute SEM)
matcon_demeaned=matcon*0;
xx=0;
% for man=1:length(contrasts_num)
%     cons_in_man=length(contrasts_num{man});
%     cons_nb(man)=cons_in_man;
%     mean_over_cons(man,:)=mean(matcon([xx+1:xx+cons_in_man],:),1);
%     matcon_demeaned([xx+1:xx+cons_in_man],:)=repmat(mean_over_cons(man,:),cons_in_man,1);
%     xx=xx+cons_in_man;
% end
cons_nb=length(contrasts_list);
mean_over_cons(:)=mean(matcon([xx+1:xx+cons_nb],:),1);
matcon_demeaned([xx+1:xx+cons_nb],:)=repmat(mean_over_cons(1,:),cons_nb,1);
xx=xx+cons_nb;

grand_mean=mean(mean_over_cons,2);

matcon_demeaned=matcon-matcon_demeaned;
% save('matcon_demeaned_aga','matcon_demeaned');

% compute for each group x contrast:
%           mean across subjects of matcon
%           and SEM across subjects of matcon_demeaned
xx=0;
for gr=1:length(subjects)
    subj_in_group=length(subjects{gr});
    if ~equate_means
        mean_over_ss(:,gr)=mean(matcon(:,[xx+1:xx+subj_in_group]),2);
    else
        mean_over_ss(:,gr)=mean(matcon_demeaned(:,[xx+1:xx+subj_in_group]),2);
    end
    SEM_over_ss(:,gr)=std(matcon_demeaned(:,[xx+1:xx+subj_in_group]),0,2)/sqrt(subj_in_group);
    xx=xx+subj_in_group;
end

% save('mean_over_ss','mean_over_ss');

% create one barchart per experiment
man_index=cell2mat(arrayfun(@(x,nx) repmat(x,1,nx), 1, cons_nb,'uniformoutput',0));
man_index=man_index';
fn=32;
figure(fn);clf;

%    if ~equate_means
%        y=mean_over_ss(man_index==man,:)+grand_mean(man);
%    else
    y=mean_over_ss(man_index==1,:);
%    end
posy=(y>=0);
errY=[];
errY(:,:,2)=SEM_over_ss(man_index==1,:);
errY(:,:,1)=errY(:,:,2);
errY(:,:,2)=errY(:,:,2).*posy;
errY(:,:,1)=errY(:,:,1).*(1-posy);
hold on
aga(1)=subplot(plot_cols,plot_rows,a{1}); % Annahita : rajouté le point-virgule et mis 1 à la place de man
[u,v]=barwitherr(errY, y); % Annahita : fonction à télécharger sur Mathworks
set (fn,'Color','w'); % background
% length(y)

set(gca,'XTick',[1:cons_nb],'XTickLabel',axe_des_x,...
    'FontSize', 12,'fontweight','n','LineWidth',2); % axes (fontweight can be b)
set(gca,'XTick',[1:5],'XTickLabel','',...
    'FontSize', 9,'fontweight','n','LineWidth',2); % axes (fontweight can be b)

% 'Ticklength', [0 0],
set(u,'LineWidth',2); % bars
set(v,'LineWidth',2); % error bars

% control the color of individual bars
col1=[0.4660 0.6740 0.1880]; % odd
col2=[0.8500 0.3250 0.0980]; % even
% u.FaceColor = 'flat';
if length(y)==6
    u.CData([1 3 5],:) = [col1;col1;col1];
    u.CData([2 4 6],:) = [col2;col2;col2];
end
if length(y)==4
    u.CData([1 3],:) = [col1;col1];
    u.CData([2 4],:) = [col2;col2];
end

%
%ylim([0 40])
% if length(subjects)>1
%     legend(group_labels,'Location','Best','Orientation','vertical')
% end
ylabel('BOLD signal','FontName','FixedWidth','FontWeight','bold')
xlabel(axe_des_x,'FontName','FixedWidth','FontWeight','bold')
colormap summer % jet gray cool etc
%YLstr = sprintf( [experiment_labels{man} ' at MNI [%g, %g, %g] in a cube of edge %g' ], round(xyzmm), cubesize ) ;
YLstr = sprintf( ['Activations at MNI [%g, %g, %g]' ], round(xyzmm)) ;
title( YLstr, 'FontSize', 12, 'FontName','FixedWidth','FontWeight','bold')
set(gcf,'units','points','position',[x0,y0,width,height])

hold off

saveas(fn, [plot_filename '-' num2str(fn) '.png'],'png');


%%%%%
linkaxes(aga(1),'y');
