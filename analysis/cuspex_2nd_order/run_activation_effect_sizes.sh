#!/bin/bash

path_loc_vid=/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_2nd_order/loc_vid/loc_vid_t-tests/results_s4/

cons=("Sound_LPC" "Silent_LPC" "Manual_cues" "Labial" "Pseudo" "Sound_LPC - Silent_LPC" "Silent_LPC - Sound_LPC" "Silent_LPC - Manual_cues"
"Manual_cues - Silent_LPC" "Silent_LPC - Labial" "Labial - Silent_LPC" "Silent_LPC - Pseudo"
"Pseudo - Silent_LPC" "Manual_cues - Labial" "Labial - Manual_cues" "Pseudo - Labial" "Pseudo - Manual cues")

for con in "${cons[@]}"; do
  matlab -nodisplay -nosplash -r "try; activation_effect_sizes('$path_loc_vid', '$con'); catch e; disp(getReport(e)); end; exit;"
done

path_loc_stat=/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_2nd_order/loc_stat/loc_stat_t-tests/results_s4/

cons=("Faces" "Bodies" "Words" "Houses" "Tools"
"Faces-others" "Bodies-others" "Words-others" "Houses-others" "Tools-others")

for con in "${cons[@]}"; do
  matlab -nodisplay -nosplash -r "try; activation_effect_sizes('$path_loc_vid', '$con'); catch e; disp(getReport(e)); end; exit;" &
done
