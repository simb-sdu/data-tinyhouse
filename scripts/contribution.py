from bw2calc import *
from bw2data import *
from bw2data import *
from bw2io import *

projects.set_current('tinyhouse')
LCIA =  ('EF v3.1', 'climate change', 'global warming potential (GWP100)')

def save_recursive_calculation(activity, lcia_method, file, lca_obj=None, total_score=None, amount=1, level=0, max_level=3, cutoff=1e-2):
    if lca_obj is None:
        lca_obj = LCA({activity: amount}, lcia_method)
        lca_obj.lci()
        lca_obj.lcia()
        total_score = lca_obj.score
    elif total_score is None:
        raise ValueError
    else:
        lca_obj.redo_lcia({activity: amount})
        if abs(lca_obj.score) <= abs(total_score * cutoff):
            return
    z = "{}{:<5}\t{:>3.0f}\t\t({:5.1f}) \t{:.70}\n".format(" " * level, level, lca_obj.score / total_score * 100, lca_obj.score, str(activity))
    file.write(z)
    print(z)
    
    if level < max_level:
        for exc in activity.technosphere():
            save_recursive_calculation(
                activity=exc.input, 
                lcia_method=lcia_method, 
                file=file,
                lca_obj=lca_obj, 
                total_score=total_score, 
                amount=amount * exc['amount'], 
                level=level + 1, 
                max_level=max_level, 
                cutoff=cutoff
            )

def contribution_from_calcsetup(calcsetup):
    
    print("starting contribution analysis. This method is slow, so be pateint")
    
    cs = calculation_setups[calcsetup]
    
    with open('contribution_output.txt', 'w') as file:
        for lca in cs['inv']:
            for key in lca.keys():  # based on the key, find activity name
                act = get_activity(key)
                amount = list(lca.values())[0]
                
                x=f"{act.get('name')},{act.get('database')}, {amount}, {act.get('unit')}\n"
                file.write(x)
                print(x)
                
                y='LEVEL \tCONTRIBUTION % \t(KG CO2) \tACTIVITY\n'
                file.write(y)
                print(y)
                save_recursive_calculation(act, LCIA, file, amount=amount, max_level=1, cutoff=0.005)
                file.write('\n')

contribution_from_calcsetup("all comparison")
