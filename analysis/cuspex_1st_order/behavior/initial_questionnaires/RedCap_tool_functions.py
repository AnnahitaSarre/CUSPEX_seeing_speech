# -*- coding: utf-8 -*-
"""
CUSPEX script cleaing the initial questionnaire
Original script by Imane Boudjelal

"""

#%% Import modules

import pandas as pd


#%% command to write in the terminal for example 
#         df= function_final_table(nom_etude='custime',type_csv = 'with_comment')
#--> it calls the last function of this doc, this function call itself the 4 previous functions define bellow


#%% Debuging variables

#nom_etude = 'cuspex'
#nom_etude = 'custime'

#type_csv = 'with_comment'
#type_csv = 'without_comment'


def clean_RC_DATA (nom_etude,type_csv):
    
    #%% import the only raw csv data from the 3 questionnaires of RedCap
    if type_csv == 'without_comment':
        df = pd.read_csv('RedCap_data_raw/' + nom_etude +'_raw.csv', sep=',')
    else :
        df = pd.read_csv('RedCap_data_raw/' + nom_etude +'_raw_comm.csv', sep=',')
    
    #%% Annahita: add 17 to get the real age since this variable was coded like 1->18 years old in RedCap
    with pd.option_context('mode.chained_assignment', None): # To desactivate SettingWithCopyWarning
        for index in df.index:
            df['age'].loc[index] = df['age'].loc[index] + 17
            
    #%% Annahita: change one inapropriate colunne name in the cuspex experiment
    if nom_etude== 'cuspex':
        df = df.rename(columns={'comprehension_lpc_soncomprehension_lpc_sans_son': 'comprehension_lpc_sans_son'})
        
    #%% Annahita: Add participant 01/pilote1 (laterality answers come from custime)
    if nom_etude== 'cuspex':
        df.loc[15.5] = {'record_id':17, 'questionnaire_lpc_timestamp':'07-04-2021 13:23.', 'id_sujet':'{:02d}'.format(1), 'age':23, 'sex':2, 'pref_manuelle':0,
                        'native_language':'Français', 'diplome':5, 'vision':0, 'metal':0, 'group':3, 'origine_sujet': 'Connaissance', 'questionnaire_lpc_complete':2,
                        'gr1_entourage_type___0':0, 'gr1_entourage_type___1':0, 'gr1_entourage_type___2':0, 'gr1_entourage_type___3':0,
                        'gr1_lpc_apprentissage___0':0, 'gr1_lpc_apprentissage___1':0, 'gr1_lpc_apprentissage___2':0, 'gr1_lpc_apprentissage___3':0, 'gr1_lpc_apprentissage___4':0,
                        'gr1_lpc_cadre___0':0, 'gr1_lpc_cadre___2':0, 'gr1_lpc_cadre___3':0, 'gr1_lpc_cadre___4':0,
                        'gr1_lsf_apprentissage___0':0, 'gr1_lsf_apprentissage___1':0, 'gr1_lsf_apprentissage___2':0, 'gr1_lsf_apprentissage___3':0, 'gr1_lsf_apprentissage___4':0,
                        'gr1_lsf_cadre___0':0, 'gr1_lsf_cadre___2':0, 'gr1_lsf_cadre___3':0, 'gr1_lsf_cadre___4':0,
                        'gr2_entourage_type___0':0, 'gr2_entourage_type___1':0, 'gr2_entourage_type___2':0, 'gr2_entourage_type___3':0,
                        'gr2_lpc_apprentissage___0':0, 'gr2_lpc_apprentissage___1':0, 'gr2_lpc_apprentissage___2':0, 'gr2_lpc_apprentissage___3':0, 'gr2_lpc_apprentissage___5':0, 'gr2_lpc_apprentissage___4':0,
                        'gr2_lpc_cadre___0':0, 'gr2_lpc_cadre___2':0, 'gr2_lpc_cadre___3':0, 'gr2_lpc_cadre___4':0,
                        'gr2_lsf_apprentissage___0':0, 'gr2_lsf_apprentissage___1':0, 'gr2_lsf_apprentissage___2':0, 'gr2_lsf_apprentissage___3':0, 'gr2_lsf_apprentissage___4':0,
                        'gr2_lsf_cadre___0':0, 'gr2_lsf_cadre___2':0, 'gr2_lsf_cadre___3':0, 'gr2_lsf_cadre___4':0,
                        'date_inclusion':'2021-04-07', 'age_yn': 1, 'securite_sociale_yn':1, 'consentement_yn':1, 'natif_francais_yn':1, 'droitier_yn':1, 'audition_normale_gr3_yn':1, 'lpc_gr3_yn':1,
                        'enceinte_yn':0, 'tutelle_yn':0, 'antecedents_psy_yn':0, 'substances_yn':0, 'deficit_visuel_yn':0, 'contre_indication_irm_yn':0, 'recueil_consentement_yn':1, 'date_consentement':'2021-04-07',
                        'nom_investigateur':'Laurent COHEN', 'signature_investigateur':'Signature p.o..png', 'sortie_prematuree_yn':0, 'evenements_indesirables_yn':0, 'langue_maternelle':'Francais',
                        'ecrire':4, 'dessiner':4, 'balle':4, 'ciseaux':4, 'brosse_dent':4, 'couteau':3, 'balai':4, 'allumette':4, 'cuiller':3, 'couvercle':3, 'score_manuelle':100,
                        'irm_effectuee_yn':1, 'date_irm':'2021-04-07', 'visite_dinclusion_complete':2,
                        'concentration_localizer':0, 'comprehension_lpc_son':5, 'comprehension_lpc_sans_son':2, 'comprehension_lpc_pseudo':0, 'comprehension_labial':2, 'comprehension_indices':1, 'comprehension_localier_confusion':'En LfPC complet sans son : faux confondu avec vrais',
                        'concentration_decoding':1, 'comprehension_decoding':2, 'difficulte_decoding':1, 'confiance_decoding':2, 'concentration_static':0, 'difficulte_static':0, 'confiance_static':4,
                        'vibrations_irm':0, 'concentration_vibrations_irm':0, 'bruit_irm':2, 'concentration_bruit_irm':1, 'debrief_remarques':'Exp decoding : préciser quil ne faut pas forcément identifier les syllabes. Pause entre les syllabes bienvenues... Videos lumineuses, + contraste quand la codeuse disparait Deuxième casque audio pas assez fort', 'questionnaire_debrief_complete':2}
        df = df.sort_index().reset_index(drop = True)
    
    #%% ERASE all the KO participants
    #%%generate a list of ko_participant 
    na=df.questionnaire_debrief_complete
    A_new= 0
    A=[]
    
    for index in na.index:
        if (na[index]==0):
           A_new=df.record_id[index]
           A=A + [A_new]
           
    ko_participant=A      
    
    #%%erase the ko participant from the df
    B_new=0
    B=[]
    
    for index in df.index:
        for i in range(len(ko_participant)):
            if (df.record_id[index]==ko_participant[i]):
                B_new=index
                B=B +[B_new]
                
    ko_participant_index=B 
    df= df.drop(df.index[ko_participant_index])
    #df.to_csv(nom_etude+'_essai.csv',index=False)
    df_valid_participant=df
    
    return df_valid_participant


