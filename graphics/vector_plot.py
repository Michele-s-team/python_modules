import numpy as np
import matplotlib.colors as mcolors
import pandas as pd
from scipy.interpolate import griddata

import list.column_labels as clab
import graphics.graph as gr
import calculus.geometry as geo

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
    X, Y, Z, V = tabulate_analytical_vector_field_on_surface(v, f, mins, maxs, n_bins)

    plot_vector_field(ax, [X, Y, Z], V, scale_factor_z, z_min, shaft_length, head_over_shaft_length, head_angle,
                      line_width, alpha, color, z_order)


def plot_analytical_vector_field_on_surface_outside_disk(ax, v, f, mins, maxs, r, cr, n_bins, scale_factor_z, z_min, shaft_length,
                                                         head_over_shaft_length, threshold_arrow_length, head_angle, line_width, color, alpha, z_order):
    X, Y, Z, V = tabulate_analytical_vector_field_on_surface(v, f, mins, maxs, n_bins)

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
'''
def plot_vector_field(ax, grid_r, grid_v, scale_factor_z, z_min, shaft_length, head_over_shaft_length, head_angle, threshold_arrow_length,
                      line_width, alpha, color, z_order):
    grid_norm_v, norm_v_min, norm_v_max, norm_v = norm_vector_field(grid_v)

    for i in range(len(grid_r[0])):
        for j in range(len(grid_r[1][i])):
            vector_norm = grid_norm_v[i, j]

            if color == 'color_from_map':
                # Get corresponding arrow_color from colormap
                arrow_color = gr.cb.color_map_type(norm_v(vector_norm))
            else:
                arrow_color = color

            gr.plot_arrow(ax, [grid_r[0][i, j], grid_r[1][i, j], grid_r[2][i, j]],
                          np.add([grid_r[0][i, j], grid_r[1][i, j], grid_r[2][i, j]],
                                 [grid_v[0][i, j], grid_v[1][i, j], grid_v[2][i, j]]), \
                          shaft_length, head_over_shaft_length, head_angle, [0, 0, z_min],
                          [1, 1, scale_factor_z], threshold_arrow_length,
                          line_width, arrow_color, alpha, z_order)


'''
plot a two-dimensional vector field
'''


def plot_2d_vector_field(ax, grid_r, grid_v, shaft_length, head_over_shaft_length, head_angle, line_width, alpha, color, z_order):
    grid_norm_v, norm_v_min, norm_v_max, norm_v = norm_2d_vector_field(grid_v)

    for i in range(len(grid_r[0])):
        for j in range(len(grid_r[1][i])):
            vector_norm = grid_norm_v[i, j]

            if color == 'color_from_map':
                # Get corresponding arrow_color from colormap
                arrow_color = gr.cb.color_map_type(norm_v(vector_norm))
            else:
                arrow_color = color

            gr.plot_2d_arrow(ax, [grid_r[0][i, j], grid_r[1][i, j]],
                             np.add([grid_r[0][i, j], grid_r[1][i, j]],
                                    [grid_v[0][i, j], grid_v[1][i, j]]), \
                             shaft_length, head_over_shaft_length, head_angle, line_width, arrow_color, alpha, z_order)

def plot_2d_vector_field_scaled_length(ax, grid_r, grid_v, shaft_length, head_over_shaft_length, head_angle, line_width, alpha, color, z_order):
    grid_norm_v, norm_v_min, norm_v_max, norm_v = norm_2d_vector_field(grid_v)

    for i in range(len(grid_r[0])):
        for j in range(len(grid_r[1][i])):
            vector_norm = grid_norm_v[i, j]

            if color == 'color_from_map':
                # Get corresponding arrow_color from colormap
                arrow_color = gr.cb.color_map_type(norm_v(vector_norm))
            else:
                arrow_color = color

            gr.plot_2d_arrow(ax, [grid_r[0][i, j], grid_r[1][i, j]],
                             np.add([grid_r[0][i, j], grid_r[1][i, j]],
                                    [grid_v[0][i, j], grid_v[1][i, j]]), \
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

            gr.plot_arrow(ax, [grid_r[0][i, j], grid_r[1][i, j], grid_r[2][i, j]],
                          np.add([grid_r[0][i, j], grid_r[1][i, j], grid_r[2][i, j]],
                                 [grid_v[0][i, j], grid_v[1][i, j], grid_v[2][i, j]]), \
                          shaft_length, head_over_shaft_length, head_angle, [0, 0, z_min],
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


def norm_vector_field(grid_v):
    grid_norm_v = np.sqrt(grid_v[0] ** 2 + grid_v[1] ** 2 + grid_v[2] ** 2)
    norm_v_min, norm_v_max = np.nanmin(grid_norm_v), np.nanmax(grid_norm_v)
    norm_v = mcolors.Normalize(vmin=norm_v_min, vmax=norm_v_max)  # Normalize norms to [0,1]

    return grid_norm_v, norm_v_min, norm_v_max, norm_v


def norm_2d_vector_field(grid_v):
    grid_norm_v = np.sqrt(grid_v[0] ** 2 + grid_v[1] ** 2)
    norm_v_min, norm_v_max = np.nanmin(grid_norm_v), np.nanmax(grid_norm_v)
    norm_v = mcolors.Normalize(vmin=norm_v_min, vmax=norm_v_max)  # Normalize norms to [0,1]

    return grid_norm_v, norm_v_min, norm_v_max, norm_v


'''
interpolate a vector field on the tangent bundle of a manifold
'''


def interpolate_t_vector_field(data_v, data_z, data_omega, mins, maxs, z_min, N_bins_v, label_x_column, label_y_column,
                               label_z_column, label_v_column, label_omega_column):
    X_v, Y_v, Z_v = gr.interpolate_surface(data_z, mins, maxs, z_min, N_bins_v, 1, label_x_column,
                                           label_y_column, label_z_column)

    points = []
    points.extend([list(element) for element in zip(data_v[label_x_column], data_v[label_y_column])])
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

    grid_norm_v, norm_v_min, norm_v_max, norm_v = gr.vp.norm_vector_field([v_x, v_y, v_z])

    return X_v, Y_v, Z_v, v_x, v_y, v_z, grid_norm_v, norm_v_min, norm_v_max, norm_v


'''
interpolate a two-dimensional vector field living on a plane 
Input values:
- 'data_v': data where the values of the vector field, on an arbitrary set of points, xy, are stored
- 'min', 'maxs': limits of the rectangular region where to interpolate
- 'n_bins_v': number of bins along each axis of the rectangular region where to interpolate
- 'label_x_column': label of the x axis in data_v
- 'label_y_column': label of the y axis in data_v
- 'label_v_column': label of the vector field in data_v

