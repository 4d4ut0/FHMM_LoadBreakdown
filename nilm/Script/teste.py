from __future__ import print_function, division
import  imp, sys
from os.path import join
from nilmtk import DataSet, HDFDataStore, RNNDisaggregator


# Load the dataset
dataset = DataSet('redd.h5')
# Load first house
building = dataset.buildings[1]
print("building", describe)
# Remove records where voltage<160
'''
building = filter_out_implausible_values(building, Measurement('voltage', ''), 160)
# Downsample to 1 minute
building = downsample(building, rule='1T')
# Choosing feature for disaggregation
DISAGG_FEATURE = Measurement('power', 'active')
# Dividing the data into train and test
train, test = train_test_split(building)
# Train on DISAGG_FEATURES using FHMM
disaggregator = FHMM()
disaggregator.train(train, disagg_features=[DISAGG_FEATURE])
# Disaggregate
disaggregator.disaggregate(test)
# F1 score metric
f1_score = f1(disaggregator.predictions,test)
'''