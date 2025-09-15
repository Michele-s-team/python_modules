import numpy as np
import matplotlib.pyplot as plt

import graph as gr
import ticks

color_map_type = plt.cm.get_cmap(
    'jet')  # 'plasma' or 'viridis'values_sigma = data_sigma[label_sigma_column].apply( lambda x: gr.scale( x, sigma_min, scale_factor_sigma ) )

'''
make a color bar and return the relative color map. 
Arguments:
- 'figure' : the figure where the colorbar is made
- 'grid_values' the grid values of the field over which the color bar is made
- 'min_value', 'max_value' the minimal , maximal value of the field above
- 'scale_factor': the scale_factor of the field above with respect to 'min'
- 'n_ticks' the number of ticks of the colorbar
- 'position': position of the colorbar
- 'size': size of the colorbar
- 'angle' : rotation angle of the colorbar
- 'label_pad': displacement of the label of the colorbar with respect to the origin of the colorbar, in units given by the size of the colorbar
- 'label' the label of the colorbar
- 'font_size' : the font size of all texts in the colorbar
'''

def make_colorbar(figure, grid_values, min_value, max_value, scale_factor,  position, size, angle, label_pad, label, font_size):

    scaled_max = gr.scale(max_value, min_value, scale_factor)
    colorbar_ticks = ticks.generate_ticks(min_value, scaled_max)
    # colorbar_ticks = np.linspace(min_value, scaled_max, num=3)  # Adjust tick count as needed

    color_normalization = plt.Normalize(vmin=min(colorbar_ticks), vmax=max(colorbar_ticks))
    color_map = color_map_type(color_normalization(grid_values))

    mappable = plt.cm.ScalarMappable(cmap=color_map_type, norm=color_normalization)
    mappable.set_array(grid_values)

    colorbar_position = figure.add_axes([position[0], position[1], size[0], size[1]])
    colorbar = figure.colorbar(mappable, shrink=0.2, aspect=10, location='left', cax=colorbar_position)
    gr.set_colorbar_ticks(colorbar, colorbar_ticks, min_value, scale_factor, font_size)
    colorbar.set_label(label, rotation=angle, fontsize=font_size)

    # colorbar.ax.yaxis.label.set_position((label_pad[0], label_pad[1]))  # Adjust y-value to fine-tune
    colorbar.ax.yaxis.set_label_coords(label_pad[0], label_pad[1])  # Adjust -1.2 for spacing
    colorbar.ax.set_label("colorbar")  # Tag this axis for future deletion, if needed

    return color_map

'''
def make_colorbar(figure, grid_values, min, max, scale_factor, n_ticks, position, size, angle, label_pad, label, font_size):

    scaled_max = gr.scale(max, min, scale_factor)

    color_normalization = plt.Normalize(vmin=min, vmax=scaled_max)
    color_map = color_map_type(color_normalization(grid_values))

    mappable = plt.cm.ScalarMappable(cmap=color_map_type, norm=color_normalization)
    mappable.set_array(grid_values)

    colorbar_position = figure.add_axes([position[0], position[1], size[0], size[1]])
    colorbar_ticks = np.linspace(min, scaled_max, num=n_ticks)  # Adjust tick count as needed
    colorbar = figure.colorbar(mappable, shrink=0.2, aspect=10, location='left', cax=colorbar_position)
    gr.set_colorbar_ticks(colorbar, colorbar_ticks, min, scale_factor, font_size)
    colorbar.set_label(label, rotation=angle, fontsize=font_size)

    # colorbar.ax.yaxis.label.set_position((label_pad[0], label_pad[1]))  # Adjust y-value to fine-tune
    colorbar.ax.yaxis.set_label_coords(label_pad[0], label_pad[1])  # Adjust -1.2 for spacing

    return color_map
'''
