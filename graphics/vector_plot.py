import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.colors as mcolors
from matplotlib.path import Path
import pandas as pd
from scipy.interpolate import CloughTocher2DInterpolator
from scipy.interpolate import RBFInterpolator
from scipy.interpolate import griddata
from scipy.interpolate import interp1d

import calculus.geometry as geo
import constants.utils as const
import graphics.arrow as arr
import graphics.utils as gr
import list.column_labels as clab
import text.utils as txt

'''
tabulate a vector field given by an analytical expression
- 'v': the analytical function  v(x,y) for the vector field
- 'mins', 'maxs': min and max values of x,y where to tabulate the vector field
- 'n_bins': number of bins in which x and y axes are divided
Return values:

- three tables V_x, V_y, V_z, where each table is the table of a component of the vector field  on the grid

'''


def tabulate_analytical_vector_field_on_curve(v, gamma, min, max, n_bins):
    X, Y, Z, ts = gr.tabulate_analytical_curve(gamma, min, max, n_bins)

    V = []
    for t in ts:
        V.append(v(t))

    return X, Y, Z, V, ts


def tabulate_analytical_vector_field_on_surface(v, f, mins, maxs, n_bins):
    X, Y, Z = gr.tabulate_analytical_surface(f, mins, maxs, n_bins)

    return X, Y, Z, v(X, Y)


def plot_analytical_vector_field_on_surface(ax, v, f, mins, maxs, n_bins, scale_factor_z, z_min, shaft_length,
                                            head_over_shaft_length, head_angle, line_width, color, alpha, z_order):
    X, Y, Z, V = tabulate_analytical_vector_field_on_surface(
        v, f, mins, maxs, n_bins)

    plot_vector_field(ax, [X, Y, Z], V, scale_factor_z, z_min, shaft_length, head_over_shaft_length, head_angle,
                      line_width, alpha, color, z_order)


def plot_analytical_vector_field_on_surface_outside_disk(ax, v, f, mins, maxs, r, cr, n_bins, scale_factor_z, z_min, shaft_length,
                                                         head_over_shaft_length, threshold_arrow_length, head_angle, line_width, color, alpha, z_order):
    X, Y, Z, V = tabulate_analytical_vector_field_on_surface(
        v, f, mins, maxs, n_bins)

    for i in range(len(X)):
        for j in range(len(X[i])):
            if (X[i, j] - cr[0]) ** 2 + (Y[i, j] - cr[1]) ** 2 < r ** 2:
                V[0][i, j] = np.nan
                V[1][i, j] = np.nan
                V[2][i, j] = np.nan

    plot_vector_field(ax, [X, Y, Z], V, scale_factor_z, z_min, shaft_length, head_over_shaft_length, head_angle,
                      threshold_arrow_length, line_width, alpha, color, z_order)


'''
plot a vector field
Input values:
- 'ax': the axis on which the vector field will be plotted
- 'grid_r': the grid where the vector field is defined, given as a list of three tables, one for each component of the position vector, it is of the form [X, Y, Z]
- 'grid_v': the vector field on the grid, given as a list of three tables, one for each component of the vector field, it is of the form [V_x, V_y, V_z]
- 'scale_factor_z': scale factor for the z axis of the shape contained in grid_r
- 'z_min': minimum value of the z axis of the shape contained in grid_r
- 'shaft_length': length of the shaft of the arrows
- 'head_over_shaft_length': ratio between the length of the head and the length of
- 'head_angle': angle of between the head and the shaft of the arrows
- 'threshold_arrow_length': minimum length of the arrow to be plotted: arrows with length smaller than this value are not plotted
- 'line_width': line width of the arrows
- 'alpha': transparency of the arrows, between 0 (fully transparent) and 1
- 'color': color of the arrows, or 'color_from_map' to get the color from a colormap
- 'z_order': z-order of the arrows
'''


def plot_vector_field(ax, grid_r, grid_v, scale_factor_z, z_min, shaft_length, head_over_shaft_length, head_angle, threshold_arrow_length,
                      line_width, alpha, color, z_order):

    grid_norm_v, _, _, norm_v = norm_vector_field(grid_v)

    for i in range(len(grid_r[0])):
        for j in range(len(grid_r[1][i])):
            vector_norm = grid_norm_v[i, j]

            if color == 'color_from_map':
                # Get corresponding arrow_color from colormap
                arrow_color = gr.cb.color_map_type(norm_v(vector_norm))
            else:
                arrow_color = color

            arr.plot_arrow(ax, [grid_r[0][i, j], grid_r[1][i, j], grid_r[2][i, j]],
                           np.add([grid_r[0][i, j], grid_r[1][i, j], grid_r[2][i, j]],
                                  [grid_v[0][i, j], grid_v[1][i, j], grid_v[2][i, j]]),
                           shaft_length, head_over_shaft_length, head_angle, [
                               0, 0, z_min],
                           [1, 1, scale_factor_z], threshold_arrow_length,
                           line_width, arrow_color, alpha, z_order)


