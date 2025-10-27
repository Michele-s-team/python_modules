import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import proplot as pplt

import calculus.utils as cal
import constants.utils as const
import graphics.utils as gr
import list.utils as lis
import text.utils as text


'''
generate the ticks for a plot on an axis between a minimum and a maximum value
Input values: 
    - 'min', 'max': the minimal and maximal values on the axis
    - 'custom_ticks' [optional]: a set of custom ticks to add to the list of generated ticks
    - 'scale' [optional]: the scale of the axis for which ticks will be generated, 'lin' or 'log'
    - 'log_base' [optional]: for 'scale' = 'log', the base of the logarithmic ticks

Return values:
    - a list of  ticks values
'''
def generate_ticks(min, max, custom_ticks=None, scale='lin', log_base=10):
    
    if scale == 'lin':
    
        # compute the rounded-off values of min and max with respect to powers of 10
        rounded_min, rounded_max = cal.floor_base_10(min), cal.ceil_base_10(max) 
        

        # rounded_max and min are both positive
        
        ticks = []
        
        # set the maximal value of the ticks list
        if (max > rounded_max/2.0):
            
            # 'max' lies in the upper half of its 'decade' -> add to ticks the upper value of the decade (because this is closer to 'max') and its mid value
            ticks.extend([rounded_max, rounded_max/2])
        else:
            
            # 'max' lies in the lower half of its 'decade -> add to ticks the lower value of the decade (because this is clorser to 'max')
            ticks.append(max)
            
            
        # set the maximal value of the ticks list, see the comments for the max
        if (min < rounded_min/2.0):
            ticks.extend([rounded_min, rounded_min/2])
        else:
            ticks.append(min)

        
        # if max and min have different signs, add 0 to the ticks
        if max * min < 0:
            ticks.append(0)
            
        # if the user specified custom ticks, add them 
        if custom_ticks is not None:
            ticks.extend(custom_ticks)
        
        
        if len(ticks) <= 2:
            # there are only two ticks -> add the tick in the middle for clarity 
            
            ticks.append((min+max)/2)

        
        # remove duplicates from ticks, if any, and sort ticks
        lis.remove_duplicates(ticks)
        ticks = np.sort(ticks)
        
    elif scale=='log':
        
         ticks = [i for i in range(round(np.emath.logn(log_base, min)), round(np.emath.logn(log_base, max))+2)]
    
    return ticks


'''
plot a tick on a two-dimensional axis
Input values: 
    - 'ax': the matplotlib axis
    - 'axis_direction': 'x' or 'y', the direction of the axis
    - 'value': the numerical value of the tick
    - 'tick_length': a list with two entries, one for 'x' and one for 'y'. The length of the tick relative to the max-min span of the relative axis. 
    - 'tick_label_offset':  a list with two entries, one for 'x' and one for 'y'. The offset of the tick with respect to the axis, relative to the max-min span of the relative axis. 
    - 'tick_label_format': 'f' or 'e', the numerical format of the tick
    - 'origin': a list with two entries, one for 'x' and one for 'y', the starting position of the axis
    - 'length': a list with two entries, one for 'x' and one for 'y', the length of the axis
    - 'axis_origin': the origin of the axis; for an 'y' axis, by varying axis_origin[0]  one shifts the y axis in the left-right direction of the plot, and similarly for axis_origin[1]
    - 'log_base' [optional]: the base of the logarithm for log-scale axes
    - 'font_size' [optional]: the font size
    - 'z_order' [optional] : the z order
    - 'color' [optional]: the tick color
    - 'line_width' [optional]: the line width of ticks
    - 'scale' [optional]: the scale of the axis, either 'lin' or 'log'
    - 'tick_label_angle' [optional]: the rotation angle with which the tick labels will be drawn
'''

def plot_2d_tick(ax, axis_direction, value, tick_length, tick_label_offset, tick_label_format, 
              origin, length, axis_origin=None, log_base=10, font_size=8, z_order=0, color='black', line_width=const.default_line_width, scale='lin', tick_label_angle=0):
    
    if axis_origin is None:
        axis_origin = origin
    
    if scale == 'lin':
        
        if axis_direction == 'x':
            
            ax.plot([value, value], [axis_origin[1], axis_origin[1] + tick_length[1] * length[1]], color=color, linewidth=line_width,
                        zorder=z_order)  
            
            if tick_label_format[0] != '':
                    ax.text(value, axis_origin[1] - tick_label_offset[1], 
                            text.float_to_latex(value, tick_label_format[0]), fontsize=font_size, ha='center', va='center', zorder=z_order, rotation=tick_label_angle)
            
            
        elif axis_direction == 'y':
            
            ax.plot([axis_origin[0], axis_origin[0] + tick_length[0] * length[0]], [value, value], color=color, linewidth=line_width,
                        zorder=z_order)  
            
            if tick_label_format[1] != '':
                    ax.text(axis_origin[0] - tick_label_offset[0], value, text.float_to_latex(value, tick_label_format[1]), fontsize=font_size,
                            ha='center', va='center', zorder=z_order, rotation=tick_label_angle)
        
        
    elif scale == 'log':
        
        if axis_direction == 'x':
        
            ax.plot([value, value], [np.emath.logn(log_base, axis_origin[1]), np.emath.logn(log_base, axis_origin[1]) + tick_length * np.emath.logn(log_base,( origin[1] + length[1])/origin[1])], color=color, linewidth=line_width,
                                    zorder=z_order)  
                            
            ax.text(value, np.emath.logn(log_base, axis_origin[1]) - tick_label_offset[1] * np.emath.logn(log_base, (origin[1] + length[1]/origin[1])), 
                                    text.float_to_latex(log_base**value, tick_label_format[0]), fontsize=font_size, ha='center', va='center', zorder=z_order)
            
        elif axis_direction == 'y':
                
            ax.plot([np.emath.logn(log_base, axis_origin[0]), np.emath.logn(log_base, axis_origin[0]) + tick_length * np.emath.logn(log_base,( origin[0] + length[0])/origin[0])], [value, value], 
            color=color, linewidth=line_width, zorder=z_order) 
            
            ax.text(np.emath.logn(log_base, axis_origin[0]) - np.emath.logn(log_base, (origin[0]+length[0])/origin[0]) * tick_label_offset[0], value, 
                text.float_to_latex(log_base**value, tick_label_format[1]), fontsize=font_size, ha='center', va='center', zorder=z_order)