def function_Q_lpc (nom_etude,type_csv): 
    
    from RedCap_tool_functions import clean_RC_DATA   

    #%% REMODEL THE Q_LPC ITEM
    
    #import the df previously created with the function clean_RC_DATA
    df = clean_RC_DATA (nom_etude=nom_etude, type_csv=type_csv)
    
    #%%define the df with only Q_LPC columns
    num_lim = df.columns.get_loc("questionnaire_lpc_complete")
    
    A=[i for i in range (0,num_lim)]
    df=df.iloc[:,A]
    
    #%% reorganization of data
    df.sort_values(by=['group'],inplace=True) # sorted by group
    df.reset_index(drop = True, inplace = True) # establish new index

    #%% modify value  for  gr1_nb_appareils (1 appareil was coded 0 and 2 coded 1 )	 gr1_appareil_yn
      
    for index in df.index:
        
        if (df.iloc[index]['gr1_nb_appareils']==1):
           df.loc[index, 'gr1_nb_appareils']=2
        if (df.iloc[index]['gr1_nb_appareils']==0):
           df.loc[index, 'gr1_nb_appareils']=1
                    
    #%% merging differents columns with the item "famille/ecole/amis" into a unique column where number are next to each other
    # ecole/amis/ pro ------> entourage_merged
    # 1 / 0 / 1        ------> 02
    
    #'entourage_type' 
    List =[]
    List_colonne_names=[]
    List_col_a_supprimer=[]
    for index_group in [1,2]:
        
        for num_col_checkbox in range (4): 
           
            colonne_name = 'gr'+str(index_group)+'_entourage_type___'+ str(num_col_checkbox)
            New='New_'+ colonne_name
            for index in df.index:
                if (df.loc[index][colonne_name] == 0):
                    val_colonne = ''
                if (df.loc[index][colonne_name] == 1):
                    val_colonne = str(num_col_checkbox)
                List.append(val_colonne)
            df['New_'+ colonne_name]= List    
            List=[]
            List_col_a_supprimer=List_col_a_supprimer +[colonne_name]
            List_colonne_names=List_colonne_names + [New]
            
           
    df['Entourage_merged']=df.loc[:,List_colonne_names].sum(axis=1)
    df=df.drop(List_colonne_names, axis=1, index=None, columns=None, level=None, inplace=False, errors='raise') # erase precedent column no longer usefull
    
    #%% 'lpc_apprentissage___' et 'lsf_apprentissage___'
    for index_variable in [0,1] :
        names=['lsf_apprentissage___','lpc_apprentissage___']
        
        List = []
        List_colonne_names = []
        for index_group in [1,2]:
            
            for num_col_checkbox in range(5): 
               
                colonne_name = 'gr' + str(index_group) + '_' + names[index_variable] + str(num_col_checkbox)
                New='New_'+ colonne_name
                for index in df.index: # For a given checkbox column, loop into each participant to code the response
                    if (df.loc[index][colonne_name] == 0):
                        val_colonne = ''
                    if (df.loc[index][colonne_name] == 1):
                        val_colonne = str(num_col_checkbox)
                    List.append(val_colonne) # Append the individual result to a list containing all results for this column
                df['New_'+ colonne_name] = List # Make a new version of this column with the code instead of 0 and 1
                List=[]
                List_col_a_supprimer = List_col_a_supprimer + [colonne_name]
                List_colonne_names = List_colonne_names + [New]
                
        if index_variable == 0:
            df[names[0]+'merged'] = df.loc[:,List_colonne_names].sum(axis=1) # create the final lsf_apprentissage_merged column
            df = df.drop(List_colonne_names, axis=1, index=None, columns=None, level=None, inplace=False, errors='raise') # erase the lpc_apprentissage columns no longer usefull
    
    num_col_checkbox = 5 # process the added option "licence codeur"
    colonne_name = 'gr2_lpc_apprentissage___'+ str(num_col_checkbox)
    New='New_'+ colonne_name
    for index in df.index:
        if (df.loc[index][colonne_name] == 0):
            val_colonne = ''
        if (df.loc[index][colonne_name] == 1):
            val_colonne = str(num_col_checkbox)
        List.append(val_colonne)
    df['New_'+ colonne_name] = List    
    List = []
    List_col_a_supprimer = List_col_a_supprimer + [colonne_name]
    List_colonne_names = List_colonne_names + [New]
    
    
    df[names[1]+'merged'] = df.loc[:,List_colonne_names].sum(axis=1) # create the final lpc_apprentissage_merged column
    df = df.drop(List_colonne_names, axis=1, index=None, columns=None, level=None, inplace=False, errors='raise') # erase the lsf_apprentissage columns no longer usefull

    
    #%% '_lpc_cadre___' et '_lsf_cadre___' 
    for index_variable in [0,1] :
        names=['lpc_cadre___','lsf_cadre___']
              
        List =[]
        List_colonne_names=[]
        for index_group in [1,2]:
            
            for num_col_checkbox in [0,2,3,4]: 
               
                colonne_name = 'gr'+str(index_group)+'_'+names[index_variable]+ str(num_col_checkbox)
                New='New_'+ colonne_name
                for index in df.index:
                    if (df.loc[index][colonne_name] == 0):
                        val_colonne = ''
                    if (df.loc[index][colonne_name] == 1):
                        val_colonne = str(num_col_checkbox)
                    List.append(val_colonne)
                df['New_'+ colonne_name]= List    
                List=[]
                List_colonne_names=List_colonne_names + [New]
                List_col_a_supprimer=List_col_a_supprimer + [colonne_name]
                
        df[names[index_variable]+'merged']=df.loc[:,List_colonne_names].sum(axis=1)  # create the final lpc_cadre_merged  and lsf_cadre columns
        df=df.drop(List_colonne_names, axis=1, index=None, columns=None, level=None, inplace=False, errors='raise')
    
    df=df.drop(List_col_a_supprimer, axis=1, index=None, columns=None, level=None, inplace=False, errors='raise')
    
    
    #%% merged gr1 and gr2 into 1 column 
    #df = df.fillna(0) #remplace NaN par des 0
    
    group_prefix= ['gr1_','gr2_']
    
    name_column = ['entourage_yn','lpc_age','lpc_freq','lpc_niv_coder','lpc_niv_comprendre','lpc_niv_labial',
                   'cs_yn','cs_age','cs_age','cs_niv_coder','cs_niv_comprendre','lsf_yn','lsf_age',
                   'lsf_freq','lsf_niv_exprimer','lsf_niv_comprendre',
                   'ls_yn','ls_age','ls_niv_exprimer','ls_niv_comprendre']
    
    List_a_supp = []
    for i in range(len(name_column)):
        gr1gr2=[]
        for index_variable in [0,1]:
          A= group_prefix[index_variable]+name_column[i]
          List_a_supp=List_a_supp + [A]
          gr1gr2.append(A)
          
          
        df[name_column[i]]=(df.loc[:,gr1gr2]).sum(axis=1)  #concatenation via sum 
        df[name_column[i]]=df[name_column[i]].astype(int)  #change into int
        
    
    df=df.drop(List_a_supp, axis=1, index=None, columns=None, level=None, inplace=False, errors='raise') #erase the previous "gr1" and "gr2" column no longer usefull
    A=df
    
    #%% turning float to integer
    
    df=df.fillna(0) #remplace NaN par des 0
    
    gr1_names = ['gr1_surdite_yn','gr1_degre_surdite','gr1_surdite_progessive_yn','gr1_age_apparition_surdite',
                 'gr1_age_surdite_severe','gr1_age_surdite','gr1_famille_yn','gr1_implant_yn','gr1_implant_age',
                 'gr1_nb_implants','gr1_temps_implant','gr1_appareil_yn','gr1_nb_appareils',
                 'gr1_temps_appareil','gr1_lpc_niv_lecture','gr1_lpc_lecture_age','gr1_lpc_lecture_difficultes_yn']
    for index in df.index:
        for i in range(len(gr1_names)):
            
            if (df.loc[index][gr1_names[i]]!=int): 
             df[gr1_names[i]]=df[gr1_names[i]].astype(int)   
         

    #%%sort values       
    df.sort_values(by=['record_id'],inplace=True) # sorted by group
    df.reset_index(drop = True, inplace = True) # establish new index
         
    #%% erase some unecessary columns 
    df=df.drop(['redcap_survey_identifier','traitement_donnees','questionnaire_lpc_timestamp','vision'], axis=1, index=None, columns=None, level=None, inplace=False, errors='raise')
    #df.to_csv(nom_etude+'_Q_LPC_essai.csv',index=False)
    
    Q_LPC_df=df
    
    return Q_LPC_df   
    

