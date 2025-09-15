import os
import fnmatch


'''
count the number of files of type string_* in folder 'folder' and returns it 
'''
def count_v_files(string, folder: str) -> int:
    return len(fnmatch.filter(os.listdir(folder), string + '*'))

