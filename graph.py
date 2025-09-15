import math
from os import RTLD_LOCAL

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import pandas as pd
import proplot as pplt
from pandas.core.methods.selectn import SelectNSeries
from scipy.interpolate import griddata
from scipy.interpolate import Rbf
from sympy.codegen.ast import RuntimeError_
from sympy.polys.benchmarks.bench_solvers import R_165

# do not remove these: they are not used by graph.py but they are used by other modules calling graph.py
import color_bar as cb
import column_labels as clab
import images
import mask
import ticks as ti
import vector_plot as vp

epsilon = 1e-6
epsilon_axes = 5e-2
threshold_arrow_length = 1e-4
deg_to_rad = 2 * np.pi / 360


# convert the floating-point number 'x' to latex in format 'format'
def float_to_latex(x, format):
    if (format == 'f'):
        latex_string = fr'${x:.3g}$'
    elif (format == 'e'):
        latex_string = to_latex_scientific(x)

    return latex_string


def plot_3d_axis(ax, r, l, direction, scale_factor, tick_length, line_width, axis_label,
                 axis_label_offset, ticks_label_offset, tick_label_format, font_size, z_order):
    if direction == 'x':
        r_start = r[0]
    elif direction == 'y':
        r_start = r[1]
    elif direction == 'z':
        r_start = r[2]

    ticks = ti.generate_ticks(r_start, r_start + scale_factor * l)

    ticks_list = []
    for tick in ticks:
        ticks_list.append([
            tick,
            float_to_latex(r_start + (tick - r_start) / scale_factor, tick_label_format)
        ])

    plot_3d_axis_custom_ticks(ax, r, l, direction, scale_factor, ticks_list, tick_length, line_width, axis_label,
                              axis_label_offset, ticks_label_offset, tick_label_format, font_size, z_order)


def plot_3d_axis_custom_ticks(ax, r, l, direction, scale_factor, ticks_list, tick_length, line_width, axis_label,
                              axis_label_offset, ticks_label_offset, tick_label_format, font_size, z_order):
    if direction == "x":

        ax.plot([r[0], r[0] + scale_factor * l], [r[1], r[1]], [r[2], r[2]], color='black', linewidth=line_width,
                zorder=z_order)
        for tick in ticks_list:
            ax.plot([tick[0], tick[0]], [r[1], r[1] + tick_length], [r[2], r[2]], color='black',
                    linewidth=line_width, zorder=z_order)  # x-axis line
            if tick_label_format != '':
                ax.text(tick[0], r[1] - ticks_label_offset, r[2],
                        tick[1], fontsize=font_size, ha='center', va='center', zorder=10)

        ax.text(r[0] + scale_factor * l / 2, r[1] - axis_label_offset, r[2], axis_label, fontsize=font_size, ha='center',
                va='center', zorder=z_order)


    elif direction == "y":

        ax.plot([r[0], r[0]], [r[1], r[1] + scale_factor * l], [r[2], r[2]], color='black', linewidth=line_width,
                zorder=z_order)
        for tick in ticks_list:
            ax.plot([r[0], r[0] + tick_length], [tick[0], tick[0]], [r[2], r[2]], color='black',
                    linewidth=line_width, zorder=z_order)  # x-axis line
            if tick_label_format != '':
                ax.text(r[0] - ticks_label_offset, tick[0], r[2],
                        tick[1], fontsize=font_size, ha='center', va='center', zorder=10)

        ax.text(r[0] - axis_label_offset, r[1] + scale_factor * l / 2, r[2], axis_label, fontsize=font_size,
                ha='center', va='center', zorder=z_order)


    elif direction == "z":

        ax.plot([r[0], r[0]], [r[1], r[1]], [r[2], r[2] + scale_factor * l], color='black', linewidth=line_width,
                zorder=z_order)
        for tick in ticks_list:
            ax.plot([r[0], r[0] + tick_length], [r[1], r[1]], [tick[0], tick[0]], color='black',
                    linewidth=line_width, zorder=z_order)  # x-axis line
            if tick_label_format != '':
                ax.text(r[0] - ticks_label_offset, r[1], tick[0],
                        tick[1], fontsize=font_size,
                        ha='center', va='center',
                        zorder=10)

        ax.text(r[0] - axis_label_offset, r[1] - axis_label_offset, r[2] + scale_factor * l / 2, axis_label,
                fontsize=font_size, ha='center', va='center', zorder=z_order)


'''
plot a triad of 3d axes on 'ax', with origin 'origin' and lengths of each axis given by 'lengths'. 
Each axis is scaled up with respect to its origin coordinate by its respective entry of 'scale_factor'
'''


def plot_3d_axes(ax, origin, lengths, scale_factors, axis_labels, axis_label_offsets, tick_lengths,
                 tick_label_offsets, tick_label_formats, font_size, z_order):
    # plot x axis
    plot_3d_axis(ax, origin, lengths[0], "x", scale_factors[0],
                 tick_lengths[0] * lengths[1] * scale_factors[1], 0.3, axis_labels[0],
                 axis_label_offsets[0] * lengths[1] * scale_factors[1],
                 tick_label_offsets[0] * lengths[1] * scale_factors[1], tick_label_formats[0], font_size, z_order)

    # plot y axis
    plot_3d_axis(ax, origin, lengths[1], "y", scale_factors[1],
                 tick_lengths[1] * lengths[0] * scale_factors[0], 0.3, axis_labels[1],
                 axis_label_offsets[1] * lengths[0] * scale_factors[0],
                 tick_label_offsets[1] * lengths[0] * scale_factors[0], tick_label_formats[1], font_size, z_order)

    # plot z axis
    plot_3d_axis(ax, origin, lengths[2], "z", scale_factors[2],
                 tick_lengths[2] * (lengths[0] * scale_factors[0] + lengths[1] * scale_factors[1]) / 2, 0.3,
                 axis_labels[2],
                 axis_label_offsets[2] * (lengths[0] * scale_factors[0] + lengths[1] * scale_factors[1]) / 2,
                 tick_label_offsets[2] * (lengths[0] * scale_factors[0] + lengths[1] * scale_factors[1]) / 2,
                 tick_label_formats[2], font_size, z_order)