def function_inclusion (nom_etude,type_csv):
    
    from RedCap_tool_functions import clean_RC_DATA   

    #%% CALCULATE THE LATERALITY SCORE
    
    #import the df previously created with the function clean_RC_DATA
    df = clean_RC_DATA (nom_etude=nom_etude,type_csv=type_csv )  
    
    #%%define the df with only inclusion columns + column [0]= 'Record Id'
    num_lim_1 = df.columns.get_loc("questionnaire_lpc_complete")
    num_lim_2 = df.columns.get_loc("visite_dinclusion_complete")
    A= [0]+[i for i in range (num_lim_1+1,num_lim_2)]
    df=df.iloc[:,A]
    
    df.sort_values(by=['record_id'],inplace=True) # sorted by group
    df.reset_index(drop = True, inplace = True) # establish new index


    #%% attributing variables to edinburg questionnaire items  /!\faire bibliothèque pour optimiser
    
    ehi_0='ecrire'
    ehi_1='dessiner'
    ehi_2='balle'
    ehi_3='ciseaux'
    ehi_4='brosse_dent'
    ehi_5='couteau'
    ehi_6='balai'
    ehi_7='allumette'
    ehi_8='cuiller'
    ehi_9='couvercle'
    
    #%% Import and convert laterality answer into equivalent number
    
    for i in range (10): 
        colonne_name = eval('ehi_'+ str(i))
       
        for index in df.index:
            if (df.iloc[index][colonne_name] == 4):
                df.loc[index, colonne_name] = '2'
            elif (df.iloc[index][colonne_name] == 3):
                 df.loc[index, colonne_name] = '1'
            elif (df.iloc[index][colonne_name] == 2):
                 df.loc[index, colonne_name] = '0'
            elif (df.iloc[index][colonne_name] == 1):
                 df.loc[index, colonne_name] = '-1'
            elif (df.iloc[index][colonne_name] == 0):
                 df.loc[index, colonne_name] = '-2'
            else :
                 df.loc[index, colonne_name] = '0'    #debuging line for the inlcusion not complete
          
    #%% calculate laterality score - according to edinburg score : [(Right -Left) /(Right + Left)]* 100  with 100 = full right handed | 0 = full ambidextre  | -100 = fill left handed
    
    Laterality_item_names= []  #generate the 10 Laterality item names in a list
    
    for i in range (10): 
        New= eval('ehi_'+ str(i))
        Laterality_item_names= Laterality_item_names + [New]
        
        
    for i in range (10):       #calculate the laterality score with the 10 Items 
        
        colonne_name = eval('ehi_'+ str(i))
       
        df[colonne_name] = df[colonne_name].astype(str).astype(int)
    
    df['laterality score']=(df.loc[:,Laterality_item_names].sum(axis=1)/abs(df.loc[:, Laterality_item_names]).sum(axis=1))*100
    
    
    #%% save into csv file
    
    Lat_score_df=df.loc[:,['record_id','laterality score']]  #only select the 2 column of interest
    #Lat_score_df.to_csv( nom_etude +'_laterality_score.csv',index=False)
    
    return Lat_score_df


