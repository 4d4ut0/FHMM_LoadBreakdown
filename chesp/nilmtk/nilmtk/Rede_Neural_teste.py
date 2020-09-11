import warnings; warnings.filterwarnings('ignore')

from nilmtk.datastore import HDFDataStore
from rnndisaggregator import RNNDisaggregator
import matplotlib.pyplot as plt
from nilmtk import DataSet
#train = DataSet('ukdale.h5')
train = DataSet('redd.h5')
train.set_window(end="30-4-2011")
train_elec = train.buildings[1].elec

#train.set_window(start="06-06-2013")
#train.set_window(end="06-07-2013")
#train_elec = train.buildings[2].elec


rnn = RNNDisaggregator()

#train_mains = train_elec.mains() # The aggregated meter that provides the input
#train_meter = train_elec.submeters().select_top_k(k=5)

train_mains = train_elec.mains().all_meters()[0] # The aggregated meter that provides the input
train_meter = train_elec.submeters()['microwave'] # The microwave meter that is used as a training target

rnn.train(train_mains, train_meter, epochs=5, sample_period=1)
rnn.export_model("model-redd5.h5")

#rnn.train(train_mains, train_meter, epochs=5, sample_period=1)
#rnn.export_model("nn-ukdale.h5")


#test = DataSet('ukdale.h5')
#test.set_window(start="06-06-2013")
#test.set_window(end="06-07-2013")
#test_elec = test.buildings[2].elec.submeters().select_top_k(k=5)
#test_mains = test_elec.mains()
#disag_filename = 'disagnn-out.h5' # The filename of the resulting datastore


test = DataSet('redd.h5')
test.set_window(start="30-4-2011")
test_elec = test.buildings[1].elec
test_mains = test_elec.mains().all_meters()[0]

disag_filename = 'disag-out.h5'

output = HDFDataStore(disag_filename, 'w')

# test_mains: The aggregated signal meter
# output: The output datastore
# train_meter: This is used in order to copy the metadata of the train meter into the datastore
rnn.disaggregate(test_mains, output, train_meter, sample_period=1)

"""
result = DataSet(disag_filename)
res_elec = result.buildings[2].elec
predicted = res_elec['computer monitor']
ground_truth = test_elec['computer monitor']
"""

result = DataSet(disag_filename)
res_elec = result.buildings[1].elec
predicted = res_elec['microwave']
ground_truth = test_elec['microwave']

import matplotlib.pyplot as plt
predicted.plot()
ground_truth.plot()
plt.show()


#import metrics
#rpaf = metrics.recall_precision_accuracy_f1(predicted, ground_truth)
#print("============ Recall: {}".format(rpaf[0]))
#print("============ Precision: {}".format(rpaf[1]))
#print("============ Accuracy: {}".format(rpaf[2]))
#print("============ F1 Score: {}".format(rpaf[3]))

#print("============ Relative error in total energy: {}".format(metrics.relative_error_total_energy(predicted, ground_truth)))
#print("============ Mean absolute error(in Watts): {}".format(metrics.mean_absolute_error(predicted, ground_truth)))




""""

#<class 'list'>: [Appliance(type='computer monitor', instance=1)]

plt.figure()
predicted.plot()
ground_truth.plot()
plt.show()

#<class 'list'>: [Appliance(type='computer monitor', instance=1)]
plt.figure()
predicted2.plot()
testim.plot()
plt.show()


result = DataSet(disag_filename)
res_elec = result.buildings[2].elec
predicted9 = res_elec[8]
testim3 = test_elec[8]

plt.figure()
predicted9.plot()
testim3.plot()
plt.show()

"""
