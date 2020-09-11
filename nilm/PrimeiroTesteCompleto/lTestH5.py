from pandas import DataFrame, HDFStore
import pandas as pd
import sys
import matplotlib.pyplot as plt
import csv
import h5py

data = {
	'instance': 5,
	'original_name': 'house_5',
	'elec_meters':
	{
		1:
		{
			'site_meter': True,
			'device_model': 'REDD_whole_house',
			'data_location': '/building5/elec/meter1'
		},
		2:
		{
			'site_meter': True,
			'device_model': 'REDD_whole_house',
			'data_location': '/building5/elec/meter2'
		},
		3:
		{
			'submeter_of': 0,
			'device_model': 'eMonitor',
			'data_location': '/building5/elec/meter3'
		}
	},
	'appliances':
	[	
		{
			'original_name': 'microwave',
			'room': 'banheiro',
			'type': 'microwave',
			'instance': 1,
			'multiple': True,
			'meters': [3]
		},
		{
			'original_name': 'microwave',
			'type': 'microwave',
			'instance': 1,
			'multiple': True,
			'meters': [3,4]
		},
		{
			'original_name': 'microwave',
			'room': 'sala',
			'type': 'microwave',
			'instance': 1,
			'meters': [3]
		},
		{
			'original_name': 'microwave',
			'room': 'sala',
			'type': 'microwave',
			'instance': 1,
			'multiple': True,
			'meters': [3,2,4]
		}
	]	
}

bar = DataFrame.from_dict(data,orient='index')
store = HDFStore('a512.h5')
store['building5'] = bar   # write to HDF5
bar = store['building5']   # retrieve
store.close()