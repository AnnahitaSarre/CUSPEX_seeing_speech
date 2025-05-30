#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Population analysis for the CUSPEX study

"""

#%%Import modules

import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


#%% Import and arrange df

df = pd.read_csv('/mnt/ata-ST4000NM0165_ZAD8CWEG-part1/cuspex/cuspex_analysis/cuspex_1st_order/behavior/questionnaires/RedCap_data_processed/cuspex_tableau_final_demography_comm.csv', sep=',')
df['group'] = df['group'].astype(str)


#%% Basic demographic stats for all 3 groups

print('\n\n### Basic statistics for all group ###\n')

# Arrange df
df['sex'] = df['sex'].replace([0, 2], ['H','F'])
df['diplome'] = df['diplome'].replace([0, 1, 2, 3, 4, 5, 6, 7],
                                      ['Certificat détudes primaires','Aucun diplôme','Brevet des collèges, BEPC',
                                       'Baccalauréat général, technologique, professionnel ou équivalent','CAP, BEP ou équivalent',
                                       'BTS, DUT, licence ou équivalent','Master ou équivalent','Doctorat'])

plt.figure(figsize=(8,6))
sns.violinplot(x=df['group'], y=df['age'], data=df, inner='quartile', palette='pastel', scale='count').set(title='Age by group')
sns.stripplot(x=df['group'], y=df['age'], palette='dark')
plt.show()
print(df[['group', 'age']].groupby('group').describe())

plt.figure(figsize=(8,6))
sns.histplot(x=df['group'][~df['sex'].isna()], stat='count', hue='sex', multiple='dodge', data=df[~df['sex'].isna()], palette='pastel', shrink=.8).set(title='Sex by group')
plt.show()
print(df[['group', 'sex']].groupby('group').describe())
contingency = pd.crosstab(df['sex'], df['group'])
chi2, p, dof, expected = chi2_contingency(contingency)
print(f"sex ratio between the groups = {chi2:.3f}, p-value = {p:.3f}")

plt.figure(figsize=(8,6))
sns.histplot(x=df['group'][~df['diplome'].isna()], stat='count', hue='diplome',
             hue_order=('Brevet des collèges, BEPC','Baccalauréat général, technologique, professionnel ou équivalent','BTS, DUT, licence ou équivalent','Master ou équivalent'),
             multiple='dodge', data=df[~df['diplome'].isna()], palette='pastel', shrink=.8).set(title='Diploma by group')
plt.show()
print(df[['group', 'diplome']].groupby('group').describe())

df['diplome'] = df['diplome'].replace(['Certificat détudes primaires','Aucun diplôme','Brevet des collèges, BEPC',
                                       'Baccalauréat général, technologique, professionnel ou équivalent','CAP, BEP ou équivalent',
                                       'BTS, DUT, licence ou équivalent','Master ou équivalent','Doctorat'],
                                      ["Pas d'études supérieures","Pas d'études supérieures","Pas d'études supérieures",
                                       "Pas d'études supérieures","Etudes supérieures","Etudes supérieures",
                                       "Etudes supérieures","Etudes supérieures"])
plt.figure(figsize=(8,6))
sns.histplot(x=df['group'][~df['diplome'].isna()], stat='count', hue='diplome',
             multiple='dodge', data=df[~df['diplome'].isna()], palette='pastel', shrink=.8).set(title='Diploma by group')
plt.yticks(np.arange(0, 20, 2))
plt.show()
print(df[['group', 'diplome']].groupby('group').describe())

plt.figure(figsize=(16,6))
sns.violinplot(x=df['group'], y=df['laterality score'], data=df, inner='quartile', palette='pastel').set(title='Laterality score by group')
sns.stripplot(x=df['group'], y=df['laterality score'], palette='dark')
plt.show()
print(df[['group', 'laterality score']].groupby('group').describe())


#%% Deafness in group 1

print('\n\n### Group 1 deafness and scolarity ###\n')

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['group'] == '1']['gr1_degre_surdite'], discrete=True, stat='count', multiple='dodge', palette='pastel', shrink=.8).set(title='Degre of deafness in group 1')
plt.show()

print("Progressive deafness onset?: 2 people said that their deafness appeared progressively starting at 1 year old, all the others said it began at 0")

print("\nSevere deafness onset: from the 2 people above, one of them responded 1 year old and the other 2")

print("\nDeafness onset: one person said it wasn't progressive but appeared abruptly at 1, others said it appeared at birth")

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['group'] == '1']['gr1_nb_appareils'], discrete=True, stat='count', multiple='dodge', palette='pastel', shrink=.8).set(title='Number of hearing devices in group 1')
plt.show()

plt.figure(figsize=(8,6))
sns.displot(x=df.loc[df['gr1_nb_appareils'] > 0]['gr1_temps_appareil'], palette='pastel').set(title='Time spent with hearing device(s) in group 1')
plt.show()

print(f"\nDeafness causes in participants: {df.loc[df['group'] == '1']['gr1_cause_surdite'].values.tolist()}")

print(f"\nOther deaf people in family (g1):\n\n\tFamily relationship: {df.loc[df['group'] == '1']['gr1_degre_parente'].values.tolist()}"+
      f"\n\n\tFamily degree of deafness: {df.loc[df['group'] == '1']['gr1_degre_surdite_famille'].values.tolist()}"+
      f"\n\n\tFamily hearing devices: {df.loc[df['group'] == '1']['gr1_famille_appareil'].values.tolist()}"+
      f"\n\n\tFamily language: {df.loc[df['group'] == '1']['gr1_famille_langage'].values.tolist()}"+
      f"\n\n\tFamily cause of deafness: {df.loc[df['group'] == '1']['gr1_famille_cause'].values.tolist()}")


#%% Scolarity and reading in group 1

print("Scolarity: Majority were in standard school with coders (some without), a bit of LSF classes too. I'm not sure I understand all responses")

plt.figure(figsize=(8,6))
sns.displot(x=df.loc[df['group'] == '1']['gr1_lpc_lecture_age'], palette='pastel').set(title='Age of reading acquisition in group 1')
plt.show()
print(df.loc[df['group'] == '1']['gr1_lpc_lecture_age'].describe())

print("Difficulty in reading acquisition: 5 declared they have had some. Nowadays they report a 3 (2 people) or 4 level in reading.")


#%% Deaf environment in groups 1 and 2

print('\n\n### Group 1 and 2 deaf environment ###\n')

# Arrange df
df['Entourage_merged'] = np.nan_to_num(df['Entourage_merged'], nan=9) # Because nan cannot be converted to int
with pd.option_context('mode.chained_assignment', None): # To desactivate SettingWithCopyWarning
    for response_index in df.index:
        if df['gr1_degre_parente'].loc[response_index] not in ['0','Cousin du 2eme degré']: # Take care of group 1
            coded_response = str(int(df['Entourage_merged'].loc[response_index])).replace('3','') + '4'
            coded_response = coded_response.replace('9','')
            df['Entourage_merged'].loc[response_index] = int(coded_response)
        if df['gr2_entourage_type_precision'].loc[response_index] != '0': # Take care of group 2
            coded_response = str(int(df['Entourage_merged'].loc[response_index])).replace('3','')
            coded_response = coded_response + '4'
            # coded_response = coded_response.replace('9','')
            df['Entourage_merged'].loc[response_index] = int(coded_response)

dict_entourage = {'0':'Amical', '1':'Professionnel', '2':'Scolaire ou étudiant', '4':'Familial'}
with pd.option_context('mode.chained_assignment', None): # To desactivate SettingWithCopyWarning
    for index in df.loc[df['group'] != '3'].index:
        if df.loc[index]['Entourage_merged'] == 9.0:
            df['Entourage_merged'].loc[index] = "Pas d'entourage"
        else:
            list_entourage = []
            for num in list(str(int(df.loc[index]['Entourage_merged']))):
                txt = dict_entourage[num]
                list_entourage.append(txt)
            list_entourage = (' + ').join(list_entourage)
            df['Entourage_merged'].loc[index] = list_entourage
df['Entourage_merged'] = df['Entourage_merged'].replace(9.0,np.nan) # Turn back 9 to nan


plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['group'] != '3']['group'], hue=df.loc[df['group'] != '3']['Entourage_merged'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Deaf environment of groups 1 and 2')
plt.show()

print(f"\nGroup 1 participants are mainly in contact with oralising, with or without LPC, people, with quite a few LSF.\n\
Details: {df.loc[df['gr1_entourage_langage'] != '0']['gr1_entourage_langage'].values.tolist()}")
      
print(f"\nSame with group 2 participants, with a bit less LSF.\n\
Details: {df.loc[df['gr2_entourage_langage'] != '0']['gr2_entourage_langage'].values.tolist()}")

print("\nDeaf people around both groups' participants have a mix of hearing devices and cochlear implants.")


#%% LPC in groups 1 and 2

print('\n\n### Group 1 and 2 LPC usage ###\n')

# Arrange df
df['lpc_freq'] = df['lpc_freq'].replace([0, 1, 2, 3, 4, 5, 6],
                                      ['Tous les jours','Plusieurs fois par semaine','1 fois par semaine',
                                       'Plusieurs fois par mois','1 fois par mois',
                                       'Plusieurs fois par an','1 fois par an ou moins'])
df['lpc_usefulness'] = df['lpc_niv_comprendre'] - df['lpc_niv_labial']

plt.figure(figsize=(8,6))
sns.violinplot(x=df.loc[df['group'] != '3']['group'], y=df['lpc_age'], scale='count', inner='quartile', palette='pastel').set(title='Age of LPC learning in groups 1 and 2')
sns.stripplot(x=df.loc[df['group'] != '3']['group'], y=df['lpc_age'], data=df.loc[df['group'] != '3'], palette='dark')
plt.show()
print(df.loc[df['group'] != '3'][['group','lpc_age']].groupby('group').describe())

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['group'] != '3']['group'], hue=df.loc[df['group'] != '3']['lpc_freq'],
             hue_order=('Tous les jours','Plusieurs fois par semaine',
                        'Plusieurs fois par mois','1 fois par mois',
                        'Plusieurs fois par an','1 fois par an ou moins'),
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Frequency of LPC use in groups 1 and 2')
plt.show()
print("The two partcipants who responded 'Plusieurs fois par an' and '1 fois par an ou moins' are proficient deaf CS user who started CS at 2 and 3 years old => no pb")

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['group'] != '3']['group'], hue=df.loc[df['group'] != '3']['lpc_niv_coder'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported level of LPC production in groups 1 and 2 (min 0 max 4)')
plt.show()

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['group'] != '3']['group'], hue=df.loc[df['group'] != '3']['lpc_niv_comprendre'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported level of LPC comprehension in groups 1 and 2 (min 0 max 4)')
plt.show()
print("The partcipant who responded '2' is a proficient deaf CS user who started CS at 3 years old => no pb")

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['group'] != '3']['group'], hue=df.loc[df['group'] != '3']['lpc_niv_labial'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported level of lipreading in groups 1 and 2 (min 0 max 4)')
plt.show()

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['group'] != '3']['group'], hue=df.loc[df['group'] != '3']['lpc_usefulness'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported LPC usefulness (=LPC - lipreading alone) in groups 1 and 2')
plt.show()
print(df[['group', 'lpc_usefulness']].groupby('group').describe())


# Arrange df for LPC learning ressource
with pd.option_context('mode.chained_assignment', None): # To desactivate SettingWithCopyWarning
    for response_index in df.index:
        if df['gr1_lpc_apprentissage_precision'].loc[response_index] != '0':
            coded_response = str(int(df['lpc_cadre___merged'].loc[response_index])).replace('4','')
            if 'parents' in df['gr1_lpc_apprentissage_precision'].loc[response_index]:
                coded_response = coded_response + '0'
            if 'orthophoniste' in df['gr1_lpc_apprentissage_precision'].loc[response_index]:
                coded_response = coded_response + '6'
            if 'CODALI' in df['gr1_lpc_apprentissage_precision'].loc[response_index]:
                coded_response = coded_response + '7'
            df['lpc_apprentissage___merged'].loc[response_index] = int(coded_response)
        if df['gr2_lpc_apprentissage_precision'].loc[response_index] != '0':
            df['lpc_apprentissage___merged'].loc[response_index] = '8'

dict_lpc_apprentissage = {'0':'Parents', '1':'Ecole', '2':'Stage', '3':'Autodidacte', '5':'Licence LPC','6':'Orthophoniste', '7':'Service d\'accompagnement', '8':'Pairs'}
with pd.option_context('mode.chained_assignment', None): # To desactivate SettingWithCopyWarning
    for index in df.loc[df['group'] != '3'].index:
        list_lpc_apprentissage = []
        for num in list(str(int(df.loc[index]['lpc_apprentissage___merged']))):
            txt = dict_lpc_apprentissage[num]
            list_lpc_apprentissage.append(txt)
        list_lpc_apprentissage = list(set(list_lpc_apprentissage)) # Delete duplicates
        list_lpc_apprentissage = (' + ').join(list_lpc_apprentissage)
        df['lpc_apprentissage___merged'].loc[index] = list_lpc_apprentissage

# Arrange df for LPC usage
with pd.option_context('mode.chained_assignment', None): # To desactivate SettingWithCopyWarning
    for response_index in df.index:
        if 'seule' in df['gr1_lpc_cadre_precision'].loc[response_index]:
            coded_response = str(int(df['lpc_cadre___merged'].loc[response_index])).replace('4','')
            coded_response = coded_response + '5'
            df['lpc_cadre___merged'].loc[response_index] = int(coded_response)
        if df['gr2_lpc_cadre_precision'].loc[response_index] != '0':
            coded_response = str(int(df['lpc_cadre___merged'].loc[response_index])).replace('4','')
            if 'moi' in df['gr2_lpc_cadre_precision'].loc[response_index]:
                coded_response = coded_response + '5'
            if 'conjointe' in df['gr2_lpc_cadre_precision'].loc[response_index]:
                coded_response = coded_response + '0'
            if 'formateur' in df['gr2_lpc_cadre_precision'].loc[response_index]:
                coded_response = coded_response + '3'    
            df['lpc_cadre___merged'].loc[response_index] = int(coded_response)
            
dict_lpc_cadre = {'0':'Famille', '2':'Amis', '3':'Travail/Etudes', '5':'Seul'}
with pd.option_context('mode.chained_assignment', None): # To desactivate SettingWithCopyWarning
    for index in df.loc[df['group'] != '3'].index:
        list_lpc_cadre = []
        for num in list(str(int(df.loc[index]['lpc_cadre___merged']))):
            txt = dict_lpc_cadre[num]
            list_lpc_cadre.append(txt)
        list_lpc_cadre = list(set(list_lpc_cadre)) # Delete duplicates
        list_lpc_cadre = (' + ').join(list_lpc_cadre)
        df['lpc_cadre___merged'].loc[index] = list_lpc_cadre

plt.figure(figsize=(15,11))
sns.histplot(x=df.loc[df['group'] != '3']['group'], hue=df.loc[df['group'] != '3']['lpc_apprentissage___merged'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='LPC learning ressource in groups 1 and 2')
plt.show()

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['group'] != '3']['group'], hue=df.loc[df['group'] != '3']['lpc_cadre___merged'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='LPC usage in groups 1 and 2')
plt.show()


#%% CS in groups 1 and 2

print('\n\n### Group 1 and 2 CS usage ###\n')

# Arrange df
df['cs_yn'] = df['cs_yn'].replace([0, 1], ['No','Yes'])

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['group'] != '3']['group'], hue=df.loc[df['group'] != '3']['cs_yn'], hue_order=('Yes','No'),
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Knowledge on CS in groups 1 and 2')
plt.show()

print("\nIn addition to American/UK CS, one participant mentionned Spanish CS.")

plt.figure(figsize=(8,6))
sns.violinplot(x=df.loc[df['cs_yn'] == 'Yes']['group'], y=df['cs_age'], inner='quartile', palette='pastel').set(title='Age of CS learning in groups 1 and 2')
sns.stripplot(x=df.loc[df['cs_yn'] == 'Yes']['group'], y=df['cs_age'], data=df.loc[df['group'] != '3'], palette='dark')
plt.show()
print(df.loc[df['cs_yn'] == 'Yes'][['group','cs_age']].groupby('group').describe())

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['cs_yn'] == 'Yes']['group'], hue=df.loc[df['group'] != '3']['cs_niv_coder'], hue_order=(1,2,3),
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported level of CS production in groups 1 and 2 (min 0 max 4)')
plt.show()

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['cs_yn'] == 'Yes']['group'], hue=df.loc[df['group'] != '3']['cs_niv_comprendre'], hue_order=(0,1,2,3),
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported level of CS comprehension in groups 1 and 2 (min 0 max 4)')
plt.show()


#%% LSF in groups 1 and 2

print('\n\n### Group 1 and 2 LSF usage ###\n')

# Arrange df
df['lsf_yn'] = df['lsf_yn'].replace([0, 1], ['No','Yes'])
df['lsf_freq'] = df['lsf_freq'].replace([0, 1, 2, 3, 4, 5, 6],
                                      ['Tous les jours','Plusieurs fois par semaine','1 fois par semaine',
                                       'Plusieurs fois par mois','1 fois par mois',
                                       'Plusieurs fois par an','1 fois par an ou moins'])

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['group'] != '3']['group'], hue=df.loc[df['group'] != '3']['lsf_yn'], hue_order=('Yes','No'),
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Knowledge on LSF in groups 1 and 2')
plt.show()

plt.figure(figsize=(8,6))
sns.violinplot(x=df.loc[df['lsf_yn'] == 'Yes']['group'], y=df['lsf_age'], inner='quartile', palette='pastel').set(title='Age of LSF learning in groups 1 and 2')
sns.stripplot(x=df.loc[df['lsf_yn'] == 'Yes']['group'], y=df['lsf_age'], data=df.loc[df['group'] != '3'], palette='dark')
plt.show()
print(df.loc[df['lsf_yn'] == 'Yes'][['group','lsf_age']].groupby('group').describe())

plt.figure(figsize=(12,8))
sns.histplot(x=df.loc[df['lsf_yn'] == 'Yes']['group'], hue=df.loc[df['group'] != '3']['lsf_freq'],
             hue_order=('Tous les jours','Plusieurs fois par semaine',
                        'Plusieurs fois par mois','1 fois par mois',
                        'Plusieurs fois par an','1 fois par an ou moins'),
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Frequency of LSF use in groups 1 and 2')
plt.show()

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['lsf_yn'] == 'Yes']['group'], hue=df.loc[df['group'] != '3']['lsf_niv_exprimer'], hue_order=(0,1,2,3,4),
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported level of LSF production in groups 1 and 2 (min 0 max 4)')
plt.show()

plt.figure(figsize=(8,6))
sns.histplot(x=df.loc[df['lsf_yn'] == 'Yes']['group'], hue=df.loc[df['group'] != '3']['lsf_niv_comprendre'], hue_order=(0,1,2,3,4),
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported level of LSF comprehension in groups 1 and 2 (min 0 max 4)')
plt.show()

# Arrange df for LSF learning ressource
df['lsf_apprentissage___merged'] = np.nan_to_num(df['lsf_apprentissage___merged'], nan=9.0) # Because nan cannot be converted to int
with pd.option_context('mode.chained_assignment', None): # To desactivate SettingWithCopyWarning
    for response_index in df.index:
        if df['gr1_lsf_apprentissage_precision'].loc[response_index] != '0':
            coded_response = str(int(df['lsf_apprentissage___merged'].loc[response_index])).replace('4','')
            if 'structure' in df['gr1_lsf_apprentissage_precision'].loc[response_index]:
                coded_response = coded_response + '7'
            if 'amis' in df['gr1_lsf_apprentissage_precision'].loc[response_index]:
                coded_response = coded_response + '6'
            if 'contact' in df['gr1_lsf_apprentissage_precision'].loc[response_index]:
                coded_response = coded_response + '6'
            if 'IVT' in df['gr1_lsf_apprentissage_precision'].loc[response_index]:
                coded_response = coded_response + '26'
            if 'association' in df['gr1_lsf_apprentissage_precision'].loc[response_index]:
                coded_response = coded_response + '7'
            if 'Maman' in df['gr1_lsf_apprentissage_precision'].loc[response_index]:
                coded_response = coded_response + '06'
            df['lsf_apprentissage___merged'].loc[response_index] = int(coded_response)
        if df['gr2_lsf_apprentissage_precision'].loc[response_index] != '0':
            coded_response = str(int(df['lsf_apprentissage___merged'].loc[response_index])).replace('4','')
            if 'stage' in df['gr2_lsf_apprentissage_precision'].loc[response_index]:
                coded_response = coded_response + '2'
            if 'collègues' in df['gr2_lsf_apprentissage_precision'].loc[response_index]:
                coded_response = coded_response + '56'
            if 'lycée' in df['gr2_lsf_apprentissage_precision'].loc[response_index]:
                coded_response = coded_response + '652'
            df['lsf_apprentissage___merged'].loc[response_index] = int(coded_response)

dict_lsf_apprentissage = {'0':'Parents', '1':'Ecole', '2':'Stage', '3':'Autodidacte', '5':'Licence LPC', '6': 'Pairs', '7': 'Structure d\'accueil/association'}
with pd.option_context('mode.chained_assignment', None): # To desactivate SettingWithCopyWarning
    for index in df.loc[df['group'] != '3'].index:
        list_lsf_apprentissage = []
        for num in list(str(int(df.loc[index]['lsf_apprentissage___merged']))):
            if num != '9':
                txt = dict_lsf_apprentissage[num]
                list_lsf_apprentissage.append(txt)
        list_lsf_apprentissage = list(set(list_lsf_apprentissage)) # Delete duplicates
        list_lsf_apprentissage = (' + ').join(list_lsf_apprentissage)
        df['lsf_apprentissage___merged'].loc[index] = list_lsf_apprentissage
df['lsf_apprentissage___merged'] = df['lsf_apprentissage___merged'].replace(['',9],np.nan) # Turn back 9 to nan

# Arrange df for LSF usage
df['lsf_cadre___merged'] = np.nan_to_num(df['lsf_cadre___merged'], nan=9.0) # Because nan cannot be converted to int
with pd.option_context('mode.chained_assignment', None): # To desactivate SettingWithCopyWarning
    for response_index in df.index:
        if df['gr1_lsf_cadre_precision'].loc[response_index] != '0':
            coded_response = str(int(df['lsf_cadre___merged'].loc[response_index])).replace('4','')
            if 'autodidacte' in df['gr1_lsf_cadre_precision'].loc[response_index]:
                coded_response = coded_response + '5'
            if 'Associations' in df['gr1_lsf_cadre_precision'].loc[response_index]:
                coded_response = coded_response + '3'
            if 'conjoint' in df['gr1_lsf_cadre_precision'].loc[response_index]:
                coded_response = coded_response + '0'
            if 'chéri' in df['gr1_lsf_cadre_precision'].loc[response_index]:
                coded_response = coded_response + '0'
            df['lsf_cadre___merged'].loc[response_index] = int(coded_response)
        if df['gr2_lsf_cadre_precision'].loc[response_index] != '0':
            coded_response = str(int(df['lsf_cadre___merged'].loc[response_index])).replace('4','')
            if 'conjointe' in df['gr2_lsf_cadre_precision'].loc[response_index]:
                coded_response = coded_response + '0'
            df['lsf_cadre___merged'].loc[response_index] = int(coded_response)

dict_lsf_cadre = {'0':'Avec ma famille', '2':'Avec mes amis', '3':'Dans le cadre de mon travail/de mes études', '4':'!!!', '5':'Seul'}
with pd.option_context('mode.chained_assignment', None): # To desactivate SettingWithCopyWarning
    for index in df.loc[df['group'] != '3'].index:
        list_lsf_cadre = []
        for num in list(str(int(df.loc[index]['lsf_cadre___merged']))):
            if num != '9':
                txt = dict_lsf_cadre[num]
                list_lsf_cadre.append(txt)
        list_lsf_cadre = list(set(list_lsf_cadre)) # Delete duplicates
        list_lsf_cadre = (' + ').join(list_lsf_cadre)
        df['lsf_cadre___merged'].loc[index] = list_lsf_cadre
df['lsf_cadre___merged'] = df['lsf_cadre___merged'].replace(['',9],np.nan) # Turn back 9 to nan

plt.figure(figsize=(20,11))
sns.histplot(x=df.loc[df['lsf_yn'] == 'Yes']['group'], hue=df.loc[df['group'] != '3']['lsf_apprentissage___merged'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='LSF learning ressource in groups 1 and 2')
plt.show()

plt.figure(figsize=(14,10))
sns.histplot(x=df.loc[df['lsf_yn'] == 'Yes']['group'], hue=df.loc[df['group'] != '3']['lsf_cadre___merged'],
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='LSF usage in groups 1 and 2')
plt.show()


#%% Other LS in groups 1 and 2

print('\n\n### Group 1 and 2 LS usage ###\n')

# Arrange df
df['ls_yn'] = df['ls_yn'].replace([0, 1], ['No','Yes'])

print(f"\n5 group 1 participants and no group 2 participant declared having knowledge on other SL.\n\
The 5 participants also know LSF, with a better or equal level than with LS.\n\
They mentionned: {df.loc[df['ls_yn'] == 'Yes']['gr1_ls_identite'].values.tolist()}")

plt.figure(figsize=(2,6))
sns.violinplot(y=df.loc[df['ls_yn'] == 'Yes']['ls_age'], inner='quartile', palette='pastel').set(title='Age of other LS learning in group 1')
sns.stripplot(y=df.loc[df['ls_yn'] == 'Yes']['ls_age'], palette='dark')
plt.show()

plt.figure(figsize=(4,6))
sns.histplot(x=df.loc[df['ls_yn'] == 'Yes']['group'], hue=df.loc[df['group'] != '3']['ls_niv_exprimer'], hue_order=(0,1,2,4),
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported level of other LS production in group 1 (min 0 max 4)')
plt.show()

plt.figure(figsize=(4,6))
sns.histplot(x=df.loc[df['ls_yn'] == 'Yes']['group'], hue=df.loc[df['group'] != '3']['ls_niv_comprendre'], hue_order=(0,1,2,3,4),
             stat='count', multiple='dodge', palette='pastel', shrink=.7).set(title='Self-reported level of other LS comprehension in group 1 (min 0 max 4)')
plt.show()
