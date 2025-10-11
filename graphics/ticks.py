import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import proplot as pplt

import calculus.utils as cal
import list.utils as lis


'''
generate the ticks for a plot on an axis between a minimum and a maximum value
Input values: 
- 'min', 'max': the minimal and maximal values on the axis
- 'custom_ticks' [optional]: a set of custom ticks to add to the list of generated ticks
Return values:
- a list of  ticks values
'''
def generate_ticks(min, max, custom_ticks=None):
    
    # compute the rounded-off values of min and max with respect to powers of 10
    rounded_min, rounded_max = cal.floor_base_10(min), cal.ceil_base_10(max) 
    

    # rounded_max and min are both positive
    
    ticks = []
    
    # set the maximal value of the ticks list
    if (max > rounded_max/2.0):
        
        # 'max' lies in the upper half of its 'decade' -> add to ticks the upper value of the decade (because this is closer to 'max') and its mid value
        ticks.extend([rounded_max, rounded_max/2])
    else:
        
        # 'max' lies in the lower half of its 'decade -> add to ticks the lower value of the decade (because this is clorser to 'max')
        ticks.append(max)
        
        
    # set the maximal value of the ticks list, see the comments for the max
    if (min < rounded_min/2.0):
        ticks.extend([rounded_min, rounded_min/2])
    else:
        ticks.append(min)

    ticks.append(cal.round_base_10((min+max)/2))
    
    # if max and min have different signs, add 0 to the ticks
    if max * min < 0:
        ticks.append(0)
        
    # if the user specified custom ticks, add them 
    if custom_ticks is not None:
        ticks.extend(custom_ticks)
    
    
    # remove duplicates from ticks, if any, and sort ticks
    lis.remove_duplicates(ticks)
    ticks = np.sort(ticks)
    
    return ticks