'''
plot a vector field defined on a 1d manifold
Input values:
    * Mandatory:
        - 'ax': the axis where to plot
        - 'grid_r': the grid where the vector field is defined, given as a list of two tables, one for each component of the position vector
        - 'grid_v': the vector field on the grid, given as a list of two tables, one for each component of the vector field
    * Optional:
        - 'shaft_length': length of the shaft of the arrows. If 'None' the norm of the vector field will be used as shaft length
        - 'head_over_shaft_length': ratio between the length of the head and the length of the shaft of the arrows
        - 'head_length': this is provided only if 'shaft_length' = None: the absolute length of arrow heads
        - 'head_angle': angle of between the head and the shaft of the arrows
        - 'line_width': line width of the arrows
        - 'alpha': transparency of the arrows, between 0 (fully transparent) and 1 (fully opaque)
        - 'color': color of the arrows, or 'color_from_map' to get the color from a colormap
        - 'z_order': z-order of the arrows
        - 'clip_on': chose whether the vector field will be clipped if it lies outside the axis bounds
        - 'threshold_arrow_length': the threshold for the length of the arrows such that arrows with length smaller than the threshold will not be plotted
        - 'legend': text label for the legend. If None, no legend is plotted
        - 'legend_position': position of the legend as normalized coordinates [x, y] where 0 is the axis minimum and 1 is the axis maximum
        - 'legend_text_arrow_space': spacing between the legend arrow and legend text as a fraction of axis width
        - 'legend_arrow_length': length of the arrow shown in the legend as a fraction of axis width
        - 'legend_head_over_shaft_length': ratio between head length and shaft length for the legend arrow
        - 'legend_font_size': font size for the legend text
        - 'stride': the stride with which arrows will be plotted, this method will plot every 'stride' arrows

Example of usage:

    vp.plot_1d_vector_field(ax, [X_v, Y_v], [V_x, V_y],
                            shaft_length=parameters['shaft_length'],
                            head_over_shaft_length=parameters['head_over_shaft_length'],
                            head_angle=parameters['head_angle'],
                            line_width=parameters['arrow_line_width'],
                            alpha=parameters['alpha'],
                            color='color_from_map',
                            threshold_arrow_length=parameters['threshold_arrow_length'])
'''


def plot_1d_vector_field(ax, grid_r, grid_v,
                         shaft_length=const.default_shaft_length,
                         head_over_shaft_length=const.default_head_over_shaft_length,
                         head_length=const.default_head_length,
                         head_angle=const.default_head_angle,
                         line_width=const.default_line_width,
                         alpha=const.default_alpha,
                         color=const.default_color,
                         z_order=const.default_z_order,
                         clip_on=False,
                         threshold_arrow_length=const.default_threshold_arrow_length,
                         legend=None,
                         legend_position=[0]*2,
                         legend_text_arrow_space=const.default_legend_text_arrow_space,
                         legend_arrow_length=const.default_legend_arrow_length,
                         legend_head_over_shaft_length=const.default_head_over_shaft_length,
                         legend_font_size=const.default_font_size,
                         stride=1):

    grid_norm_v, _, _, norm_v = norm_vector_field(grid_v)

    for i in range(len(grid_r[0])):

        if (i % stride) == 0:

            vector_norm = grid_norm_v[i]

            if color == 'color_from_map':
                # Get corresponding arrow_color from colormap
                arrow_color = gr.cb.color_map_type(norm_v(vector_norm))
            else:
                arrow_color = color

            if shaft_length == None:
                # the method has been called with shaft_length = None: the shaft length which will be used in the plot is set to the length of the vector [grid_v[0][i], grid_v[1][i]]
                shaft_length_to_plot = np.linalg.norm(
                    [grid_v[0][i], grid_v[1][i]])
                head_over_shaft_length_to_plot = head_length/shaft_length_to_plot
            else:
                # the method has been aclled with shaft_length != None: the shaft length which will be used in the plot is set to shaft_length
                shaft_length_to_plot = shaft_length
                head_over_shaft_length_to_plot = head_over_shaft_length

            arr.plot_2d_arrow(ax, [grid_r[0][i], grid_r[1][i]],
                              np.add([grid_r[0][i], grid_r[1][i]],
                                     [grid_v[0][i], grid_v[1][i]]),
                              shaft_length_to_plot, head_over_shaft_length_to_plot, head_angle, line_width, arrow_color, alpha, z_order, threshold_arrow_length,
                              clip_on=clip_on)

    if legend != None:
        # plot the legend of the vector field

        # get axis bounds
        axis_min_max = [np.sort(ax.get_xlim()), np.sort(ax.get_ylim())]

        # plot the arrow sample of the legend, next to the legend text
        arrow_position = [
            axis_min_max[0][0] + (axis_min_max[0][1] -
                                  axis_min_max[0][0]) * legend_position[0],
            axis_min_max[1][0] + (axis_min_max[1][1] -
                                  axis_min_max[1][0]) * legend_position[1]
        ]

        arr.plot_2d_arrow(ax,
                          arrow_position,
                          np.add(arrow_position, [
                              legend_arrow_length * (axis_min_max[0][1] - axis_min_max[0][0]), 0]),
                          legend_arrow_length,
                          legend_head_over_shaft_length,
                          head_angle,
                          line_width,
                          arrow_color,
                          alpha,
                          z_order,
                          clip_on=clip_on)

        # plot the text of the legend
        ax.text(
            arrow_position[0] + legend_text_arrow_space *
            (axis_min_max[0][1] - axis_min_max[0][0]),
            arrow_position[1],
            txt.to_latex_equation(legend),
            fontsize=legend_font_size,
            ha='center',
            va='center',
            zorder=z_order
        )