'''


def interpolate_2d_vector_field(data_v, mins, maxs, n_bins_v, label_x_column, label_y_column, label_v_column):
    # X, Y are the values of x and y coordinated over a mesh composed of tiled rectangles
    X, Y = np.meshgrid(np.linspace(mins[0], maxs[0], n_bins_v[0]), np.linspace(mins[1], maxs[1], n_bins_v[1]),
                       indexing='ij')
    # points are the values of x,y stored in data_v
    points = []
    points.extend([list(element) for element in zip(data_v[label_x_column], data_v[label_y_column])])

    # values_v_* are the values of the vector field stored in data_v, on the points stored in points
    values_v_x = data_v[label_v_column + label_x_column]
    values_v_y = data_v[label_v_column + label_y_column]

    # interpolate the vector field on the grid X, Y
    v_x = griddata(points, values_v_x, (X, Y), method='cubic')
    v_y = griddata(points, values_v_y, (X, Y), method='cubic')

    grid_norm_v, norm_v_min, norm_v_max, norm_v = gr.vp.norm_2d_vector_field([v_x, v_y])

    return X, Y, v_x, v_y, grid_norm_v, norm_v_min, norm_v_max, norm_v


'''
interpolate a vector field normal to a manifold
'''


def interpolate_n_vector_field(data_w, data_z, data_omega, mins, maxs, z_min, N_bins_w, label_x_column, label_y_column,
                               label_z_column, label_w_column, label_omega_column):
    X_w, Y_w, Z_w = gr.interpolate_surface(data_z, mins, maxs, z_min, N_bins_w, 1, label_x_column,
                                           label_y_column, label_z_column)

    points = []
    points.extend([list(element) for element in zip(data_w[label_x_column], data_w[label_y_column])])

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

    grid_norm_w, norm_w_min, norm_w_max, norm_w = gr.vp.norm_vector_field([w_x, w_y, w_z])

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

    norm_v_min, norm_v_max = min_max_vector_field([values_v_x, values_v_y, values_v_z])

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
    abs_min, abs_max = norm_v_min_max_file(file_path + name_file_v + str(n_file_min) + '.csv',
                                           file_path + name_file_omega + str(n_file_min) + '.csv',
                                           columns_v, label_v_column, columns_omega)

    for i in range(n_file_min + 1, n_file_max + 1, n_file_stride):

        min, max = norm_v_min_max_file(file_path + name_file_v + str(i) + '.csv',
                                       file_path + name_file_omega + str(i) + '.csv',
                                       columns_v, label_v_column, columns_omega)

        if min < abs_min:
            abs_min = min

        if max > abs_max:
            abs_max = max

    return abs_min, abs_max


def norm_v_min_max_file_list(name_file_v, name_file_omega, file_path, columns_v, label_v_column, columns_omega, n_file_list):
    abs_min, abs_max = norm_v_min_max_file(file_path + name_file_v + str(n_file_list[0]) + '.csv',
                                           file_path + name_file_omega + str(n_file_list[0]) + '.csv',
                                           columns_v, label_v_column, columns_omega)

    for n_file in n_file_list:

        min, max = norm_v_min_max_file(file_path + name_file_v + str(n_file) + '.csv',
                                       file_path + name_file_omega + str(n_file) + '.csv',
                                       columns_v, label_v_column, columns_omega)

        if min < abs_min:
            abs_min = min

        if max > abs_max:
            abs_max = max

    return abs_min, abs_max


def plot_analytical_vector_field_on_curve(ax, v, gamma, min, max, n_bins, scale_factor_z, z_min, shaft_length,
                                          head_over_shaft_length, head_angle, threshold_arrow_length, line_width, color, alpha, z_order):
    X, Y, Z, V, ts = tabulate_analytical_vector_field_on_curve(v, gamma, min, max, n_bins)

    for i in range(len(ts)):
        gr.plot_arrow(ax, [X[i], Y[i], Z[i]],
                      np.add([X[i], Y[i], Z[i]],
                             V[i]), \
                      shaft_length, head_over_shaft_length, head_angle, [0, 0, z_min],
                      [1, 1, scale_factor_z], threshold_arrow_length,
                      line_width, color, alpha, z_order)
