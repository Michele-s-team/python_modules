import colorama as col
import fnmatch
import os
from pathlib import Path
import re
import sys

'''
count the number of files of type string_* in folder 'folder' and returns it 
'''
def count_v_files(string, folder: str) -> int:
    return len(fnmatch.filter(os.listdir(folder), string + '*'))

'''
given a list of files ending with an integer in a path, returns the minimal and maximal integer in the file list
Input values:
- 'pattern': the pattern of the files, e.g. 'X_n_12_' for files X_n_12_1.csv, X_n_12_2.csv, ...
- 'path': the path where to look for the files
Return values:
- 'n_min', 'n_max': the minimal and maximal integers 
'''
def n_min_max(pattern, path):

    # Pattern to match pattern}n.csv files where n is a number
    pattern_new = re.compile(fr'^{pattern}(\d+)\.csv$')
        
    n_min = None
    n_max = None
        
    # Iterate through all files in the directory
    for file_path in Path(path).iterdir():
        if file_path.is_file():
            match = pattern_new.match(file_path.name)
            if match:
                n = int(match.group(1))
                if n_min is None or n < n_min:
                       n_min = n
                if n_max is None or n > n_max:
                       n_max = n
    
    if (n_min == None) or (n_max == None):
         
        print(f"{col.Fore.RED}{f'Error: n_min_max could not find the files!'}{col.Style.RESET_ALL}")
        print(f'File pattern = {pattern}\nFile path = {path}')
        # sys.exit()

    return n_min, n_max

        
'''
check if two strides are multiple of each other. This method can be used when producing the animation from data from a solution, where the solution prints out snapshots with a solution stride and the animation is saved with an animation stride. 

Input values: 
    * Mandatory: 
        - `stride_a`: first stride
        - `stride_b`: second stride
    * Optional: 
        - `name_stide_a` (`animation stride`): name to be printed out for `stride_a`
        - `name_stide_b` (`solution stride`): name to be printed out for `stride_b`

Return values: 
    An error is raised if `stride_a` is not a multiple of `stride_b`

'''
def check_strides(stride_a, stride_b,
                  name_stride_a='animation stride',
                  name_stride_b='solution stride'):

    if stride_a % stride_b != 0:
    
        raise RuntimeError(f'Error: {name_stride_a} is not a multiple of {name_stride_b} ! \n {name_stride_a} = {stride_a} \n {name_stride_b} = {stride_b} \nAborting...')