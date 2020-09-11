#!/usr/bin/env python3
import pandas as pd
import sys
import matplotlib.pyplot as plt
import csv
import h5py
import json
import requests	

#defaut
name = 'redd'
csvName = name + '.csv'
bdName = name + '.h5'
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
ip = 'http://192.168.0.30/'
urlRequest = ip +'api/estacao'

meterList = []

store = pd.HDFStore(bdName)
buildings = list(store.root._v_children.keys())
buildings.sort()

#identificar os elemtnso ddo banco
for b_key in buildings:
	for meter in store.get_node('/'+b_key)._v_attrs.metadata['elec_meters']:
		meterList.append({'house': b_key[-1::], 'name':meter, 'path': store.get_node('/'+b_key)._v_attrs.metadata['elec_meters'][meter]['data_location'], 'type' : ''})

	for appliance in store.get_node('/'+b_key)._v_attrs.metadata['appliances']:
		#print(appliance['type'])
		for meter in appliance['meters']:
			for meterAdd in meterList:
				if meterAdd['name'] == meter:
					meterAdd['type'] = dictMeter[appliance['type']]
store.close()
				
#retirar os pontos do banco
for meter in meterList:
	df = pd.read_hdf(bdName, key=meter['path'])
	if meter['type'] == '':
		meter['type'] = 1
	print('\n\nMeter atual:---->', meter)

	#gerando e enviando json

	obJson = {
		'idenderecamento':10,
		'iddispositivo': str(meter['type']),
		'idGrid': 3,
		'idInstalador': 2,
		'idUsuario': 7,
		'idHardware': str((1000*meter['name']) + int(meter['house'])),
		'invasiva': False,
		'agregada': True if meter['type'] == 1 else False,
		'ativa': True
	}

	
	serialized = json.dumps(obJson, sort_keys=False, indent=3)
	print('obj_string---->',serialized)
	r = requests.post(urlRequest, data=serialized, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
	print(r.status_code)
	

