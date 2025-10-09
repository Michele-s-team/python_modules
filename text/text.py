import colorama as col
import matplotlib as mpl

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
    
    color_map = {
        'red': col.Fore.RED,
        'green': col.Fore.GREEN,
        'blue': col.Fore.BLUE,
        'yellow': col.Fore.YELLOW,
        'magenta': col.Fore.MAGENTA,
        'cyan': col.Fore.CYAN,
        'white': col.Fore.WHITE
    }
    
    colorama_color = color_map.get(color)
    
    print(f'{colorama_color}{text}{col.Style.RESET_ALL}')
