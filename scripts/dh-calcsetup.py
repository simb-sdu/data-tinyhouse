from brightway2 import *
import pandas as pd

projects.set_current('tinyhouse')
functional_units = []
lcia_methods = []



def methodAppender(include,exclude):
	for m in methods:				#'methods' if a command that is recognized by brightway
		if include in m:
			if exclude not in m:
				lcia_methods.append(m)
			
def fuAppender(d, proces_search, db_search):
	if db_search in d:
		if "_ecoinvent" not in d: 
			result = {Database(d).search(proces_search.casefold())[0].key: 1}
			if result not in functional_units:
				functional_units.append(result)
				print(d)






def resultsExport(calcsetup):
	#nicer but not sure it works
	#https://stackoverflow.com/questions/42984831/create-a-dataframe-from-multilca-results-in-brightway2 
	mlca = MultiLCA(calcsetup)
	scores = pd.DataFrame(mlca.results, columns=mlca.methods)

	as_activities = [
	    (get_activity(key), amount) 
	    for dct in mlca.func_units 
	    for key, amount in dct.items()
	]
	nicer_fu = pd.DataFrame(
	    [
		(x['database'], x['code'], x['name'], x['location'], x['unit'], y) 
		for x, y in as_activities
	    ], 
	    columns=('Database', 'Code', 'Name', 'Location', 'Unit', 'Amount')
	)
	nicer = pd.concat([nicer_fu, scores], axis=1)
	nicer.to_excel(calcsetup+".xlsx")




#---------------- create calc setup ----------------
for d in databases:					#'databases' is a command that is recognized by brightway
	#the last variable can be more or less specified - it will search if it contains it

	fuAppender(d,"market for district heat, historical","1970")
	fuAppender(d,"market for district heat, historical","2010")
	fuAppender(d,"market for district heat, future","2035")	
	fuAppender(d,"market for district heat, future","2050")				
	#fuAppender(d,"market for heat, district or industrial, other than natural gas","ecoinvent")

	
print("appended "+ str(len(functional_units))+" datasets to calculation setup")

methodAppender("EF v3.1","EN15804")	#include, exclude


#A calculation setup is a normal Python dictionary, with keys inv and ia, for the functional units and LCIA methods, respectively.
my_calculation_setup = {'inv': functional_units, 'ia': lcia_methods}


#You define a calculation setup by name in the metadata store calculation_setups, similar to the way that LCIA methods are defined.
calculation_setups['DH timeline'] = my_calculation_setup
print("calculation setup:")
print(calculation_setups['DH timeline'])


	
#----------- calculate results and export ----------------	
resultsExport('DH timeline')

