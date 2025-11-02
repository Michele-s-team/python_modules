import calculus.utils as cal
import colorama as col
import matplotlib as mpl
import graphics.color.utils as color_utils

'''
clear all labels in figure 'figure' whose text contains at least one element of 'patterns'
'''


def clear_labels_with_patterns(figure, patterns):
    figure_texts = figure.texts

    for text in figure.texts[:]:  # copy to avoid modifying while iterating
        if any(substr in text.get_text() for substr in patterns):
            text.remove()

    # Redraw figure
    figure.canvas.draw()
    figure.canvas.flush_events()


def empty_texts(figure):
    for text in figure.findobj(mpl.text.Text):
        text.set_text('')

'''
print a text in a given color
Input values: 
- 'text': a string
- 'color': a colorama color, such as RED
'''
def print_text_color(text, color):
        
    colorama_color = color_utils.color_map.get(color)
    
    print(f'{colorama_color}{text}{col.Style.RESET_ALL}')

'''
convert the floating-point number 'x' to latex in format 'format'
Input values: 
    - 'x': the floating-point number
    - 'format': the format to which 'x' will be converted, it must be 'f' for floating-point format and 'e' for exponential format

Return values: 
    - 'latex_string': the latex string containing 'x' converted. If 'x' is so large/small that it is in scientific format, it will be converted to string by using the scientific format even if 'format' = 'f'
'''
def float_to_latex(x, format):
    
    if (format == 'f'):
        #  the chosen format is floating point
         
        if 'e' in str(x):
            # when the value 'x' is converted to string, it contains an 'e' -> 'x' is so small / large that it is written in scientific format -> convert it by using scientific format
            latex_string = cal.to_latex_scientific(x)
        else:   
            # convert 'x' by using floating-point format
             
            latex_string = fr'${x:.3g}$'
            
    elif (format == 'e'):
        # the chosen format is scientific 
        
        latex_string = cal.to_latex_scientific(x)
    else:
        
        print_text_color('Error: format is not valid!', 'red')
        latex_string = ''

    return latex_string