def plot_3d_axes_custom_ticks(ax, origin, lengths, scale_factors, ticks_list, axis_labels, axis_label_offsets,
                              tick_lengths,
                              tick_label_offsets, tick_label_formats, font_size, z_order):
    plot_3d_axis_custom_ticks(ax, origin, lengths[0], "x", scale_factors[0], ticks_list[0],
                              tick_lengths[0] * lengths[1] * scale_factors[1], 0.3, axis_labels[0],
                              axis_label_offsets[0] * lengths[1] * scale_factors[1],
                              tick_label_offsets[0] * lengths[1] * scale_factors[1], tick_label_formats[0], font_size,
                              z_order)
    plot_3d_axis_custom_ticks(ax, origin, lengths[1], "y", scale_factors[1], ticks_list[1],
                              tick_lengths[1] * lengths[0] * scale_factors[0], 0.3, axis_labels[1],
                              axis_label_offsets[1] * lengths[0] * scale_factors[0],
                              tick_label_offsets[1] * lengths[0] * scale_factors[0], tick_label_formats[1], font_size,
                              z_order)
    plot_3d_axis_custom_ticks(ax, origin, lengths[2], "z", scale_factors[2], ticks_list[2],
                              tick_lengths[2] * (lengths[0] * scale_factors[0] + lengths[1] * scale_factors[1]) / 2,
                              0.3,
                              axis_labels[2],
                              axis_label_offsets[2] * (
                                      lengths[0] * scale_factors[0] + lengths[1] * scale_factors[1]) / 2,
                              tick_label_offsets[2] * (
                                      lengths[0] * scale_factors[0] + lengths[1] * scale_factors[1]) / 2,
                              tick_label_formats[2], font_size, z_order)


def plot_2d_axis(ax, r, l, direction, tick_length, line_width, axis_label, axis_label_offset, axis_label_angle,
                 ticks_label_offset, tick_label_format, font_size,
                 z_order):
    if direction == "x":

        # ticks = ticks_base_10(r[0], r[0] + l, n_ticks)
        ticks = ti.generate_ticks(r[0], r[0] + l)

        ax.plot([r[0], r[0] + l], [r[1], r[1]], color='black', linewidth=line_width, zorder=z_order)
        for tick in ticks:
            ax.plot([tick, tick], [r[1], r[1] + tick_length], color='black', linewidth=line_width,
                    zorder=z_order)  # x-axis line
            if tick_label_format != '':
                ax.text(tick, r[1] - ticks_label_offset, float_to_latex(tick, tick_label_format), fontsize=font_size,
                        ha='center', va='center', zorder=10)

        ax.text(l / 2, r[1] - axis_label_offset, axis_label, fontsize=font_size, ha='center', va='center',
                rotation=axis_label_angle, zorder=z_order)

    elif direction == "y":

        # ticks = ticks_base_10(r[1], r[1] + l, n_ticks)
        ticks = ti.generate_ticks(r[1], r[1] + l)

        ax.plot([r[0], r[0]], [r[1], r[1] + l], color='black', linewidth=line_width, zorder=z_order)

        for tick in ticks:
            ax.plot([r[0], r[0] + tick_length], [tick, tick], color='black', linewidth=line_width,
                    zorder=z_order)  # x-axis line
            if tick_label_format != '':
                ax.text(r[0] - ticks_label_offset, tick, float_to_latex(tick, tick_label_format), fontsize=font_size,
                        ha='center', va='center', zorder=10)

        ax.text(r[0] - axis_label_offset, r[1] + l / 2, axis_label, fontsize=font_size, ha='center', va='center',
                rotation=axis_label_angle, zorder=z_order)


# set the values of 'grid' to 'value' in the disk centered at cr and with radius r, in such a way that they are not plotted and the disk is left blank
def set_inside_disk(X, Y, cr, r, grid, value):
    # Compute the distance from the center
    distance_from_center = np.sqrt((X - cr[0]) ** 2 + (Y - cr[1]) ** 2)

    # Create a mask where the distance from cr is less than r
    mask = distance_from_center < r
    # This removes the surface in the disk
    grid[mask] = value


'''
set the values of a grid of points on the xy plane to a value for points which lie in an ellipse
Input values: 
- 'X', 'Y': x and y values
- 'c' center of the ellipse
- 'a', 'b', semi-major and semi-minor axis of the ellipse
- 'phi': rotation angle of the ellipse with respect to its left focal point
- 'values': the values of the grid, it has the same structure as X and Y
- 'value_to_set': the value to be set in the ellipse
'''


def set_inside_ellipse(X, Y, c, a, b, phi, values, value_to_set):
    # left focal point of the ellipse
    focus = np.subtract(c, [np.sqrt(a ** 2 - b ** 2), 0, 0])[:2]

    R_X, R_Y = [], []
    for i in range(len(X)):
        R_X.append([])
        R_Y.append([])
        for j in range(len(X[i])):
            r = np.dot(R_2d(-phi), [X[i, j] - focus[0], Y[i, j] - focus[1]])
            R_X[i].append(r[0])
            R_Y[i].append(r[1])

    R_c = [np.sqrt(a ** 2 - b ** 2), 0]

    R_X = np.array(R_X)
    R_Y = np.array(R_Y)

    # Create a mask to tell whether the point lies in the ellipse or not
    mask = ((R_X - R_c[0]) / a) ** 2 + ((R_Y - R_c[1]) / b) ** 2 < 1
    # This removes the surface in the disk
    values[mask] = value_to_set


# set the values of 'grid' to ;value' outside the disk centered at cr and with radius r, in such a way that they are not plotted and the region outside the disk is left blank
def set_outside_disk(X, Y, cr, r, grid, value):
    # Compute the distance from the center
    distance_from_center = np.sqrt((X - cr[0]) ** 2 + (Y - cr[1]) ** 2)

    # Create a mask where the distance from cr is less than r
    mask = distance_from_center > r
    # This removes the surface in the disk
    grid[mask] = value


'''
set the values of 'grid' to 'value' in the ring between two circles: a circle with radius 'r' and center 'cr' and a circle with radius 'R' and center 'cR'
Here 'X' and 'Y' are the grid values on the xy axis
'''


def set_in_ring(X, Y, cr, r, cR, R, grid, value):
    set_inside_disk(X, Y, cr, r, grid, value)
    set_outside_disk(X, Y, cR, R, grid, value)