'''
plot a vector field defined on a 2d manifold

Input values:
    * Mandatory:
        - 'ax': the axis where to plot
        - 'grid_r': the grid where the vector field is defined, given as a list of two tables, one for each component of the position vector, of the form [X, Y]. 
            grid_r = [
                    [
                        [x_0, x_0, ..., x_0],
                        [x_1, x_1, ..., x_1],
                        ....
                    ],
                    [
                    [y_0, y_1, ...],
                    [y_0, y_1, ...],
                    ...
                    ]
                ]
        - 'grid_v': the vector field on the grid, given as a list of two tables, one for each component of the vector field, of the form [V_x, V_y]. 
                    grid_v = [
                    [
                        [V_x_00, V_x_01, ..., ],
                        [V_x_10, V_x_11, ..., ],
                        ....
                    ],
                    [
                        [V_y_00, V_y_01, ...],
                        [V_y_10, V_y_11, ...],
                        ...
                    ]
                ]
        - 'shaft_length': length of the shaft of the arrows
        - 'head_over_shaft_length': ratio between the length of the head and the length of the shaft of the arrows
        - 'head_angle': angle of between the head and the shaft of the arrows
        -  'line_width': line width of the arrows
        - 'alpha': transparency of the arrows, between 0 (fully transparent) and 1 (fully opaque)
        - 'color': color of the arrows, or 'color_from_map' to get the color from a colormap
        -  'z_order': z-order of the arrows
    * Optional:
        - 'clip_on': if False, the arrow will be plotted even if it lies outside the axes' limits
'''


def plot_2d_vector_field(ax, grid_r, grid_v, shaft_length, head_over_shaft_length, head_angle, line_width, alpha, color, z_order,
                         clip_on=True,
                         threshold_arrow_length= const.default_threshold_arrow_length):

    grid_norm_v, _, _, norm_v = norm_vector_field(grid_v)

    
    start_end_segments = []
    norm_values = [] 

    for i in range(len(grid_r[0])):
        for j in range(len(grid_r[1][i])):

            dr_shaft = np.array([grid_v[0][i, j], grid_v[1][i, j]])
            
            if ((np.linalg.norm(dr_shaft) > threshold_arrow_length)):
                
                dr_shaft = dr_shaft * shaft_length / np.linalg.norm(dr_shaft)

                start_end_segments.append(
                    [
                        [grid_r[0][i, j], grid_r[1][i, j]],
                        np.add([grid_r[0][i, j], grid_r[1][i, j]], dr_shaft)
                    ]
                )

                norm_values.append(norm_v(grid_norm_v[i, j]))


    if color == 'color_from_map':

        lc = LineCollection(start_end_segments,
                    linewidths=line_width,
                    cmap=gr.cb.color_map_type,
                    alpha=alpha,
                    zorder=z_order,
                    clip_on=clip_on)
        
        lc.set_array(np.array(norm_values))  # values in [0, 1] drive the colormap
    
    else:

        lc = LineCollection(start_end_segments,
            linewidths=line_width,
            colors=color,
            alpha=alpha,
            zorder=z_order,
            clip_on=clip_on)

    ax.add_collection(lc)

    '''
    for i in range(len(grid_r[0])):
        for j in range(len(grid_r[1][i])):

            vector_norm = grid_norm_v[i, j]

            if color == 'color_from_map':
                # Get corresponding arrow_color from colormap
                arrow_color = gr.cb.color_map_type(norm_v(vector_norm))
            else:
                arrow_color = color

            arr.plot_2d_arrow(ax, [grid_r[0][i, j], grid_r[1][i, j]],
                              np.add([grid_r[0][i, j], grid_r[1][i, j]],
                                     [grid_v[0][i, j], grid_v[1][i, j]]),
                              shaft_length, head_over_shaft_length, head_angle, line_width, arrow_color, alpha, z_order,
                              clip_on=clip_on)
    '''


def plot_2d_vector_field_scaled_length(ax, grid_r, grid_v, shaft_length, head_over_shaft_length, head_angle, line_width, alpha, color, z_order):
    grid_norm_v, norm_v_min, norm_v_max, norm_v = norm_vector_field(grid_v)

    for i in range(len(grid_r[0])):
        for j in range(len(grid_r[1][i])):
            vector_norm = grid_norm_v[i, j]

            if color == 'color_from_map':
                # Get corresponding arrow_color from colormap
                arrow_color = gr.cb.color_map_type(norm_v(vector_norm))
            else:
                arrow_color = color

            arr.plot_2d_arrow(ax, [grid_r[0][i, j], grid_r[1][i, j]],
                              np.add([grid_r[0][i, j], grid_r[1][i, j]],
                                     [grid_v[0][i, j], grid_v[1][i, j]]),
                              0.0 + shaft_length * (vector_norm - norm_v_min)/(norm_v_max-norm_v_min), head_over_shaft_length, head_angle, line_width, arrow_color, alpha, z_order)


'''
plot a vector field by setting the shaft length of each arrow according
to the norm of the vector and to a parameter shaft_length selected by the user
'''