def function_debrief (nom_etude,type_csv):
    
    from RedCap_tool_functions import clean_RC_DATA   

    #%% CALCULATE THE LATERALITY SCORE
    
    #import the df previously created with the function clean_RC_DATA
    df = clean_RC_DATA (nom_etude=nom_etude,type_csv=type_csv) 
    
    num_lim_1 = df.columns.get_loc("visite_dinclusion_complete")
    num_lim_2 = df.columns.get_loc("questionnaire_debrief_complete")
    
    df.sort_values(by=['record_id'],inplace=True) # sorted by group
    df.reset_index(drop = True, inplace = True) # establish new index

    A= [0]+[i for i in range (num_lim_1+1,num_lim_2)]
    df=df.iloc[:,A]
    
    # Annahita: Get rid of the '0' in the loc vid answers
    # df = df.astype('int')
    for index in df.index:
        if int(df['comprehension_lpc_son'].loc[index]) == 0:
            df['comprehension_lpc_son'].loc[index] = 5
        if int(df['comprehension_lpc_sans_son'].loc[index]) == 0:
            if int(df['record_id'].loc[index]) == 23:
                df['comprehension_lpc_sans_son'].loc[index] = 1
            else:
                df['comprehension_lpc_sans_son'].loc[index] = int(df['comprehension_lpc_son'].loc[index])
        if int(df['comprehension_lpc_pseudo'].loc[index]) == 0:
            df['comprehension_lpc_pseudo'].loc[index] = int(df['comprehension_lpc_sans_son'].loc[index])

    df_debrief = df
  
    return df_debrief
    

