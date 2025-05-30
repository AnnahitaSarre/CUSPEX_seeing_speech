% Exp LPC localizer static (CENIR Prisma).
% Annahita Sarre, adapted from scripts by Fabien Hauw and Minye Zhan
% 04/2021
% Press ESCAPE to exit

%% Parameters for psychtoolbox
% deviceIndex=7; % 7 index is for the linux computer in the lab
deviceIndex=-1; % this index is for the CENIR.
KbName('UnifyKeyNames');
% pkg load statistics; %Octave specific: uncomment for octave
AssertOpenGL;
skipscreencheck=0; % skip psychtoolbox screen test 1 or not 0

%% Collect subject info

subjno=input('Please input date (YYYY_MM_DD): ', 's');
subjid=input('Please input subject id: ', 's');
inputrunnum=input('Please input the run number: ','s');
runnum=str2double(inputrunnum); % the current run number
main_path=pwd;
cd ..
main_path2=pwd;
cd (main_path)
dirdata=fullfile(main_path2,'LPC_results/LPC_results_localizer_static/');
file_name=sprintf('LPC_res_loc_static_%s_%s.mat',subjno,subjid);

%% Values specific to the scanner environment.
% define screen size
distance=120;% in cm. temporary // CENIR MRI = 120cm
screenwid=51; % in cm. temporary // CENIR MRI = 51cm
screenpx=1920; % in px. temporary // CENIR MRI = 1920px

%% Parameters of the stimulation protocol
% runnum=1; % number of runs
nconditions=5;
catcodes={'Face';'Body';'Word';'House';'Tool';'Target';'Keypress'};
names={'Face';'Body';'Word';'House';'Tool';'Target';'Keypress'};
motor_cat_num=7;
nrepetition=12; % number of repetitions (=nb of miniblocks) per condition
n_stim_in_block=20; % number of stimuli in each block
n_stim_in_cat=20; %number of stimuli in each category
%nrestblocks=0; %number of resting blocks, included in nconditions2.
first_pos_oddball=6; % this stimulus is the first which may be replaced with an oddball
nblocks=nconditions*nrepetition;
%nblocks2=nconditions1*nrepetition1 + nconditions2*nrepetition2 - nrestblocks;

num_blank=101;
num_oddball=102;


%% contents of the instruction screen, modify here.

text_waiting_for_ttl='En attente du signal de l''irm'; % lower line
textinstruct='Fixez la croix. Appuyez sur le bouton quand vous voyez une etoile.'; % upper line

%% define the corresponding keys of the button box here
% use KbName('KeyNames') to check the key correspondence in the current system
trigger='t'; % scanner trigger key value
esckey='ESCAPE'; % escape key
spacekey='space'; % space key
button1='b'; % MR response buttons

% mapping response buttons defined above.
% here, b, y, g, r, ,< mapped to value 1-5;
keysOfInterestResp=zeros(1,256);
keysResp={esckey, button1};
keysOfInterestResp(KbName(keysResp))=1;
keycodemapping=zeros(1,256);
keycodemappingind=zeros(1,length(keysResp)-1);

for kmind=2:length(keysResp)
    keycodemappingind(kmind-1)=KbName(keysResp{kmind});
    keycodemapping(KbName(keysResp{kmind}))=kmind-1;
end

%% Stimuli size definition
stimsize=22/640*screenpx; % font size, not used in the script (used pictures instead)
stimcolor=[128 128 128]; % font color
instructsize=40; % instruction font size

% theta=atan(stimwidth/2/distance)*180/pi*2; % for calculating visual
% angles. stimwidth is in cm. theta is in degrees (not radius).

%% Temporal parameters
fixationstart=6;  % fixation at the start of the run. set to 1 or 0 when debugging
fixationend=6;  % fixation after the last ITI  %/!!!!!!!!/ 6
jitter_values=5; % durations in seconds between miniblocks, mean set to 6 (see line 142-246)
fix_duration=0.2; % in seconds
stim_duration=0.1;
minresp=0.15; % min RT considered valid
maxresp=2.5; % max RT considered valid