def create_3d_disk(center, radius, num_points, color):
    theta = np.linspace(0, 2 * np.pi, num_points)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    z = np.full_like(x, center[2])  # Keep z constant
    points = [list(zip(x, y, z))]
    return Poly3DCollection(points, color=color)


# the radius of the cone as a function of z
def rho_cone(z, r_A_cone, r_B_cone, z_A_cone, z_B_cone, L, h):
    return (h / L * (r_B_cone + (r_A_cone - r_B_cone) / (z_A_cone - z_B_cone) * (z - z_B_cone)))


# tabulate the coordinates of the cone surface and return them as a 3d vector
def tabulate_cone(z_A_cone, z_B_cone, r_A_cone, r_B_cone, cr, L, h):
    z_cone, theta_cone = np.mgrid[z_A_cone:z_B_cone:100j, 0:2 * (np.pi):100j]
    X_cone = cr[0] + rho_cone(z_cone, r_A_cone, r_B_cone, z_A_cone, z_B_cone, L, h) * np.cos(theta_cone)
    Y_cone = cr[1] + rho_cone(z_cone, r_A_cone, r_B_cone, z_A_cone, z_B_cone, L, h) * np.sin(theta_cone)
    Z_cone = cr[2] + z_cone

    return X_cone, Y_cone, Z_cone


# tabulate the coordinates of the cylinder surface and return them as a 3d vector
def tabulate_cylinder(z_top, z_bottom, r, cr, z_min, scale_factor):
    z_A, z_B = set_cylinder(r, z_top, z_bottom, z_min, scale_factor)

    z, theta = np.mgrid[z_A:z_B:100j, 0:2 * (np.pi):100j]
    X = cr[0] + r * np.cos(theta)
    Y = cr[1] + r * np.sin(theta)
    Z = cr[2] + z

    return X, Y, Z


'''
tabulate a surface from an analytical solution
- 'f' : the analytical solution f(x,y)
- 'mins', 'maxs': limits of the rectangular region where 'f' will be tabulated
- 'n_bins': number of bins 
- 'mask' [optional]: a mask defining a subdomain where the plot will be made. This can be generated, for example, with mask.flat_surface_mask_disk
Return values: 
- 'X', 'Y', 'Z': the grids of x, y, and of the tabulated function z = f(x,y)
'''


def tabulate_analytical_surface(f, mins, maxs, n_bins, mask=None):
    X, Y = np.mgrid[mins[0]:maxs[0]:n_bins[0] * 1j, mins[1]:maxs[1]:n_bins[1] * 1j]
    Z = f(X, Y)

    if mask is not None:
        X[~mask] = np.nan
        Y[~mask] = np.nan
        Z[~mask] = np.nan

    return X, Y, Z


'''
plot a surface given by an analytical expression
- 'ax': the axis where the plot will be made
- 'f': f(x,y): the function defining the surface
- 'mins': mins, maxs: limits of the rectangular region where the plot will be made
- 'n_bins': number of bins 
- 'color': the color of the plotted surface
- 'z_order': the z-order of the plotted surface
- 'mask' [optional]: a mask defining a subdomain where the plot will be made, generated, for example, with mask.flat_surface_mask_disk

'''


def plot_analytical_surface(ax, f, mins, maxs, n_bins, color, alpha, z_order, mask=None):
    if mask is None:

        X, Y, Z = tabulate_analytical_surface(f, mins, maxs, n_bins)
        surface = ax.plot_surface(X, Y, Z, color=color, alpha=alpha, zorder=z_order)

    else:
        # Plot by keeping only the  triangles whose distance from cr is > r
        surface = ax.plot_trisurf(mask[1][0], mask[1][1], mask[1][2], triangles=mask[2], color=color, alpha=alpha,
                                  zorder=z_order, shade=True)
        surface.set_edgecolor('none')

    return surface


def gamma_x(t, mins, maxs, f, y):
    return [mins[0] + (maxs[0] - mins[0]) * t, y, f(mins[0] + (maxs[0] - mins[0]) * t, y)]


def gamma_y(t, mins, maxs, f, x):
    return [x, mins[0] + (maxs[0] - mins[0]) * t, f(x, mins[0] + (maxs[0] - mins[0]) * t)]


'''
plot the grid describing a surface given by an analytical expression
- 'ax' : the axis where the plot will be made
- 'f': the analytical expression for the surface f(x,y)
- 'mins', 'maxs': limits of the rectangular region where 'f' will be plotted
- 'color': the color of the gird
- 'z_order' : the z-order of the grid
- 'mask': a mask which defines a region where the grid will not be plotted. The mask may be genereated with mask.grid_mask_disk
Return vallues: 
- 'curves': a list containig the curves of the grid 
'''


def plot_analytical_grid(ax, f, mins, maxs, n_curves, n_bins, color, line_width, z_order, mask):
    X = np.mgrid[mins[0]:maxs[0]:n_curves[0] * 1j]
    Y = np.mgrid[mins[1]:maxs[1]:n_curves[1] * 1j]

    curves = []

    for i in range(len(X)):
        # curve_mask = mask.curve_mask_disk(lambda t: gamma_y(t, mins, maxs, f, x), 0, 1, r, cr, n_bins_curve)

        # plot a curve which runs along the y axis
        curves.append(plot_analytical_curve(ax,
                                            lambda t: gamma_y(t, mins, maxs, f, X[i]),
                                            0, 1, n_bins, color, '', z_order, line_width,
                                            mask[0][i]
                                            ))

    for i in range(len(Y)):
        # plot a curve which runs along the x axis
        curves.append(plot_analytical_curve(ax,
                                            lambda t: gamma_x(t, mins, maxs, f, Y[i]),
                                            0, 1, n_bins, color, '', z_order, line_width,
                                            mask[1][i]
                                            ))

    return curves


'''
plot a point 
- 'ax' : the axis where the point will be plotted
- 'r' :the point coordinates
- 'color' : the point color
- 'point_size' : the size of the point
- 'legend': the legend of the point
- 'z_order' : the z_order of the point

Return values: 
- 'point': the point 
'''