def plot_vector_field_alpha_map(ax, grid_r, grid_v, scale_factor_z, z_min, shaft_length, head_over_shaft_length,
                                head_angle, threshold_arrow_length, line_width, alpha_map, z_order):
    grid_norm_v, norm_v_min, norm_v_max, norm_v = norm_vector_field(grid_v)

    for i in range(len(grid_r[0])):
        for j in range(len(grid_r[1][i])):
            vector_norm = grid_norm_v[i, j]

            # Get corresponding color from colormap
            color = gr.cb.color_map_type(norm_v(vector_norm))

            arr.plot_arrow(ax, [grid_r[0][i, j], grid_r[1][i, j], grid_r[2][i, j]],
                           np.add([grid_r[0][i, j], grid_r[1][i, j], grid_r[2][i, j]],
                                  [grid_v[0][i, j], grid_v[1][i, j], grid_v[2][i, j]]),
                           shaft_length, head_over_shaft_length, head_angle, [
                               0, 0, z_min],
                           [1, 1, scale_factor_z], threshold_arrow_length,
                           line_width, color, alpha_map[i][j], z_order)


'''
compute the minimum and maximum norm of a vector field
Input values:
- 'grid_v': the vector field on a grid, given as a list of three tables, one for each component of the vector field
Return values:
- 'norm_v_min', 'norm_v_max': minimum and maximal norm of the vector field across the grid
'''


def min_max_vector_field(grid_v):
    grid_norm_v = np.sqrt(grid_v[0] ** 2 + grid_v[1] ** 2 + grid_v[2] ** 2)
    norm_v_min, norm_v_max = np.nanmin(grid_norm_v), np.nanmax(grid_norm_v)

    return norm_v_min, norm_v_max


'''
compute the norm of a vector field

Input values:
    - 'grid_v': the vector field on a grid, given as a list of three tables, of the form [V_x, V_y, V_z]

Return values:
    - 'grid_norm_v': the table of the norm of the vector field on the grid
    - 'norm_v_min', 'norm_v_max': minimum and maximal norm of the vector field
    - 'norm_v': the normalization function for color maps, with respect to the norm of the vector field
'''


def norm_vector_field(grid_v):

    grid_norm_v = 0
    for i in range(len(grid_v)):
        grid_norm_v += grid_v[i]**2

    grid_norm_v = np.sqrt(grid_norm_v)

    norm_v_min, norm_v_max = np.nanmin(grid_norm_v), np.nanmax(grid_norm_v)
    # Normalize norms to [0,1]
    norm_v = mcolors.Normalize(vmin=norm_v_min, vmax=norm_v_max)

    return grid_norm_v, norm_v_min, norm_v_max, norm_v


'''
interpolate a vector field on the tangent bundle of a 2d manifold parameterized with the arc-length gauge
Input values:
- 'data_v': table where the values of the vector field on the grid of the coordinate x^1 are stored.
- 'data_X': table where the values of the vector of the manifold (X^1, x^2) on the grid of the coordinate x^1 are stored.
- 'n_bins': number of bins of the grid where to interpolate the vector field

Return values:
- 'X' the table of the x coordinates of interpolated points of the manifold
- 'Y' the table of the y coordinates of interpolated points of the manifold
- 'V_x' the table of the x components of the interpolated vector field
- 'V_y' the table of the y components of the interpolated vector field
- 'grid_norm_v' the table of the norm of the interpolated vector field
- 'norm_v_min' the minimum of the norm of the interpolated vector field
- 'norm_v_max' the maximum of the norm of the interpolated vector field
- 'norm_v' the normalization function for color maps, with respect to the norm of the interpolated vector field
'''


def interpolate_t_vector_field_2d_arc_length_gauge(data_X,
                                                   data_omega,
                                                   data_v,
                                                   bins_v):

    # transform the value v^1 of the vector field in the tangent manifold into the value v^{2d alpha} of the vector field in the 2d euclidean space where the manifold is embedded, by using data_omega
    values_v_2d = pd.DataFrame({
        'f:0': data_v['f:0'] * data_omega['f:0'],
        'f:1': data_v['f:0'] * data_omega['f:1'],
        'f:2': 0,
        ':0': data_v[':0'],
        ':1': 0,
        ':2': 0
    })

    # compute min and max of the coordinate x^1
    x_min = np.min(data_X[':0'])
    x_max = np.max(data_X[':0'])

    # the non-interpolated  (abscissa) points of the fields to interpolate
    points = data_v[':0']
    # the interpolated points of the fields to interpolate
    points_interpolated = np.linspace(x_min, x_max, bins_v)

    idx = data_v[':0'].argsort()

    # interpolate the values of the parametric curve
    values_X_interpolated = pd.DataFrame({
        'f:0': np.interp(points_interpolated, points.iloc[idx].values, data_X['f:0'].iloc[idx].values),
        'f:1': np.interp(points_interpolated, points.iloc[idx].values, data_X['f:1'].iloc[idx].values),
        'f:2': 0,
        ':0': points_interpolated,
        ':1': 0,
        ':2': 0
    })

    # interpolate the values of the vector field in the 2d euclidean space where the manifold is embedded
    values_v_2d_interpolated = pd.DataFrame({
        'f:0': np.interp(points_interpolated, points.iloc[idx].values, values_v_2d['f:0'].iloc[idx].values),
        'f:1': np.interp(points_interpolated, points.iloc[idx].values, values_v_2d['f:1'].iloc[idx].values),
        'f:2': 0,
        ':0': points_interpolated,
        ':1': 0,
        ':2': 0
    })

    X = values_X_interpolated['f:0']
    Y = values_X_interpolated['f:1']

    V_x = values_v_2d_interpolated['f:0']
    V_y = values_v_2d_interpolated['f:1']

    grid_norm_v, norm_v_min, norm_v_max, norm_v = norm_vector_field([V_x, V_y])

    return X, Y, V_x, V_y, grid_norm_v, norm_v_min, norm_v_max, norm_v


