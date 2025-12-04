import numpy as np
import matplotlib.pyplot as plt

import constants.utils as const
import graphics.color_bar as cb
import graphics.utils as gr
import graphics.ticks as ticks
from scipy.interpolate import interp1d

color_map_type = plt.cm.get_cmap(
    'jet')  # 'plasma' or 'viridis'values_sigma = data_sigma[label_sigma_column].apply( lambda x: gr.scale( x, sigma_min, scale_factor_sigma ) )

'''
make a color bar and return the relative color map. 
Arguments:
    * Mandatory
        - 'figure' : the figure where the colorbar is made
        - 'grid_values' the grid values of the field over which the color bar is made
        - 'min_value', 'max_value' the minimal , maximal value of the field above
        - 'position': position of the colorbar
    * Optional:
        - 'scale_factor': the scale_factor of the field above with respect to 'min'
        - 'label': the label of the color bar
        - 'font_size' : the font size of all texts in the colorbar
        - 'label_angle' the label of the colorbar
        - 'label_pad': displacement of the label of the colorbar with respect to the origin of the colorbar, in units given by the size of the colorbar
        - 'shrink_value'  : the shrink value of the colorbar
        - 'aspect_value' : the aspect value of the colorbar
        - 'tick_label_angle' : the rotation angle of the tick labels
        - 'custom_ticks': a list of custom ticks for the colorbar
        - 'tick_label_format': the format in which the tick labels will be displayed, e.g., 'e' or 'f'
'''


def make_colorbar(figure, grid_values, min_value, max_value, position, size,
                  scale_factor=1,
                  label=None,
                  font_size=const.default_font_size,
                  label_angle=90,
                  label_pad=[0, 0],
                  shrink_value=const.colorbar_shrink_value,
                  aspect_value=const.colorbar_aspect_value,
                  tick_label_angle=0,
                  tick_length=const.default_tick_length,
                  tick_label_offset=[0, 0],
                  line_width=const.default_line_width,
                  mappable=None,
                  prune_ticks=True,
                  custom_ticks=None,
                  tick_label_format=const.default_label_format,
                  axis=None):

    # Use existing axis or create new one
    if axis is None:
        colorbar_axis = figure.add_axes(
            [position[0], position[1], size[0], size[1]])
    else:
        axis.clear()  # Clear the existing axis
        colorbar_axis = axis

    if mappable is None:
        # the user provided no map between the values of the field and the colors -> build this map.

        scaled_max = gr.scale(max_value, min_value, scale_factor)

        color_normalization = plt.Normalize(
            vmin=min_value, vmax=scaled_max)  # Use max_value, not scaled_max!
        color_map = color_map_type(color_normalization(grid_values))

        mappable = plt.cm.ScalarMappable(
            cmap=color_map_type, norm=color_normalization)
        mappable.set_array(grid_values)

    else:
        # the user provided the mappable argument, which defines min_value, max_value and color_map

        norm = mappable.norm
        min_value = norm.vmin
        max_value = norm.vmax

        color_map = mappable.cmap

        scaled_max = gr.scale(max_value, min_value, scale_factor)


    if custom_ticks == None:
        # the method has not been called with custom ticks -> generate ticks
        
        colorbar_ticks = np.asarray(ticks.generate_ticks(min_value, scaled_max))
    else:
        # the method has been called with  custom ticks -> draw the custom ticks
        
        colorbar_ticks = custom_ticks


    colorbar = figure.colorbar(mappable, 
                               shrink=shrink_value,
                               aspect=aspect_value, 
                               location='left', 
                               cax=colorbar_axis)

    # --- Remove border and outline ---
    colorbar.outline.set_visible(False)  # removes the black rectangle border
    for spine in colorbar.ax.spines.values():
        spine.set_visible(False)  # hides all spines around the colorbar axis

    gr.set_colorbar_ticks(colorbar, colorbar_ticks, min_value, scale_factor, font_size, tick_label_angle,
                          tick_length=tick_length,
                          tick_label_offset=tick_label_offset,
                          line_width=line_width,
                          tick_label_format=tick_label_format,
                          prune=prune_ticks)

    if label is not None:

        colorbar_axis.text(
            colorbar_axis.get_xlim()[0] + (0.5 - label_pad[0]) *
            (colorbar_axis.get_xlim()[1] - colorbar_axis.get_xlim()[0]),
            colorbar_axis.get_ylim()[1] + (-0.5 + label_pad[1]) *
            (colorbar_axis.get_ylim()[1] - colorbar_axis.get_ylim()[0]),
            rf'${label}$',
            fontsize=font_size,
            ha='center', va='center',
            rotation=label_angle,
            clip_on=False
        )

    # Tag this axis for future deletion, if needed
    colorbar.ax.set_label("colorbar")

    return color_map


