from __future__ import print_function, division
from nilmtk import DataSet, HDFDataStore, RNNDisaggregator
from nilmtk.disaggregate import fhmm_exact
from nilmtk.metrics import f1_score
from os.path import join
import matplotlib.pyplot as plt
from nilmtk import metricas

"""
This file replicates issue #376 (which should now be fixed)
https://github.com/nilmtk/nilmtk/issues/376
"""





#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
data_dir = ''
building_number = 2

#Tati: This line is about the disaggregated file #disag-fhmm3.h5
disag_filename = join(data_dir, 'disag-fhmm2' + str(building_number) + '.h5')

#print("disag_filename:  ", disag_filename)

#data = DataSet(join(data_dir, 'redd.h5'))
data = DataSet(join(data_dir, 'ukdale.h5'))



print("Loading building " + str(building_number))
elec = data.buildings[building_number].elec
print("elec:  ", elec)
#print("elec_meters:  ", elec['microwave'])
#print("elec_meters  2 :  ", elec[1])



top_train_elec = elec.submeters().select_top_k(k=5)
#print("top_train_elec: ", top_train_elec)


#Essa a parte que desagrega

fhmm = fhmm_exact.FHMM()
#print("fhmm: ", fhmm)


fhmm.train(top_train_elec)

output = HDFDataStore(disag_filename, 'w')
fhmm.disaggregate(elec.mains(), output)
output.close()


### f1score fhmm
disag = DataSet(disag_filename)
disag_elec = disag.buildings[building_number].elec
print("fhmm: ", disag_elec)








""""
elec.mains().plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("FHMM");
plt.savefig(join(data_dir, 'f1-fhmmtt7' + str(building_number) + '.png'))
disag.store.close()
"""








#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
disag_elec[6].plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("FHMM");
plt.xlim(('2013-06-06', '2013-07-06'))
plt.savefig(join(data_dir, 'f1-fhmmttz5' + str(building_number) + '.png'))

#///////////////////////////////////////////////////////////////////


#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
plt.figure()
disag_elec.plot()
plt.ylabel('potência [W]');
plt.xlabel('data');
plt.title("Desagregação");
plt.xlim(('2013-06-06', '2013-07-06'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'f1-fhmmz67' + str(building_number) + '.png'))
disag.store.close()
#///////////////////////////////////////////////////////////////////




"""
f1 = f1_score(disag_elec, elec)
f1.index = disag_elec.get_labels(f1.index)
f1.plot(kind='barh')
plt.ylabel('appliance');
plt.xlabel('f-score');
plt.title("FHMM");
plt.savefig(join(data_dir, 'f1-fhmm' + str(building_number) + '.png'))
disag.store.close()

print("Finishing building " + str(building_number))
"""