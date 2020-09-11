from __future__ import division, print_function
from fractions import Fraction
import numpy as np
import scipy.integrate as integrate
from scipy.integrate import quad
import sympy as sp


def interpolate_fi(inp, fi):
    i, f = int(fi // 1), fi % 1
    j = i+1 if f > 0 else i
    return (1-f) * inp[i] + f * inp[j]


def interpolate(inp, new_len):
    delta = (len(inp) - 1) / (new_len - 1)
    return [interpolate_fi(inp, i * delta) for i in range(new_len)]


def discrete_integrate(y, x=True):
    if x:
        return integrate.simps(np.array(y))
    else:
        return integrate.simps(np.array(y), np.array(x))


def function_discrete_integrate(f, yi, yf):
    res, err = quad(f, yi, yf)
    return res


def line_eq(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - (m*x1)

    return lambda x: ((m*x) + b)


def set_period(array):
    del_list = []
    '''
    for i, pp in enumerate(array):
        if pp.date_is_not_zero_minute():
            del_list.append(i)

    for i in del_list:
        del array[i]
    '''
    for pp in array:
        if pp.date_is_not_zero_minute():
            array.remove(pp)
    for i in array:
        i.print()
    input()
    return array

