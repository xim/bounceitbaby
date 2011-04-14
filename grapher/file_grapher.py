import logging

from matplot import Graph

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def save_file(data, linear=False, output_file='out.png'):
    figure = Graph(data, linear=linear)

    # This updates the Figure object with a reference to the FigureCanvasAgg
    # object so it knows how to save to file.
    canvas = FigureCanvas(figure)

    logging.info('Saving figure to %s' % output_file)
    figure.savefig(filename=output_file, facecolor='.75')
