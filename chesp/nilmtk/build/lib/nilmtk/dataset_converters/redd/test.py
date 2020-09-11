#from nilmtk.utils import show_versions;
#show_versions()

import h5py
import numpy as np

hdf= h5py.File('C:\\Users\\Engenharia\\nilmtk\\nilmtk\\dataset_converters\\redd\\redd.h5','r')
ls= list(hdf.keys())
print('list of datasets in this file \n', ls)

data = hdf.get('building1')
hdf.close()
data2 = np.array(data)
print(data2.shape)

f = h5py.File('redd.h5', 'r+')
f.keys()
f.values()
members = []
f.visit(members.append)
for i in range(len(members)):
    print(members[i])

#####################################################################################################

file = h5py.File('redd.h5','r+')
#
# Open "dset" dataset under the root group.
#
dataset = file['/building1']
#
# Initialize buffers,read and print data.
#
# Python float type is 64-bit, one needs to use NATIVE_DOUBLE HDF5 type to read data.
data_read64 = np.zeros((4,6,), dtype=float)
#dataset.id.read(h5py.h5s.ALL, h5py.h5s.ALL, data_read64, mtype=h5py.h5t.NATIVE_DOUBLE)
print ("Printing data 64-bit floating numbers...")
print (data_read64)

data_read32 = np.zeros((4,6,), dtype=np.float32)
#dataset.id.read(h5py.h5s.ALL, h5py.h5s.ALL, data_read32, mtype=h5py.h5t.NATIVE_FLOAT)
print ("Printing data 32-bit floating numbers...")
print (data_read32)
#
# Close the file before exiting
#
file.close()


#from nilmtk.dataset_converters import convert_redd
#convert_redd('nexdataset', 'nexdataset.h5')
#convert_redd('low_freq', 'redd.h5')

"""

from __future__ import print_function, division
import time

from nilmtk import DataSet, TimeFrame, MeterGroup, HDFDataStore
from nilmtk.disaggregate import CombinatorialOptimisation

train = DataSet('redd.h5')
test = DataSet('redd.h5')

train.set_window(end="30-4-2011")
test.set_window(start="30-4-2011")

building = 1

train_elec = train.buildings[1].elec
test_elec = test.buildings[1].elec
print("test_elec",test_elec)


fridge_meter = train_elec['fridge']
print("fridge_meter",fridge_meter)

#fridge_df = fridge_meter.load().next()
#print("fridge_df: ",fridge_df)

mains = train_elec.mains()
print("mains : ",mains)


#mains_df = mains.load().next()

top_5_train_elec = train_elec.submeters().select_top_k(k=5)

top_5_train_elec

start = time.time()


co = CombinatorialOptimisation()
# Note that we have given the sample period to downsample the data to 1 minute


co.train(top_5_train_elec, sample_period=90)
end = time.time()
print("Runtime =", end-start, "seconds.")

disag_filename = 'reddt-disag-co.h5'
output = HDFDataStore(disag_filename, 'w')
# Note that we have mentioned to disaggregate after converting to a sample period of 60 seconds
co.disaggregate(test_elec.mains(), output, sample_period=90)
output.close()

disag_co = DataSet(disag_filename)
disag_co_elec = disag_co.buildings[building].elec

from nilmtk.metrics import f1_score
f1_co= f1_score(disag_co_elec, test_elec)
f1_co.index = disag_co_elec.get_labels(f1_co.index)

print(f1_co)


"""