'''
interpolate a vector field on the tangent bundle of a 3d manifold parameterized with the Monge guage
'''


def interpolate_t_vector_field_3d_monge_gauge(data_v, data_z, data_omega,
                                              mins, maxs, z_min, N_bins_v,
                                              label_x_column, label_y_column, label_z_column, label_v_column, label_omega_column):

    X_v, Y_v, Z_v, _, _, _ = gr.interpolate_surface(data_z, mins, maxs, N_bins_v,
                                                    f_min=z_min, method='griddata')

    points = []
    points.extend([list(element) for element in zip(
        data_v[label_x_column], data_v[label_y_column])])
    # 2 re-arrange the f-values into values

    # Transformation from v^i to v^{3d alpha}:
    #
    # index alpha runs over coordinates of 3d euclidean space
    # v^{3d alpha} = v^i e_i^alpha
    # v^{3d 1} = v^1
    # v^{3d 2} = v^2
    # v^{3d 3} = v^1 omega_1 + v^2 omega_2
    values_v_x = data_v[label_v_column + label_x_column]
    values_v_y = data_v[label_v_column + label_y_column]
    values_v_z = data_v[label_v_column + label_x_column] * data_omega[label_omega_column + label_x_column] + data_v[
        label_v_column + label_y_column] * data_omega[label_omega_column + label_y_column]

    # 3 interpolate values_z and points, and write the result of the interpolated function on the lattice (X, Y_quiver) into grid
    v_x = griddata(points, values_v_x, (X_v, Y_v), method='cubic')
    v_y = griddata(points, values_v_y, (X_v, Y_v), method='cubic')
    v_z = griddata(points, values_v_z, (X_v, Y_v), method='cubic')

    grid_norm_v, norm_v_min, norm_v_max, norm_v = norm_vector_field([
        v_x, v_y, v_z])

    return X_v, Y_v, Z_v, v_x, v_y, v_z, grid_norm_v, norm_v_min, norm_v_max, norm_v


def interpolating_function_2d_vector_field(data_v,
                                           label_x_column=':0',
                                           label_y_column=':1',
                                           label_v_column='f'
                                           ):

    # points are the values of the coordinates x, y stored in data_v
    points = []
    points.extend([list(element) for element in zip(
        data_v[label_x_column], data_v[label_y_column])])

    # values_v_* are the values of the vector field stored in data_v, on the points stored in points
    values_v_x = data_v[label_v_column + label_x_column]
    values_v_y = data_v[label_v_column + label_y_column]

    # Create interpolating functions
    V_x = CloughTocher2DInterpolator(points, values_v_x)
    V_y = CloughTocher2DInterpolator(points, values_v_y)

    return V_x, V_y


'''
interpolate a two-dimensional vector field living on a square region, by treating separately the interpolation on the bottom edge of the square. On this edge, the vector field is interpolated with a one-dimensional interpolation, while on the rest of the square a two-dimensional RBF interpolation is used.
Input values:
    * Mandatory: 
        - 'data_v': data where the values of the vector field, on an arbitrary set of points, xy, are stored
        - 'min', 'maxs': limits of the rectangular region where to interpolate
        - 'n_bins_v': number of bins along each axis of the rectangular region where to interpolate
    * Optional:
        - 'right_edge_x': x value around which points are considered to be on the right edge of the square
        - 'bottom_edge_epsilon': y value below which points are considered to be on the bottom edge of the square
        - 'right_edge_epsilon': y value below which points are considered to be on the right edge of the square
        - 'label_x_column': label of the x axis in data_v
        - 'label_y_column': label of the y axis in data_v
        - 'label_v_column': label of the vector field in data_v

Return values:
    - 'X' the table of the x coordinates of interpolated points
    - 'Y' the table of the y coordinates of interpolated points
    - 'v_x' the table of the x components of the interpolated vector field
    - 'v_y' the table of the y components of the interpolated vector field
    - 'grid_norm_v' the table of the norm of the interpolated vector field
    - 'norm_v_min' the minimum of the norm of the interpolated vector field
    - 'norm_v_max' the maximum of the norm of the interpolated vector field
    - 'norm_v' the normalization function for color maps, with respect to the norm of the
'''

