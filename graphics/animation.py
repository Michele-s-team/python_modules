import numpy as np
import pandas as pd

'''
add an element (edge, triangle, tetrahedron, ....) to an existing list of elements by looking for elements that share a vertex with the last element in the list
Input values: 
    - `elements_to_plot`: the list of  IDs of elements that are already plotted
    - `data_elements`: a dataframe containing all elements

Return values: 
    the list `elements_to_plot` is modified, additional elements to plot are added
'''
def add_element(elements_to_plot, data_elements):

    '''
    n is the number of vertices contained in an element. 
    n = 
     - 2 if element is an edge
     - 3 if element is a triangle
     - ....
    '''
    n = data_elements.columns.str.match(r"^p_\d+$").sum()


    p_vertex = n * [None]

      # 
    # update `elements_to_plot`
    if len(elements_to_plot) > 1:

        match = pd.Series(False, index=data_elements.index)

        for i in range(len(elements_to_plot)):

            plotted_element = data_elements.iloc[elements_to_plot[i]]

            for i in range(n):
                p_vertex[i] = plotted_element[[f'p_{i+1}']].values[0]

            for i in range(n):
                for j in range(n):
                    match = match | data_elements[f'p_{i+1}'].eq(p_vertex[j]) 

            # match = match | ( 

            #     data_elements[f'p_{i+1}'].eq(p_vertex[0]) 
            #     | data_elements[f'p_{i+1}'].eq(p_vertex[1])
            #     | data_elements[f'p_{i+1}'].eq(p_vertex[2])

            #     | data_elements[f'p_{i+1}'].eq(p_vertex[0])
            #     | data_elements[f'p_{i+1}'].eq(p_vertex[1])
            #     | data_elements[f'p_{i+1}'].eq(p_vertex[2])

            #     | data_elements[f'p_{i+1}'].eq(p_vertex[0])
            #     | data_elements[f'p_{i+1}'].eq(p_vertex[1])
            #     | data_elements[f'p_{i+1}'].eq(p_vertex[2])

            #     )

        # don't reuse rows already in the path
        match.iloc[elements_to_plot] = False

    else: 

        match = np.bool_(False)


    if match.any():

        next_triangle = []
        for i in range(len(match)):

            if match[i]:

                next_triangle.append(i)

    else:
        # match contains no Trues -> the search algorithm is stuch -> look for a new "connected component" by picking a new tetrahedron not in `tetrahedra_to_plot`

        remaining_colored_triangles = [i for i in range(len(data_elements)) if i not in elements_to_plot]
        next_triangle = [remaining_colored_triangles[-1]] if remaining_colored_triangles else None

    if next_triangle != None:

        elements_to_plot.extend(next_triangle)


