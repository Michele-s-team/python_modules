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