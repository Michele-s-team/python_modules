import numpy as np
import pandas as pd

'''
return a list which has the same structure as a given list, but with all entries filled with the same value
- 'refrence_list': the given list
- 'value' : the value

return values:
- the list with the same structure as 'reference_list' and filled with 'value' everywhere
'''


def uniform_nested_list(reference_list, value):
    reference_list_flat = []
    for i in range(len(reference_list)):
        reference_list_flat.append([])
        for j in range(len(reference_list[i])):
            reference_list_flat[i].append(value)

    return reference_list_flat


'''
return the min and max values in a nested list
- 'list': the list
return values
- 'min', 'max': the min and max values

'''


def min_max(list):
    min = list[0, 0]
    max = min

    for row in list:
        for column in row:
            if column < min:
                min = column
            if column > max:
                max = column

    return min, max


'''
remove from a list all the double elements which are close to an element in the list by epsilon
Input values: 
- 'list': the list
- 'epsilon': the threshold
Return values: 
- the purges list

Example of usage: 
    data = [1.0, 1.01, 2.0, 2.001, 3.0, 3.1]
    filtered = lis.remove_close_elements(data, epsilon=0.2)
    print(filtered)
'''
def remove_close_elements(input_list, epsilon):
    result = []
    for x in input_list:
        if all(abs(x - y) >= epsilon for y in result):
            result.append(x)
    return result

'''
add element by element two lists of lists
Input values: 
- 'list_a', 'list_b': the two lists of lists
Return values: 
- the sum, element by element, of 'list_a' and 'list_b'

Example of usage: 
    add_lists_of_lists([[1,2],[2,4]], [[3,2],[2,3]])
'''

def add_lists_of_lists(list_a, list_b):
    return [[A - B for A, B in zip(row_A, row_B)] for row_A, row_B in zip(list_a, list_b)]


'''
combine the data for nu and psi for a 1d manifold in the arc-length gauge to obtain the data for omega = \partial_1 X^alpha
Input values:
- 'data_nu': the data for nu, the stetch factor
- 'data_psi': the data for psi, the angle of the tangent vector
Return values:
- the data for omega, a data frame with columns 'f:0', 'f:1', 'f:2', ':0', ':1', ':2'
'''
def data_omega(data_nu, data_psi):
    
    return pd.DataFrame({
        'f:0': data_nu['f'] * np.cos(data_psi['f']),
        'f:1': -data_nu['f'] * np.sin(data_psi['f']),
        'f:2': 0,
        ':0': data_nu[':0'],
        ':1': data_nu[':1'],
        ':2': data_nu[':2']
    })
   
    
'''
Compute the min and max of the coordinates in a data set
Input values: 
- 'data': an array of the for [[x_{11}, x_{12}, ...], [x_{21}, x_{22}, ...], ...] where each entry has the same length

Return values: 
- [[min_i x_{i1}, max_i x_{i1}], [min_i x_{i2}, max_i x_{i2}, ...]]
'''
def min_max_coordinates(data):
    
    result = []
    for i in range(len(data[0])):    
        result.append([min(data[:,i]), max(data[:,i])])
        
    return np.array(result)



'''
remove some elements in 'list' in such a way that 'list' has no more than 'n' elements and return the result
Input values: 
- 'list': the list to purce
- 'n': the number of elements

Return values: 
- the purged list
'''
def purge_list(list, n):
    i = 0
    result = []
    for element in list:
        if ((i % np.rint(len(list) / n)) == 0):
            result.append(element)
        i += 1

    return result


'''
remove duplicates from a list and write the result in the input variable
Input values: 
    - 'list', the list
'''

def remove_duplicates(a):
    a[:] = list(set(a))
    
'''
Find the  element in a list which is closest to a value
Input values: 
    - 'list': the list
    - 'value': the value
    
Return values: 
    - the closest element 
'''
def closest_element(list, value):
    
    diff = abs(list[0]-value)
    result = list[0]
    
    for i in range(1, len(list)): 
        if abs(list[i]-value) < diff: 
            result = list[i]            

    return result

'''
multiply each element of a list by a value, and return the resulting list
Input values: 
    - 'list': the list
    - 'value': the value
Return values:
    - the resulting list, whose ith element is list[i] * value
'''
def multiply(value, list):
    return np.multiply(value, list).tolist()
    