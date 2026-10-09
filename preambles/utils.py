'''
this module contains preambles used to produce figures  and other objects
'''

import os 


'''
return a figure preamble 
Input values; 
    - 'definition_paths': [definition_path_1, definition_path_2, ... ], a list of paths which contian the .tex definition paths to be included in the preabmle

Return values: 
    - 'figure_preamble': a string containing the preamble 

'''
def figure_preamble(definitions_paths): 

    figure_preamble = (
        r"\usepackage{bm} "
        r"\usepackage{newpxtext,newpxmath} "
        r"\usepackage{xcolor} "
        r"\usepackage{glossaries} "
        r"\usepackage{graphicx} "
        r"\usepackage{tikz} "
        r"\usetikzlibrary{math} "
        r"\usepackage{relsize} "
        r"\renewcommand{\scalebox}[2]{\mbox{\textscale{#1}{#2}}} "
    )

    for defiition_path in definitions_paths:

        figure_preamble += rf"\input{{{defiition_path}}}" 

    return figure_preamble