'''
create a colorbar for a curve, by plotting the value of a field along the curve in terms of a color map
Input values: 
    * Mandatory:
        - 'figure' : the figure where the colorbar is made
        - 't_values': a list with the grid of the values of the parametric coordinate t which parametrizes the curve
        - 'f_values': a dataframe with the values of the field f along the curve
        - 'size': size of the colorbar
    * Optional:
        - 'position': position of the colorbar
        - 'angle' : rotation angle of the colorbar
        - 'label_offset': displacement of the label of the colorbar
        - 'label' the label of the colorbar
        - 'font_size' : the font size of all texts in the colorbar
        - 'min_max' [optional]: a list with two entries, the min and max of the values which will bound the color bar. If none, this method will compute the min and max values of the field f along the curve and assign them to min_max
        - 'tick_label_offset': the offset of tick labels
        - 'tick_label_format': the format with which tick labels are displayed, for example, 'e' or 'f'
        - 'tick_label_angle': the rotation angle of tick labels
        - 'tick_length': the length of the ticks
        - 'line_width': the line width for the ticks
'''


def make_curve_colorbar(figure, t_values, f_values, 
                        position=None,
                        size=None,
                        tick_label_angle=const.default_tick_label_angle,
                        label_offset=[0, 0],
                        label='',
                        font_size=const.default_font_size,
                        min_max=None,
                        tick_label_offset=[0, 0],
                        tick_label_format=const.default_label_format,
                        label_angle=0,
                        line_width=const.default_line_width,
                        tick_length=const.default_tick_length,
                        axis=None):

    # Use existing axis or create new one
    if axis is None:

        colorbar_axis = figure.add_axes()

        if position is not None:
            cb.set_position(colorbar_axis, position)
                    
        if size is not None:
            cb.set_size(colorbar_axis, size)
            
    else:
        axis.clear()  # Clear the existing axis
        colorbar_axis = axis

    if min_max is None:
        min_max = [np.min(f_values['f']), np.max(f_values['f'])]

    colorbar_ticks = ticks.generate_ticks(min_max[0], min_max[1])

    f_interpolated = interp1d(
        f_values[":0"].values, f_values["f"].values, kind='cubic', fill_value='extrapolate')

    color_normalization = plt.Normalize(vmin=min_max[0], vmax=min_max[1])

    mappable = plt.cm.ScalarMappable(
        cmap=color_map_type, norm=color_normalization)

    field_values = f_values['f'].values[::-1]  # Extract just the 'f' column
    field_values = f_interpolated(t_values)

    mappable.set_array(field_values)
    color_map = color_map_type(color_normalization(field_values))

    colorbar = figure.colorbar(
        mappable, shrink=0.2, aspect=10, location='left', cax=colorbar_axis)

    # --- Remove border and outline ---
    colorbar.outline.set_visible(False)  # removes the black rectangle border
    for spine in colorbar.ax.spines.values():
        spine.set_visible(False)  # hides all spines around the colorbar axis

    gr.set_colorbar_ticks(colorbar, colorbar_ticks, min_max[0], 1, font_size,
                          tick_label_offset=tick_label_offset,
                          tick_label_angle=tick_label_angle,
                          line_width=line_width,
                          tick_label_format=tick_label_format,
                          tick_length=tick_length)

    # colorbar.set_label(label, rotation=label_angle, fontsize=font_size)
    # colorbar.ax.yaxis.set_label_coords(label_offset[0], 0.5 + label_offset[1])  #

    if label is not None:

        colorbar_axis.text(
            colorbar_axis.get_xlim()[0] + (0.5 - label_offset[0]) *
            (colorbar_axis.get_xlim()[1] - colorbar_axis.get_xlim()[0]),
            colorbar_axis.get_ylim()[1] + (-0.5 + label_offset[1]) *
            (colorbar_axis.get_ylim()[1] - colorbar_axis.get_ylim()[0]),
            rf'${label}$',
            fontsize=font_size,
            ha='center', va='center',
            rotation=label_angle,
            clip_on=False
        )

    # Tag this axis for future deletion, if needed
    colorbar.ax.set_label("colorbar")

    return color_map

'''
set the position of a an axis
Input values:
    - 'ax': the axis
    - 'position': the position
'''
def set_position(ax, position):

    # Get current position and size
    current_position = ax.get_position()

    # Set position while keeping current size
    ax.set_position([position[0], position[1],
                    current_position.width,  current_position.height])
    

'''
Set axis size while preserving its position.

Input values: 
    - ax : matplotlib axis
    - size : the size of the axis to be set
'''
def set_size(ax, size):

    # Get current position
    current_position = ax.get_position()

    # Set size while keeping current position
    ax.set_position([current_position.x0, current_position.y0,
                     size[0], size[1]])