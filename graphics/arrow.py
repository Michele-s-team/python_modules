import math
import numpy as np
import pandas as pd

import constants.utils as const
import list.column_labels as clab
import graphics.utils as gr
import calculus.geometry as geo





'''
plot an arrow head, where 'arrow_shaft_start' is the start position of the shaft, 'arrow_shaft_end' is the end position of the shaft, 'arrow_shaft_length" is the length of the shaft
'dr_arrow_head' is the increment leading from the end of the shaft to the enf of the arrow head
'arrow_head_length' is the length of the arrow head
'''


def plot_arrow_head(ax, arrow_shaft_start, arrow_shaft_end, arrow_shaft_length, dr_arrow_head, arrow_head_length, mins,
                    scale_factors, line_width, color, alpha, z_order):
    # compute arrow_head_start_scaled = arrow_shaft_end_scaled
    arrow_shaft_start_scaled = gr.scale_list(arrow_shaft_start, mins, scale_factors)
    arrow_shaft_end_scaled = gr.scale_list(arrow_shaft_end, mins, scale_factors)

    dr_shaft_scaled = np.subtract(arrow_shaft_end_scaled, arrow_shaft_start_scaled)

    norm_dr_shaft_scaled = np.sqrt(np.dot(dr_shaft_scaled, dr_shaft_scaled))
    arrow_shaft_end_scaled = arrow_shaft_start_scaled + dr_shaft_scaled / norm_dr_shaft_scaled * arrow_shaft_length

    arrow_head_start_scaled = arrow_shaft_end_scaled
    '''
    arrow_head_end_scaled lives in a space which is not dilated according to scale_factors: 
    it is thus simply arrow_head_start_scaled + dr_arrow_head [non-scaled and dilated to obtain the correct length of the arrow head]
    '''
    arrow_head_end_scaled = np.add(arrow_head_start_scaled,
                                   dr_arrow_head / np.sqrt(np.dot(dr_arrow_head, dr_arrow_head)) * arrow_head_length)

    arrow_head_start_end = list(zip(arrow_head_start_scaled, arrow_head_end_scaled))

    ax.plot(arrow_head_start_end[0], arrow_head_start_end[1], arrow_head_start_end[2],
            color=color, linewidth=line_width, alpha=alpha, zorder=z_order)


'''
plot an arrow 
- 'ax': the axis
- 'shaft_start_position', 'shaft_end_position': the coordinates of the start and end of the shaft of the arrow
- 'shaft_length': all arrows will be renormalized and plotted with a length equal to 'shaft_length'
- 'head_over_shaft_length' : ratio between the length of each arrow head and the length of the shaft 
- 'head_angle': angle (in degrees) between each arrow head and the shaft
- 'mins': vector of minima in 3d space with respect to which the rescaling of scale_factor will be made
- 'scale_factor': scaling coefficients with respect to 'mins'
- 'threshold_arrow_length": an argument which sets the minimal arrow length that will be plotted, only arrows |r_end - r_start| > threshold_arrow_length will be plotted 
- 'line_width': line width for shaft and arrow heads
- 'color': the color
- 'alpha': transparency
- 'z_order': the z-order
'''