approx_duration= fixationstart + fixationend*nrepetition + ((nconditions)* nrepetition * (n_stim_in_block * (fix_duration + stim_duration) + jitter_values));
% this computes the length per run.

%% load stimuli file
load('stimloc.mat');% % 102 stim pictures, 20(stimuli)*5(categories)+1(blank)+1(star)

% Set the rand method
% rdsetting=rng('shuffle');
%rng('shuffle'); % octave specific: comment this;

%% Block randomization:
blocklist=repmat(1:nconditions,nrepetition,1);
blocklist=blocklist(:);

% Pick oddball blocks; pick half of the repetitions per condition (in the case of odd repetition number: half-1);
condrandlist=cat(1,ones(floor(nrepetition/2),1),zeros(nrepetition-floor(nrepetition/2),1));
oddassign=[];

for condind=1:nconditions
    condtemp=condrandlist(NRandPerm(nrepetition,nrepetition)); %conrandlist=vector of nrepetition1 number between 0&1 (1 0 0 1) for example, if you call conrandlist(4) = 1
    oddassign=cat(2,oddassign,condtemp);
end
% currentoddassign=cat(2,ones(1,7*nrepetition),zeros(1,repetition)); % for debugging target presentation;
currentoddassign=oddassign(:);

% Randomize the block orders; currentoddassign linked to the original blocklist;
blockorder=NRandPerm(nblocks,nblocks);

%% Add trial info to the log file
% definition of log fields
log(nblocks).category=[]; % categories, value: 1-5
log(1).catcontent=[]; % categories in text, see catcodes below.
log(1).odd=[]; % 1=oddball (star); 0=no oddball;
log(1).oddnum=[]; % n-th stimulus replaced by the star;
log(1).oddtime=[];
log(1).nbblockcat=[]; % cumulative number of this cat;
log(1).resp=[]; % first button press RT from the star stimulus onset; for no-oddball blocks: RT from block onset;
log(1).resptime=[]; % button press time from the first scanner trigger
log(1).key=[]; % pressed button by the participant
log(1).SDT=[]; % 0.3<resp<1.3: 1=hit; otherwise: 2=miss;
log(1).blockstart=[]; % block onset time, time lapsed from the first scanner trigger
log(1).blockend=[];
log(1).resttime=[];
log(1).restduration=[];
log(1).duration=[];
log(1).duration2=[];
log(1).contentindtemp=[];
progSent='The paradigm has done block %d/%d\n';

%  event time data;
pict(1200).category=[];
pict(1).catcontent=[];
pict(1).start=[];
pict(1).end=[];
pict(1).duration=[];
pict(1).stim=[];

% motor time data;
MotResp(30).press=[];
MotResp(1).block=[];
MotResp(1).presstime=[];
MotResp(1).onsets=[];
MotResp(1).key=0;
MotResp(1).timerelease=0;
MotResp(1).end=0;

% odds/press/release time data;
odds(1).pressedkey=[];
odds(1).onsets=[];
odds(1).end=[];
odds(1).duration=[];
j=0;

data(1).press=[];
data(1).pressedkey=[];
data(1).onsets=[];
data(1).end=[];
data(1).duration=[];

for blockind=1:nblocks
    tempID=blockorder(blockind); %takes the nth block of blockorder
    categoryind=blocklist(tempID); %takes the 'tempID'th element of blocklist
    log(blockind).category=categoryind;
    log(blockind).catcontent=catcodes{categoryind};
    log(blockind).odd=currentoddassign(tempID);
    log(blockind).nbblockcat=length(find([log.category]==categoryind));
    nbblockcat=length(find([log.category]==categoryind));
    contentindtemp=n_stim_in_cat*(categoryind-1)+1:n_stim_in_cat*(categoryind);
    log(blockind).content(:,1)=contentindtemp(NRandPerm(n_stim_in_cat,n_stim_in_block))';
    log(blockind).contentindtemp=contentindtemp;
    log(blockind).content(:,2)=0; % flag of oddball stimulus within a block

    if log(blockind).odd==1
        oddnumpick=RandSel(first_pos_oddball:n_stim_in_block,1); % pick one stimulus as the oddball
        log(blockind).oddnum=oddnumpick;
        log(blockind).content(oddnumpick,1)=num_oddball;% oddball content: index of the star
        log(blockind).content(oddnumpick,2)=1; % flag of the odd;
    end