def plot_point(ax, r, color, point_size, legend, legend_position, legend_font_size, z_order):
    point = ax.plot(r[0], r[1], r[2], 'o', color=color, zorder=z_order, label=legend, markersize=point_size)
    legend = ax.legend(handles=[ax.lines[-1]], loc="upper left",
                       bbox_to_anchor=(legend_position[0], legend_position[1]), frameon=False,
                       fontsize=legend_font_size)
    ax.add_artist(legend)

    return point, legend


'''
tabulate a curve
- 'f': the analytical function desccribing the curve: f(t) = (x(t), y(t), z(t))
- 't_min', 't_max', the minimum and maximum values of the curve parameter t
- 'n_bins': the nunber of bins in which the interval [t_min, t_max] will be divided

Return values:
- the tables of the coordinates [x,y,z] of the curve 

'''


def tabulate_analytical_curve(f, t_min, t_max, n_bins, mask=None):
    t = np.mgrid[t_min:t_max:n_bins * 1j]

    X, Y, Z = [], [], []

    for tau in t:
        X.append(f(tau)[0])
        Y.append(f(tau)[1])
        Z.append(f(tau)[2])

    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)

    if mask is not None:
        X[~mask] = np.nan
        Y[~mask] = np.nan
        Z[~mask] = np.nan

    return X, Y, Z, t


'''
plot a curve defined by an analytical function
- 'ax' : the axes where the plot will be made
- 'f' : the parametric function f(t) = (x(t), y(t), z(t)) of the curve
- 't_min', 't_max', the minimum and maximum values of the curve parameter t
- 'n_bins': the nunber of bins in which the interval will be divided
- 'color': the color of the curve
- 'z_order': the z-order of the curve
- 'line_width': the linewidth of the curve

Return values :
the plotted curve

'''


def plot_analytical_curve(ax, f, t_min, t_max, n_bins, color, legend, z_order, line_width, mask=None, style=None, alpha=None):
    X, Y, Z, t = tabulate_analytical_curve(f, t_min, t_max, n_bins, mask)
    if style is None:
        curve = ax.plot(X, Y, Z, color=color, zorder=z_order, linewidth=line_width, label=legend, alpha=alpha)
    else:
        curve = ax.plot(X, Y, Z, color=color, zorder=z_order, linewidth=line_width, label=legend, linestyle=style, alpha=alpha)

    return curve


def plot_analytical_curve_with_legend(ax, f, t_min, t_max, n_bins, color, label, legend_position, label_font_size,
                                      z_order, line_width, style=None):
    curve = plot_analytical_curve(ax, f, t_min, t_max, n_bins, color, label, z_order, line_width, None, style)
    legend = ax.legend(handles=[ax.lines[-1]], loc="upper left",
                       bbox_to_anchor=(legend_position[0], legend_position[1]), frameon=False,
                       fontsize=label_font_size)
    ax.add_artist(legend)

    return curve, legend


'''
plot an analytical curve by loading the symbol of its legend from a pdf file
- 'ax' : the axes where the plot will be made
- 'f' : the parametric function f(t) = x(t) of the curve
- 't_min', 't_max', the minimum and maximum values of the curve parameter t
- 'n_bins': the nunber of bins in which the interval [  't_min', 't_max' ] will be divided
- 'color': the color of the curve
- 'legend': the name of the symbol which will be loaded from the pdf file
- 'legend_position': the position of the legend of the curve
- 'z_order': the z-order of the curve
- 'line_width': the linewidth of the curve
- 'zoom': the zoom factor of the image loaded from pdf file (it sets the image size)
- 'dpi': the dpi of the image loaded from pdf file (it sets the image resolution)

'''


def plot_analytical_curve_with_legend_pdf_image(ax, f, t_min, t_max, n_bins, color, legend, legend_position,
                                                z_order, line_width, zoom, box_alignment, dpi, style=None):
    plot_analytical_curve_with_legend(ax, f, t_min, t_max, n_bins, color, r' ', legend_position, 0, z_order, line_width, style)
    images.import_pdf_image(legend + '.pdf', zoom, legend_position, box_alignment, dpi, ax)


'''
tabulate a circle:
- 'r' circle radius
- 'c_r' circle center
Return values:
- 'X', 'Y', grid of the points describing the circle

'''


def tabulate_cicle(r, cr):
    theta = np.mgrid[0:2 * (np.pi):100j]
    X = cr[0] + r * np.cos(theta)
    Y = cr[1] + r * np.sin(theta)

    return X, Y


'''
tabulate a line 
- 'p_start', 'p_end': coordinates of the start and end points
Return values:
- 'X', 'Y', grid of the points describing the line
'''


def tabulate_line(p_start, p_end):
    t = np.mgrid[0:1:100j]
    X = p_start[0] + (p_end[0] - p_start[0]) * t
    Y = p_start[1] + (p_end[1] - p_start[1]) * t

    return X, Y


# empties x, y and z panel of axis 'ax'
def empty_panes(ax):
    ax.xaxis.pane.fill = False  # Left pane
    ax.yaxis.pane.fill = False  # Right pane
    ax.zaxis.pane.fill = False  # Bottom pane


# set the ticks of colorbar 'colorar' equal to the vector of ticks values 'ticks'
def set_colorbar_ticks(colorbar, ticks, min, scale_factor, font_size):
    latex_ticks = []
    for tick in ticks:
        latex_ticks.append(to_latex_scientific(min + (tick - min) / scale_factor))

    colorbar.set_ticks(ticks)
    colorbar.ax.set_yticklabels(latex_ticks, fontsize=font_size)


# convert a floating-point number 'x' in scientific format and return the related string in latex format
def to_latex_scientific(x):
    formatted = "{:.1e}".format(x)  # Convert to scientific notation with 3 significant figures
    base, exponent = formatted.split("e")  # Split into base and exponent

    base = float(base)  # Convert base to float to check if it's an integer
    exponent = int(exponent)  # Convert exponent to integer to remove leading zeros

    # Convert base to int if it is a whole number
    base_is_integer = base.is_integer()
    if base_is_integer:
        base = int(base)

    if x != 0:
        if exponent == 0:
            result = r"${}$".format(base)
        else:
            if base_is_integer and (np.abs(base) == 1):
                if base == 1:
                    result = r"$10^{{{}}}$".format(exponent)
                elif base == -1:
                    result = r"$-10^{{{}}}$".format(exponent)
            else:
                result = r"${} \times 10^{{{}}}$".format(base, exponent)

    else:
        result = r"$0$"
    return result