def function_final_table(nom_etude,type_csv):
    
    from RedCap_tool_functions import function_debrief, function_Q_lpc , function_inclusion 
     
    #%% CHOOSE YOUR ARGUMENT
    #nom_etude= 'cuspex' 
    #nom_etude= 'custime' 
      
    df1 = function_Q_lpc(nom_etude=nom_etude,type_csv=type_csv)
    df2 = function_inclusion (nom_etude=nom_etude,type_csv=type_csv)
    df3 = function_debrief (nom_etude=nom_etude,type_csv=type_csv)
    
    #%% erase basic stuff
    df2=df2.drop(['record_id'], axis=1, index=None, columns=None, level=None, inplace=False, errors='raise')
    df3=df3.drop(['record_id'], axis=1, index=None, columns=None, level=None, inplace=False, errors='raise')  #only select the 3 columns of interest
    
    #%% generate final table
    df4= pd.concat([df1,df2,df3],axis=1)
    # Annahita: Replace the questionnaire ID with the final MRI ID
    df4 = df4.rename(columns={'id_sujet': 'subject'})
    df4['subject'] = [12, 25, 28, 26, 11, 27, 21, 24, 13, 221, 22, 23, 16,
                      f'{1:02d}', 14, 19, 31, 214, 211, 17, 29, 215, 15, 212,
                      210, 213, 18, 216, 39, 310, 35, 33, 32, 37, 311, 36, 315,
                      312, 38, 34, 316, 110, 111, 313, 314, 113, 115, 317, 217,
                      117, 112, 114, 318, 219, 220, 218, 319, 116, 118, 119]
    df4 = df4.drop(['record_id'], axis=1, index=None, columns=None, level=None, inplace=False, errors='raise')
    df=df4
    
