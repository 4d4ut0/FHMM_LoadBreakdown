from __future__ import print_function, division
import time
from matplotlib import rcParams
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
from six import iteritems

warnings.filterwarnings('ignore')
#matplotlib inline

rcParams['figure.figsize'] = (13, 6)

from nilmtk import DataSet, TimeFrame, MeterGroup, HDFDataStore
from nilmtk.disaggregate import CombinatorialOptimisation, FHMM

train = DataSet('redd.h5')
test = DataSet('redd.h5')

building = 1

train.set_window(end="30-4-2011")
test.set_window(start="30-4-2011")


train_elec = train.buildings[1].elec
test_elec = test.buildings[1].elec


top_5_train_elec = train_elec.submeters().select_top_k(k=5)


def predict(clf, test_elec, sample_period, timezone):
    pred = {}
    gt = {}

    for i, chunk in enumerate(test_elec.mains().load(sample_period=sample_period)):
        chunk_drop_na = chunk.dropna()
        pred[i] = clf.disaggregate_chunk(chunk_drop_na)
        gt[i] = {}

        for meter in test_elec.submeters().meters:
            # Only use the meters that we trained on (this saves time!)
            gt[i][meter] = next(meter.load(sample_period=sample_period))
        gt[i] = pd.DataFrame({k: v.squeeze() for k, v in iteritems(gt[i])},
                             index=next(iter(gt[i].values())).index).dropna()

    # If everything can fit in memory
    gt_overall = pd.concat(gt)
    gt_overall.index = gt_overall.index.droplevel()
    pred_overall = pd.concat(pred)
    pred_overall.index = pred_overall.index.droplevel()

    # Having the same order of columns
    gt_overall = gt_overall[pred_overall.columns]

    # Intersection of index
    gt_index_utc = gt_overall.index.tz_convert("UTC")
    pred_index_utc = pred_overall.index.tz_convert("UTC")
    common_index_utc = gt_index_utc.intersection(pred_index_utc)

    common_index_local = common_index_utc.tz_convert(timezone)
    gt_overall = gt_overall.ix[common_index_local]
    pred_overall = pred_overall.ix[common_index_local]
    appliance_labels = [m.label() for m in gt_overall.columns.values]
    gt_overall.columns = appliance_labels
    pred_overall.columns = appliance_labels
    return gt_overall, pred_overall

classifiers = {'CO':CombinatorialOptimisation(), 'FHMM':FHMM()}
predictions = {}
sample_period = 120
for clf_name, clf in classifiers.items():
    print("*"*20)
    print(clf_name)
    print("*" *20)
    clf.train(top_5_train_elec, sample_period=sample_period)
    gt, predictions[clf_name] = predict(clf, test_elec, 120, train.metadata['timezone'])
    print("PREDICTIONS: ", predictions)
    print("gt: ", gt)

    def compute_rmse(gt: object, pred: object) -> object:
        from sklearn.metrics import mean_squared_error
        rms_error = {}
        for appliance in gt.columns:
            rms_error[appliance] = np.sqrt(mean_squared_error(gt[appliance], pred[appliance]))
        return pd.Series(rms_error)


    disag_fhmm = DataSet(disag_filename)
    disag_fhmm_elec = disag_fhmm.buildings[1].elec
    disag_fhmm_elec.plot()






    rmse = {}
    for clf_name in classifiers.keys():
        print("classifiers.keys()::", classifiers.keys())
        print("clf_name:", clf_name)
        rmse[clf_name] = compute_rmse(gt, predictions[clf_name])

    rmse = pd.DataFrame(rmse)

    rmse