def plot_arrow(ax, shaft_start_position, shaft_end_position, shaft_length, 
               head_over_shaft_length, head_angle, 
               mins,
               scale_factors, threshold_arrow_length, line_width, 
               color, alpha, z_order):
    head_length = head_over_shaft_length * shaft_length

    # plot the shaft
    shaft_start_position_scaled = gr.scale_list(shaft_start_position, mins, scale_factors)
    shaft_end_position_scaled = gr.scale_list(shaft_end_position, mins, scale_factors)
    dr_shaft_scaled = np.subtract(shaft_end_position_scaled, shaft_start_position_scaled)

    dr_shaft = np.subtract(shaft_end_position, shaft_start_position)

    if (np.sqrt(np.dot(dr_shaft, dr_shaft)) > threshold_arrow_length):
        dr_shaft = dr_shaft * shaft_length / np.sqrt(np.dot(dr_shaft, dr_shaft))

        shaft_end_position = np.add(shaft_start_position, dr_shaft)
        # arrow_head_start = arrow_shaft_end

        gr.plot_line_scaled(ax, shaft_start_position, shaft_end_position, shaft_length, mins, scale_factors, line_width,
                         color,
                         alpha, z_order)

        theta_shaft = np.arccos(dr_shaft_scaled[2] / np.sqrt(np.dot(dr_shaft_scaled, dr_shaft_scaled)))
        phi_shaft = np.arctan2(dr_shaft_scaled[1], dr_shaft_scaled[0])

        # compute coordinates for arrow heads
        up_head = [-head_length * np.sin(head_angle * const.deg_to_rad), 0, -head_length * np.cos(head_angle * const.deg_to_rad)]
        down_head = [+head_length * np.sin(head_angle * const.deg_to_rad), 0, - head_length * np.cos(head_angle * const.deg_to_rad)]
        up_head = np.matmul(gr.R(theta_shaft, phi_shaft), up_head)
        down_head = np.matmul(gr.R(theta_shaft, phi_shaft), down_head)

        # plot the arrow heads
        plot_arrow_head(ax, shaft_start_position, shaft_end_position, shaft_length, up_head, head_length, mins,
                        scale_factors, line_width, color, alpha, z_order)
        plot_arrow_head(ax, shaft_start_position, shaft_end_position, shaft_length, down_head, head_length, mins,
                        scale_factors, line_width, color, alpha, z_order)


'''
plot a 2d arrow

'''
def plot_2d_arrow(ax, shaft_start_position, shaft_end_position, shaft_length, head_over_shaft_length, head_angle, line_width, color, alpha, z_order, 
                  threshold_arrow_length = const.default_threshold_arrow_length,
                  clip_on=True):
    head_length = head_over_shaft_length * shaft_length

    # plot the shaft
    dr_shaft = np.subtract(shaft_end_position, shaft_start_position)

    if ((np.linalg.norm(dr_shaft) > threshold_arrow_length)): 

        dr_shaft = dr_shaft * shaft_length / np.sqrt(np.dot(dr_shaft, dr_shaft))

        ax.plot([shaft_start_position[0], shaft_start_position[0] + dr_shaft[0]], [shaft_start_position[1], shaft_start_position[1] + dr_shaft[1]], color=color, linewidth=line_width, alpha=alpha, zorder=z_order, clip_on=clip_on)

        theta_shaft = -np.pi / 2 + math.atan2(dr_shaft[1], dr_shaft[0])

        # plot the heads
        # consider heads related to a fictitious arrow pointing up
        up_head = [-head_length * np.sin(head_angle * const.deg_to_rad), -head_length * np.cos(head_angle * const.deg_to_rad)]
        down_head = [+head_length * np.sin(head_angle * const.deg_to_rad), - head_length * np.cos(head_angle * const.deg_to_rad)]
        # rotate the heads above
        up_head = np.matmul(gr.R_2d(theta_shaft), up_head)
        down_head = np.matmul(gr.R_2d(theta_shaft), down_head)

        # plot the heads
        ax.plot([shaft_start_position[0] + dr_shaft[0], shaft_start_position[0] + dr_shaft[0] + up_head[0]], [shaft_start_position[1] + dr_shaft[1], shaft_start_position[1] + dr_shaft[1] + up_head[1]], color=color, linewidth=line_width, alpha=alpha, zorder=z_order, clip_on=clip_on)
        
        ax.plot([shaft_start_position[0] + dr_shaft[0], shaft_start_position[0] + dr_shaft[0] + down_head[0]], [shaft_start_position[1] + dr_shaft[1], shaft_start_position[1] + dr_shaft[1] + down_head[1]], color=color, linewidth=line_width, alpha=alpha, zorder=z_order, clip_on=clip_on)

