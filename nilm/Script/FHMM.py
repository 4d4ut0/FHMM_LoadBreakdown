from __future__ import print_function, division
import  imp, sys
from os.path import join
from nilmtk import DataSet, HDFDataStore, RNNDisaggregator
from nilmtk.disaggregate import fhmm_exact
from nilmtk.metergroup import MeterGroup
from nilmtk.metrics import f1_score
import matplotlib.pyplot as plt
from nilmtk import metricas


#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
data_dir = ''
building_number = 1


disag_filename = join(data_dir, 'disag-fhmm2' + str(building_number) + '.h5')

#print("disag_filename:  ", disag_filename)

data = DataSet(join(data_dir, 'redd.h5'))
print (data.store)
'''
#data = DataSet(join(data_dir, 'ukdale.h5'))
#print("data", data.store.load_metadata()['meter_devices'].keys())
#print("data", data.store.load_metadata()['meter_devices']['REDD_whole_house']['measurements'][0]['physical_quantity'])


print("Loading building " + str(building_number))
building = data.buildings[building_number]
elec = building.elec
print("\n------------->",elec.meters[7].appliances[0])
'''
'''
top_train_elec = elec.submeters().select_top_k(k=)

print("elec.submeters(): ", elec.submeters())
print("***************************************")

print("\n***************************************")
print("\ntop_train_elec: ", top_train_elec)

print(elec.train_test_split())
#Essa a parte que desagrega
fhmm = fhmm_exact.FHMM()
fhmm.train(top_train_elec)

print("\n**************************************************\n")
print("Bonde dos treinadore: ", top_train_elec)
print("Gurizada pra testar: ",elec.mains())
print("Vem de super shock: ", elec.mains())
print("\n**************************************************\n")
output = HDFDataStore(disag_filename, 'w')
fhmm.disaggregate(elec.mains(), output)
output.close()


elec.mains().plot()
plt.ylabel('appliance')
plt.xlabel('valor')
plt.title("FHMM")
plt.xlim(('2013-06-06', '2013-07-06'))
plt.show()


### f1score fhmm
disag = DataSet(disag_filename)
disag_elec = disag.buildings[building_number].elec
print("fhmm: ", disag_elec)


#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
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
'''