end

%% display trials
screens=Screen('Screens');
screen_index = 1; %max(screens); % CENIR MRI = 1 (if only one screen = 0)

white = WhiteIndex(screen_index);
try
    Priority(1);
    LoadPsychHID;
    Screen('Preference', 'SkipSyncTests', skipscreencheck); % set to 1 only when debugging
    PsychImaging('PrepareConfiguration');
    [w,rect]=PsychImaging('OpenWindow',screen_index,[0 0 0]); % black BG
    Screen('BlendFunction',w,GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA);
    Screen('Preference', 'DefaultFontSize', instructsize);
    Screen('Preference', 'DefaultFontStyle',1);
    Screen('Preference', 'TextRenderer',1);
    Screen('Preference', 'DefaultFontName','Courier New');
    Screen('Preference', 'VisualDebugLevel',3); % skip the psychtoolbox welcome screen
    HideCursor;
    sxsize=rect(3); % window size
    sysize=rect(4);
    [cx, cy] = RectCenter(rect);
    fixCrossDimPix = sxsize/50; %or = 40;
    xCoords = [0 0 -fixCrossDimPix/2 fixCrossDimPix/2];
    yCoords = [fixCrossDimPix/2 -fixCrossDimPix/2 0 0];
    allCoords = [xCoords; yCoords];
    lineWidthPix = sxsize/450;
    Screen('DrawLines', w, allCoords, lineWidthPix, white, [cx cy],2);

    hz=Screen('FrameRate',w); % stimuli are presented by numbers of frames
    ifi=Screen('GetFlipInterval',w,100);
    stimflipnum=stim_duration/ifi-0.5;
    fixflipnum=fix_duration/ifi-0.5;

    exp_term=0; % flag for exiting

    for i=1:length(stimloc)
        stimloc1(i)=Screen('MakeTexture',w,stimloc(i).img);
    end

    pictblk=Screen('MakeTexture',w,stimloc(num_blank).img); % blank
    pictstar=Screen('MakeTexture',w,stimloc(num_oddball).img); % star

    % Instruction screen
    Screen('TextSize',w,instructsize);
    Screen('TextStyle',w,1);
    Screen('TextFont',w,'Courier New');
    wtinstruct_1=RectWidth(Screen('TextBounds',w,textinstruct));
    htinstruct_1=RectHeight(Screen('TextBounds',w,textinstruct));
    wtstart=RectWidth(Screen('TextBounds',w,text_waiting_for_ttl));
    htstart=RectHeight(Screen('TextBounds',w,text_waiting_for_ttl));
    Screen('DrawText',w,textinstruct,cx-ceil(wtinstruct_1/2),cy-ceil(htinstruct_1/2)-60,[255 255 255]);
    Screen('DrawText',w,text_waiting_for_ttl,cx-ceil(wtstart/2),cy-ceil(htstart/2)+120,[255 255 255]);
    Screen('DrawLines', w, allCoords, lineWidthPix, white, [cx cy],2);
    Screen('Flip',w);

    fprintf('### Waiting for the trigger... \n')

    keysOfInterest=zeros(1,256);
    keysOfInterest(KbName({spacekey,esckey,trigger,button1}))=1; % initialize keys for the trigger
    KbQueueCreate(deviceIndex);
    KbQueueStart(deviceIndex);

    % Get the trigger from the scanner
    TTL=0; % flag of starting the experiment
    keyIsDown=0;
    while TTL==0
        [keyIsDown, secs, keyCode] = KbCheck(deviceIndex);
        if keyIsDown
            if strcmp(KbName(keyCode),trigger)==1 % TTL
                TTL=1;    % Start the experiment
                run_starttime=GetSecs;
                break;
            elseif strcmp(KbName(keyCode),esckey)==1
                exp_term=1;
                break;
            else
                TTL=0;
            end
        end
        if exp_term
            Priority(0);
            ShowCursor;
            Screen('CloseAll');
            return;
        end
    end

    fprintf('### Trigger received \n')
    WaitSecs(0.5); % otherwise, kbcheck will record the trigger;
    wstim=sysize/3; %set the picture size, initially 310/2   !!!!!
    hstim=sysize/3; % !!!!!
    Screen('DrawTexture',w,pictblk,[],[cx-wstim,cy-hstim,cx+wstim,cy+hstim]);
    Screen('DrawLines', w, allCoords, lineWidthPix, white, [cx cy],2);
    Screen('Flip',w);
    nHit=0;
    numpict=0;
    num=1;
    nbpress=0;
    keyIsDown=0;
    haspressed=0;
    t=GetSecs;
    while GetSecs<t+fixationstart-0.5
        [keyIsDown, secs, keyCode] = KbCheck(deviceIndex);
        if keyIsDown & ~haspressed & ~isempty(MotResp(num).timerelease) & (strcmp(KbName(keyCode),button1)==1 | strcmp(KbName(keyCode),esckey)==1)
            disp(KbName(keyCode))
            Resp=GetSecs;
            haspressed=1;
            num=num+1;
            MotResp(num).press=1;
            MotResp(num).block=0;
            MotResp(num).presstime=Resp-run_starttime;
            MotResp(num).onsets=Resp-run_starttime;
            MotResp(num).pressedkey=KbName(keyCode);
        elseif ~keyIsDown && ~haspressed && isempty(MotResp(num).timerelease)
            Release=GetSecs;
            MotResp(num).timerelease=Release-run_starttime-MotResp(num).onsets;
            MotResp(num).end=Release-run_starttime;
            MotResp(num).duration=MotResp(num).end-MotResp(num).onsets;
        elseif ~keyIsDown && haspressed
            haspressed=0;
            Release=GetSecs;
            MotResp(num).timerelease=Release-run_starttime-MotResp(num).onsets;
            MotResp(num).end=Release-run_starttime;
            MotResp(num).duration=MotResp(num).end-MotResp(num).onsets;
        else
            %pass
        end
    end

    % Block loop
    for blockind=1:nblocks
        stimblock=log(blockind).content;
        TstartTime=GetSecs;
        log(blockind).blockstart=TstartTime-run_starttime;
        starttime=GetSecs;
        prev_nbpress=nbpress;
        for stimind=1:n_stim_in_block
            stimpic=stimloc1(stimblock(stimind,1));
            Screen('DrawTexture',w,stimpic,[],[cx-wstim,cy-hstim,cx+wstim,cy+hstim]); % stimulus
            Screen('DrawLines', w, allCoords, lineWidthPix, white, [cx cy],2); % fixation
            vbl=Screen('Flip',w);
            %end and duration of the previous blank:
            if numpict>0
                pict(numpict).end=vbl-run_starttime;
                pict(numpict).duration=pict(numpict).end-pict(numpict).start;
            end

            %start and category of the stim:
            numpict=numpict+1;
            log(blockind).content(stimind,3)=vbl-run_starttime;
            pict(numpict).start=vbl-run_starttime;
            pict(numpict).category=log(blockind).category;
            pict(numpict).catcontent=log(blockind).catcontent;
            pict(numpict).stim=log(blockind).content(stimind,1);
            if stimblock(stimind,2)==1 % flag of oddball
                respstart=vbl;
                log(blockind).oddtime=respstart-run_starttime;
                pict(numpict).category=7;
                pict(numpict).catcontent='Target';
                pict(numpict).stim=102;
            end
            % button response check during stim projection;
            keyIsDown=0;
            haspressed=0;
            while GetSecs<vbl+stimflipnum*ifi
                [keyIsDown, secs, keyCode] = KbCheck(deviceIndex);
                if keyIsDown & ~haspressed & ~isempty(MotResp(num).timerelease) & (strcmp(KbName(keyCode),button1)==1 | strcmp(KbName(keyCode),esckey)==1)
                    disp(KbName(keyCode))
                    Resp=GetSecs;
                    haspressed=1;
                    num=num+1;
                    MotResp(num).press=1;
                    MotResp(num).block=blockind;
                    if log(blockind).odd==1 & (Resp-run_starttime)>log(blockind).oddtime
                        MotResp(num).presstime=Resp-respstart;
                    else
                        MotResp(num).presstime=Resp-starttime;
                    end
                    MotResp(num).onsets=Resp-run_starttime;
                    MotResp(num).pressedkey=KbName(keyCode);
                elseif ~keyIsDown && ~haspressed && isempty(MotResp(num).timerelease)
                    Release=GetSecs;
                    MotResp(num).timerelease=Release-run_starttime-MotResp(num).onsets;
                    MotResp(num).end=Release-run_starttime;
                    MotResp(num).duration=MotResp(num).end-MotResp(num).onsets;
                elseif ~keyIsDown && haspressed
                    haspressed=0;
                    Release=GetSecs;
                    MotResp(num).timerelease=Release-run_starttime-MotResp(num).onsets;
                    MotResp(num).end=Release-run_starttime;
                    MotResp(num).duration=MotResp(num).end-MotResp(num).onsets;
                else
                    %pass
                end
            end
            Screen('DrawTexture',w,pictblk,[],[cx-wstim,cy-hstim,cx+wstim,cy+hstim]);
            Screen('DrawLines', w, allCoords, lineWidthPix, white, [cx cy],2);
            vbl=Screen('Flip',w,vbl+stimflipnum*ifi);

            log(blockind).content(stimind,4)=vbl-run_starttime;%time when 'blank' starts;
            log(blockind).content(stimind,5)=log(blockind).content(stimind,4)-log(blockind).content(stimind,3);%stim duration;

            %end/duration of the stim:
            pict(numpict).end=vbl-run_starttime;
            pict(numpict).duration=pict(numpict).end-pict(numpict).start;
            %start of the blank:
            numpict=numpict+1;
            pict(numpict).start=vbl-run_starttime;
            pict(numpict).category=6;
            pict(numpict).catcontent='Resting';

            % button response check during blank projection;
            keyIsDown=0;
            haspressed=0;
            while GetSecs<vbl+(fixflipnum-1)*ifi
                [keyIsDown, secs, keyCode] = KbCheck(deviceIndex);
                if keyIsDown & ~haspressed & ~isempty(MotResp(num).timerelease) & (strcmp(KbName(keyCode),button1)==1 | strcmp(KbName(keyCode),esckey)==1)
                    disp(KbName(keyCode))
                    Resp=GetSecs;
                    haspressed=1;
                    num=num+1;
                    MotResp(num).press=1;
                    MotResp(num).block=blockind;
                    if log(blockind).odd==1 & (Resp-run_starttime)>log(blockind).oddtime
                        MotResp(num).presstime=Resp-respstart;
                    else
                        MotResp(num).presstime=Resp-starttime;
                    end
                    MotResp(num).onsets=Resp-run_starttime;
                    MotResp(num).pressedkey=KbName(keyCode);

                elseif ~keyIsDown && ~haspressed && isempty(MotResp(num).timerelease)
                    Release=GetSecs;
                    MotResp(num).timerelease=Release-run_starttime-MotResp(num).onsets;
                    MotResp(num).end=Release-run_starttime;
                    MotResp(num).duration=MotResp(num).end-MotResp(num).onsets;
                elseif ~keyIsDown && haspressed
                    haspressed=0;
                    Release=GetSecs;
                    MotResp(num).timerelease=Release-run_starttime-MotResp(num).onsets;
                    MotResp(num).end=Release-run_starttime;
                    MotResp(num).duration=MotResp(num).end-MotResp(num).onsets;
                else
                    %pass
                end
            end
            Screen('DrawTexture',w,pictblk,[],[cx-wstim,cy-hstim,cx+wstim,cy+hstim]);
            Screen('DrawLines', w, allCoords, lineWidthPix, white, [cx cy],2);
            vbl=Screen('Flip',w,vbl+(fixflipnum-1)*ifi);
        end
        if exp_term
            Priority(0);
            TendTime = GetSecs;
            log(blockind).blockend = TendTime-run_starttime;
            log(blockind).duration= log(blockind).blockend-log(blockind).blockstart;
            log(blockind).duration2= log(blockind).blockend-log(blockind).blockstart;
            break;
        end
        Screen('DrawTexture',w,pictblk,[],[cx-wstim,cy-hstim,cx+wstim,cy+hstim]);
        Screen('DrawLines', w, allCoords, lineWidthPix, white, [cx cy],2);
        Screen('Flip',w);
        JitterTime=GetSecs;
        log(blockind).resttime=JitterTime-run_starttime;

        % button response check during jitter;
        keyIsDown=0;
        haspressed=0;
        while GetSecs<vbl+jitter_values
            [keyIsDown, secs, keyCode] = KbCheck(deviceIndex);
            if keyIsDown & ~haspressed & ~isempty(MotResp(num).timerelease) & (strcmp(KbName(keyCode),button1)==1 | strcmp(KbName(keyCode),esckey)==1)
                disp(KbName(keyCode))
                Resp=GetSecs;
                haspressed=1;
                num=num+1;
                MotResp(num).press=1;
                MotResp(num).block=blockind;
                if log(blockind).odd==1 & (Resp-run_starttime)>log(blockind).oddtime
                    MotResp(num).presstime=Resp-respstart;
                else
                    MotResp(num).presstime=Resp-starttime;
                end
                MotResp(num).onsets=Resp-run_starttime;
                MotResp(num).pressedkey=KbName(keyCode);

            elseif ~keyIsDown && ~haspressed && isempty(MotResp(num).timerelease)
                Release=GetSecs;
                MotResp(num).timerelease=Release-run_starttime-MotResp(num).onsets;
                MotResp(num).end=Release-run_starttime;
                MotResp(num).duration=MotResp(num).end-MotResp(num).onsets;
            elseif ~keyIsDown && haspressed
                haspressed=0;
                Release=GetSecs;
                MotResp(num).timerelease=Release-run_starttime-MotResp(num).onsets;
                MotResp(num).end=Release-run_starttime;
                MotResp(num).duration=MotResp(num).end-MotResp(num).onsets;
            else
                %pass
            end
        end
        nbpress=length(find([MotResp.press]~=0));
        % Button response check and logging at the end of the block (including the inter-block interval, in case of late button presses)
        if log(blockind).odd==1
            for n=1+1+prev_nbpress:1+nbpress % one +1 is because the first line of MotResp is empty...
                if strcmp(MotResp(n).pressedkey,button1)==1
                    presstime=MotResp(n).presstime;
                    if isempty(log(blockind).key) % to avoid rewritting in log file if multiple presses of the 'b' button during this block;
                        if presstime>0 && KbName(MotResp(n).pressedkey)==keycodemappingind(1) % used button number instead of button content
                            log(blockind).key=keycodemapping(KbName(MotResp(n).pressedkey)); % key response, button 1-5. Will only log these button presses
                            log(blockind).resp=presstime; % RT
                            log(blockind).resptime=MotResp(n).onsets;
                        end
                    end
                elseif strcmp(MotResp(n).pressedkey,esckey)==1
                    exp_term=1;
                    break;
                end
                if KbName(MotResp(n).pressedkey)==keycodemappingind(1) && MotResp(n).presstime<maxresp && MotResp(n).presstime>minresp && MotResp(n).onsets>log(blockind).oddtime
                    nHit=nHit+1;
                    fprintf('### Odd hit! Number of success = %d/%d\n',nHit, sum([log(1:blockind).odd]))
                    break
                elseif KbName(MotResp(n).pressedkey)==keycodemappingind(1)
                    fprintf('### Odd missed! Number of success = %d/%d\n',nHit, sum([log(1:blockind).odd]))
                end
            end
        end
        for n=1+1+prev_nbpress:1+nbpress
            if strcmp(MotResp(n).pressedkey,esckey)==1
                exp_term=1;
                break;
            end
        end
        if exp_term
            Priority(0);
            TendTime = GetSecs;
            log(blockind).blockend = TendTime-run_starttime;
            log(blockind).duration= log(blockind).blockend-log(blockind).blockstart;
            log(blockind).duration2=log(blockind).resttime-log(blockind).blockstart;
            break;
        end
        fprintf(progSent,blockind,nblocks)
        prev_nbpress=nbpress;
        if exp_term
            Priority(0);
            TendTime=GetSecs;
            log(blockind).blockend=TendTime-run_starttime;
            log(blockind).duration=log(blockind).blockend-log(blockind).blockstart;
            log(blockind).duration2=log(blockind).resttime-log(blockind).blockstart;
            break;
        end
        TendTime=GetSecs;
        log(blockind).restduration=TendTime-JitterTime;
        log(blockind).blockend=TendTime-run_starttime;
        log(blockind).duration=log(blockind).blockend-log(blockind).blockstart;
        log(blockind).duration2=log(blockind).resttime-log(blockind).blockstart;
    end

    % Fixation (end of experiment)
    keyIsDown=0;
    haspressed=0;
    t=GetSecs;
    while GetSecs<t+fixationend
        [keyIsDown, secs, keyCode] = KbCheck(deviceIndex);
        if keyIsDown & ~haspressed & ~isempty(MotResp(num).timerelease) & (strcmp(KbName(keyCode),button1)==1 | strcmp(KbName(keyCode),esckey)==1)
            disp(KbName(keyCode))
            Resp=GetSecs;
            haspressed=1;
            num=num+1;
            MotResp(num).press=1;
            MotResp(num).block=blockind;
            if log(blockind).odd==1 & (Resp-run_starttime)>log(blockind).oddtime
                MotResp(num).presstime=Resp-respstart;
            else
                MotResp(num).presstime=Resp-starttime;
            end
            MotResp(num).onsets=Resp-run_starttime;
            MotResp(num).pressedkey=KbName(keyCode);
        elseif ~keyIsDown && ~haspressed && isempty(MotResp(num).timerelease)
            Release=GetSecs;
            MotResp(num).timerelease=Release-run_starttime-MotResp(num).onsets;
            MotResp(num).end=Release-run_starttime;
            MotResp(num).duration=MotResp(num).end-MotResp(num).onsets;
        elseif ~keyIsDown && haspressed
            haspressed=0;
            Release=GetSecs;
            MotResp(num).timerelease=Release-run_starttime-MotResp(num).onsets;
            MotResp(num).end=Release-run_starttime;
            MotResp(num).duration=MotResp(num).end-MotResp(num).onsets;
        else
            %pass
        end
    end
    run_endtime=GetSecs;
    pict(numpict).end=run_endtime-run_starttime;
    pict(numpict).duration=pict(numpict).end-pict(numpict).start;
    ShowCursor;
    Priority(0);
    KbQueueStop(deviceIndex);
    while KbEventAvail(deviceIndex)
        j=j+1;
        [evt, n] = KbEventGet(deviceIndex);
        data(j).press=evt.Pressed;
        data(j).pressedkey=KbName(evt.Keycode);
        if evt.Pressed==1
            data(j).onsets=evt.Time-run_starttime;
        else
            data(j).end=evt.Time-run_starttime;
        end
    end
    n=0;
    for i=1:length(data)
        if data(i).press==1
            n=n+1;
            odds(n).pressedkey=data(i).pressedkey;
            odds(n).onsets=data(i).onsets;
        elseif data(i).press==0
            o=data(i).pressedkey;
            o=strcmp({odds.pressedkey},o);
            o=find(o==1,1,'last');
            odds(o).end=data(i).end;
        end
    end
    for i=1:length(odds)
        odds(i).duration=odds(i).end-odds(i).onsets;
    end
    KbQueueRelease(deviceIndex);
    Screen('CloseAll');
    total_duration=sprintf('%.0fmin%.0fsec.\n',floor((run_endtime-run_starttime)/60),mod((run_endtime-run_starttime),60))
    fprintf('The subject hit %d/%d targets.\n',nHit, sum([log(1:blockind).odd]))
    fprintf('The mean response time was %.3fsecs.\n', mean([log.resp]))

