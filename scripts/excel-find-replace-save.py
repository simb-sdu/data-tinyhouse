import openpyxl
import os
from os import listdir



def findReplaceSave(filename_input, old_db, new_db):
    filenameNoExtension = os.path.splitext(filename_input)[0]
    findReplace = {old_db : new_db, filenameNoExtension:filenameNoExtension + "_" + new_db}
    wb = openpyxl.load_workbook("/home/simb/Nextcloud/tinyhouse case study/excl-input/"+filename_input, data_only=True) # Set data_only=True to load values instead of formulas
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if cell.value in findReplace.keys():
                    cell.value=findReplace.get(cell.value)
        tempTuple = os.path.splitext(filename_input)
        filename_out = tempTuple[0] + "_" + new_db + ".xlsx"
        wb.save('/home/simb/Nextcloud/tinyhouse case study/excl-output/'+filename_out)


fileList = listdir ('/home/simb/Nextcloud/tinyhouse case study/excl-input/')	#path to folder with input files (lise's models)
#print(fileList)

#run list(bw.databases) in a conda environment with brightway to get the list. remeber to run projects.set_current("lise-ei391")
databases = ['cutoff391',
     #'ecoinvent_cutoff_3.9_image_SSP2-Base_1860_denmark-retrospective-lca',
     #'ecoinvent_cutoff_3.9_image_SSP2-Base_1890_denmark-retrospective-lca',
     #'ecoinvent_cutoff_3.9_image_SSP2-Base_1920_denmark-retrospective-lca',
     'ecoinvent_cutoff_3.9_image_SSP2-Base_1970_denmark-retrospective-lca',
     'ecoinvent_cutoff_3.9_image_SSP2-Base_2010_denmark-retrospective-lca',
     'ecoinvent_cutoff_3.9_remind_SSP1-Base_2035_dk-scenarios',
     'ecoinvent_cutoff_3.9_remind_SSP1-Base_2050_dk-scenarios',
     'ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2035_dk-scenarios',
     'ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2050_dk-scenarios',
     'ecoinvent_cutoff_3.9_remind_SSP2-Base_2035_dk-scenarios',
     'ecoinvent_cutoff_3.9_remind_SSP2-Base_2050_dk-scenarios',
     'ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2035_dk-scenarios',
     'ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2050_dk-scenarios',
     'ecoinvent_cutoff_3.9_remind_SSP5-Base_2035_dk-scenarios',
     'ecoinvent_cutoff_3.9_remind_SSP5-Base_2050_dk-scenarios',
     'ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2035_dk-scenarios',
     'ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2050_dk-scenarios'
 ]

for f in fileList:
	if ".~lock." not in f:
		for db in databases: #distinct between consequential and cutoff models
			if ".xlsx" in f.casefold() and "cut" in db.casefold(): findReplaceSave(f,"cutoff391", db)	#just looking for "cut" in the filename should capture all spelling variations of cut-of, cutoff, cut off etc.

	
#findReplaceSave("case1.xlsx","cutoff391", "newdb")