def floor_base_10(x):
    if x > 0:
        return (10.0 ** (np.floor(np.log10(x))))
    elif x < 0:
        return (- 10.0 ** (np.ceil(np.log10(-x))))
    elif x == 0:
        return 0


def ceil_base_10(x):
    if x > 0:
        return (10.0 ** (np.ceil(np.log10(x))))
    elif x < 0:
        return (- 10.0 ** (np.floor(np.log10(-x))))
    elif x == 0:
        return 0


# remove some elements in 'list' in such a way that 'list' has no more than 'n' elements and return the result
def purge_list(list, n):
    i = 0
    result = []
    for element in list:
        if ((i % np.rint(len(list) / n)) == 0):
            result.append(element)
        i += 1

    return result


# create a list of ticks on a 'base 10 ' grid between 'min' and 'max'
def ticks_base_10(min, max, n):
    # increment
    delta = 10 ** np.floor(np.log10(np.max([np.abs(max), np.abs(min)])))

    # set the list of ticks to a preliminary list containing only the lowest and highest values
    ticks = [ceil_base_10(min), floor_base_10(max)]

    if np.abs(max) > np.abs(min):

        x = ceil_base_10(max)
        while x > min:
            if x < max:
                ticks.append(x)
            x -= delta

        ticks.sort()

    else:

        x = floor_base_10(min)
        while x < max:
            if x > min:
                ticks.append(x)
            x += delta

        ticks.sort()

    result = purge_list(ticks, n)

    return list(dict.fromkeys(result))


'''
plot a pair of 2d axes in 'ax' with origin at [origin[0], origin[1]], lengths 'lengths[0]' and 'lengths[1]' and scale factor 'scale_factor_x' and 'scale_factors[1]'.
the offset on axes are relative to the axes' lengths
'''


def plot_2d_axes(ax, origin, lengths, \
                 tick_length_x, tick_length_y, line_width, \
                 axis_label_x, axis_label_y, axis_label_angle_x, axis_label_angle_y, \
                 axis_label_offset_x, axis_label_offset_y, ticks_label_offset_x, ticks_label_offset_y,
                 ticks_label_format_x, ticks_label_format_y, \
                 font_size, z_order):
    ax.set(xlim=[origin[0] - epsilon, origin[0] + lengths[0] + epsilon], \
           ylim=[origin[1] - epsilon, origin[1] + lengths[1] + epsilon])

    # plot the x axis
    plot_2d_axis(ax, origin, lengths[0], "x", tick_length_x * lengths[1], line_width, \
                 axis_label_x, axis_label_offset_x * lengths[1], axis_label_angle_x, ticks_label_offset_x * lengths[1],
                 ticks_label_format_x, font_size, z_order)

    # plot the y axis
    plot_2d_axis(ax, origin, lengths[1], "y", tick_length_y * lengths[0], line_width, \
                 axis_label_y, axis_label_offset_y * lengths[0], axis_label_angle_y, ticks_label_offset_y * lengths[0],
                 ticks_label_format_y, font_size, z_order)


# call plot_2d_axes and draw on top of the axes a plot label 'plot_label' on the top-left corner of the plot,  whose relative displacement with respect to the plot dimensions is plot_label_offset
def plot_2d_axes_label(ax, origin, lengths,
                       tick_length_x, tick_length_y, line_width, \
                       axis_label_x, axis_label_y, axis_label_angle_x, axis_label_angle_y, \
                       axis_label_offset_x, axis_label_offset_y, ticks_label_offset_x, ticks_label_offset_y,
                       ticks_label_format_x, ticks_label_format_y, \
                       panel_label_font_size, font_size, z_order, plot_label, plot_label_offset):
    # plot the axes
    plot_2d_axes(ax, origin, lengths, \
                 tick_length_x, tick_length_y, line_width, \
                 axis_label_x, axis_label_y, axis_label_angle_x, axis_label_angle_y, \
                 axis_label_offset_x, axis_label_offset_y, ticks_label_offset_x, ticks_label_offset_y,
                 ticks_label_format_x, ticks_label_format_y, \
                 font_size, z_order)

    # draw the panel label
    ax.text(origin[0] - plot_label_offset[0] * lengths[0], origin[1] + lengths[1] + plot_label_offset[1] * lengths[1],
            plot_label, fontsize=panel_label_font_size, ha='center', va='center',
            zorder=z_order)


# scale up by 'scale_factor' the scalar 'x' with respect to the reference value 'min'
def scale(x, min, scale_factor):
    return min + (x - min) * scale_factor


# scale up by 'scale_factors' the list 'v' with respect to the reference values 'mins'
def scale_list(v, mins, scale_factors):
    return [scale(v[i], mins[i], scale_factors[i]) for i in range(len(mins))]


'''
plot a surface from the data in 'X', 'Y' and 'grid', with colormap 'color_map', with surface stride 'stride_surface' and opacity 'alpha_surface' 
Plot  a grid on top of the surface with the same data, stride 'stride_grid' and line_width 'line_width_grid' 
the surface and the surface grid are returned 
'''


def plot_surface_grid(ax, X, Y, Z, color_map, surface_stride, grid_stride, surface_alpha, line_width_grid):
    surface_grid = ax.plot_surface(X, Y, Z,
                                   edgecolor='black',
                                   rstride=grid_stride,
                                   cstride=grid_stride,
                                   alpha=0,
                                   linewidth=line_width_grid,
                                   shade=False
                                   )
    surface_grid.set_facecolor((0, 0, 0, 0))  # RGBA with alpha=0 (fully transparent)

    if (len(color_map) != 0):
        surface = ax.plot_surface(X, Y, Z,
                                  facecolors=color_map,
                                  edgecolor='black',
                                  rstride=surface_stride,
                                  cstride=surface_stride,
                                  alpha=surface_alpha,
                                  linewidth=0,
                                  shade=False)
    else:
        surface = ax.plot_surface(X, Y, Z,
                                  color='gray',
                                  edgecolor='black',
                                  rstride=surface_stride,
                                  cstride=surface_stride,
                                  alpha=surface_alpha,
                                  linewidth=0,
                                  shade=False
                                  )

    return (surface, surface_grid)


