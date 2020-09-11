#!/usr/bin/env python3
import pandas as pd
import sys
import matplotlib.pyplot as plt
import csv
import h5py
import json
import requests
from threading import Thread	

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
urlRequest = ip +'api/Consumo'


def enviar(name, house, value, data):
	if(value != 0.0):
		obJson = {
			'potencia': str(value),
			'id': str((1000*name) + int(house)),	
			'temperatura':1,
			'umidade':1,
			'dataregistro':str(data),
			'potencias': []
		}

		serialized = json.dumps(obJson, sort_keys=False, indent=3)
		#print(serialized)
		try:
			r = requests.post(urlRequest, data=serialized, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
			print(r, obJson['id'])
		except:
			print("esse cara deu erro:", obJson)

meterList = []

store = pd.HDFStore(bdName)
buildings = list(store.root._v_children.keys())
buildings.sort()

#identificar os elemtnso ddo banco
for b_key in buildings:
	for meter in store.get_node('/'+b_key)._v_attrs.metadata['elec_meters']:
		meterList.append({'house': b_key[-1::], 'name':meter, 'path': store.get_node('/'+b_key)._v_attrs.metadata['elec_meters'][meter]['data_location'], 'type' : ''})

store.close()

workers = []				
#retirar os pontos do banco
for meter in meterList:
	if((meter['house'] == '5') and (int(meter['name'])>14) ):
		df = pd.read_hdf(bdName, key=meter['path'])
		print('\n\nMeter atual:---->', meter)

		#gerando e enviando json

		for j in range(1,int(df.shape[0]/6000)):
			for k in range(1,1000):
				i = j * 6 * k
				t = Thread(target=enviar,args=[meter['name'], meter['house'], df.values[i][0], df.index[i]])
				t.start()
				workers.append(t)

			for t in workers:
				t.join()

		
		print('Medidor', meter['name'],' da casa ', meter['house'], ' enviado\n')
	

