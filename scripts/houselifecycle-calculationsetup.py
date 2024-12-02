from brightway2 import *
import pandas as pd

projects.set_current('tinyhouse')
functional_units = []
lcia_methods = []

amounts = { #m2 per person
    'Tinyhouse': {
        '1970': 20,
        '2010': 20,
        '391': 20, #2024
        '2035': 20,
        '2050': 20,
    },
    'Singlefamily': {
        '1970': 42,
        '2010': 55,
        '391': 55, #2024
        '2035': 55,
        '2050': 55,
    },
    'Multifamily': {
        '1970': 39,
        '2010': 44,
        '391': 44, #2024
        '2035': 44,
        '2050': 44,
    },
}

def methodAppender(include,exclude):
	for m in methods:				#'methods' if a command that is recognized by brightway
		if include in m:
			if exclude not in m:
				lcia_methods.append(m)
			
def fuAppender(d, proces_search, db_search, house_types):
	for house_type, year_dict in house_types.items():
		for year_key, amount in year_dict.items():
			if year_key in d and db_search.casefold() in d.casefold() and house_type.casefold() in d.casefold():
				result = {Database(d).search(proces_search.casefold())[0].key: amount}
				if result not in functional_units:
					functional_units.append(result)






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
	fuAppender(d,"C2G","Multifamilyconventional", amounts)		
	fuAppender(d,"C2G","Multifamilywood", amounts)
	fuAppender(d,"C2G","Singlefamilyconventional", amounts)		
	fuAppender(d,"C2G","Singlefamilywood", amounts)
	fuAppender(d,"C2G","tinyhouse", amounts)
	fuAppender(d,"wood tinyhouse C2G","grobund tinyhouse", amounts)
	fuAppender(d,"ecococon tinyhouse C2G","grobund tinyhouse", amounts)

	
print("appended "+ str(len(functional_units))+" datasets to calculation setup")

methodAppender("EF v3.1","EN15804")	#include, exclude


#A calculation setup is a normal Python dictionary, with keys inv and ia, for the functional units and LCIA methods, respectively.
my_calculation_setup = {'inv': functional_units, 'ia': lcia_methods}


#You define a calculation setup by name in the metadata store calculation_setups, similar to the way that LCIA methods are defined.
calculation_setups['all comparison'] = my_calculation_setup
print("calculation setup:")
print(calculation_setups['all comparison'])


	
#----------- calculate results and export ----------------	
resultsExport('all comparison')

