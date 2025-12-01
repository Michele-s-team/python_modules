import numpy as np

'''
conversion from degree to radians: 
[deg] = deg_to_rad [rad]
'''
deg_to_rad = 2 * np.pi / 360
rad_to_deg = 1/deg_to_rad
default_log_base = 10

default_font_size = 8
default_label_format = 'f'

colorbar_shrink_value = 0.2
colorbar_aspect_value = 10

default_head_length = 0.5
default_shaft_length = 1
default_legend_arrow_length = 0.1
default_head_over_shaft_length = 0.3
default_head_angle = 30
# the default value of the arrow length such that arrows with lengths below this value will not be plotted
default_threshold_arrow_length = 1e-4

default_tick_length = 0.1
default_minor_tick_length = 0.01
default_tick_label_pad = 0.1
default_line_width = 0.1
default_tick_label_angle = 0

default_z_order = 0
high_z_order = 100

default_color = 'black'
default_alpha = 1

default_column_name = 'f'

default_legend_location = 'center'
default_legend_position = [0.5] * 2
