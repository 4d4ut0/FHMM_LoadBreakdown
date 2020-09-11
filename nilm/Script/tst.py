#!/usr/bin/env python3
import pandas as pd
import sys
import matplotlib.pyplot as plt
import csv
import h5py

name = 'redd'
csvName = name + '.csv'
bdName = name + '.h5'
keysListMeter = []
keysListCache = []

bd = h5py.File(bdName, 'r')

for key in bd.keys():
	for kkey in bd[key].keys():
		for kkkey in bd[key][kkey].keys():
			if(kkkey != 'cache'):
				keysListMeter.append({'key' : key+ '/' + kkey + '/' + kkkey, 'building' : key, 'meter' : kkkey})
			else:
				keysListCache.append({'key' : key+ '/' + kkey + '/' + kkkey, 'building' : key, 'cache' : kkkey})

#print(keysList)
#df = pd.read_hdf(bdName, key='building1/elec/cache')

for key in keysListMeter:
	print('Key atual ------>', key, '\n')
	df = pd.read_hdf(bdName, key=key['key'])
	
	#for eita in df.items():
		#print(eita)
	#print(df.items())

	'''
	with open(csvName, mode='a+', encoding='utf-8', newline='') as csv_file:
	    fieldnames = ['power', 'timestamp', 'building' ,'meter']
	    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
	    writer.writeheader()

	    for i in range(df.shape[0]):
	    	writer.writerow({'power':df.values[i][0],'timestamp':df.index[i],
	    		'building' : key['building'], 'meter': key['meter']})

'''	
