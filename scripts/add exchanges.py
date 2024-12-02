#!/usr/bin/env python
# coding: utf-8

# In[1]:


import bw2data as bw

# Initialize the project
bw.projects.set_current("tinyhouse")

# List of ecoinvent databases
ecoinvent_dbs = [
    'cutoff391',
     'ecoinvent_cutoff_3.9_image_SSP2-Base_1860_denmark-retrospective-lca',
     'ecoinvent_cutoff_3.9_image_SSP2-Base_1890_denmark-retrospective-lca',
     'ecoinvent_cutoff_3.9_image_SSP2-Base_2010_denmark-retrospective-lca',
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
     'ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2050_dk-scenarios',
]

# Amount mapping based on year and type
amounts = { #in kWh
    'Tinyhouse': {
        '1970': 170,
        '2010': 170,
        '391': 170, #2024
        '2035': 170,
        '2050': 170,
    },
    'Singlefamily': {
        '1970': 269,
        '2010': 151,
        '391': 130, #2024
        '2035': 117,
        '2050': 99,
    },
    'Multifamily': {
        '1970': 150,
        '2010': 107,
        '391': 95, #2024
        '2035': 86,
        '2050': 73,
    },
}



#mapping to use correct energy mix for year and type
energymix = {
    'Tinyhouse': {
        '1970': 'market for residential energy, tiny house, historical',
        '2010': 'market for residential energy, tiny house, historical',
        '2035': 'market for residential energy, tiny house, future',
        '2050': 'market for residential energy, tiny house, future',
        '391': 'market for residential energy, tiny house, historical',
    },
    'Singlefamily': {
        '1970': 'market for residential energy, historical',
        '2010': 'market for residential energy, historical',
        '2035': 'market for residential energy, future',
        '2050': 'market for residential energy, future',
        '391': 'market for residential energy, historical',
    },
    'Multifamily': {
        '1970': 'market for residential energy, historical',
        '2010': 'market for residential energy, historical',
        '2035': 'market for residential energy, future',
        '2050': 'market for residential energy, future',
        '391': 'market for residential energy, historical',
    },
}


# In[2]:


# Function to determine the amount based on db_name
def get_amount(db_name):
    for key in amounts:
        if key.lower() in db_name.lower():
            for year in amounts[key]:
                if year in db_name:
                    #print(f"Amount for {key} in {year}: {amounts[key][year]}")  # Debugging output
                    return amounts[key][year]
    return 1  # Default amount if no match found

def get_mix(db_name):
    for key in energymix:
        if key.lower() in db_name.lower():
            for year in energymix[key]:
                if year in db_name:
                    #print(f"Mix for {key} in {year}: {energymix[key][year]}")  # Debugging output
                    #print("succes")
                    return energymix[key][year]
                    
    print("fail")
    return None
    


# In[3]:


# Function to add exchange
def add_exchange(db_name):
    db = bw.Database(db_name)
    #print("Looking in: " + db_name)
    for act in db:
        if "c2g" in act['name'].casefold():
            #print("Found: " + act['name'])
            
            
            for eco_db_name in ecoinvent_dbs:
                
                if eco_db_name in db_name:
                    eco_db = bw.Database(eco_db_name)
                    
                    if "391" in db_name: #if we are in 2024 (cutoff391) we must instead use the 2010 hisotircal databse, as the energy mixes do not exists in ecoinvent per standard, and it is a unreasonable work to include it.
                        eco_db = bw.Database('ecoinvent_cutoff_3.9_image_SSP2-Base_2010_denmark-retrospective-lca')
                    
                    #print("Matching ecoinvent database: " + eco_db.name)
                    mix=get_mix(db_name)
                    amount=0
                    for eco_act in eco_db:
                        if mix in eco_act['name'].casefold():
                            amount = get_amount(db_name)*3.6  # Get the amount based on db_name AND multiply by 3.6 to convert to MJ
                            
                            # Check if the exchange already exists
                            existing_exchange = next((ex for ex in act.exchanges() if ex.input == eco_act.key and ex['type'] == 'technosphere'), None)
                            
                            if existing_exchange:
                                # Overwrite the existing exchange
                                existing_exchange['amount'] = amount
                                existing_exchange.save()
                                print(f"Updated existing exchange for {eco_act['name']}.")
                            else:
                                # Create a new exchange
                                act.new_exchange(
                                    input=eco_act.key,
                                    amount=amount,  # Use the determined amount
                                    type='technosphere'
                                ).save()
                                print(f"Created new exchange for {eco_act['name']}.")
        
                                print(f"Exchange: {amount}: {eco_act['name']} from {eco_db_name}")
                                print(f"   Added to activity: {act['name']} in {db_name}")
                                print()