'''
plot a tick on a three-dimensional axis

'''
def plot_3d_tick(ax, axis_direction, value, tick_length, tick_label_offset, tick_label_format, origin, length, 
                 scale_factor = [1] * 3,
                 axis_origin=[0] * 3, font_size=const.default_font_size, z_order=const.default_z_order, color='black', line_width=const.default_line_width, tick_label_angle=const.default_tick_label_angle):
    
    if axis_direction == 0:
    
        # plot the tick line
        ax.plot(
            [gr.scale(value, origin[0], scale_factor[0])] * 2,
            [
                gr.scale((origin[1] + length[1] * axis_origin[0][0]), origin[1], scale_factor[1]), 
                gr.scale((origin[1] + length[1] * axis_origin[0][0]) + tick_length[0] * length[1], (origin[1] + length[1] * axis_origin[0][0]), scale_factor[1])
            ],
            [gr.scale((origin[2] + length[2] * axis_origin[0][1]), origin[2], scale_factor[2])] * 2,
            color=color, linewidth=line_width, clip_on=False, zorder=z_order) 
        
        # plot the tick label
        if tick_label_format != '':
            ax.text(
                    gr.scale(value, origin[0], scale_factor[0]), 
                    gr.scale((origin[1] + length[1] * axis_origin[0][0]) - tick_label_offset * length[1], origin[1], scale_factor[1]), 
                    gr.scale((origin[2] + length[2] * axis_origin[0][1]), origin[2], scale_factor[2]),
                    text.float_to_latex(value, tick_label_format[0]), fontsize=font_size, ha='center', va='center', zorder=z_order
                )
            
    elif axis_direction == 1:
        # plot the tick line
        ax.plot(
            [
                gr.scale((origin[0] + length[0] * axis_origin[1][0]), origin[0], scale_factor[0]), 
                gr.scale((origin[0] + length[0] * axis_origin[1][0]) + tick_length[1] * length[0], (origin[0] + length[0] * axis_origin[1][0]), scale_factor[0])
            ],
            [gr.scale(value, origin[1], scale_factor[1])] * 2,
            [gr.scale((origin[2] + length[2] * axis_origin[1][1]), origin[2], scale_factor[2])] * 2,
            color=color, linewidth=line_width, clip_on=False, zorder=z_order) 
    
        # plot the tick label
        if tick_label_format != '':
            ax.text(
                    gr.scale((origin[0] + length[0] * axis_origin[1][0]) - tick_label_offset * length[0], origin[0], scale_factor[0]), 
                    gr.scale(value, origin[1], scale_factor[1]), 
                    gr.scale((origin[2] + length[2] * axis_origin[1][1]), origin[2], scale_factor[2]),
                    text.float_to_latex(value, tick_label_format[0]), fontsize=font_size, ha='center', va='center', zorder=z_order
                )
            
    elif axis_direction == 2:
        
        # plot the tick line
        ax.plot(
            [
                gr.scale((origin[0] + length[0] * axis_origin[2][0]), origin[0], scale_factor[0]), 
                gr.scale((origin[0] + length[0] * axis_origin[2][0]) + tick_length[2] * length[0], (origin[0] + length[0] * axis_origin[2][0]), scale_factor[0])
            ],
            [gr.scale((origin[1] + length[1] * axis_origin[2][1]), origin[1], scale_factor[1])] * 2,
            [gr.scale(value, origin[2], scale_factor[2])] * 2,
            color=color, linewidth=line_width, clip_on=False, zorder=z_order) 
        
    
        # plot the tick label
        if tick_label_format != '':
            ax.text(
                    gr.scale((origin[0] + length[0] * axis_origin[2][0]) - tick_label_offset * length[0], origin[0], scale_factor[0]), 
                    gr.scale((origin[1] + length[1] * axis_origin[2][1]), origin[1], scale_factor[1]),
                    gr.scale(value, origin[2], scale_factor[2]), 
                    text.float_to_latex(value, tick_label_format[0]), fontsize=font_size, ha='center', va='center', zorder=z_order
                )
    