catch exception
    PsychHID('KbQueueStop',deviceIndex);
    PsychHID('KbQueueRelease',deviceIndex);
    Screen('CloseAll');
    rethrow(exception)
end

%% Compute hit/miss per trial (logged in the field SDT)
nHit=0;
nMiss=0;
for ind=1:nblocks
    if log(ind).odd==1
        if log(ind).resp<maxresp & log(ind).resp>minresp
            log(ind).SDT=1;
            nHit=nHit+1;
        else
            log(ind).SDT=2;
            nMiss=nMiss+1;
        end
    else
        log(ind).SDT=0;
    end
end

%% Recording of the names/onsets/durations of the conditions:
onsets{nconditions+2,1}=0;
durations{nconditions+2,1}=0;
o=[];
d=[];
for i=1:nconditions
    blocks_nd=setdiff(find([log.category]==i),find([log.duration]~=0));%if stopped before the end, gives the blocks with a duration=0 (blocks not done);
    blocks_done=setdiff(find([log.category]==i),blocks_nd);%if stopped before the end, gives the blocks with a duration != 0 (avoid matrix exceeds);
    for j=1:length(blocks_done)
        o=[log(find([log.category]==i)).blockstart];
        d=[log(find([log.category]==i)).duration2];
        onsets{i,1}(j,1)=o(j);
        durations{i,1}(j,1)=d(j);
    end
