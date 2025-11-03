import matplotlib.colors as mcolors

import constants.utils as const
import numpy as np
import os
import pandas as pd

import graphics.utils as gr
import graphics.vector_plot as vp

# convert a floating-point number 'x' in scientific format and return the related string in latex format
def to_latex_scientific(x):
    formatted = "{:.1e}".format(x)  # Convert to scientific notation with 3 significant figures
    base, exponent = formatted.split("e")  # Split into base and exponent

    base = float(base)  # Convert base to float to check if it's an integer
    exponent = int(exponent)  # Convert exponent to integer to remove leading zeros

    # Convert base to int if it is a whole number
    base_is_integer = base.is_integer()
    if base_is_integer:
        base = int(base)

    if x != 0:
        if exponent == 0:
            result = r"${}$".format(base)
        else:
            if base_is_integer and (np.abs(base) == 1):
                if base == 1:
                    result = r"$10^{{{}}}$".format(exponent)
                elif base == -1:
                    result = r"$-10^{{{}}}$".format(exponent)
            else:
                result = r"${} \times 10^{{{}}}$".format(base, exponent)

    else:
        result = r"$0$"
    return result

'''
compute the floor of a number with respect to multiples of 10
Input values: 
- 'x': the number

Output values: 
- the floor
'''
def floor_base_10(x):
    if x > 0:
        return (10.0 ** (np.floor(np.log10(x))))
    elif x < 0:
        return (- 10.0 ** (np.ceil(np.log10(-x))))
    elif x == 0:
        return 0

'''
compute the ceil of a number with respect to multiples of 10
Input values: 
- 'x': the number

Output values: 
- the ceil
'''
def ceil_base_10(x):
    if x > 0:
        return (10.0 ** (np.ceil(np.log10(x))))
    elif x < 0:
        return (- 10.0 ** (np.floor(np.log10(-x))))
    elif x == 0:
        return 0

'''
compute the round off of a number with respect to multiples of 10
Input values: 
- 'x': the number

Output values: 
- the rounded-off value
'''
def round_base_10(x):
    if x > 0:
        return (10.0 ** (np.round(np.log10(x))))
    elif x < 0:
        return (- 10.0 ** (np.round(np.log10(-x))))
    elif x == 0:
        return 0
    
'''
compute min and max of the norm of an interpolated vector field across multiple snapshots of the vector field
Input values: 
    -  'n_min', 'n_max', 'stride': ids of the first and last snapshot, and snapshot stride to consider while running through the snapshots
    - 'file_path': the path of the file, e.g. '/solution/'
    - 'file_name': the pattern of the file name, e.g. 'v_n_' to look through all filed v_n_*
    - 'n_bins' : [n_x, n_y] the bins used to make the interpolation 
    - 'min_max': [[min_x, min_y], [max_x, max_y]] the boundaries of the rectangular region where the interpolation will be made

Return values:
    - 'norm_v_min_max': [norm_v_min, norm_v_max] the minimal and maximal value of the norm found 
'''
def min_max_vector_field(n_min, n_max, stride, file_path, file_name, n_bins, min_max):
    
    # initialize norm_v_min_max
    norm_v_min_max = [np.inf,-np.inf]
    
    for n_snapshot in range(n_min, n_max+1, stride):
    
        data_v = pd.read_csv(os.path.join(file_path, file_name) + str(n_snapshot) + '.csv')

        _, _, _, _, _, norm_v_min, norm_v_max, _ = vp.interpolate_2d_vector_field(
                                                                                    data_v,
                                                                                    min_max[0],
                                                                                    min_max[1],
                                                                                    n_bins
                                                                                )
        
        if norm_v_min < norm_v_min_max[0]:
            norm_v_min_max[0] = norm_v_min
            
        if norm_v_max > norm_v_min_max[1]:
            norm_v_min_max[1] = norm_v_max
    
    return norm_v_min_max


def norm_min_max_file(file_name, 
                 column_name=const.default_column_name):
    
    data = pd.read_csv(file_name)
    
    min = np.inf
    max = -np.inf
    
    for index, row in data.iterrows():
        
        norm=0.0
        
        for i in range(3): 
            norm += (row[column_name + f':{i}'])**2
            
        norm = np.sqrt(norm)
        
        
        if norm < min:
            min = norm
            
        if norm > max: 
            max = norm

    return [min, max]


def norm_min_max_files(file_name, file_path, n_file_min, n_file_max, n_file_stride,
                  field_column_name=const.default_column_name):
    
    min = np.inf
    max = -np.inf

    for i in range(n_file_min , n_file_max+1, n_file_stride):

        [min, max] = norm_min_max_file(os.path.join(file_path, file_name) + str(i) + '.csv', field_column_name)

        if min < min:
            min = min
            
        if max > max:
            max = max

    return [min, max]




'''
compute the min and max values of a field in a csv file
Input values:
    * Mandatory: 
        - 'file_name': the path + name + extension of the file
    * Optional:
        - 'column_name': the name of the column where the values of the field are stored
Return values; 
    - 'min', 'max': the minimum and maximum of the field
'''

def min_max_file(file_name, 
                 column_name=const.default_column_name):
    data = pd.read_csv(file_name, usecols=[column_name])

    min = np.min(data[column_name])
    max = np.max(data[column_name])

    return min, max




'''
compute the minimal and maximal value of a field across multiple snapshots, where each snapshot is stored in a file
Input values: 
    * Mandatory:
        - 'file_name': the pattern of the file name
        - 'file_path': the path where the snapshots are located
        - 'n_file_min', 'n_file_max': the integers of the first and last file to consider
        - 'n_file_stride': the stride with which the files will be read
    * Optional:
        - 'field_column_name': the name of the column containing the values of the field

Return values: 
- 'abs_min', 'abs_max': the minimal and maximal values of the field across the snapshots
'''

def min_max_files(file_name, file_path, n_file_min, n_file_max, n_file_stride,
                  field_column_name='f'):
    
    abs_min = None
    abs_max = None

    for i in range(n_file_min , n_file_max+1, n_file_stride):

        min, max = min_max_file(os.path.join(file_path, file_name) + str(i) + '.csv', field_column_name)

        if abs_min is None:
            abs_min = min
        elif min < abs_min:
            abs_min = min

        if abs_max is None:
            abs_max = max
        elif max > abs_max:
            abs_max = max

    return [abs_min, abs_max]


def min_max_file_list(file_name, file_path, columns_name, column_name, n_file_list):
    abs_min, abs_max = min_max_file(file_path + file_name + str(n_file_list[0]) + '.csv', column_name)

    for n_file in n_file_list:

        min, max = min_max_file(file_path + file_name + str(n_file) + '.csv', column_name)

        if min < abs_min:
            abs_min = min

        if max > abs_max:
            abs_max = max

    return abs_min, abs_max


'''
compute the norm of a scalar field

Input values:
    - 'grid': the scalar field on a grid, given as a table
Return values:
    - 'min', 'max': minimum and maximal absolut of the vector field
    - 'norm': the normalization function for color maps, with respect to the norm of the vector field
'''
def min_max_scalar_field(grid):
    
    
    min, max = np.nanmin(grid), np.nanmax(grid)
    norm = mcolors.Normalize(vmin=min, vmax=max)  # Normalize norms to [0,1]

    return min, max, norm