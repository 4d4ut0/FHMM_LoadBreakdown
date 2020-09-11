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
building_number = 2
UNIT = 'kW'

#Tati: This line is about the disaggregated file #disag-CO3.h5
disag_filename = join(data_dir, 'disag-CO_ukdale222' + str(building_number) + '.h5')

#print("disag_filename:  ", disag_filename)

#data = DataSet(join(data_dir, 'redd.h5'))
data = DataSet(join(data_dir, 'ukdale.h5'))

TZ_STRING = data.metadata['timezone']
TZ = pytz.timezone(TZ_STRING)
print("CARREGUEI O DATASET")


print("Loading building " + str(building_number))
elec = data.buildings[building_number].elec
print("elec:  ", elec)
#print("elec_meters:  ", elec['microwave'])
#print("elec_meters  2 :  ", elec[1])

print("SELECIONANDO OS TOPS")

top_train_elec = elec.submeters().select_top_k(k=5)
#print("top_train_elec: ", top_train_elec)


CO =CombinatorialOptimisation()
#print("CO: ", CO)
#print("CHEGUEI ATE AQUI")



#########################################################################################################
CO.train(top_train_elec)

#Abre o arquivo, não escreve no arquivo
output = HDFDataStore(disag_filename, 'w')
#print("OUTPUT1::::", output)



#SEPARA E ESCREVE!!!!!!!!!!!!!!!
CO.disaggregate(elec.mains(), output)


#print("OUTPUT2::::", output)
output.close()


### f1score CO
disag = DataSet(disag_filename)
disag_elec = disag.buildings[building_number].elec

print("disag_elec", disag_elec)

""""
elec.mains().plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.savefig(join(data_dir, 'f1-COtt7' + str(building_number) + '.png'))
disag.store.close()
"""

#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
plt.figure()
disag_elec[1].plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-06-06', '2013-07-06'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'f1-CO_ukdale_GERAL' + str(building_number) + '.png'))

#///////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////
plt.figure()
disag_elec[14].plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-06-06', '2013-07-06'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'f1-CO_ukdale_FRIDGE' + str(building_number) + '.png'))

#///////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////
plt.figure()
disag_elec[13].plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-06', '2013-10'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'f1-CO_ukdale_DISH' + str(building_number) + '.png'))



plt.figure()
elec.mains().plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-06-06', '2013-07-06'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'INPUT_TOTAL_UKDALE_CO' + str(building_number) + '.png'))




#///////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////
plt.figure()
disag_elec[3].plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-06', '2013-10'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'f1-CO_ukdale_MONITOR' + str(building_number) + '.png'))

#///////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////
plt.figure()
disag_elec[8].plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-06', '2013-10'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'f1-CO_ukdale_KETTLE' + str(building_number) + '.png'))

#///////////////////////////////////////////////////////////////////

##-------------------------------------------------------------------------------------------------
##TOTAL:
##-------------------------------------------------------------------------------------------------


#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
plt.figure()
disag_elec.plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-06', '2013-10'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'f1-fhmmtt11' + str(building_number) + '.png'))

#///////////////////////////////////////////////////////////////////

#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
plt.figure()
disag_elec[13].plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-06', '2013-10'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'DISAG_DISH_UKDALE_CO' + str(building_number) + '.png'))

plt.figure()
elec[13].plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-06', '2013-10'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'INPUT_DISH_UKDALE_CO' + str(building_number) + '.png'))

#///////////////////////////////////////////////////////////////////




#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
plt.figure()
disag_elec[1].plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-06', '2013-10'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'DISAG_TOTAL_UKDALE_CO' + str(building_number) + '.png'))

plt.figure()
elec.mains().plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-06', '2013-10'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'INPUT_TOTAL_UKDALE_CO' + str(building_number) + '.png'))

#///////////////////////////////////////////////////////////////////



#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
plt.figure()
disag_elec[1].plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-09-26', '2013-09-27'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'DISAG_TOTAL_UKDALE_CO_PARCIAL' + str(building_number) + '.png'))

plt.figure()
elec.mains().plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-09-26', '2013-09-27'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'INPUT_TOTAL_UKDALE_CO_PARCIAL' + str(building_number) + '.png'))

#///////////////////////////////////////////////////////////////////