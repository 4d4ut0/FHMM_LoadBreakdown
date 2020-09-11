from __future__ import print_function, division
from nilmtk import DataSet, HDFDataStore
from nilmtk.disaggregate import CombinatorialOptimisation
from nilmtk.metrics import f1_score
from os.path import join
import matplotlib.pyplot as plt
import pytz
from datetime import timedelta
import plot_config
from pylab import rcParams
import seaborn as sns

"""
This file replicates issue #376 (which should now be fixed)
https://github.com/nilmtk/nilmtk/issues/376
"""


#########################################################################################################
data_dir = ''
building_number = 1
UNIT = 'kW'

#Tati: This line is about the disaggregated file #disag-CO3.h5
disag_filename = join('ZZZZZZZZZZZZZZZZZZZZZZZZZZ' + str(building_number) + '.h5')

#print("disag_filename:  ", disag_filename)

#data = DataSet(join(data_dir, 'redd.h5'))
data = DataSet(join(data_dir, 'nexdataset_ukdalek.h5'))

TZ_STRING = data.metadata['timezone']
TZ = pytz.timezone(TZ_STRING)
print("CARREGUEI O DATASET")


print("Loading building " + str(building_number))
elec = data.buildings[building_number].elec
print("elec:  ", elec)
#print("elec_meters:  ", elec['microwave'])
#print("elec_meters  2 :  ", elec[1])

print("SELECIONANDO OS TOPS")

top_train_elec = elec.submeters().select_top_k(k=2)
#print("top_train_elec: ", top_train_elec)


#Talvez seja essa a parte que desagrega
CO =CombinatorialOptimisation()
print("CO: ", CO)
print("CHEGUEI ATE AQUI")



#########################################################################################################
CO.train(top_train_elec)

#Abre o arquivo, não escreve no arquivo
output = HDFDataStore(disag_filename, 'w')
print("OUTPUT1::::", output)



#SEPARA E ESCREVE!!!!!!!!!!!!!!!
CO.disaggregate(elec.mains(), output)


print("OUTPUT2::::", output)
output.close()

