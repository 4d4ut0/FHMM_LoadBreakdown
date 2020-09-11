#!/usr/bin/env python3
import pandas as pd
import sys
import matplotlib.pyplot as plt
import csv
import h5py

name = 'redd'
csvName = name + '.csv'
bdName = name + '.h5'


meterList = []

dictMeter = {'main': 1,
	'geladeira': 2,
	'microondas': 3,
	'ar-condicionado':4,
	'cafeteira':5,
	'torradeira':6,
	'máquina de lavar roupas':7,
	'outro':8,
	'air conditioner':9,
	'air handling unit':10,
	'CE appliance':11,
	'dish washer':12,
	'electric furnace':13,
	'electric oven':14,
	'electric space heater':15,
	'electric stove':16,
	'fridge':17,
	'light':18,
	'microwave':19,
	'smoke alarm':20,
	'sockets':21,
	'subpanel':22,
	'unknown':23,
	'washer dryer':24,
	'waste disposal unit':25}

store = pd.HDFStore(bdName)
buildings = list(store.root._v_children.keys())
buildings.sort()


#identificar os elemtnso ddo banco
for b_key in buildings:
	for meter in store.get_node('/'+b_key)._v_attrs.metadata['elec_meters']:
		meterList.append({'house': b_key, 'name':meter, 'path': store.get_node('/'+b_key)._v_attrs.metadata['elec_meters'][meter]['data_location'], 'type' : ''})

	for appliance in store.get_node('/'+b_key)._v_attrs.metadata['appliances']:
		#print(appliance['type'])
		for meter in appliance['meters']:
			for meterAdd in meterList:
				if meterAdd['name'] == meter:
					meterAdd['type'] = dictMeter[appliance['type']]

store.close()
				
#retirar os pontos do banco
for meter in meterList:
	print(meter['house'])
	if meter['house'] == 'building5':
		df = pd.read_hdf(bdName, key=meter['path'])
		if meter['type'] == '':
			meter['type'] = 1
			print('\n\nMeter atual:---->', meter)

			#grando dados em arquivo csv
			with open('no05-5-main'+csvName, mode='a+', encoding='utf-8', newline='') as csv_file:
			    fieldnames = ['Potencia', 'DataRegistro', 'building' ,'Id', 'type']
			    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
			    writer.writeheader()

			    for j in range(int(df.shape[0]/6)):
			    	i = j*6
			    	if(df.values[i][0] != 0.0):
				    	writer.writerow({'Potencia':df.values[i][0],'DataRegistro':df.index[i],
				    		'building' : meter['house'], 'Id': meter['name'],
				    		'type' : meter['type']})



	


'''
	print(store.get_node('/'+b_key)._v_attrs.metadata)
	typeBuilding = store.get_node('/'+b_key)._v_attrs.metadata['appliances'][0]['type']
	nameBuilding =	store.get_node('/'+b_key)._v_attrs.metadata['appliances'][0]['original_name']
	print(typeBuilding, nameBuilding, b_key)
	'''

    #building.import_metadata(store, '/'+b_key, self.metadata.get('name'))
    
#print(store.get_node('/building1/elec/meter8')._v_attrs)
#for att in store.root._v_attrs.metadata:
#	print(att)