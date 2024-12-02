# data-historical-LCA
This repository contains data and scripts used in my publication "historical and future LCA insights on tiny houses in Denmark".\
\
The folder excl-input contains the base brightway2 inventories.\
\
Via the script excel-find-replace-save.py, many versions of the inventories are created with different background databases (made in premise).\
\
The bulk of inventories are improted to birghtway2 via the script bw-excelimport.py. \
\
in order to make brightway activities with both materials astage and use-phase, we need to use a script to add use-phase energy use. 'run add exchanges.py'\
\
run 'houselifecycle-calculationsetup.py' to create calculation setup and save al lresults to excel (the calculation setuyp can also be opened and calculated in activity browser, but it is faster to do it this way in brightway code)\
\
use contribution.py to calculate a contrib ution analysis with desired aggregation level.\
\