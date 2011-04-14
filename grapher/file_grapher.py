# encoding: utf-8

import logging

from matplot import Graph

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def save_file(data, linear=False, output_file='out.png'):
    """
    Saves the Figure to a file. This is highly automagic, handled by the
    FigureCanvasAgg backend of matplotlib.
    """
    logging.debug('Building Figure from data')
    figure = Graph(data, linear=linear)

    # This updates the Figure object with a reference to the FigureCanvasAgg
    # object so it knows how to save to file.
    canvas = FigureCanvas(figure)

    logging.info('Saving figure to %s' % output_file)
    figure.savefig(filename=output_file, facecolor='.75')
    logging.info(u'… done!' % output_file)
