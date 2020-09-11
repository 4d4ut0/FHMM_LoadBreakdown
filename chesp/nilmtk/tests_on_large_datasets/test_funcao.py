import numpy as np
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

array = np.random.random(10)
print(array)
# [ 0.21069679  0.61290182  0.63425412  0.84635244  0.91599191  0.00213826
#   0.17104965  0.56874386  0.57319379  0.28719469]

value = 0.5

find_nearest(array, value)



print(find_nearest(array, value))
# 0.568743859261
