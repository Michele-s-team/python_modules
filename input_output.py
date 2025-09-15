import os
import matplotlib.pyplot as plt
import sys

# add the path where to find the shared modules
module_path = '/Users/michelecastellana/Documents/paper-membrane/figures/modules'
sys.path.append(module_path)
sys.path.append(module_path)

import paths as paths

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
        result = rf'${minutes} \, \minute \, {seconds:.{number_of_decimals}f}\, \second$'

    elif format == 'hr_min_s':
        hours = int(t/(60.0*60.0))
        minutes = int((t - hours*60*60)/60)
        seconds = t - hours*60*60 - minutes*60
        result = rf'${hours} \hour \, {minutes} \, \minute \, {seconds:.{number_of_decimals}f}\, \second$'


    return result
