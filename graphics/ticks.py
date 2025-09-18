import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import proplot as pplt
import math
import warnings

import list.list as lis

'''
generate the ticks for a plot on an axis between a minimum and a maximum value
Input values: 
- 'min', 'max': the minimal and maximal values on the axis
Return values:
- a list of  ticks values
'''

tick_threshold = 2e-1


def generate_ticks(min, max):

    if min <= max:
        sorted_min = min
        sorted_max = max
    else:
        sorted_min = max
        sorted_max = min



    if ((sorted_min >= 0) and (sorted_max >= 0)):

        n_max = math.floor(np.log10(sorted_max))
        X_max = 10 ** (n_max - 1) * math.ceil(sorted_max / 10 ** (n_max - 1))

        if sorted_min > 1:
            n_min = math.floor(np.log10(sorted_min))
            X_min = 10 ** n_min

            ticks = [np.max([1, X_min]), X_max / 2, X_max]

        else:
            ticks = [0, X_max / 2, X_max]


    elif ((sorted_min < 0) and (sorted_max >= 0)):
        n_min = math.floor(np.log10(abs(sorted_min)))

        X_min = -10 ** (n_min - 1) * math.floor(abs(sorted_min) / 10 ** (n_min - 1))

        if sorted_max > 0:
            n_max = math.floor(np.log10(sorted_max))
            X_max = 10 ** (n_max - 1) * math.floor(sorted_max / 10 ** (n_max - 1))

            if (sorted_max > abs(sorted_min)):
                ticks = [X_min, 0, X_max / 2, X_max]
            else:
                ticks = [X_max, 0, X_min / 2, X_min]

        else:
            ticks = [0, X_min / 2, X_min]


    elif ((sorted_min < 0) and (sorted_max < 0)):

        n_min = math.floor(np.log10(abs(sorted_min)))
        X_min = -10 ** (n_min - 1) * math.ceil(abs(sorted_min) / 10 ** (n_min - 1))

        if sorted_max < -1:
            n_max = math.floor(np.log10(abs(sorted_max)))
            X_max = -(10 ** n_max)

            ticks = [np.min([-1, X_max]), X_min / 2, X_min]

        else:
            ticks = [0, X_min / 2, X_min]



    ticks = np.sort(ticks)

    return np.sort(lis.remove_close_elements(ticks, tick_threshold * (sorted_max - sorted_min)))