def set_axes_limits(ax, mins, maxs):
    lengths = np.subtract(maxs, mins)

    ax.set( \
        xlim=[mins[0] - epsilon_axes * lengths[0], maxs[0] + epsilon_axes * lengths[0]], \
        ylim=[mins[1] - epsilon_axes * lengths[1], maxs[1] + epsilon_axes * lengths[1]], \
        zlim=[mins[2] - epsilon_axes * lengths[2], maxs[2] + epsilon_axes * lengths[2]] \
        )


'''
given the upper radius of the cone 'r', the intervals for the z axis 'z_min', 'z_max' and the z-value 'z_circle' where one wants to put the upper ring of the cone,
return the parameters for a cone: r_A_cone, r_B_cone, z_A_cone, z_B_cone, 
'''


def set_cone(r, z_circle, z_min, z_max, scale_factor_z, height_fraction, omega_circle_const):
    # here z_A_cone > z_B_cone
    z_A_cone = scale(z_circle, z_min, scale_factor_z)
    r_A_cone = r

    # this sets the height of the cone
    z_B_cone = z_A_cone - (z_max - z_min) * scale_factor_z * height_fraction
    # the lower radius of the cone is set by the condition that the membrane is orthogonal to the cone at the membrane-cone junction
    r_B_cone = r_A_cone + (z_B_cone - z_A_cone) / omega_circle_const

    return r_A_cone, r_B_cone, z_A_cone, z_B_cone


'''
give the radius 'r' of the cylinder, the heights   'z_top' ('z_bottom') of the top (bottom) face, the min value for the z axis 'z_min' and the scale factor 'scale_factor' for the z axis,
return the cylinder parametrers z_A (z-value of the top face), z_B (z-value of the bottom face)
'''


def set_cylinder(r, z_top, z_bottom, z_min, scale_factor_z):
    # here z_A > z_B
    z_A = scale(z_top, z_min, scale_factor_z)
    z_B = scale(z_bottom, z_min, scale_factor_z)

    return z_A, z_B


# plot a line fom point 'r_start' to point 'r_end' by stretching it by the vector 'scale_factor' in each respective direction
def plot_line_scaled(ax, r_start, r_end, length, mins, scale_factors, line_width, color, alpha, z_order):
    r_start_scaled = scale_list(r_start, mins, scale_factors)
    r_end_scaled = scale_list(r_end, mins, scale_factors)

    dr_scaled = np.subtract(r_end_scaled, r_start_scaled)

    norm_dr_scaled = np.sqrt(np.dot(dr_scaled, dr_scaled))
    r_end_scaled = r_start_scaled + dr_scaled / norm_dr_scaled * length

    r_start_end = list(zip(r_start_scaled, r_end_scaled))

    ax.plot(r_start_end[0], r_start_end[1], r_start_end[2],
            color=color, linewidth=line_width, alpha=alpha, zorder=z_order)


'''
plot an arrow head, where 'arrow_shaft_start' is the start position of the shaft, 'arrow_shaft_end' is the end position of the shaft, 'arrow_shaft_length" is the length of the shaft
'dr_arrow_head' is the increment leading from the end of the shaft to the enf of the arrow head
'arrow_head_length' is the length of the arrow head
'''


def plot_arrow_head(ax, arrow_shaft_start, arrow_shaft_end, arrow_shaft_length, dr_arrow_head, arrow_head_length, mins,
                    scale_factors, line_width, color, alpha, z_order):
    # compute arrow_head_start_scaled = arrow_shaft_end_scaled
    arrow_shaft_start_scaled = scale_list(arrow_shaft_start, mins, scale_factors)
    arrow_shaft_end_scaled = scale_list(arrow_shaft_end, mins, scale_factors)

    dr_shaft_scaled = np.subtract(arrow_shaft_end_scaled, arrow_shaft_start_scaled)

    norm_dr_shaft_scaled = np.sqrt(np.dot(dr_shaft_scaled, dr_shaft_scaled))
    arrow_shaft_end_scaled = arrow_shaft_start_scaled + dr_shaft_scaled / norm_dr_shaft_scaled * arrow_shaft_length

    arrow_head_start_scaled = arrow_shaft_end_scaled
    '''
    arrow_head_end_scaled lives in a space which is not dilated accoriding to scale_factors: 
    it is thus simply arrow_head_start_scaled + dr_arrow_head [non-scaled and dilated to obtain the correct length of the arrow head]
    '''
    arrow_head_end_scaled = np.add(arrow_head_start_scaled,
                                   dr_arrow_head / np.sqrt(np.dot(dr_arrow_head, dr_arrow_head)) * arrow_head_length)

    arrow_head_start_end = list(zip(arrow_head_start_scaled, arrow_head_end_scaled))

    ax.plot(arrow_head_start_end[0], arrow_head_start_end[1], arrow_head_start_end[2],
            color=color, linewidth=line_width, alpha=alpha, zorder=z_order)


# rotation matrix about the y axis by an angle theta, theta > 0 corresponds to a rotation in counter-clock wise sense as seen from the tip of the arrow of the y axis
def R_y(theta):
    return [[np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]]


# rotation matrix about the z axis by an angle theta, theta > 0 corresponds to a rotation in counter-clock wise sense as seen from the tip of the arrow of the z axis
def R_z(theta):
    return [[np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]]


# rotation matrix about the z axis by an angle theta for 2d vectors, theta > 0 corresponds to a rotation in counter-clock wise sense as seen from the tip of the arrow of the z axis
def R_2d(theta):
    return [[np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]]


# rotation corresponding to the polar angles theta, phi
def R(theta, phi):
    return np.matmul(R_z(phi), R_y(theta))


'''
plot an arrow 
- 'ax': the axis
- 'shaft_start_position', 'shaft_end_position': the coordinates of the start and end of the shaft of the arrow
- 'shaft_length': all arrows will be renormalized and plotted with a length equal to 'shaft_length'
- 'head_over_shaft_length' : ratio between the lenght of each arrow head and the length of the shaft 
- 'head_angle': angle (in degrees) between each arrow head and the shaft
- 'mins': vector of minima in 3d space with respect to which the rescaling of scale_factor will be made
- 'scale_factor': scaling coefficients with respect to 'mins'
- 'threshold_arrow_length": an argument which sets the minimal arrow lenght that will be plotted, only arrows |r_end - r_start| > threshold_arrow_length will be plotted 
- 'line_width': line width for shaft and arrow heads
- 'color': the color
- 'alpha': transparency
- 'z_order': the z-order
'''