def interpolate_2d_vector_field_layer(data_v, mins, maxs, n_bins_v,
                                      right_edge_x=None,
                                      bottom_edge_epsilon=const.default_interpolation_layer_threshold,
                                      right_edge_epsilon=const.default_interpolation_layer_threshold,
                                      label_x_column=':0',
                                      label_y_column=':1', 
                                      label_v_column='f'):

    
    X, Y = np.meshgrid(np.linspace(mins[0], maxs[0], n_bins_v[0]), 
                       np.linspace(mins[1], maxs[1], n_bins_v[1]),
                       indexing='ij')
    
    # Build empty arrays of v_x and v_y
    v_x = np.zeros_like(X)
    v_y = np.zeros_like(Y)
    
    # Mask to track which grid points have been filled
    filled_mask = np.zeros(X.shape, dtype=bool)
    
    # ==========================================
    # 1. BOTTOM EDGE: 1D interpolation along x
    # ==========================================
    bottom_data = data_v[data_v[label_y_column] < bottom_edge_epsilon]
    
    if len(bottom_data) > 0:
        # Extract bottom layer data
        x_bottom = bottom_data[label_x_column].values
        v_x_bottom = bottom_data[label_v_column + label_x_column].values
        v_y_bottom = bottom_data[label_v_column + label_y_column].values
        
        # Sort by x
        sort_idx = np.argsort(x_bottom)
        x_bottom = x_bottom[sort_idx]
        v_x_bottom = v_x_bottom[sort_idx]
        v_y_bottom = v_y_bottom[sort_idx]
        
        # Create 1D interpolation functions
        interp_v_x = interp1d(x_bottom, v_x_bottom, kind='linear', 
                             fill_value='extrapolate')
        interp_v_y = interp1d(x_bottom, v_y_bottom, kind='linear',
                             fill_value='extrapolate')
        
        # Fill bottom row (first column in second index, all rows in first index)
        v_x[:, 0] = interp_v_x(X[:, 0])
        v_y[:, 0] = interp_v_y(X[:, 0])
        filled_mask[:, 0] = True
    
    # ==========================================
    # 2. RIGHT EDGE: 1D interpolation along y
    # ==========================================
    if right_edge_x is not None and right_edge_epsilon is not None:
        # Filter data near right edge
        right_data = data_v[np.abs(data_v[label_x_column] - right_edge_x) < right_edge_epsilon]
        
        if len(right_data) > 0:
            # Extract right edge data
            y_right = right_data[label_y_column].values
            v_x_right = right_data[label_v_column + label_x_column].values
            v_y_right = right_data[label_v_column + label_y_column].values
            
            # Sort by y
            sort_idx = np.argsort(y_right)
            y_right = y_right[sort_idx]
            v_x_right = v_x_right[sort_idx]
            v_y_right = v_y_right[sort_idx]
            
            # Create 1D interpolation functions along y
            interp_v_x = interp1d(y_right, v_x_right, kind='linear',
                                 fill_value='extrapolate')
            interp_v_y = interp1d(y_right, v_y_right, kind='linear',
                                 fill_value='extrapolate')
            
            # Fill right column (last row in first index, all columns in second index)
            v_x[-1, :] = interp_v_x(Y[-1, :])
            v_y[-1, :] = interp_v_y(Y[-1, :])
            filled_mask[-1, :] = True
    
    # ==========================================
    # 3. INTERIOR: 2D RBF interpolation
    # ==========================================

    # Build points array for RBF
    points = []
    points.extend([list(element) for element in zip(
        data_v[label_x_column], data_v[label_y_column])])

    rbf_x = RBFInterpolator(points, data_v[label_v_column + label_x_column].values,
                            kernel='thin_plate_spline')
    rbf_y = RBFInterpolator(points, data_v[label_v_column + label_y_column].values,
                            kernel='thin_plate_spline')
    
    # Interpolate interior points (those not already filled)
    interior_mask = ~filled_mask
    if np.any(interior_mask):
        interior_points = np.column_stack([X[interior_mask], Y[interior_mask]])
        v_x[interior_mask] = rbf_x(interior_points)
        v_y[interior_mask] = rbf_y(interior_points)

    # Compute norms
    grid_norm_v, norm_v_min, norm_v_max, norm_v = norm_vector_field([v_x, v_y])

    return X, Y, v_x, v_y, grid_norm_v, norm_v_min, norm_v_max, norm_v

'''
interpolate a two-dimensional vector field living on a plane

Input values:
    - 'data_v': data where the values of the vector field, on an arbitrary set of points, xy, are stored
    - 'min', 'maxs': limits of the rectangular region where to interpolate
    - 'n_bins_v': number of bins along each axis of the rectangular region where to interpolate
    - 'label_x_column': label of the x axis in data_v
    - 'label_y_column': label of the y axis in data_v
    - 'label_v_column': label of the vector field in data_v

Return values: 
    - 'X' the table of the x coordinates of interpolated points
    - 'Y' the table of the y coordinates of interpolated points
    - 'v_x' the table of the x components of the interpolated vector field
    - 'v_y' the table of the y components of the interpolated vector field
    - 'grid_norm_v' the table of the norm of the interpolated vector field
    - 'norm_v_min' the minimum of the norm of the interpolated vector field
    - 'norm_v_max' the maximum of the norm of the interpolated vector field
    - 'norm_v' the normalization function for color maps, with respect to the norm of the
'''