#%%could save into a CSV for the raw data at this stage, according to CSV type 
         
#    if type_csv == 'without_comment':   
#         df4.to_csv(nom_etude +'_tableau_final_raw_data.csv',index=False)                                    
#    else :
#       df4.to_csv(nom_etude +'_tableau_final_raw_data_comm.csv',index=False)
      
    #%% GENERATE 2 FINALS TABLE AT DIFFERENT LEVEL
    
        #LEVEL 1: generate demography table
    if nom_etude== 'cuspex':
        erase_lvl_1=['metal','pref_manuelle','gr1_surdite_yn','gr1_surdite_progessive_yn','gr1_implant_yn','gr1_implant_age',
                 'gr1_nb_implants','gr1_temps_implant','gr1_appareil_yn','bruit_irm','concentration_bruit_irm']
        
        erase_lvl_1_comm=['native_language','vision_precision','precision_metal','origine_sujet',
                          'gr1_entourage_type_precision']
    else :
        erase_lvl_1=['pref_manuelle','gr1_surdite_yn','gr1_surdite_progessive_yn','gr1_implant_yn','gr1_appareil_yn']
        
        erase_lvl_1_comm=['native_language','vision_precision','origine_sujet',
                      'gr1_entourage_type_precision']

    
    df=df.drop(erase_lvl_1, axis=1, index=None, columns=None, level=None, inplace=False, errors='raise')
    
    # Take care of leading zeroes that drop when saving the csv file by appending them to the end
    column_names = ['Entourage_merged','lsf_apprentissage___merged','lpc_apprentissage___merged','lsf_cadre___merged','lpc_cadre___merged']
    for column_name in column_names:
        for index in df.index:
            if df[column_name].loc[index].startswith('0') and len(df[column_name].loc[index]) > 1:
                df[column_name].loc[index] = df[column_name].loc[index].replace('0','')
                df[column_name].loc[index] = df[column_name].loc[index] + '0'
    
    # LEVEL 1 : save into CSV file
    if type_csv == 'without_comment':
        df.to_csv('RedCap_data_processed/' + nom_etude +'_tableau_final_demography.csv',index=False)
    else :
        df=df.drop(erase_lvl_1_comm, axis=1, index=None, columns=None, level=None, inplace=False, errors='raise')  
        df.to_csv('RedCap_data_processed/' + nom_etude +'_tableau_final_demography_comm.csv',index=False)
    
    print('  Table_demography.csv generated !')
    
    # LEVEL 2: covariable table
    if nom_etude== 'cuspex':
        erase_lvl_2 = ['group','gr1_age_apparition_surdite','gr1_age_surdite_severe','gr1_age_surdite',
                       'gr1_famille_yn','gr1_temps_appareil','Entourage_merged','lsf_apprentissage___merged',
                       'lpc_apprentissage___merged','lpc_cadre___merged','lsf_cadre___merged','entourage_yn',
                       'cs_yn','cs_age','cs_niv_coder','cs_niv_comprendre','ls_yn','ls_age','ls_niv_exprimer','ls_niv_comprendre',
                       'vibrations_irm','concentration_vibrations_irm']
        
    else :
        erase_lvl_2 = ['group','gr1_age_apparition_surdite','gr1_age_surdite_severe','gr1_age_surdite',
                       'gr1_famille_yn','gr1_temps_appareil','Entourage_merged','lsf_apprentissage___merged',
                       'lpc_apprentissage___merged','lpc_cadre___merged','lsf_cadre___merged','entourage_yn',
                       'cs_yn','cs_age','cs_niv_coder','cs_niv_comprendre','ls_yn','ls_age','ls_niv_exprimer','ls_niv_comprendre']
    

    df=df.drop(erase_lvl_2, axis=1, columns=None, level=None, inplace=False, errors='raise')
    
    # LEVEL 2: save into CSV file 
        
    if type_csv == 'without_comment':                                     
        df.to_csv('RedCap_data_processed/' + nom_etude +'_tableau_final_covariates.csv')
        
    print('  Table_covariable.csv generated !')
    print('  :D ')
    
    return df 


