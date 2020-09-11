import matplotlib.pyplot as plt
import metrics
from nilmtk import DataSet

result = DataSet(disag_filename)
res_elec = result.buildings[1].elec
predito = res_elec['microwave']
entrada = test_elec['microwave']

predito.plot()
entrada.plot()
plt.show()

rpaf = metrics.recall_precision_accuracy_f1(predito, entrada)
print("============ Recall: {}".format(rpaf[0]))
print("============ Precision: {}".format(rpaf[1]))
print("============ Accuracy: {}".format(rpaf[2]))
print("============ F1 Score: {}".format(rpaf[3]))

print("============ Relative error in total energy: {}".format(metrics.relative_error_total_energy(predito, entrada)))
print("============ Mean absolute error(in Watts): {}".format(metrics.mean_absolute_error(predito, entrada)))