def plot_arrow(ax, shaft_start_position, shaft_end_position, shaft_length, head_over_shaft_length, head_angle, mins,
               scale_factors, threshold_arrow_length, line_width, color, alpha, z_order):
    head_length = head_over_shaft_length * shaft_length

    # plot the shaft
    shaft_start_position_scaled = scale_list(shaft_start_position, mins, scale_factors)
    shaft_end_position_scaled = scale_list(shaft_end_position, mins, scale_factors)
    dr_shaft_scaled = np.subtract(shaft_end_position_scaled, shaft_start_position_scaled)

    dr_shaft = np.subtract(shaft_end_position, shaft_start_position)

    if (np.sqrt(np.dot(dr_shaft, dr_shaft)) > threshold_arrow_length):
        dr_shaft = dr_shaft * shaft_length / np.sqrt(np.dot(dr_shaft, dr_shaft))

        shaft_end_position = np.add(shaft_start_position, dr_shaft)
        # arrow_head_start = arrow_shaft_end

        plot_line_scaled(ax, shaft_start_position, shaft_end_position, shaft_length, mins, scale_factors, line_width,
                         color,
                         alpha, z_order)

        theta_shaft = np.arccos(dr_shaft_scaled[2] / np.sqrt(np.dot(dr_shaft_scaled, dr_shaft_scaled)))
        phi_shaft = np.arctan2(dr_shaft_scaled[1], dr_shaft_scaled[0])

        # compute coordinates for arrow heads
        up_head = [-head_length * np.sin(head_angle * deg_to_rad), 0, -head_length * np.cos(head_angle * deg_to_rad)]
        down_head = [+head_length * np.sin(head_angle * deg_to_rad), 0, - head_length * np.cos(head_angle * deg_to_rad)]
        up_head = np.matmul(R(theta_shaft, phi_shaft), up_head)
        down_head = np.matmul(R(theta_shaft, phi_shaft), down_head)

        # plot the arrow heads
        plot_arrow_head(ax, shaft_start_position, shaft_end_position, shaft_length, up_head, head_length, mins,
                        scale_factors, line_width, color, alpha, z_order)
        plot_arrow_head(ax, shaft_start_position, shaft_end_position, shaft_length, down_head, head_length, mins,
                        scale_factors, line_width, color, alpha, z_order)


'''
plot a 2d arrow

'''


def plot_2d_arrow(ax, shaft_start_position, shaft_end_position, shaft_length, head_over_shaft_length, head_angle, line_width, color, alpha, z_order):
    head_length = head_over_shaft_length * shaft_length

    # plot the shaft
    dr_shaft = np.subtract(shaft_end_position, shaft_start_position)

    if (np.sqrt(np.dot(dr_shaft, dr_shaft)) > threshold_arrow_length):
        dr_shaft = dr_shaft * shaft_length / np.sqrt(np.dot(dr_shaft, dr_shaft))

        ax.plot([shaft_start_position[0], shaft_start_position[0] + dr_shaft[0]], [shaft_start_position[1], shaft_start_position[1] + dr_shaft[1]], color=color, linewidth=line_width, alpha=alpha, zorder=z_order)

        theta_shaft = -np.pi / 2 + math.atan2(dr_shaft[1], dr_shaft[0])

        # plot the heads
        # consider heads related to a ficititious arrow pointing up
        up_head = [-head_length * np.sin(head_angle * deg_to_rad), -head_length * np.cos(head_angle * deg_to_rad)]
        down_head = [+head_length * np.sin(head_angle * deg_to_rad), - head_length * np.cos(head_angle * deg_to_rad)]
        # rotate the heads above
        up_head = np.matmul(R_2d(theta_shaft), up_head)
        down_head = np.matmul(R_2d(theta_shaft), down_head)

        # plot the heads
        ax.plot([shaft_start_position[0] + dr_shaft[0], shaft_start_position[0] + dr_shaft[0] + up_head[0]], [shaft_start_position[1] + dr_shaft[1], shaft_start_position[1] + dr_shaft[1] + up_head[1]], color=color, linewidth=line_width, alpha=alpha, zorder=z_order)
        ax.plot([shaft_start_position[0] + dr_shaft[0], shaft_start_position[0] + dr_shaft[0] + down_head[0]], [shaft_start_position[1] + dr_shaft[1], shaft_start_position[1] + dr_shaft[1] + down_head[1]], color=color, linewidth=line_width, alpha=alpha, zorder=z_order)


'''
remove axis 'axis'
'''


def remove_axis(axis):
    axis.clear()
    axis.set_axis_off()
    axis.remove()  # This removes it from the figure entirely


'''
remove all axes in figure 'fig'
'''


def remove_all_axes(fig):
    axes = fig.get_axes()
    for axis in axes:
        remove_axis(axis)


'''
delete all axes of a figure: unlike 'remove_all_axes', this method uses 'delaxes' to remove the axes
Input values: 
- 'fig': the figure whose axes will be rewmoved
'''
def delete_all_axes(fig):
    for ax in fig.axes[:]:
        fig.delaxes(ax)

'''
interpolate a set of discrete data for a surface f(x,y) into a grid points
- 'data': the data containing the values of x, y and f(x,y)
- 'mins', 'maxs' the bounds of the region where the interpolation should be made
- 'n_bins' the number of bins (for x and y, in each entry) in which the intervals given by 'mins' and 'maxs' should be divided
- 'scale_factor': the scale factor for the field f
- 'label_x_column' ... the labels for x, y, and f in 'data'
'''


def interpolate_surface(data, mins, maxs, f_min, n_bins, scale_factor, label_x_column, label_y_column, label_f_column):
    X, Y = np.meshgrid(np.linspace(mins[0], maxs[0], n_bins[0]), np.linspace(mins[1], maxs[1], n_bins[1]),
                       indexing='ij')
    # f_min = np.min(data[label_f_column])

    # 1. re-arrange the x, y values into a points
    points = []
    points.extend([list(element) for element in zip(data[label_x_column], data[label_y_column])])
    # 2 re-arrange the function  values into values
    values = data[label_f_column].apply(lambda x: scale(x, f_min, scale_factor))
    # 3 interpolate values and points, and write the result of the interpolated function on the lattice (X, Y) into grid
    Z = griddata(points, values, (X, Y), method='cubic')

    return X, Y, Z


