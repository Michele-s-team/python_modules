import system.paths as paths
import ast
import csv
import os
import matplotlib.pyplot as plt
import sys

# add the path where to find the shared modules
module_path = '/Users/michelecastellana/Documents/paper-membrane/figures/modules'
sys.path.append(module_path)
sys.path.append(module_path)


number_of_decimals = 2


# clean the matplotlib cache to load the correct version of definitions.tex
os.system(" rm -rf ~/.matplotlib/tex.cache")

plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": rf"\usepackage{{xcolor}} \usepackage{{glossaries}} \input{paths.definitions_path}"
})


'''
convert time to a sting
- 't': the time, expressed in seconds
- 'format': the format of the output: 
    * 's': the output will be in seconds
    * 'ms' : the output will be  in milliseconds
    * 'min_s': the output will be min minutes + seconds
    * 'hr_min_s': the output will be min hours + minutes + seconds
'''


def time_to_string(t, format, number_of_decimals):

    if format == 's':
        result = rf'${t:.{number_of_decimals}f}\, \second$'

    elif format == 'ms':
        result = rf'${t * 1000:.{number_of_decimals}f}\, \msecond$'

    elif format == 'min_s':
        minutes = int(t/60.0)
        seconds = t - minutes*60
        if minutes != 0:
            result = rf'${minutes} \, \minute \, {seconds:.{number_of_decimals}f}\, \second$'
        else:
            result = rf'${seconds:.{number_of_decimals}f}\, \second$'

    elif format == 'hr_min_s':
        hours = int(t/(60.0*60.0))
        minutes = int((t - hours*60*60)/60)
        seconds = t - hours*60*60 - minutes*60
        result = rf'${hours} \hour \, {minutes} \, \minute \, {seconds:.{number_of_decimals}f}\, \second$'

    return result


'''
print the type of a variable
Input values: 
- x <any>: the variable
'''


def print_type(x, var_name=None):
    if var_name is None:
        print(f'type of variable is {type(x)}')
    else:
        print(f'type of {var_name} is {type(x)}')


'''
Read a set of parameters from a csv file
Input values:
- 'file_path': the path of the file, including file name and extension
Return value:
- the list of parameter names and values, e.g., [('L', 0.4334), ('x_p', 2.23), ('resolution', 0.01)]
'''


def read_parameters_from_csv_file(file_path):

    print_type(file_path, 'file_path')

    print(f'Reading parameters from {file_path}...', flush=True)

    file = open(file_path, newline='')

    reader = csv.reader(file)

    parameter_names = next(reader)
    parameter_values = next(reader)

    # print(f'parameter_names: {parameter_names}')
    # print(f'parameter_values: {[string_to_value(parameter_value) for parameter_value in parameter_values]}')

    file.close()
    print('... close.', flush=True)

    result = dict([(parameter_name, string_to_value(parameter_value))
                  for parameter_name, parameter_value in zip(parameter_names, parameter_values)])
    print(f'Read parameters : {result}.', flush=True)

    return result


'''
Convert a string containing a numerical value to a number
Input values :
- 'string': the string containing the value (it may be an int, a float or a list)

Example of usage:
    string_to_value('13')
    string_to_value('2.43')
    string_to_value('[1,2]')
'''


def string_to_value(value):
    value = value.strip()

    # check whether 'value' is a list
    if value.startswith("[") and value.endswith("]"):
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return parsed
        except (ValueError, SyntaxError):
            pass

    # Try int
    try:
        return int(value)
    except ValueError:
        pass

    # Try float
    try:
        return float(value)
    except ValueError:
        pass

    # Fallback: return as string
    return value
