from __future__ import print_function, division
from nilmtk import DataSet, HDFDataStore, RNNDisaggregator
from nilmtk.disaggregate import fhmm_exact
from nilmtk.metrics import f1_score
from os.path import join
import matplotlib.pyplot as plt

"""
This file replicates issue #376 (which should now be fixed)
https://github.com/nilmtk/nilmtk/issues/376
"""




"""
#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
data_dir = ''
building_number = 2

#Tati: This line is about the disaggregated file #disag-fhmm3.h5
disag_filename = join(data_dir, 'disag-fhmm' + str(building_number) + '.h5')

#print("disag_filename:  ", disag_filename)

#data = DataSet(join(data_dir, 'redd.h5'))
data = DataSet(join(data_dir, 'redd.h5'))



print("Loading building " + str(building_number))
elec = data.buildings[building_number].elec
print("elec:  ", elec)
#print("elec_meters:  ", elec['microwave'])
#print("elec_meters  2 :  ", elec[1])



top_train_elec = elec.submeters().select_top_k(k=3)
#print("top_train_elec: ", top_train_elec)


#Talvez seja essa a parte que desagrega
fhmm = fhmm_exact.FHMM()
print("fhmm: ", fhmm)


fhmm.train(top_train_elec)

output = HDFDataStore(disag_filename, 'w')
fhmm.disaggregate(elec.mains(), output)
output.close()


### f1score fhmm
disag = DataSet(disag_filename)
disag_elec = disag.buildings[building_number].elec


"""






""""
elec.mains().plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("FHMM");
plt.savefig(join(data_dir, 'f1-fhmmtt7' + str(building_number) + '.png'))
disag.store.close()
"""







"""
#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
disag_elec[1].plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("FHMM");
plt.savefig(join(data_dir, 'f1-fhmmtt101' + str(building_number) + '.png'))

#///////////////////////////////////////////////////////////////////


#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
plt.figure()
disag_elec.plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("FHMM");
plt.savefig(join(data_dir, 'f1-fhmmtt101' + str(building_number) + '.png'))
disag.store.close()
#///////////////////////////////////////////////////////////////////

"""


"""
f1 = f1_score(disag_elec, elec)
f1.index = disag_elec.get_labels(f1.index)
f1.plot(kind='barh')
plt.ylabel('appliance');
plt.xlabel('f-score');
plt.title("FHMM");
plt.savefig(join(data_dir, 'f1-fhmm' + str(building_number) + '.png'))
disag.store.close()
####
print("Finishing building " + str(building_number))
"""

print("INICIANDO REDE:  ")
train = DataSet('redd.h5')
train.set_window(end="30-4-2011") #Use data only until 4/30/2011
train_elec = train.buildings[1].elec

rnn = RNNDisaggregator()

train_mains = train_elec.mains().all_meters()[0] # The aggregated meter that provides the input
train_meter = train_elec.submeters()['microwave'] # The microwave meter that is used as a training target

rnn.train(train_mains, train_meter, epochs=2, sample_period=2)
rnn.export_model("model-redd5.h5")


#///////////////////////////////////////////////////////////////////////////////
test = DataSet('redd.h5')
test.set_window(start="23-4-2011")
test_elec = test.buildings[1].elec
test_mains = test_elec.mains().all_meters()[0]

disag_filename = 'disag-out.h5' # The filename of the resulting datastore

output = HDFDataStore(disag_filename, 'w')
# test_mains: The aggregated signal meter
# output: The output datastore
# train_meter: This is used in order to copy the metadata of the train meter into the datastore
rnn.disaggregate(test_mains, output, train_meter, sample_period=1)



#///////////////////////////////////////////////////////////////////////////////
result = DataSet(disag_filename)
res_elec = result.buildings[1].elec
predicted = res_elec['microwave']
ground_truth = test_elec['microwave']

#///////////////////////////////////////////////////////////////////////////////
predicted.plot()
ground_truth.plot()
plt.show()

#///////////////////////////////////////////////////////////////////////////////
rpaf = metricas.recall_precision_accuracy_f1(predicted, ground_truth)
print("============ Recall: {}".format(rpaf[0]))
print("============ Precision: {}".format(rpaf[1]))
print("============ Accuracy: {}".format(rpaf[2]))
print("============ F1 Score: {}".format(rpaf[3]))

print("============ Relative error in total energy: {}".format(metricas.relative_error_total_energy(predicted, ground_truth)))
print("============ Mean absolute error(in Watts): {}".format(metricas.mean_absolute_error(predicted, ground_truth)))


#Pra plotar a desagregação:
#///////////////////////////////////////////////////////////////////
plt.figure()
train_elec.plot()
plt.ylabel('dispositivo');
plt.xlabel('valor');
plt.title("Residencia");
plt.savefig(join( 'artg'  + '.png'))
#///////////////////////////////////////////////////////////////////