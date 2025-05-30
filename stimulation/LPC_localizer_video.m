% Exp LPC localizer video (CENIR Prisma).
% Annahita Sarre
% 04/2021
% Press ESCAPE to exit

function LPC_localizer_video(movie_name, windowrect)

% Check if Psychtoolbox is properly installed:
AssertOpenGL;

%% Collect subject info and choose videot

subject_id = input('Numero de sujet : ');

main_path = pwd; % current path
date_of_day = date; % date of the day

if nargin < 1 || isempty(movie_name)
    if mod(subject_id,2)==0
        movie_name = fullfile(main_path,'LPC_videos_irm','LPC_localizer_2.mp4');
        file_name = fullfile(main_path,'LPC_results','LPC_results_localizer_video', ['LPC_res_loc_video_s' num2str(subject_id) '_vid2.mat']);
        common_onsets_of_run = fullfile(main_path,'Common_timetables','lpc_localizer_2_timetable.mat');
    else
        movie_name = fullfile(main_path,'LPC_videos_irm','LPC_localizer_1.mp4');
        file_name = fullfile(main_path,'LPC_results','LPC_results_localizer_video', ['LPC_res_loc_video_s' num2str(subject_id) '_vid1.mat']);
        common_onsets_of_run = fullfile(main_path,'Common_timetables','lpc_localizer_1_timetable.mat');
    end
end

if nargin < 2 || isempty(windowrect)
    windowrect = [];
end

% Copy the file of onsets corresponding to the selected video and copy it in the 'results' folder
copyfile(common_onsets_of_run, file_name);


%% Keyboard parameters

% Switch KbName into unified mode: It will use the names of the OS-X
% platform on all platforms in order to make this script portable:
KbName('UnifyKeyNames');
esc=KbName('ESCAPE');
mri_key = KbName('t');
deviceIndex = [];
key_list = [];

% Wait until user releases keys on keyboard: make sure that all keys are idle
% before you start some new trial that collects keyboard responses
KbReleaseWait;

% Select screen for display of movie:
%screenid = max(Screen('Screens'));
screenid = 1;


%% Display video

try

    Screen('Preference', 'VisualDebugLevel', 1);

    % Open 'windowrect' sized window on screen, with grey (128) background color:
    win = Screen('OpenWindow', screenid, 128, windowrect); %[0 0 400 200]
    HideCursor;

    % Show instructions...
    tsize_instructions = 45;
    tsize_waiting_for_ttl = 25;
    Screen('TextSize', win, tsize_instructions);
    [x, y]=Screen('DrawText', win, 'Restez attentif aux videos',725, 500); %900, 500
    Screen('TextSize', win, tsize_waiting_for_ttl);
    [x, y]=Screen('DrawText', win, 'En attente du signal de l''IRM',810, 600); %900, 500

    % Flip to show the grey screen:
    Screen('Flip',win);

    % Wait for MRI trigger
    fprintf('##### Waiting for MRI trigger ... \n')
    while 1
        [keyIsDown, secs, keyCode]=KbCheck;
        if keyIsDown
            if keyCode(mri_key)
                first_volume_timestamp = secs;
                fprintf('##### MRI trigger received \n')
                break;
            end
        end
    end

    % Open movie file:
    movie = Screen('OpenMovie', win, movie_name);

    % Create and start the KQueue (to better record all keystrokes, for safety)
    KbQueueCreate(deviceIndex);
    KbQueueStart(deviceIndex);

    % Start playback engine:
    Screen('PlayMovie', movie, 1);

    % Playback loop: Runs until end of movie or escape keypress:
    A = 42;
    while A
        % Wait for next movie frame, retrieve texture handle to it
        tex = Screen('GetMovieImage', win, movie);

        % Valid texture returned? A negative value means end of movie reached:
        if tex<=0
            break;
        end

        % Escape key pressed ?
        [keyIsDown, secs, keyCode]=KbCheck;
        if keyIsDown
            if keyCode(esc)
                fprintf('##### Escape key was pressed \n')
                break;
            end
        end

        % Draw the new texture immediately to screen:
        Screen('DrawTexture', win, tex);

        % Update display:
        Screen('Flip', win);

        % Release texture:
        Screen('Close', tex);
    end

KbQueueStop(deviceIndex);

end_of_run_timestamp = secs;
duration = end_of_run_timestamp-first_volume_timestamp;

%% Quit

% Stop playback:
Screen('PlayMovie', movie, 0);

% Close movie:
Screen('CloseMovie', movie);

% Create list of key events to be saved in the control file
while KbEventAvail(deviceIndex)
    key_list = [key_list, KbEventGet(deviceIndex)];
end

% Save files
save(file_name, 'subject_id', 'movie_name', 'date_of_day', 'first_volume_timestamp', 'end_of_run_timestamp','duration','key_list', '-append');

% Close Screen, we're done
sca;

fprintf('##### Script execution has finished correctly \n')


catch %#ok<CTCH>
    sca;
    psychrethrow(psychlasterror);
end

return
