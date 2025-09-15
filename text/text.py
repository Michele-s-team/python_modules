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
