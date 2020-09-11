
from __future__ import print_function
from __future__ import division
from nilmtk import DataSet, HDFDataStore
from nilmtk.disaggregate import fhmm_exact
from nilmtk.metrics import f1_score
from os.path import join
import matplotlib.pyplot as plt

### f1score fhmm
disag = DataSet('C:\\Users\\Engenharia\\nilmtk\\nilmtk\\dataset_converters\\ukdale\\ukdalekE31.h5')
disag_elec = disag.buildings.elec

