
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





data_dir = ''
building_number = 1
UNIT = 'kW'
disag_filename = join('ZZZZZZZZZZZZZZZZZZZZZZZZZZ' + str(building_number) + '.h5')

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
plt.xlim(('2013-06', '2013-10'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'f1-CO_NEXukdale_GERAL' + str(building_number) + '.png'))

#///////////////////////////////////////////////////////////////////


plt.figure()
elec.mains().plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-06', '2013-10'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'INPUT_TOTAL_NEXUKDALE_CO' + str(building_number) + '.png'))




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
plt.savefig(join(data_dir, 'f1-NEXfhmmtt11' + str(building_number) + '.png'))

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
plt.savefig(join(data_dir, 'DISAG_TOTAL_NEXUKDALE_CO' + str(building_number) + '.png'))

plt.figure()
elec.mains().plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-06', '2013-10'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'INPUT_TOTAL_NEXUKDALE_CO' + str(building_number) + '.png'))

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
plt.savefig(join(data_dir, 'DISAG_TOTAL_NEXUKDALE_CO_PARCIAL' + str(building_number) + '.png'))

plt.figure()
elec.mains().plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("CO");
plt.xlim(('2013-09-26', '2013-09-27'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'INPUT_TOTAL_NEXUKDALE_CO_PARCIAL' + str(building_number) + '.png'))

#///////////////////////////////////////////////////////////////////