def interpolate_2d_vector_field(data_v, mins, maxs, n_bins_v,
                                label_x_column=':0',
                                label_y_column=':1',
                                label_v_column='f'):
    # X, Y are the values of x and y coordinated over a mesh composed of tiled rectangles
    X, Y = np.meshgrid(np.linspace(mins[0], maxs[0], n_bins_v[0]), np.linspace(mins[1], maxs[1], n_bins_v[1]),
                       indexing='ij')
    # points are the values of x,y stored in data_v
    points = []
    points.extend([list(element) for element in zip(
        data_v[label_x_column], data_v[label_y_column])])

    # values_v_* are the values of the vector field stored in data_v, on the points stored in points
    values_v_x = data_v[label_v_column + label_x_column]
    values_v_y = data_v[label_v_column + label_y_column]

    # # interpolate the vector field on the grid X, Y
    # v_x = griddata(points, values_v_x, (X, Y), method='cubic')
    # v_y = griddata(points, values_v_y, (X, Y), method='cubic')

    # interpolate the vector field on the grid X, Y with extrapolation
    rbf_x = RBFInterpolator(points, values_v_x, kernel='thin_plate_spline')
    rbf_y = RBFInterpolator(points, values_v_y, kernel='thin_plate_spline')

    v_x = rbf_x(np.column_stack([X.ravel(), Y.ravel()])).reshape(X.shape)
    v_y = rbf_y(np.column_stack([X.ravel(), Y.ravel()])).reshape(X.shape)

    grid_norm_v, norm_v_min, norm_v_max, norm_v = norm_vector_field([v_x, v_y])

    return X, Y, v_x, v_y, grid_norm_v, norm_v_min, norm_v_max, norm_v


'''
interpolate a vector field normal to a manifold in the Monge gauge

Input values:
- 'data_w': table containing the values of the vector field
- 'data_z': table containing the values of the manifold
- 'data_omega': table containing the values of the manifold gradient
- 'mins', 'maxs': the bounds of the rectangular region where to interpolate the surface
- 'z_min': minimum value of the height of the surface
- 'N_bins_w': number of bins with which the vector field is interpolated
- 'label_x_column': label of the x column
- 'label_y_column': label of the y column
- 'label_z_column': label of the z column
- 'label_w_column': label of the column of the vector field
- 'label_omega_column': label of the column of the manifold gradient

Return values:
- 'X_w', 'Y_w', 'Z_w': table of the interpolated manifold
- 'w_x', 'w_y', 'w_z': table of the interpolated vector field
- 'grid_norm_w': table of the norm of the interpolated vector field
- 'norm_w_min': minimum of the norm of the interpolated vector field
- 'norm_w_max': maximum of the norm of the interpolated vector field
- 'norm_w': normalization function for color maps, with respect to the norm of the interpolated vector field
'''


def interpolate_n_vector_field(data_w, data_z, data_omega, mins, maxs, z_min, N_bins_w, label_x_column, label_y_column,
                               label_z_column, label_w_column, label_omega_column):

    X_w, Y_w, Z_w = gr.interpolate_surface(data_z, mins, maxs, z_min, N_bins_w, 1, label_x_column,
                                           label_y_column, label_z_column)

    points = []
    points.extend([list(element) for element in zip(
        data_w[label_x_column], data_w[label_y_column])])

    data_omega_w = zip(data_omega[label_omega_column + label_x_column], data_omega[label_omega_column + label_y_column],
                       data_w[label_w_column])

    values_w_x = []
    values_w_y = []
    values_w_z = []
    for element in data_omega_w:
        value_w = element[2] * geo.normal([element[0], element[1]])
        values_w_x.append(value_w[0])
        values_w_y.append(value_w[1])
        values_w_z.append(value_w[2])

    # 3 interpolate values_z and points, and write the result of the interpolated function on the lattice (X, Y_quiver) into grid
    w_x = griddata(points, values_w_x, (X_w, Y_w), method='cubic')
    w_y = griddata(points, values_w_y, (X_w, Y_w), method='cubic')
    w_z = griddata(points, values_w_z, (X_w, Y_w), method='cubic')

    grid_norm_w, norm_w_min, norm_w_max, norm_w = norm_vector_field([
        w_x, w_y, w_z])

    return X_w, Y_w, Z_w, w_x, w_y, w_z, grid_norm_w, norm_w_min, norm_w_max, norm_w


'''
return the min/max norm of the vector on a manifold considered as a vector in three-dimensional euclidean space in which the manifold is embedded
- 'name_file_v' : name of file storing the data for the vector field
- 'name_file_omega' : name of file storing the data for the manifold gradient
- 'columns_v' : column labels of the file for the vector field
- 'label_v_column' : label of the column of the vector field
- 'columns_omega' : column labels of the file for the omega (manifold gradient) field

Return values:
- 'norm_v_min' : minimal norm of the vector field
- 'norm_v_max' : maximal norm of the vector field
'''


def norm_v_min_max_file(name_file_v, name_file_omega, columns_v, label_v_column, columns_omega):
    data_v = pd.read_csv(name_file_v, usecols=columns_v)
    data_omega = pd.read_csv(name_file_omega, usecols=columns_omega)

    values_v_x = data_v[label_v_column + clab.label_x_column]
    values_v_y = data_v[label_v_column + clab.label_y_column]
    values_v_z = data_v[label_v_column + clab.label_x_column] * data_omega[
        clab.label_omega_column + clab.label_x_column] + data_v[
        clab.label_v_column + clab.label_y_column] * data_omega[
        clab.label_omega_column + clab.label_y_column]

    norm_v_min, norm_v_max = min_max_vector_field(
        [values_v_x, values_v_y, values_v_z])

    return norm_v_min, norm_v_max


