import numpy as np
from matplotlib.tri import Triangulation

import graph as gr

'''
return a mask for a cruve which is True outside a circle and False inside
- 'gamma': the function of the curve gamma(t) : [t_min, t_max] -> R^3
- 't_min', 't_max': the minimum and maximum values of the parameter t
- 'r', 'cr': radius and center of the circle
- 'n_bins': number of bins with which 'gamma' is tabulated

return values:
- 'mask': a 1d array of Trues of False, runningn along t. Each entry is True if the corresponding gamma(t) is outside the circle, and False otherwise

'''


def curve_mask_disk(gamma, t_min, t_max, r, cr, n_bins):
    t = np.mgrid[t_min:t_max:n_bins * 1j]

    mask = (gamma(t)[0] - cr[0]) ** 2 + (gamma(t)[1] - cr[1]) ** 2 > r ** 2

    return mask


def flat_surface_mask_disk(f, mins, maxs, r, cr, n_bins):
    # Generate a grid of X, Y values and flatten them and store them in X_flattened, Y_flattened
    X = np.linspace(mins[0], maxs[0], n_bins[0])
    Y = np.linspace(mins[1], maxs[1], n_bins[1])
    X_flattened, Y_flattened = np.meshgrid(X, Y)
    X_flattened = X_flattened.ravel()
    Y_flattened = Y_flattened.ravel()

    # Mask points inside the disk
    distance_from_cr = (X_flattened - cr[0]) ** 2 + (Y_flattened - cr[1]) ** 2
    mask = distance_from_cr > r ** 2

    # X_trimmed contains only the entries of X_flattened for which mask = True
    X_trimmed = X_flattened[mask]
    Y_trimmed = Y_flattened[mask]
    Z_trimmed = f(X_trimmed, Y_trimmed)

    # Triangulate the trimmed points
    tri = Triangulation(X_trimmed, Y_trimmed)

    # Compute triangle centroids
    triangle_centers_X = X_trimmed[tri.triangles].mean(axis=1)
    triangle_centers_Y = Y_trimmed[tri.triangles].mean(axis=1)

    # Mask out triangles whose centroids lie inside the circle
    triangle_distance_from_cr = (triangle_centers_X - cr[0]) ** 2 + (triangle_centers_Y - cr[1]) ** 2
    valid_triangles = tri.triangles[triangle_distance_from_cr >= r ** 2]

    return mask, [X_trimmed, Y_trimmed, Z_trimmed], valid_triangles



'''
generate a mask for a grid of curves, which prevent the curves in the grid from being plotted in a disk within a rectangular region
- 'ax': the axis where the plot will be made
- 'f' : the function definiing the manifold
- 'mins', 'maxs': the mins and maxs defining the rectangular region
- 'n_curves' : the number of curves in the grid
- 'r', 'cr': the radius and center of the disk
- 'n_bins_curve' : the number of bins (segments) used to plot each curve in the grid

Return values: 
- 'curve_mask_x', 'curve_mask_y': a list of masks for the curves along the y and x axis, respectively 
'''
def grid_mask_disk(ax, f, mins, maxs, n_curves, r, cr, n_bins_curve):
    X = np.mgrid[mins[0]:maxs[0]:n_curves[0] * 1j]
    Y = np.mgrid[mins[1]:maxs[1]:n_curves[1] * 1j]

    curve_mask_x = []
    curve_mask_y = []

    for x in X:
        curve_mask_x.append(curve_mask_disk(lambda t: gr.gamma_y(t, mins, maxs, f, x), 0, 1, r, cr, n_bins_curve))

    for y in Y:
        curve_mask_y.append(curve_mask_disk(lambda t: gr.gamma_x(t, mins, maxs, f, y), 0, 1, r, cr, n_bins_curve))

    return curve_mask_x, curve_mask_y
