import bw2data as bd
import bw2calc as bc
import bw2io as bi
import numpy as np
from pathlib import Path
import pandas as pd
import os
from os import listdir
bd.projects.set_current('tinyhouse')


def bwImport(excelFile,database):
	imp = bi.ExcelImporter(excelFile)	#"/home/simb/Nextcloud/Cut-off_DK_BAU.xlsx"
	imp.apply_strategies()
	imp.match_database(database, fields=('name','unit','location', 'reference product'))
	imp.match_database(fields=('name', 'unit', 'location'))
	imp.statistics()
	imp.write_excel()
	imp.write_database()


def multiRun():
	fileDir = '/home/simb/Nextcloud/tinyhouse case study/excl-output/'	
	fileList = listdir (fileDir)	#path to folder with input files (lises models)

	#run list(bw.databases) in a conda environment with brightway to get the list. remember to run projects.set_current("lise-ei391")
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
	n=1
	for f in fileList:
		for db in databases:
			if ".~lock." not in f:
				importdb = ""
				if db in f:
					importdb = db	#match the correct database name to the output file, and save it to a variable
					print("importing dataset "+str(n)+" of "+str(len(fileList)))
					print(fileDir + f)
					print(importdb)
					bwImport(fileDir + f, importdb)	#database variable is used here for correct importing		#!!! actually, it seems that we could just have used one file in the ecvl.output folder, it was obsolete to have one for each databse
					n+=1

#if it gives an error about locked database, then just kill all terminals and start anew
multiRun()





