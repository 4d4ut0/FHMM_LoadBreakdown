import numpy as np
import h5py
import pandas as pd



f = h5py.File('redd.h5', 'r')
'''
#Get the HDF5 group
group1 = f['building3']

#Checkout what keys are inside that group.
for key in group1.keys():
    print(key)

group2 = group1['elec']

for key in group2.keys():
    print(key)

group3 = group2['meter22']

for key in group3.keys():
    print(key)

table = group3['table']
_i_table = group3['_i_table']


for key in _i_table.keys():
	print(key)

index = _i_table['index']

print("\n\n\nindices da tabela--->",index.keys())
print("\n\n\n")

print (table.shape[0])

#print(np.array().shape)

#data = group['elec'].value
'''
building = f['building2']
elec = building['elec']

for key in elec.keys():
    print(key)

print(elec.keys())
meter = elec['meter1']

for key in meter.keys():
    print(key)


table = meter['table']
_i_table = meter['_i_table']

index = _i_table['index']
print("\n\n\nindices da tabela--->",index.keys())
print("\n\n\n")


print(type(table))