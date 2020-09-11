from __future__ import print_function
from __future__ import division
from nilmtk import DataSet, HDFDataStore
from nilmtk.disaggregate import fhmm_exact
from nilmtk.metrics import f1_score
from os.path import join
import matplotlib.pyplot as plt


##//////////////////////////////////// DESAGREGAÇÃO///////////////////////////////////////



"""
This file replicates issue #376 (which should now be fixed)
https://github.com/nilmtk/nilmtk/issues/376
"""


data_dir = ''
building_number = 2

# Tati: This line is about the disaggregated file #disag-fhmm3.h5
disag_filename = join(data_dir, 'ukdalekD2' + str(building_number) + '.h5')

# print("disag_filename:  ", disag_filename)

# data = DataSet(join(data_dir, 'redd.h5'))
data = DataSet(join(data_dir, 'ukdale.h5'))

print("Loading building " + str(building_number))
elec = data.buildings[building_number].elec
print("elec:  ", elec)
# print("elec_meters:  ", elec['microwave'])
# print("elec_meters  2 :  ", elec[1])


top_train_elec = elec.submeters().select_top_k(k=2)
#top_train_elec = elec.submeters()
# print("top_train_elec: ", top_train_elec)


# Talvez seja essa a parte que desagrega
fhmm = fhmm_exact.FHMM()
print("fhmm: ", fhmm)

fhmm.train(top_train_elec)

output = HDFDataStore(disag_filename, 'w')
fhmm.disaggregate(elec.mains(), output)
output.close()