'''
compute the minimum and maximum norm, across multiple snapshots of the field, of a vector field defined on the tangent bundle of a manifold
- 'file_path' : path where to find both the file for the vector field and the one for the manifold gradient (omega)
- 'name_file_v' : name of file storing the data for the vector field
- 'name_file_omega' : name of file storing the data for the manifold gradient
- 'columns_v' : column labels of the file for the vector field
- 'label_v_column' : label of the column of the vector field
- 'columns_omega' : column labels of the file for the omega (manifold gradient) field
- 'n_file_min' : the snapshot to start with'
- 'n_file_max' : the snapshot to end with'
- 'n_file_stride' : the stride across one snapshot and the next
'''


def norm_v_min_max_files(name_file_v, name_file_omega, file_path, columns_v, label_v_column, columns_omega, n_file_min,
                         n_file_max, n_file_stride):

    abs_min = np.inf
    abs_max = - np.inf

    for i in range(n_file_min, n_file_max, n_file_stride):

        min, max = norm_v_min_max_file(file_path + name_file_v + str(i) + '.csv',
                                       file_path + name_file_omega +
                                       str(i) + '.csv',
                                       columns_v, label_v_column, columns_omega)

        if min < abs_min:
            abs_min = min

        if max > abs_max:
            abs_max = max

    return abs_min, abs_max


def norm_v_min_max_file_list(name_file_v, name_file_omega, file_path,
                             n_file_list,
                             columns_v, label_v_column, columns_omega):

    abs_min, abs_max = norm_v_min_max_file(file_path + name_file_v + str(n_file_list[0]) + '.csv',
                                           file_path + name_file_omega +
                                           str(n_file_list[0]) + '.csv',
                                           columns_v, label_v_column, columns_omega)

    for n_file in n_file_list:

        min, max = norm_v_min_max_file(file_path + name_file_v + str(n_file) + '.csv',
                                       file_path + name_file_omega +
                                       str(n_file) + '.csv',
                                       columns_v, label_v_column, columns_omega)

        if min < abs_min:
            abs_min = min

        if max > abs_max:
            abs_max = max

    return abs_min, abs_max


def plot_analytical_vector_field_on_curve(ax, v, gamma, min, max, n_bins, scale_factor_z, z_min, shaft_length,
                                          head_over_shaft_length, head_angle, threshold_arrow_length, line_width, color, alpha, z_order):
    X, Y, Z, V, ts = tabulate_analytical_vector_field_on_curve(
        v, gamma, min, max, n_bins)

    for i in range(len(ts)):
        arr.plot_arrow(ax, [X[i], Y[i], Z[i]],
                       np.add([X[i], Y[i], Z[i]],
                              V[i]),
                       shaft_length, head_over_shaft_length, head_angle, [
                           0, 0, z_min],
                       [1, 1, scale_factor_z], threshold_arrow_length,
                       line_width, color, alpha, z_order)

'''
set both components of a vector field to a value inside a polygonal region
Input values: 
    * Mandatory:
        - 'polygon_points': list of the vertices of the polygon
        - 'R': [X, Y] grid where the vector field is defined
        - 'V': [V_x, V_y] vector field defined on the grid R
    * Optional:
        - 'value': value to set inside the polygon (default: np.nan)
'''
def set_in_polygon(polygon_points, R, V, 
                   value=np.nan):

    # Create a Path object from the polygon vertices
    polygon_path = Path(polygon_points)

    # Create a 2D array of all (x, y) points from your grid
    # Flatten X and Y to 1D arrays, then stack them
    points = np.column_stack((R[0].flatten(), R[1].flatten()))

    # Check which points are inside the polygon
    inside_mask = polygon_path.contains_points(points)

    # Reshape the mask back to the grid shape
    inside_mask = inside_mask.reshape(R[0].shape)

    # Set V_x and V_y to value where points are inside the polygon
    V[0][inside_mask] = value
    V[1][inside_mask] = value


'''
set componenta of a vector field equal to a value in a region delimited by two polygons
Input values: 
    * Mandatory:
        - 'polygon_points_a', 'polygon_points_b': list of the vertices of  polygon_a and polygon_b, respectively
        - 'R': [X, Y] grid where the vector field is defined
        - 'V': [V_x, V_y] vector field defined on the grid R
    * Optional:
        - 'value': value to set inside the polygon (default: np.nan)
'''
def set_between_polygons(polygon_points_a, polygon_points_b, R, V,
                         value=np.nan):


    '''
    R[0] and R[1] are in this format
        R[0] (X):          R[1] (Y):
        [[0, 1, 2],        [[0, 0, 0],
        [0, 1, 2],         [1, 1, 1],
        [0, 1, 2]]         [2, 2, 2]]

    and here they are reshaped as follows and written into points

        points = [
            [0, 0],
            [0, 1],
            [0, 2],
            [1, 0],
            [1, 1],
            ...
        ]
    '''
    points = np.column_stack((R[0].flatten(), R[1].flatten()))

    inside_a = Path(polygon_points_a).contains_points(points).reshape(R[0].shape)
    inside_b = Path(polygon_points_b).contains_points(points).reshape(R[0].shape)

    # Region between polygons a and b: inside one but not the other
    between_a_and_b = inside_a ^ inside_b

    V[0][between_a_and_b] = value
    V[1][between_a_and_b] = value 


