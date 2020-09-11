
from __future__ import print_function
from __future__ import division
from nilmtk import DataSet, HDFDataStore
from nilmtk.disaggregate import fhmm_exact
from nilmtk.metrics import f1_score
from os.path import join
import matplotlib.pyplot as plt

### f1score fhmm
disag = DataSet('C:\\Users\\Engenharia\\nilmtk\\nilmtk\\dataset_converters\\ukdale\\ukdalekD22.h5')
disag_elec = disag.buildings[2].elec

""""
elec.mains().plot()
plt.ylabel('appliance');
plt.xlabel('valor');
plt.title("FHMM");
plt.savefig(join(data_dir, 'f1-fhmmtt7' + str(building_number) + '.png'))
disag.store.close()
"""
