## Seeing speech: neural mechanisms of cued speech perception in prelingually deaf and hearing users

### 🧠 Presentation
Repository containing the stimulation and analysis scripts for the first article of the CUSPEX project.

The goal of this paper was to delineate the brain regions involved in cued speech perception and to identify their role in visual and language-related processes.

Article reference:

> Sarré, A., & Cohen, L. (2024). Seeing speech: Neural mechanisms of cued speech perception in prelingually deaf and hearing users. bioRxiv, 2024.12.06.626971. https://doi.org/10.1101/2024.12.06.626971


### 🔗 Related material
Preprocessing was done with the CENIR preprocessing pipeline: https://github.com/romainVala/matvol

Group-level results can be found at: https://doi.org/10.5281/zenodo.15516222

### 📂 Repository structure
The main experiment is often called *video localizer* or *loc_vid* and the localizer experiment *static localizer* or *loc_stat*.

The term *LPC* refers to the French version of cued speech (CS), the *Langue française Parlée Complétée*.

Please feel free to reach me for additional information!
```
CUSPEX article 1
├── analysis
│   ├── cuspex_1st_order
│   │   ├── behavior
│   │   │   ├── create_covariates.m
│   │   │   ├── initial_questionnaires
│   │   │   │   ├── cuspex_population_analysis.py
│   │   │   │   ├── Final_table.py
│   │   │   │   └── RedCap_tool_functions.py
│   │   │   ├── mri_tasks
│   │   │   │   ├── behavior_loc_stat.m
│   │   │   │   ├── loc_vid_debrief_analysis.py
│   │   │   │   └── mri_tasks_analysis.py
│   │   │   └── pretest_comprehension_analysis.py
│   │   ├── contrasts
│   │   │   ├── contrasts_loc_stat_job.m
│   │   │   ├── contrasts_loc_vid_job.m
│   │   │   └── run_contrasts.m
│   │   └── glm
│   │       ├── model_loc_stat_job.m
│   │       ├── model_loc_vid_job.m
│   │       └── run_GLM.m
│   └── cuspex_2nd_order
│       ├── analyse_roi_results.py
│       ├── compute_effect_sizes.m
│       ├── compute_roi_results.py
│       ├── plot_activation_x_covariate.py
│       ├── plot_voxel_profil.m
│       ├──  run_activation_effect_sizes.sh
│       ├── loc_stat
│       │   ├── loc_stat_conjonction
│       │   │   ├── second_level_loc_stat_conjonction_job.m
│       │   │   └── second_level_loc_stat_conjonction.m
│       │   └── loc_stat_t-tests
│       │       ├── run_loc_stat_2nd_level_t_test.m
│       │       ├── second_level_loc_stat_1g_t_test_job.m
│       │       └── second_level_loc_stat_2g_t_test_job.m
│       └── loc_vid
│           ├── loc_vid_conjonction
│           │   ├── model_individual_intersect_job.m
│           │   ├── second_level_loc_vid_conjonction_job.m
│           │   ├── second_level_loc_vid_conjonction.m
│           │   └── threshold_intersect_individual.py
│           └── loc_vid_t-tests
│               ├── run_loc_vid_2nd_level_t_test.m
│               ├── second_level_loc_vid_1g_t_test_job.m
│               └── second_level_loc_vid_2g_t_test_job.m
├── stimulation
│    ├── LPC_localizer_statique.m
│    └── LPC_localizer_video.m
├── Design_overview.pdf
└── README.md
```