end

%recording of the odd, motor and resting onsets/duration:
odds_nd=setdiff(find([log.odd]==1),find([log.duration]~=0));%if stopped before the end, gives the blocks with a duration=0 (blocks not done);
odds_done=setdiff(find([log.odd]==1),odds_nd);%if stopped before the end, gives the odds with a duration ? 0;
o=[];
d=[];
for n=1:length([pict.category]~=0)
    if pict(n).category==7
        d=[d pict(n).duration];
    end
end
for j=1:length(odds_done)
    o=[log.oddtime];
    onsets{nconditions+1,1}(j,1)=o(j);
    durations{nconditions+1,1}(j,1)=d(j);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
o=[];
d=[];
for i=1:length(MotResp)
    if MotResp(i).pressedkey==button1
        o=[o MotResp(i).onsets];
        d=[d MotResp(i).duration];
    end
end
for j=1:length(o)
    onsets{nconditions+2,1}(j,1)=o(j);
    durations{nconditions+2,1}(j,1)=d(j);
end

%% Saving the results
result.subjno=subjno;
result.subjid=subjid;
result.log=log;
result.pict=pict;
result.motresp=MotResp;
result.nHit=nHit;
result.nMiss=nMiss;
result.total_duration=total_duration;

% resextension='.mat';
% resnameappend=[];
% resnameappendnum=0;
% resnamestring=sprintf('result_%s_run%d',subjid,runnum);
% resname=sprintf('%s%s%s',resnamestring,resnameappend,resextension);
% respath=fullfile(dirdata,file_name,resname);
%
% if exist(file_name,'dir')==0
%     mkdir(file_name);
% end
%
% while exist(respath,'file')
%     resnameappendnum=resnameappendnum+1;
%     resnameappend=sprintf('_%s',string(resnameappendnum));
%     resnamestring=sprintf('result_%s_%s_run%d',subjid,runnum);
%     resname=sprintf('%s%s%s',resnamestring,resnameappend,resextension);
%     respath=fullfile(dirdata,file_name,resname);
% end
% save(respath,'result','pict','odds','data');

save(fullfile(dirdata,file_name),'subjno','subjid','runnum','currentoddassign','distance','screenpx','screenwid','result','pict','odds','names','onsets','durations');

%% Time data saving
% timeextension='.mat';
% timenameappend=[];
% timenameappendnum=0;
% timenamestring=sprintf('Timedata_%s_run%d',subjid,runnum);
% timename=sprintf('%s%s%s',timenamestring,timenameappend,timeextension);
% timepath=fullfile(dirdata,file_name,timename);
% while exist(timepath,'file')
%     timenameappendnum=timenameappendnum+1;
%     timenameappend=sprintf('_%d',string(timenameappendnum));
%     timenamestring=sprintf('Timedata_%s_run%d',subjid,runnum);
%     timename=sprintf('%s%s%s',timenamestring,timenameappend,timeextension);
%     timepath=fullfile(dirdata,file_name,timename);
% end
% save(timepath,'names','onsets','durations');