# In[ ]:


# Iterate over all your databases
#sometimes needs to run twice to get all? weird?

db_names = [
     'grobund tinyhouse_cutoff391',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_image_SSP2-Base_1970_denmark-retrospective-lca',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_image_SSP2-Base_2010_denmark-retrospective-lca',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_remind_SSP1-Base_2035_dk-scenarios',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_remind_SSP1-Base_2050_dk-scenarios',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2035_dk-scenarios',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2050_dk-scenarios',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_remind_SSP2-Base_2035_dk-scenarios',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_remind_SSP2-Base_2050_dk-scenarios',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2035_dk-scenarios',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2050_dk-scenarios',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_remind_SSP5-Base_2035_dk-scenarios',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_remind_SSP5-Base_2050_dk-scenarios',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2035_dk-scenarios',
     'grobund tinyhouse_ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2050_dk-scenarios',
     'Multifamilyconventional_cutoff391',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_image_SSP2-Base_1970_denmark-retrospective-lca',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_image_SSP2-Base_2010_denmark-retrospective-lca',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_remind_SSP1-Base_2035_dk-scenarios',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_remind_SSP1-Base_2050_dk-scenarios',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2035_dk-scenarios',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2050_dk-scenarios',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_remind_SSP2-Base_2035_dk-scenarios',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_remind_SSP2-Base_2050_dk-scenarios',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2035_dk-scenarios',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2050_dk-scenarios',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_remind_SSP5-Base_2035_dk-scenarios',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_remind_SSP5-Base_2050_dk-scenarios',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2035_dk-scenarios',
     'Multifamilyconventional_ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2050_dk-scenarios',
     'Multifamilywood_cutoff391',
     'Multifamilywood_ecoinvent_cutoff_3.9_image_SSP2-Base_1970_denmark-retrospective-lca',
     'Multifamilywood_ecoinvent_cutoff_3.9_image_SSP2-Base_2010_denmark-retrospective-lca',
     'Multifamilywood_ecoinvent_cutoff_3.9_remind_SSP1-Base_2035_dk-scenarios',
     'Multifamilywood_ecoinvent_cutoff_3.9_remind_SSP1-Base_2050_dk-scenarios',
     'Multifamilywood_ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2035_dk-scenarios',
     'Multifamilywood_ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2050_dk-scenarios',
     'Multifamilywood_ecoinvent_cutoff_3.9_remind_SSP2-Base_2035_dk-scenarios',
     'Multifamilywood_ecoinvent_cutoff_3.9_remind_SSP2-Base_2050_dk-scenarios',
     'Multifamilywood_ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2035_dk-scenarios',
     'Multifamilywood_ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2050_dk-scenarios',
     'Multifamilywood_ecoinvent_cutoff_3.9_remind_SSP5-Base_2035_dk-scenarios',
     'Multifamilywood_ecoinvent_cutoff_3.9_remind_SSP5-Base_2050_dk-scenarios',
     'Multifamilywood_ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2035_dk-scenarios',
     'Multifamilywood_ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2050_dk-scenarios',
     'Singlefamilyconventional_cutoff391',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_image_SSP2-Base_1970_denmark-retrospective-lca',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_image_SSP2-Base_2010_denmark-retrospective-lca',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_remind_SSP1-Base_2035_dk-scenarios',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_remind_SSP1-Base_2050_dk-scenarios',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2035_dk-scenarios',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2050_dk-scenarios',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_remind_SSP2-Base_2035_dk-scenarios',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_remind_SSP2-Base_2050_dk-scenarios',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2035_dk-scenarios',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2050_dk-scenarios',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_remind_SSP5-Base_2035_dk-scenarios',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_remind_SSP5-Base_2050_dk-scenarios',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2035_dk-scenarios',
     'Singlefamilyconventional_ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2050_dk-scenarios',
     'Singlefamilywood_cutoff391',
     'Singlefamilywood_ecoinvent_cutoff_3.9_image_SSP2-Base_1970_denmark-retrospective-lca',
     'Singlefamilywood_ecoinvent_cutoff_3.9_image_SSP2-Base_2010_denmark-retrospective-lca',
     'Singlefamilywood_ecoinvent_cutoff_3.9_remind_SSP1-Base_2035_dk-scenarios',
     'Singlefamilywood_ecoinvent_cutoff_3.9_remind_SSP1-Base_2050_dk-scenarios',
     'Singlefamilywood_ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2035_dk-scenarios',
     'Singlefamilywood_ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2050_dk-scenarios',
     'Singlefamilywood_ecoinvent_cutoff_3.9_remind_SSP2-Base_2035_dk-scenarios',
     'Singlefamilywood_ecoinvent_cutoff_3.9_remind_SSP2-Base_2050_dk-scenarios',
     'Singlefamilywood_ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2035_dk-scenarios',
     'Singlefamilywood_ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2050_dk-scenarios',
     'Singlefamilywood_ecoinvent_cutoff_3.9_remind_SSP5-Base_2035_dk-scenarios',
     'Singlefamilywood_ecoinvent_cutoff_3.9_remind_SSP5-Base_2050_dk-scenarios',
     'Singlefamilywood_ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2035_dk-scenarios',
     'Singlefamilywood_ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2050_dk-scenarios',
     'tinyhouse_cutoff391',
     'tinyhouse_ecoinvent_cutoff_3.9_image_SSP2-Base_1970_denmark-retrospective-lca',
     'tinyhouse_ecoinvent_cutoff_3.9_image_SSP2-Base_2010_denmark-retrospective-lca',
     'tinyhouse_ecoinvent_cutoff_3.9_remind_SSP1-Base_2035_dk-scenarios',
     'tinyhouse_ecoinvent_cutoff_3.9_remind_SSP1-Base_2050_dk-scenarios',
     'tinyhouse_ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2035_dk-scenarios',
     'tinyhouse_ecoinvent_cutoff_3.9_remind_SSP1-PkBudg500_2050_dk-scenarios',
     'tinyhouse_ecoinvent_cutoff_3.9_remind_SSP2-Base_2035_dk-scenarios',
     'tinyhouse_ecoinvent_cutoff_3.9_remind_SSP2-Base_2050_dk-scenarios',
     'tinyhouse_ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2035_dk-scenarios',
     'tinyhouse_ecoinvent_cutoff_3.9_remind_SSP2-PkBudg500_2050_dk-scenarios',
     'tinyhouse_ecoinvent_cutoff_3.9_remind_SSP5-Base_2035_dk-scenarios',
     'tinyhouse_ecoinvent_cutoff_3.9_remind_SSP5-Base_2050_dk-scenarios',
     'tinyhouse_ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2035_dk-scenarios',
     'tinyhouse_ecoinvent_cutoff_3.9_remind_SSP5-PkBudg500_2050_dk-scenarios',
]

for db_name in db_names:
    add_exchange(db_name)

#print(f" modified {n} activities")


# In[ ]:


def check_residential_energy_exchange(db_name):
    db = bw.Database(db_name)
    for act in db:
        if "c2g" in act['name'].casefold():
            # Check if the activity has an exchange with "residential energy"
            has_residential_energy = any("residential energy" in ex.input['name'].casefold() for ex in act.exchanges())
            if not has_residential_energy:
                print(f"Activity without 'residential energy' exchange: {act['name']} in {db_name}")

# Iterate over each database and check activities

for db_name in bw.databases:
    check_residential_energy_exchange(db_name)


# In[ ]:


#list(bw.databases)


# In[ ]:


bw.Database('ecoinvent_cutoff_3.9_image_SSP2-Base_2010_denmark-retrospective-lca').search('market for residential energy')


# In[ ]:




