import fnmatch
import os
from pathlib import Path
import re

'''
count the number of files of type string_* in folder 'folder' and returns it 
'''
def count_v_files(string, folder: str) -> int:
    return len(fnmatch.filter(os.listdir(folder), string + '*'))


def n_min_max(pattern, path):

    # Pattern to match pattern}n.csv files where n is a number
    pattern = re.compile(fr'^{pattern}(\d+)\.csv$')
        
    n_min = None
    n_max = None
        
    # Iterate through all files in the directory
    for file_path in Path(path).iterdir():
        if file_path.is_file():
            match = pattern.match(file_path.name)
            if match:
                n = int(match.group(1))
                if n_min is None or n < n_min:
                       n_min = n
                if n_max is None or n > n_max:
                       n_max = n
        
    return n_min, n_max
        
