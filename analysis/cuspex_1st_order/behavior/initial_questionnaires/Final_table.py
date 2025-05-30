# -*- coding: utf-8 -*-
"""
CUSPEX script to launch the initial questionnaire cleaning function
Original script by Imane Boudjelal

"""
from RedCap_tool_functions import function_final_table 

df3= function_final_table(nom_etude='cuspex',type_csv = 'with_comment')
df4= function_final_table(nom_etude='cuspex',type_csv = 'without_comment')