#%% List of the demography item from the commented CSV


#    cuspex
#         erase_lvl_2_comm = ['gr1_cause_surdite','gr1_degre_parente','gr1_degre_surdite_famille','gr1_famille_appareil','gr1_famille_langage'
#                       ,'gr1_famille_cause','gr1_entourage_langage','gr1_entourage_appareil','gr1_lpc_apprentissage_precision','gr1_scolarisation'
#                       ,'gr1_lpc_lecture_difficultes_precision','gr1_cs_identite','gr1_lsf_apprentissage_precision','gr1_lsf_cadre_precision'
#                      ,'gr1_ls_identite','gr1_commentaires','gr2_entourage_type_precision','gr2_entourage_langage','gr2_entourage_appareil'
#                       ,'gr2_lpc_raison','gr2_lpc_cadre_precision','gr2_cs_identite','gr2_lsf_apprentissage_precision','gr2_lsf_cadre_precision'
#                        ,'gr2_ls_identite','gr2_commentaires','comprehension_localier_confusion','debrief_remarques']

#     custime
#         erase_lvl_2_comm = ['gr1_cause_surdite','gr1_degre_parente','gr1_degre_surdite_famille','gr1_famille_appareil','gr1_famille_langage'
#                       ,'gr1_famille_cause','gr1_entourage_langage','gr1_entourage_appareil','gr1_lpc_apprentissage_precision','gr1_scolarisation' 
#                       ,'gr1_lpc_lecture_difficultes_precision','gr1_cs_identite','gr1_lsf_apprentissage_precision','gr1_lsf_cadre_precision'
#                       ,'gr1_ls_identite','gr1_commentaires','gr2_entourage_type_precision','gr2_entourage_langage','gr2_entourage_appareil'
#                        ,'gr2_lpc_raison','gr2_lpc_cadre_precision','gr2_cs_identite','gr2_lsf_apprentissage_precision','gr2_lsf_cadre_precision'
#                        ,'gr2_ls_identite','gr2_commentaires','debrief_remarques']
