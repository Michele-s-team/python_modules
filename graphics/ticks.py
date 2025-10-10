import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import proplot as pplt
import math

import calculus.utils as cal
import list.utils as lis
import text.utils as text

tick_threshold = 1.0


'''
generate the ticks for a plot on an axis between a minimum and a maximum value
Input values: 
- 'min', 'max': the minimal and maximal values on the axis
Return values:
- a list of  ticks values
'''
def generate_ticks(min, max):
    
    rounded_min, rounded_max = cal.floor_base_10(min), cal.ceil_base_10(max) 

    if (max > rounded_max/2.0):
        ticks = [rounded_min, rounded_max, rounded_max/2]
    else:
        ticks = [min, max, cal.round_base_10((min+max)/2.0)]
        

    '''
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


    '''
    
    ticks = np.sort(ticks)
    
    return ticks

    # return np.sort(lis.remove_close_elements(ticks, tick_threshold * (sorted_max - sorted_min)))
