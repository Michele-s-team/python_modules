import numpy as np
import matplotlib.pyplot as plt

import constants.utils as const
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
        - 'shrink_value' [optional] : the shrink value of the colorbar
        - 'aspect_value' [optional]: the aspect value of the colorbar
        - 'tick_label_angle' [optional]: the rotation angle of the tick labels
'''

def make_colorbar(figure, grid_values, min_value, max_value, position, size, 
                  scale_factor=1,
                  label = None, 
                  font_size = const.default_font_size, 
                  label_angle=90, 
                  label_pad=[0, 0], 
                  shrink_value=const.colorbar_shrink_value, 
                  aspect_value=const.colorbar_aspect_value, 
                  tick_label_angle=0,
                  tick_length=const.default_tick_length,
                  tick_label_offset=[0, 0],
                  line_width=const.default_line_width):
    
    scaled_max = gr.scale(max_value, min_value, scale_factor)
    
    colorbar_ticks = ticks.generate_ticks(min_value, scaled_max)
    
    color_normalization = plt.Normalize(vmin=min_value, vmax=scaled_max)  # Use max_value, not scaled_max!
    color_map = color_map_type(color_normalization(grid_values))

    mappable = plt.cm.ScalarMappable(cmap=color_map_type, norm=color_normalization)
    mappable.set_array(grid_values)

    colorbar_position = figure.add_axes([position[0], position[1], size[0], size[1]])
    colorbar = figure.colorbar(mappable, shrink=shrink_value, aspect=aspect_value, location='left', cax=colorbar_position)
    
    gr.set_colorbar_ticks(colorbar, colorbar_ticks, min_value, scale_factor, font_size, tick_label_angle,
                          tick_length=tick_length,
                          tick_label_offset=tick_label_offset,
                          line_width=line_width)
    
    
    colorbar.set_label(label, rotation=label_angle, fontsize=font_size)

    # colorbar.ax.yaxis.label.set_position((label_pad[0], label_pad[1]))  # Adjust y-value to fine-tune
    colorbar.ax.yaxis.set_label_coords(label_pad[0], label_pad[1])  # Adjust -1.2 for spacing
    colorbar.ax.set_label("colorbar")  # Tag this axis for future deletion, if needed

    return color_map

'''
create a colorbar for a curve, by plotting the value of a field along the curve in terms of a color map
Input values: 
- 'figure' : the figure where the colorbar is made
- 't_values': a list with the grid of the values of the parametric coordinate t which parametrizes the curve
- 'f_values': a dataframe with the values of the field f along the curve
- 'min_max' [optional]: a list with two entries, the min and max of the values which will bound the color bar. If none, this method will compute the min and max values of the field f along the curve and assign them to min_max
- 'position': position of the colorbar
- 'size': size of the colorbar
- 'angle' : rotation angle of the colorbar
- 'label_pad': displacement of the label of the colorbar
- 'label' the label of the colorbar
- 'font_size' : the font size of all texts in the colorbar
'''

def make_curve_colorbar(figure, t_values, f_values,  
                        position, size, angle, label_pad, label, font_size, min_max=None):
    

    if min_max is None: 
        min_max = [np.min(f_values['f']), np.max(f_values['f'])]

    colorbar_ticks = ticks.generate_ticks(min_max[0], min_max[1])

    
    f_interpolated = interp1d(f_values[":0"].values, f_values["f"].values, kind='cubic', fill_value='extrapolate')

    color_normalization = plt.Normalize(vmin=min(colorbar_ticks), vmax=max(colorbar_ticks))

    mappable = plt.cm.ScalarMappable(cmap=color_map_type, norm=color_normalization)
    
    field_values = f_values['f'].values[::-1]  # Extract just the 'f' column
    field_values = f_interpolated(t_values)
    
    mappable.set_array(field_values)
    color_map = color_map_type(color_normalization(field_values))


    colorbar_position = figure.add_axes([position[0], position[1], size[0], size[1]])
    colorbar = figure.colorbar(mappable, shrink=0.2, aspect=10, location='left', cax=colorbar_position)
    gr.set_colorbar_ticks(colorbar, colorbar_ticks, min_max[0], 1, font_size)
    colorbar.set_label(label, rotation=angle, fontsize=font_size)

    # colorbar.ax.yaxis.label.set_position((label_pad[0], label_pad[1]))  # Adjust y-value to fine-tune
    colorbar.ax.yaxis.set_label_coords(label_pad[0], label_pad[1])  # Adjust -1.2 for spacing
    colorbar.ax.set_label("colorbar")  # Tag this axis for future deletion, if needed

    return color_map


