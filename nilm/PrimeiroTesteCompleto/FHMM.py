from __future__ import print_function, division
import  imp, sys
from os.path import join
from nilmtk import DataSet, HDFDataStore, RNNDisaggregator
from nilmtk.disaggregate import fhmm_exact
from nilmtk.metrics import f1_score
import matplotlib.pyplot as plt
from nilmtk import metricas


#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
data_dir = ''
building_number = 2


disag_filename = join(data_dir, 'disag-fhmm2' + str(building_number) + '.h5')

print("disag_filename:  ", disag_filename)

data = DataSet(join(data_dir, 'redd.h5'))
#data = DataSet(join(data_dir, 'ukdale.h5'))
print("data", data.store.load_metadata())



print("Loading building " + str(building_number))
elec = data.buildings[building_number].elec
#print("elec:  ", elec)
#print("elec_meters:  ", elec['microwave'])
#print("elec_meters  2 :  ", elec[1])



top_train_elec = elec.submeters().select_top_k(k=1)
print("\ntop_train_elec: ", top_train_elec)


#Essa a parte que desagrega
fhmm = fhmm_exact.FHMM()
fhmm.train(top_train_elec)
#fhmm.nexTrain()


print("elec",elec.mains())


output = HDFDataStore(disag_filename, 'w')
fhmm.disaggregate(elec.mains(), output)
output.close()


### f1score fhmm
disag = DataSet(disag_filename)
disag_elec = disag.buildings[building_number].elec
print("fhmm: ", disag_elec)


#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
#########Adauto###########
print("Estudando o problema o plot")	
#disag_elec.plot('separate lines')

##########FIM!############
disag_elec.plot()
plt.ylabel('appliance')
plt.xlabel('valor')
plt.title("FHMM")
plt.xlim(('2013-06-06', '2013-07-06'))
plt.savefig(join(data_dir, 'f1-fhmmttz5' + str(building_number) + '.png'))

#///////////////////////////////////////////////////////////////////


#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
plt.figure()
disag_elec.plot()
plt.ylabel('potência [W]')
plt.xlabel('data')
plt.title("Desagregação")
plt.xlim(('2013-06-06', '2013-07-06'))
plt.ylim((0, 5000))
plt.savefig(join(data_dir, 'f1-fhmmz67' + str(building_number) + '.png'))
disag.store.close()
#///////////////////////////////////////////////////////////////////