'''
set the limits of a 2d axis:
- 'ax' the axis where to set the limits
- 'mins' the min value for the x axis (min[0]) and for the y axis (min[1])
- 'maxs' the max value for the x axis (max[0]) and for the y axis (max[1])
- 'margins' the margin, relative to max-min, which will be included in the axes limits to enlarge them
'''


def set_2d_axes_limits(ax, mins, maxs, margins):
    ax.set_xlim(mins[0] - (maxs[0] - mins[0]) * margins[0], maxs[0] + (maxs[0] - mins[0]) * margins[0])
    ax.set_ylim(mins[1] - (maxs[1] - mins[1]) * margins[1], maxs[1] + (maxs[1] - mins[1]) * margins[1])


'''
compute the min and max values occurring in column 'column_name' of csv file 'file_name', where 'file_name' contains the set of columns 'columns_name'
'''


def min_max_file(file_name, columns_name, column_name):
    data = pd.read_csv(file_name, usecols=columns_name)

    min = np.min(data[column_name])
    max = np.max(data[column_name])

    return min, max


def min_max_files(file_name, file_path, columns_name, column_name, n_file_min, n_file_max, n_file_stride):
    abs_min, abs_max = min_max_file(file_path + file_name + str(n_file_min) + '.csv', columns_name, column_name)

    for i in range(n_file_min + 1, n_file_max + 1, n_file_stride):

        min, max = min_max_file(file_path + file_name + str(i) + '.csv', columns_name, column_name)

        if min < abs_min:
            abs_min = min

        if max > abs_max:
            abs_max = max

    return abs_min, abs_max


def min_max_file_list(file_name, file_path, columns_name, column_name, n_file_list):
    abs_min, abs_max = min_max_file(file_path + file_name + str(n_file_list[0]) + '.csv', columns_name, column_name)

    for n_file in n_file_list:

        min, max = min_max_file(file_path + file_name + str(n_file) + '.csv', columns_name, column_name)

        if min < abs_min:
            abs_min = min

        if max > abs_max:
            abs_max = max

    return abs_min, abs_max


'''
plot a line
- 'ax' the axis where to plot the line
- 'p_start', 'p_end' the start and end points of the line
- 'color' the color of the line
- 'line_width' the linewidth  of the line
- 'z_order' the z_order of the line
'''


def plot_line(ax, p_start, p_end, color, line_width, z_order):
    X, Y = tabulate_line(p_start, p_end)
    line = ax.plot(X, Y, color=color, zorder=z_order, linewidth=line_width)

    return line


'''
plot a circle: 
- 'ax' the axis where to plot the circle
- 'r' the radius of the circle
- 'c_r' : the center of the circle
- 'line_width' : the line width of the circle
- 'z_order' the z_order of the circle
'''


def plot_circle(ax, r, cr, color, line_width, z_order):
    X, Y = tabulate_cicle(r, cr)
    circle = ax.plot(X, Y, color=color, zorder=z_order, linewidth=line_width)

    return circle


'''
plot a rectangle
- 'ax' the axis where to plot the rectangle
- 'p_left_bottom' the left bottom point of the rectangle
- 'L', 'h' : width and height of the rectangle
- 'color': the color of the rectangle
- 'line_width' : the line width of the rectangle
- 'z_order' the z_order of the rectangle

Return values:
- 'rectangle': a list of the rectangle segments
'''


def plot_rectangle(ax, p_left_bottom, L, h, color, line_width, z_order):
    rectangle = []

    rectangle.append(plot_line(ax, p_left_bottom, np.add(p_left_bottom, [L, 0, 0]), color, line_width, z_order))
    rectangle.append(
        plot_line(ax, np.add(p_left_bottom, [L, 0, 0]), np.add(p_left_bottom, [L, h, 0]), color, line_width, z_order))
    rectangle.append(
        plot_line(ax, np.add(p_left_bottom, [L, h, 0]), np.add(p_left_bottom, [0, h, 0]), color, line_width, z_order))
    rectangle.append(
        plot_line(ax, np.add(p_left_bottom, [0, h, 0]), np.add(p_left_bottom, p_left_bottom), color, line_width,
                  z_order))

    return rectangle


'''
plot a mesh by drawing its edges
Input values
- 'data_line_vertices': the data containing the coordinates of the lines which connect the vertices, as generated, for example, from 
'data_line_vertices = pd.read_csv(mesh_path + "line_vertices.csv", usecols=columns_line_vertices)'
- 'line_width': the width of the mesh edges lines
- 'color': the color of the mesh edges lines
- 'alpha': the opacity with which the lines will be plotted
'''


def plot_mesh(data_line_vertices, line_width, color, alpha):
    points_start = []
    points_end = []
    points_start.extend([list(a) for a in
                         zip(data_line_vertices[clab.label_start_x_column], data_line_vertices[clab.label_start_y_column],
                             data_line_vertices[clab.label_start_z_column])])
    points_end.extend(
        [list(a) for a in zip(data_line_vertices[clab.label_end_x_column], data_line_vertices[clab.label_end_y_column],
                              data_line_vertices[clab.label_end_z_column])])

    for i in range(len(points_start)):
        plt.plot([points_start[i][0], points_end[i][0]], [points_start[i][1], points_end[i][1]],
                 [points_start[i][2], points_end[i][2]], linewidth=line_width, color=color, alpha=alpha)


def plot_2d_mesh(ax, data_line_vertices, line_width, color, alpha):
    points_start = []
    points_end = []
    points_start.extend([list(a) for a in
                         zip(data_line_vertices[clab.label_start_x_column], data_line_vertices[clab.label_start_y_column],
                             data_line_vertices[clab.label_start_z_column])])
    points_end.extend(
        [list(a) for a in zip(data_line_vertices[clab.label_end_x_column], data_line_vertices[clab.label_end_y_column],
                              data_line_vertices[clab.label_end_z_column])])

    for i in range(len(points_start)):
        ax.plot([points_start[i][0], points_end[i][0]], [points_start[i][1], points_end[i][1]], linewidth=line_width, color=color, alpha=alpha)
