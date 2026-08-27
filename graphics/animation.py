import more_itertools 
import numpy as np
import pandas as pd

'''
add a triangle to an existing list of triangles by looking for triangles that share a vertex with the last triangle in the list
Input values: 
    - `elements_to_plot`: the list of triangle IDs of triangles that are already plotted
    - `data_elements`: a dataframe containing all triangles

Return values: 
    the list `triangles_to_plot` is modified, additional triangles to plot are added
'''
def add_triangle(triangles_to_plot, data_triangles):

      # 
    # update `elements_to_plot`
    if len(triangles_to_plot) > 1:

        match = pd.Series(False, index=data_triangles.index)

        for i in range(len(triangles_to_plot)):

            plotted_triangle = data_triangles.iloc[triangles_to_plot[i]]

            p_1_vertex = plotted_triangle[['p_1']].values[0]
            p_2_vertex = plotted_triangle[['p_2']].values[0]
            p_3_vertex = plotted_triangle[['p_3']].values[0]

            match = match | ( 

                data_triangles['p_1'].eq(p_1_vertex) 
                | data_triangles['p_1'].eq(p_2_vertex)
                | data_triangles['p_1'].eq(p_3_vertex)

                | data_triangles['p_2'].eq(p_1_vertex)
                | data_triangles['p_2'].eq(p_2_vertex)
                | data_triangles['p_2'].eq(p_3_vertex)

                | data_triangles['p_3'].eq(p_1_vertex)
                | data_triangles['p_3'].eq(p_2_vertex)
                | data_triangles['p_3'].eq(p_3_vertex)

                )

        # don't reuse rows already in the path
        match.iloc[triangles_to_plot] = False

    else: 

        match = np.bool_(False)


    if match.any():

        next_mesh_triangle = []
        for i in range(len(match)):

            if match[i]:

                next_mesh_triangle.append(i)

    else:
        # match contains no Trues -> the search algorithm is stuch -> look for a new "connected component" by picking a new tetrahedron not in `tetrahedra_to_plot`

        remaining_colored_triangles = [i for i in range(len(data_triangles)) if i not in triangles_to_plot]
        next_mesh_triangle = remaining_colored_triangles[-1] if remaining_colored_triangles else None

    if next_mesh_triangle != None:

        triangles_to_plot.append(next_mesh_triangle)
        # flatten `triangles_to_plot`
        triangles_to_plot[:] = list(more_itertools.collapse(triangles_to_plot))


